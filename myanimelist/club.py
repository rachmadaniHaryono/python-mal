#!/usr/bin/python
# -*- coding: utf-8 -*-
"""module for myanimelist user."""
import argparse
import shlex

from six import string_types

try:
    from base import Base, MalformedPageError, InvalidBaseError, loadable
    import utilities
except ImportError:
    from .base import Base, MalformedPageError, InvalidBaseError, loadable
    from . import utilities


class MalformedClubPageError(MalformedPageError):
    """Error raised when page is malformed."""

    pass


class InvalidClubError(InvalidBaseError):
    """error raised when invalid input or club found."""

    pass


class Club(Base):
    """club object."""

    def __init__(self, session, club_id):
        """init func."""
        super(Club, self).__init__(session)
        self.id = club_id
        if isinstance(self.id, string_types) and not self.id.isdigit():
            raise InvalidClubError(self.id)
        elif isinstance(self.id, string_types):
            self.id = int(self.id)
        elif not isinstance(self.id, int) or int(self.id) < 1:
            raise InvalidClubError(self.id)

        # loadable from load func
        self._name = None
        self._num_members = None
        self._status = None
        self._officers = None
        self._type = None
        self._officers = None
        # loadable from their own func
        self._members = None
        self._pictures = None

    def load(self):
        """load info."""
        url_tmpl = 'https://myanimelist.net/clubs.php?cid={club_id}'
        page_url = url_tmpl.format(**{'club_id': self.id})
        page = self.session.session.get(page_url).text
        html_soup = utilities.get_clean_dom(page, fix_html=False)
        # club name
        self._name = html_soup.select_one('h1').text
        # club information
        self._information = html_soup.select_one('.clearfix').text.strip()
        # club status
        self._status = self._parse_club_status(html_soup)
        # club number of members
        self._num_members = self._status.members
        # club type
        self._type = self._parse_club_type(html_soup)
        # club officers
        self._officers = self._parse_club_officers(html_soup)

        # self.set
        return self

    def _parse_club_officers(self, html_soup):
        """parse the club officers from page.

        :param url: html_soup
        :type url: :class:`bs4.BeautifulSoup`
        :return: officers of the club and her/his position.
        :rtype: dict
        """
        officers_section_tag = [
            x for x in html_soup.select('.normal_header') if 'Club Officers' in x.text][0].parent
        user_tag = [
            x.parent for x in officers_section_tag.select('a') if '/profile/' in x.get('href')
        ]
        result = {}
        for tag in user_tag:
            user_id = tag.find('a').get('href').split('/profile/')[1]
            user = self.session.user(user_id)
            _, position = tag.contents[:2]
            if not position.strip():
                position = None
            else:
                position.strip()
                position = position.split('(', 1)[1].rsplit(')', 1)[0].strip()
            result[user] = position
        return result

    def _parse_club_status(self, html_soup):
        """parse the club type from page.

        :param url: html_soup
        :type url: :class:`bs4.BeautifulSoup`
        :return: status of the club
        :rtype: `argparse.namespace`
        """
        club_status_tag = [
            x for x in html_soup.select('.normal_header') if 'Club Stats' in x.text][0].parent

        filtered_club_status_lines = [x for x in club_status_tag.text.splitlines() if x]
        limit_post = filtered_club_status_lines.index('Club Officers')
        filtered_club_status_lines = filtered_club_status_lines[:limit_post]
        filtered_club_status_lines = [x for x in filtered_club_status_lines if ':' in x]

        # create namespace from argparse
        parser = argparse.ArgumentParser()
        status_dict = {}
        int_key = ['members', 'pictures']
        date_key = ['created']
        for line in filtered_club_status_lines:
            key, value = line.split(':', 1)
            key = key.strip().lower()
            status_dict[key] = value.strip()
            if key in int_key:
                parser.add_argument('--{}'.format(key), type=int)
            elif key in date_key:
                parser.add_argument('--{}'.format(key), type=utilities.parse_profile_date)
            else:
                parser.add_argument('--{}'.format(key))
        args = []
        for key in status_dict:
            args.append('--{} "{}"'.format(key, status_dict[key]))
        parsed_result = parser.parse_args(args=shlex.split(' '.join(args)))
        return parsed_result

    def _parse_club_type(self, html_soup):
        """parse the club type from page.

        :param url: html_soup
        :type url: :class:`bs4.BeautifulSoup`
        :return: description of the type of the club
        :rtype: `six.string_type`
        """
        club_type_tag = [
            x for x in html_soup.select('.normal_header') if 'Club Stats' in x.text][0].parent

        filtered_info_lines = [x for x in club_type_tag.text.splitlines() if x]

        club_type_text = 'Club Type'
        limit_post = utilities.index_containing_substring(filtered_info_lines, club_type_text)
        filtered_info_lines = filtered_info_lines[limit_post:]
        type_txt = '\n'.join(filtered_info_lines)
        if type_txt.startswith(club_type_text):
            type_txt = type_txt[len(club_type_text):]
        return type_txt

    @property
    @loadable('load')
    def name(self):
        """name of the club."""
        return self._name

    @property
    @loadable('load')
    def num_members(self):
        """number of members."""
        return self._num_members

    @property
    @loadable('load')
    def status(self):
        """get status of the club."""
        return self._status

    @property
    @loadable('load')
    def information(self):
        """get information from the club."""
        return self._information

    @property
    @loadable('load')
    def type(self):
        """get club type."""
        return self._type

    @property
    @loadable('load')
    def officers(self):
        """get officers of the club."""
        return self._officers

    @property
    @loadable('load_members')
    def members(self):
        """get members of the club."""
        return self._members

    def load_members(self):
        """load all members."""
        def parse_page():
            """parse the page."""
            user_per_page = 36
            # second page url example
            # https://myanimelist.net/clubs.php?action=view&t=members&id={club_id}&show=36
            page_num = 0
            is_user_found = None
            while is_user_found or is_user_found is None:
                is_user_found = False
                url_tmpl = 'https://myanimelist.net/clubs.php?id={club_id}&action=view&t=members'
                page_num += 1
                user_idx = (page_num - 1) * user_per_page
                if user_idx > 0:
                    url_tmpl += '&show={}'.format(user_idx)
                page_url = url_tmpl.format(**{'club_id': self.id})
                page = self.session.session.get(page_url).text
                html_soup = utilities.get_clean_dom(page, fix_html=False)

                member_ids = [
                    x.select_one('a').get('href').split('/profile/')[1]
                    for x in html_soup.select('td')]
                is_user_found = bool(member_ids)
                for mid in member_ids:
                    yield self.session.user(mid)

        self._members = parse_page()

        return self

    @property
    @loadable('load_pictures')
    def pictures(self):
        """get pictures from the club."""
        return self._pictures

    def load_pictures(self):
        """load pictures."""
        # TODO: or not
        pass
