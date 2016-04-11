#!/usr/bin/python
# -*- coding: utf-8 -*-
"""module for user object."""
import re

try:  # py2
    from urllib import urlencode

    from base import Base, MalformedPageError, InvalidBaseError, loadable
    import utilities
except ImportError:  # py3
    from urllib.parse import urlencode

    from . import utilities
    from .base import Base, MalformedPageError, InvalidBaseError, loadable

from bs4 import BeautifulSoup
import bs4

try:
    unicode
    IS_PYTHON3 = False
except NameError:
    unicode = str
    IS_PYTHON3 = True


class MalformedUserPageError(MalformedPageError):
    """Indicates that a user-related page on MAL has irreparably broken markup in some way."""

    pass


class InvalidUserError(InvalidBaseError):
    """Indicates that the user requested does not exist on MAL."""

    pass


class User(Base):
    """Primary interface to user resources on MAL."""

    _id_attribute = "username"

    @staticmethod
    def find_username_from_user_id(session, user_id):
        """Look up a MAL username's user ID.

        :type session: :class:`myanimelist.session.Session`
        :param session: A valid MAL session.

        :type user_id: int
        :param user_id: The user ID for which we want to look up a username.

        :raises: :class:`.InvalidUserError`

        :rtype: str
        :return: The given user's username.
        """
        comments_page = session.session.get( 'http://myanimelist.net/comments.php?' +
                                            urlencode({'id': int(user_id)})).text
        comments_page = bs4.BeautifulSoup(comments_page, 'lxml')
        username_elt = comments_page.find('h1')
        if "'s Comments" not in username_elt.text:
            raise InvalidUserError(user_id,
                                   message="Invalid user ID given when looking up username")
        return username_elt.text.replace("'s Comments", "")

    def __init__(self, session, username):
        """Create a new instance of User.

        :type session: :class:`myanimelist.session.Session`
        :param session: A valid MAL session
        :type username: str
        :param username: The desired user's username on MAL

        :raises: :class:`.InvalidUserError`

        """
        super(User, self).__init__(session)
        self.username = username

        is_name_string = False
        if isinstance(self.username, unicode) or isinstance(self.username, str):
            is_name_string = True

        if not is_name_string or len(self.username) < 1:
            raise InvalidUserError(self.username)

        self._picture = None
        self._website = None
        self._access_rank = None
        self._last_list_updates = None
        self._about = None
        self._reviews = None
        self._recommendations = None
        self._clubs = None
        self._friends = None
        # user media stats
        self._anime_stats = None
        self._manga_stats = None
        # user favorites
        self._favorite_anime = None
        self._favorite_manga = None
        self._favorite_characters = None
        self._favorite_people = None
        # top parts of sidebar
        self._last_online = None
        self._gender = None
        self._birthday = None
        self._location = None
        self._join_date = None
        # bottom parts of sidebar
        self._num_forum_posts = None
        self._num_reviews = None
        self._num_recommendations = None
        self._num_blog_posts = None
        self._num_clubs = None
        # Deprecated
        self._num_comments = None
        self._anime_list_views = None
        self._manga_list_views = None

    def _parse_sidebar_user_status_top_section(self, user_page):
        """parse the top section below the user profile picture."""
        # user detail parts
        top_section_tags = [xx for xx in user_page.select('ul.user-status.border-top')[0].children
                            if type(xx) == bs4.element.Tag]
        top_section = {}
        for tag in top_section_tags:
            tag_children = list(tag.children)
            if len(tag_children) >= 2:
                top_section[tag_children[0].text.lower()] = tag_children[1].text
        # statistic parts
        statistic_tags = [xx
                          for xx in user_page.select('ul.user-status.border-top')[2].select('li')
                          if type(xx) == bs4.element.Tag]
        for tag in statistic_tags:
            span_tags = tag.select('span')
            top_section[span_tags[0].text.lower()] = int(span_tags[1].text.replace(',', ''))
        return top_section

    def _parse_sidebar_user_status(self, user_page):
        """Parse the DOM and return user status on sidebar."""
        user_info = {}
        top_section = self._parse_sidebar_user_status_top_section(user_page)
        # variable for easier key on key comparator
        parse_date = 'parse_date'
        user_info_key = 'user_info_key'
        # top part of side bar
        key_comparator = {
            'last online': {user_info_key: 'last_online', parse_date: True},
            'gender': {user_info_key: 'gender', parse_date: False},
            'birthday': {user_info_key: 'birthday', parse_date: True},
            'location': {user_info_key: 'location', parse_date: False},
            'joined': {user_info_key: 'join_date', parse_date: True},
        }
        # bottom part of sidebar
        bottom_part_key = [
            ['forum posts', 'num_forum_posts'],
            ['reviews', 'num_reviews'],
            ['recommendations', 'num_recommendations'],
            ['blog posts', 'num_blog_posts'],
            ['clubs', 'num_clubs'],
        ]
        for key in bottom_part_key:  # add bottom part key to key_comparator
            key_comparator[key[0]] = {user_info_key: key[1], parse_date: False}
        # convert top section dictionary into user info dict
        for keyc in key_comparator:
            if keyc in top_section:
                if key_comparator[keyc][parse_date]:
                    user_info[key_comparator[keyc][user_info_key]] = utilities.parse_profile_date(
                        top_section[keyc])
                else:
                    user_info[key_comparator[keyc][user_info_key]] = top_section[keyc]
        # fix bottom part keys on user info.
        # remove the comma and convert into integer
        for key in bottom_part_key:
            try:
                if user_info[key[1]] is not None and type(user_info[key[1]]) != int:
                    user_info[key[1]] = int(user_info[key[1]].replace(',', ''))
            except KeyError:
                pass  # pass for unsuspected keyerror
        return user_info

    def parse_sidebar(self, user_page):
        """Parse the DOM and returns user attributes in the sidebar.

        :type user_page: :class:`bs4.BeautifulSoup`
        :param user_page: MAL user page's DOM

        :rtype: dict
        :return: User attributes

        :raises: :class:`.InvalidUserError`, :class:`.MalformedUserPageError`
        """
        # if MAL says the series doesn't exist, raise an InvalidUserError.
        error_tag = user_page.find('div', {'class': 'badresult'})
        if error_tag:
            raise InvalidUserError(self.username)

        # parse sidebar user status
        user_info = self._parse_sidebar_user_status(user_page)
        # parse user picture
        try:
            user_info['picture'] = user_page.select('div.user-image img')[0].get('src')
        except IndexError:
            pass  # user dont' have profile picture
        except:
            if not self.session.suppress_parse_exceptions:
                raise

        try:
            # the user ID is always present in the blogfeed link.
            user_info['id'] = int([xx.get('href').split('&id=')[1]
                                    for xx in user_page.select('div.user-profile-sns a')
                                    if '&id=' in xx.get('href')][0])
        except:
            if not self.session.suppress_parse_exceptions:
                raise

        return user_info

    def _parse_favorite_characters(self, user_page):
        """parse user last online date."""
        try:
            rows_tags = user_page.select('div.user-favorites ul.favorites-list.characters li')
            favorite_list = {}
            for row in rows_tags:
                # get second div which have more information
                links = row.select('div')[1].select('a')
                for link in links:
                    href = link.get('href')
                    if '/character/' in href:
                        character_id = int(href.split('/character/')[1].split('/')[0])
                        char_name = link.text
                        key = self.session.character(character_id).set({'title': char_name})
                    elif '/anime/' in href:
                        media_id = int(href.split('/anime/')[1].split('/')[0])
                        item = self.session.anime(media_id).set({'title': link.text})
                    elif '/manga/' in href:
                        media_id = int(href.split('/manga/')[1].split('/')[0])
                        item = self.session.manga(media_id).set({'title': link.text})
                favorite_list[key] = item
            return favorite_list
        except:
            if not self.session.suppress_parse_exceptions:
                raise

    def _parse_favorite(self, user_page, mode='anime'):
        """parse user last online date."""
        try:
            rows_tags = user_page.select('div.user-favorites ul.favorites-list.{} li'.format(mode))
            if mode == 'characters':
                return self._parse_favorite_characters(user_page)
            else:
                favorite_list = []
            for row in rows_tags:
                row_link = row.select('a')[1]
                href = row_link.get('href')
                # myanimelist.net/anime/237/Eureka_Seven  # anime link form
                # myanimelist.net/manga/9711/Bakuman  # manga link form
                if mode == 'manga':
                    favorite_id = int(href.split('myanimelist.net/manga/')[1]
                                      .split('/')[0])
                    row_text = row_link.text
                    favorite_list.append(self.session.manga(favorite_id)
                                         .set({'title': row_text}))
                elif mode == 'people':
                    favorite_id = int(href.split('myanimelist.net/people/')[1]
                                      .split('/')[0])
                    row_text = row_link.text
                    favorite_list.append(self.session.person(favorite_id)
                                         .set({'title': row_text}))
                else:  # mode = anime
                    favorite_id = int(href.split('myanimelist.net/anime/')[1]
                                      .split('/')[0])
                    row_text = row_link.text
                    favorite_list.append(self.session.anime(favorite_id)
                                         .set({'title': row_text}))
            return favorite_list
        except:
            if not self.session.suppress_parse_exceptions:
                raise

    def _parse_stats(self, user_page, mode='anime'):
        """parse user media (manga,anime) status."""
        try:
            stats = {}
            stats_tag_css_selector = 'div.stats.{}'.format(mode)
            stats_tag = user_page.select(stats_tag_css_selector)[0]
            # parse top parts (days and mean score)
            top_parts = stats_tag.select('div.stat-score div')
            for tag in top_parts:
                text = tag.text
                key = text.split(':')[0].strip()
                item = float(text.split(':')[1].strip())
                stats[key] = item
            # parse bottom part
            bottom_parts = user_page.select('{} > div'
                                            .format(stats_tag_css_selector))[2].select('li')
            for tag in bottom_parts:
                children = [xx for xx in tag.children if type(xx) == bs4.element.Tag]
                key = children[0].text.strip()
                item = int(children[1].text.strip().replace(',', ''))
                stats[key] = item
            return stats
        except:
            if not self.session.suppress_parse_exceptions:
                raise

    def _parse_access_rank(self, user_page):
        """parse user access rank."""
        try:
            return user_page.select('span.profile-team-title')[0].text
        except IndexError:
            return None
        except:
            if not self.session.suppress_parse_exceptions:
                raise

    def _parse_update_media_status(self, status):
        result = {}
        # parse score
        try:
            score = int(status.lower().split('scored')[1])
            result['score'] = score
        except ValueError:
            pass  # user don't give score
        # parse detail
        detail = status.lower().split('scored')[0].strip()
        media_status = ' '.join(detail.split('/')[0].rsplit()[:-1])
        media_status = media_status.title()
        try:
            episode = int(detail.split('/')[0].rsplit()[-1])  # for manga and anime
        except ValueError:
            episode = 0
        try:
            total_episode = int(detail.split('/')[1].split()[0])
        except (IndexError, ValueError):
            total_episode = 0
        # assign to result
        result['status'] = media_status
        result['episodes'] = episode
        result['total_episodes'] = total_episode
        return result

    def _parse_last_list_updates(self, user_page):
        """parse user last media update (manga and anime)."""
        def parse_media(user_page, mode='anime'):
            # get div tags
            divs = user_page.select('div.updates.{}'.format(mode))[0].select('div')
            media_list = {}
            for div in divs:
                # parse the media
                try:
                    media_link_tag = div.select('a')[0]
                except IndexError:
                    continue
                media_link = media_link_tag.get('href')
                media_id = int(media_link.split('/{}/'.format(mode))[1].split('/')[0])
                media_title = media_link_tag.text
                media = getattr(self.session, mode)(media_id).set({'title': media_title})
                # stats
                status_tag = div.select('div')[-1]
                status = status_tag.text
                # update_date
                date_tag = div.select('div span')[0]
                update_date = utilities.parse_profile_date(date_tag.text)
                media_list[media] = self._parse_update_media_status(status)  # first media list dict
                media_list[media]['time'] = update_date  # add more key and item
            return media_list
        try:
            anime = parse_media(user_page, mode='anime')
            manga = parse_media(user_page, mode='manga')
            return dict(list(anime.items()) + list(manga.items()))
        except:
            if not self.session.suppress_parse_exceptions:
                raise

    def _parse_user_website(self, user_page):
        """parse user website."""
        try:
            website = user_page.select('div.user-profile-sns a')[0].get('href')
            if 'myanimelist.net/' not in website:
                return website
            else:
                return None
        except:
            if not self.session.suppress_parse_exceptions:
                raise

    def parse(self, user_page):
        """Parse the DOM and returns user attributes in the main-content area.

        :type user_page: :class:`bs4.BeautifulSoup`
        :param user_page: MAL user page's DOM

        :rtype: dict
        :return: User attributes.

        """
        user_info = self.parse_sidebar(user_page)
        user_info['access_rank'] = self._parse_access_rank(user_page)
        user_info['website'] = self._parse_user_website(user_page)
        # parse favorite
        user_info['favorite_anime'] = self._parse_favorite(user_page, 'anime')
        user_info['favorite_manga'] = self._parse_favorite(user_page, 'manga')
        user_info['favorite_characters'] = self._parse_favorite(user_page, 'characters')
        user_info['favorite_people'] = self._parse_favorite(user_page, 'people')
        # parse stats
        user_info['anime_stats'] = self._parse_stats(user_page, 'anime')
        user_info['manga_stats'] = self._parse_stats(user_page, 'manga')
        user_info['last_list_updates'] = self._parse_last_list_updates(user_page)
        return user_info

    def parse_reviews(self, reviews_page):
        """Parse the DOM and returns user reviews attributes.

        :type reviews_page: :class:`bs4.BeautifulSoup`
        :param reviews_page: MAL user reviews page's DOM

        :rtype: dict
        :return: User reviews attributes.

        """
        user_info = self.parse_sidebar(reviews_page)
        second_col = \
            reviews_page.find('div', {'id': 'content'}).find('table').find('tr') \
            .find_all('td', recursive=False)[1]
        try:
            user_info['reviews'] = {}
            reviews = second_col.find_all('div', {'class': 'borderDark'}, recursive=False)
            if reviews:
                for row in reviews:
                    review_info = {}
                    try:
                        (meta_elt, review_elt) = row.find_all('div', recursive=False)[0:2]
                    except ValueError:
                        raise
                    meta_rows = meta_elt.find_all('div', recursive=False)
                    review_info['date'] = utilities.parse_profile_date(meta_rows[0]
                                                                        .find('div').text)
                    media_link = meta_rows[0].find('a')
                    link_parts = media_link.get('href').split('/')
                    # of the form /(anime|manga)/9760/Hoshi_wo_Ou_Kodomo
                    media_id = link_parts[2]
                    media = getattr(self.session,
                                    link_parts[1])(int(media_id)).set({'title': media_link.text})

                    helpfuls = meta_rows[1].find('span', recursive=False)
                    try:
                        regex_str = r'(?P<people_helped>[0-9]+) of (?P<people_total>[0-9]+)'
                        helpful_match = re.match(regex_str, helpfuls.text).groupdict()
                        review_info['people_helped'] = int(helpful_match['people_helped'])
                        review_info['people_total'] = int(helpful_match['people_total'])
                    except AttributeError:
                        # total of people is no longer shown
                        # try another method, not using regex method.
                        # ie: 805 people found this review helpful
                        helpful_match = helpfuls.text.split('people found this review helpful')[0]
                        review_info['people_helped'] = int(helpful_match)
                        # review_info[u'people_total'] = int(helpful_match[u'people_total'])
                        review_info['people_total'] = None

                    try:
                        regex_str = r'(?P<media_consumed>[0-9]+) of (?P<media_total>[0-9?]+)'
                        consumption_match = re.match(regex_str, meta_rows[2].text).groupdict()
                        review_info['media_consumed'] = int(consumption_match['media_consumed'])
                        if consumption_match['media_total'] == '?':
                            review_info['media_total'] = None
                        else:
                            review_info['media_total'] = int(consumption_match['media_total'])
                    except AttributeError:
                        # available format
                        # ie anime: 25 of 25 episodes seen
                        # ie : 25 of ? episodes seen
                        # ie : ? episodes
                        # ie manga: 40 chapters
                        # ie : 60 of ? chapters read
                        # ie : ? chapters
                        # <div class="lightLink" style="float: right;">24 of 24 episodes seen</div>

                        media_tag = meta_rows[1].find_all('div')[0]
                        if ' episodes' in media_tag.text:
                            user_media_consumption = media_tag.text.split(' episodes')[0].strip()
                        elif ' chapters' in media_tag.text:
                            user_media_consumption = media_tag.text.split(' chapters')[0].strip()
                        else:
                            # no format recognized
                            raise AttributeError
                        # user_media_consumption : 'xx of xx', 'xx of ?', '? of xx', or '?'
                        if 'of' not in user_media_consumption:
                            review_info['media_consumed'] = None
                            review_info['media_total'] = None
                        else:
                            # temp var for variable media_consumed
                            temp_consumed = user_media_consumption.split('of')[0].strip()
                            # temp var for variable media_total
                            temp_total = user_media_consumption.split('of')[1].strip()
                            if temp_consumed == '?':
                                review_info['media_consumed'] = None
                            else:
                                review_info['media_consumed'] = int(temp_consumed)
                            if temp_total == '?':
                                review_info['media_total'] = None
                            else:
                                review_info['media_total'] = int(temp_total)

                    review_info['rating'] = int(meta_rows[2]
                                                 .text
                                                 .replace('Overall Rating: ', '')
                                                 .split('Other review')[0])

                    for x in review_elt.find_all(['div', 'a']):
                        x.extract()

                    try:
                        review_info['text'] = review_elt.text.strip()
                    except AttributeError:
                        # sometime reviw_elt cant produce attribute error
                        # one of the solution is to reparse the tag
                        review_info['text'] = BeautifulSoup(str(review_elt), "lxml").text.strip()

                    user_info['reviews'][media] = review_info
        except:
            if not self.session.suppress_parse_exceptions:
                raise

        return user_info

    def parse_recommendations(self, recommendations_page):
        """Parse the DOM and returns user recommendations attributes.

        :type recommendations_page: :class:`bs4.BeautifulSoup`
        :param recommendations_page: MAL user recommendations page's DOM

        :rtype: dict
        :return: User recommendations attributes.

        """
        user_info = self.parse_sidebar(recommendations_page)
        second_col = (recommendations_page
                      .find('div', {'id': 'content'})
                      .find('table')
                      .find('tr')
                      .find_all('td', recursive=False)[1])

        try:
            recommendations = second_col.find_all("div", {"class": "spaceit borderClass"})
            if recommendations:
                user_info['recommendations'] = {}
                for row in recommendations[1:]:
                    anime_table = row.find('table')
                    animes = anime_table.find_all('td')
                    liked_media_link = animes[0].find('a', recursive=False)
                    link_parts = liked_media_link.get('href').split('/')
                    # of the form /anime|manga/64/Rozen_Maiden
                    liked_media = getattr(self.session, link_parts[1])(int(link_parts[2])).set(
                        {'title': liked_media_link.text})

                    recommended_media_link = animes[1].find('a', recursive=False)
                    link_parts = recommended_media_link.get('href').split('/')
                    # of the form /anime|manga/64/Rozen_Maiden
                    recommended_media = (getattr(self.session, link_parts[1])(int(link_parts[2]))
                                         .set({'title': recommended_media_link.text}))

                    recommendation_text = row.find('p').text

                    recommendation_menu = row.find('div', recursive=False)
                    utilities.extract_tags(recommendation_menu)
                    recommendation_date = utilities.parse_profile_date(recommendation_menu
                                                                       .text.split(' - ')[1])

                    user_info['recommendations'][liked_media] = {link_parts[1]: recommended_media,
                                                                  'text': recommendation_text,
                                                                  'date': recommendation_date}
        except:
            if not self.session.suppress_parse_exceptions:
                raise

        return user_info

    def parse_clubs(self, clubs_page):
        """Parse the DOM and returns user clubs attributes.

        :type clubs_page: :class:`bs4.BeautifulSoup`
        :param clubs_page: MAL user clubs page's DOM

        :rtype: dict
        :return: User clubs attributes.

        """
        user_info = self.parse_sidebar(clubs_page)
        second_col = (clubs_page
                      .find('div', {'id': 'content'})
                      .find('table')
                      .find('tr')
                      .find_all('td', recursive=False)[1])
        try:
            user_info['clubs'] = []

            club_list = second_col.find('ol')
            if club_list:
                clubs = club_list.find_all('li')
                for row in clubs:
                    club_link = row.find('a')
                    link_parts = club_link.get('href').split('?cid=')
                    # of the form /clubs.php?cid=10178
                    user_info['clubs'].append(self
                                               .session
                                               .club(int(link_parts[1]))
                                               .set({'name': club_link.text}))
        except:
            if not self.session.suppress_parse_exceptions:
                raise
        return user_info

    def parse_friends(self, friends_page):
        """Parse the DOM and returns user friends attributes.

        :type friends_page: :class:`bs4.BeautifulSoup`
        :param friends_page: MAL user friends page's DOM

        :rtype: dict
        :return: User friends attributes.

        """
        user_info = self.parse_sidebar(friends_page)
        second_col = (friends_page
                      .find('div', {'id': 'content'})
                      .find('table')
                      .find('tr')
                      .find_all('td', recursive=False)[1])

        try:
            user_info['friends'] = {}

            friends = second_col.find_all('div', {'class': 'friendHolder'})
            if friends:
                for row in friends:
                    block = row.find('div', {'class': 'friendBlock'})
                    cols = block.find_all('div')

                    friend_link = cols[1].find('a')
                    friend = self.session.user(friend_link.text)

                    friend_info = {}
                    if len(cols) > 2 and cols[2].text != '':
                        friend_info['last_active'] = utilities.parse_profile_date(cols[2]
                                                                                   .text.strip())

                    if len(cols) > 3 and cols[3].text != '':
                        friend_info['since'] = utilities.parse_profile_date(
                            cols[3].text.replace('Friends since', '').strip())
                    user_info['friends'][friend] = friend_info
        except:
            if not self.session.suppress_parse_exceptions:
                raise

        return user_info

    def load(self):
        """Fetche the MAL user page and sets the current user's attributes.

        :rtype: :class:`.User`
        :return: Current user object.

        """
        user_profile = self.session.session.get(
            'http://myanimelist.net/profile/' + utilities.urlencode(self.username)).text
        self.set(self.parse(utilities.get_clean_dom(user_profile)))
        return self

    def load_reviews(self):
        """Fetche the MAL user reviews page and sets the current user's reviews attributes.

        :rtype: :class:`.User`
        :return: Current user object.

        """
        page = 0
        # collect all reviews over all pages.
        review_collection = []
        while True:
            user_reviews = (self
                            .session
                            .session
                            .get('http://myanimelist.net/profile/' +
                                 utilities.urlencode(self.username) +
                                 '/reviews&' +
                                 urlencode({'p': page}))
                            .text)
            parse_result = self.parse_reviews(utilities.get_clean_dom(user_reviews))
            if page == 0:
                # only set attributes once the first time around.
                self.set(parse_result)
            if len(parse_result['reviews']) == 0:
                break
            review_collection.append(parse_result['reviews'])
            page += 1

        # merge the review collections into one review dict, and set it.
        self.set({
            'reviews': {k: v for d in review_collection for k, v in d.items()}
        })
        return self

    def load_recommendations(self):
        """Fetche the MAL user recommendations page and sets the current user's recommendations attributes.

        :rtype: :class:`.User`
        :return: Current user object.

        """
        user_recommendations = self.session.session.get(
            'http://myanimelist.net/profile/' +
            utilities.urlencode(self.username) +
            '/recommendations').text
        self.set(self.parse_recommendations(utilities.get_clean_dom(user_recommendations)))
        return self

    def load_clubs(self):
        """Fetche the MAL user clubs page and sets the current user's clubs attributes.

        :rtype: :class:`.User`
        :return: Current user object.

        """
        user_clubs = self.session.session.get(
            'http://myanimelist.net/profile/' +
            utilities.urlencode(self.username) +
            '/clubs').text
        self.set(self.parse_clubs(utilities.get_clean_dom(user_clubs)))
        return self

    def load_friends(self):
        """Fetche the MAL user friends page and sets the current user's friends attributes.

        :rtype: :class:`.User`
        :return: Current user object.

        """
        user_friends = self.session.session.get(
            'http://myanimelist.net/profile/' +
            utilities.urlencode(self.username) + '/friends').text
        self.set(self.parse_friends(utilities.get_clean_dom(user_friends)))
        return self

    @property
    @loadable('load')
    def id(self):
        """User ID."""
        return self._id

    @property
    @loadable('load')
    def picture(self):
        """User picture."""
        return self._picture

    @property
    @loadable('load')
    def favorite_anime(self):
        """A list of :class:`myanimelist.anime.Anime` objects contain user's favorite anime."""
        return self._favorite_anime

    @property
    @loadable('load')
    def favorite_manga(self):
        """A list of :class:`myanimelist.manga.Manga` objects containing user's favorite manga."""
        return self._favorite_manga

    @property
    @loadable('load')
    def favorite_characters(self):
        """
        user favorite characters.

        A dict with :class:`myanimelist.character.Character` objects as keys
        and :class:`myanimelist.media.Media` as values.
        """
        return self._favorite_characters

    @property
    @loadable('load')
    def favorite_people(self):
        """A list of :class:`myanimelist.person.Person` objects contain user's favorite people."""
        return self._favorite_people

    @property
    @loadable('load')
    def last_online(self):
        """A :class:`datetime.datetime` object marking when this user was active on MAL."""
        return self._last_online

    @property
    @loadable('load')
    def gender(self):
        """user gender."""
        return self._gender

    @property
    @loadable('load')
    def birthday(self):
        """A :class:`datetime.datetime` object marking this user's birthday."""
        return self._birthday

    @property
    @loadable('load')
    def location(self):
        """User location."""
        return self._location

    @property
    @loadable('load')
    def website(self):
        """User website."""
        return self._website

    @property
    @loadable('load')
    def join_date(self):
        """A :class:`datetime.datetime` object marking when this user joined MAL."""
        return self._join_date

    @property
    @loadable('load')
    def access_rank(self):
        """User access rank on MAL."""
        return self._access_rank

    @property
    @loadable('load')
    def anime_list_views(self):
        """DEPRECATED! The number of times this user's anime list has been viewed."""
        return self._anime_list_views

    @property
    @loadable('load')
    def manga_list_views(self):
        """The number of times this user's manga list has been viewed."""
        return self._manga_list_views

    @property
    @loadable('load')
    def num_comments(self):
        """DEPRECATED! The number of comments this user has made."""
        return self._num_comments

    @property
    @loadable('load')
    def num_forum_posts(self):
        """The number of forum posts this user has made."""
        return self._num_forum_posts

    @property
    @loadable('load')
    def last_list_updates(self):
        """
        A dict of this user's last list updates.

        with keys as :class:`myanimelist.media.Media` objects,
        and values as dicts of attributes,
        e.g. {'status': str, 'episodes': int, 'total_episodes': int,
        'time': :class:`datetime.datetime`}
        """
        return self._last_list_updates

    @property
    @loadable('load')
    def about(self):
        """User self-bio."""
        return self._about

    @property
    @loadable('load')
    def anime_stats(self):
        """A dict of this user's anime stats, with keys as strings, and values as numerics."""
        return self._anime_stats

    @property
    @loadable('load')
    def manga_stats(self):
        """A dict of this user's manga stats, with keys as strings, and values as numerics."""
        return self._manga_stats

    @property
    @loadable('load_reviews')
    def reviews(self):
        """A dict of this user's reviews.

        with keys :class:`myanimelist.media.Media` objects, and values as dicts of attributes,
        e.g.

          {

            'people_helped': int,

            'people_total': int,

            'media_consumed': int,

            'media_total': int,

            'rating': int,

            'text': str,

            'date': :class:`datetime.datetime`

          }

        """
        return self._reviews

    @property
    @loadable('load_recommendations')
    def recommendations(self):
        """A dict of this user's recommendations.

        with keys :class:`myanimelist.media.Media` objects, and values as dicts of attributes, e.g.

          {

            'anime|media': :class:`myanimelist.media.Media`,

            'text': str,

            'date': :class:`datetime.datetime`

          }
        """
        return self._recommendations

    @property
    @loadable('load_clubs')
    def clubs(self):
        """A list of :class:`myanimelist.club.Club` objects containing user's club memberships."""
        return self._clubs

    @property
    @loadable('load_friends')
    def friends(self):
        """A dict of this user's friends.

        with keys as :class:`myanimelist.user.User` objects, and values as dicts of attributes, e.g.

          {

            'last_active': :class:`datetime.datetime`,

            'since': :class:`datetime.datetime`

          }
        """
        return self._friends

    def anime_list(self):
        """User anime list.

        :rtype: :class:`myanimelist.anime_list.AnimeList`
        :return: The desired anime list.
        """
        return self.session.anime_list(self.username)

    def manga_list(self):
        """User manga list.

        :rtype: :class:`myanimelist.manga_list.MangaList`
        :return: The desired manga list.
        """
        return self.session.manga_list(self.username)
