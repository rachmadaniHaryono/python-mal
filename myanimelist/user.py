#!/usr/bin/python
# -*- coding: utf-8 -*-
"""module for user."""
import re
import urllib
try:  # py2
    from urllib import urlencode
except ImportError:
    from urllib.parse import urlencode

import bs4

try:
    import utilities
    from base import Base, MalformedPageError, InvalidBaseError, loadable, unicode
except ImportError:
    from . import utilities
    from .base import Base, MalformedPageError, InvalidBaseError, loadable, unicode

from bs4 import BeautifulSoup


class MalformedUserPageError(MalformedPageError):
    """Indicates that a user-related page on MAL has irreparably broken markup in some way.
    """
    pass


class InvalidUserError(InvalidBaseError):
    """Indicates that the user requested does not exist on MAL.
    """
    pass


class User(Base):
    """Primary interface to user resources on MAL.
    """
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
        comments_page = session.session.get(
            u'http://myanimelist.net/comments.php?' + urllib.urlencode({'id': int(user_id)})).text
        comments_page = bs4.BeautifulSoup(comments_page, 'lxml')
        username_elt = comments_page.find('h1')
        if "'s Comments" not in username_elt.text:
            raise InvalidUserError(user_id, message="Invalid user ID given when looking up username")
        return username_elt.text.replace("'s Comments", "")

    def __init__(self, session, username):
        """Creates a new instance of User.

        :type session: :class:`myanimelist.session.Session`
        :param session: A valid MAL session
        :type username: str
        :param username: The desired user's username on MAL

        :raises: :class:`.InvalidUserError`

        """
        super(User, self).__init__(session)
        self.username = username
        if not isinstance(self.username, unicode) or len(self.username) < 1:
            raise InvalidUserError(self.username)
        self._id = None
        self._picture = None
        self._favorite_anime = None
        self._favorite_manga = None
        self._favorite_characters = None
        self._favorite_people = None
        self._last_online = None
        self._gender = None
        self._birthday = None
        self._location = None
        self._website = None
        self._join_date = None
        self._access_rank = None
        self._anime_list_views = None
        self._manga_list_views = None
        self._num_comments = None
        self._num_forum_posts = None
        self._last_list_updates = None
        self._about = None
        self._anime_stats = None
        self._manga_stats = None
        self._reviews = None
        self._recommendations = None
        self._clubs = None
        self._friends = None

    def _get_favorite(self, user_page, category):
        assert category in ['anime', 'manga', 'character', 'people']
        """get user favorite_anime."""

        # set exception for character category
        fav_cat = {} if category == 'character' else []
        cls_kw = 'characters' if category == 'character' else category

        # find which table/div
        favorite_table = user_page.select_one('.favorites-list.{}'.format(cls_kw))
        # check if there is item in table
        if favorite_table is None:
            return fav_cat

        # parse the table
        for row in favorite_table.find_all('li'):
            # parse the link_tags in row
            link_tags = []
            for x in row.find_all('a'):
                try:
                    if 'image' in x.get('class'):
                        pass
                    else:
                        link_tags.append(x)
                except TypeError:
                    # link_tag may not have any class
                    # but add it nevertheless
                    link_tags.append(x)

            # process the link
            link_tag = link_tags[0]  # assumme only the first link is the correct one
            link = link_tags[0].get('href')
            link_kw = category
            # get link keyword
            if category == 'character':
                category_id = int(link.split('/{}/'.format(link_kw))[1].split('/')[0])
                category_info = {'title': link_tag.text}
                category_obj = getattr(self.session, category)(category_id).set(category_info)

                # process the media
                # media_link form
                # '/anime/356/Fate_stay_night'
                media_link_tag = link_tags[1]  # assume it is the second link
                media_link = media_link_tag.get('href')
                media_type = media_link.split('/')[1]
                media_id = int(media_link.split('/{}/'.format(media_type))[1].split('/')[0])
                media_info = {'title': media_link_tag.text}
                media_obj = getattr(self.session, media_type)(media_id).set(media_info)

                # append to result
                fav_cat[category_obj] = media_obj

            else:
                link_kw = category
                # of the form
                # 'https://myanimelist.net/anime/467/Ghost_in_the_Shell__Stand_Alone_Complex'
                # 'https://myanimelist.net/character/498/Rin_Toosaka'
                category_id = int(link.split('/{}/'.format(link_kw))[1].split('/')[0])
                category_info = {'title': link_tag.text}
                if category == 'people':
                    category_obj = getattr(self.session, 'person')(category_id).set(category_info)
                else:
                    category_obj = getattr(self.session, category)(category_id).set(category_info)

                # append to result
                fav_cat.append(category_obj)

        if self.username == 'shaldengeki' and category == 'anime' and not fav_cat:
            from pprint import pprint
            pprint(fav_cat)
            import ipdb
            ipdb.set_trace()
        return fav_cat

    def parse_sidebar(self, user_page):
        """Parses the DOM and returns user attributes in the sidebar.

        :type user_page: :class:`bs4.BeautifulSoup`
        :param user_page: MAL user page's DOM

        :rtype: dict
        :return: User attributes

        :raises: :class:`.InvalidUserError`, :class:`.MalformedUserPageError`
        """
        user_info = {}
        # if MAL says the series doesn't exist, raise an InvalidUserError.
        error_tag = user_page.find(u'div', {u'class': u'badresult'})
        if error_tag:
            raise InvalidUserError(self.username)

        try:
            pass
            # username_tag = user_page.select('h1.h1')[0].text.replace("'s Profile", '').strip()
            """
            if not username_tag.find(u'div'):
                raise MalformedUserPageError(
                    self.username,
                    user_page,
                    message=u"Could not find title div"
                )
            """
        except:
            if not self.session.suppress_parse_exceptions:
                raise

        try:
            user_pic_tag = user_page.select('div.user-image img')
            if user_pic_tag:
                user_info[u'picture'] = user_pic_tag[0].get('src')
        except:
            if not self.session.suppress_parse_exceptions:
                raise

        try:
            # the user ID is always present in the blogfeed link.
            user_info[u'id'] = [xx.get('href').split('&id=')[1]
                                for xx in user_page.select('div.user-profile-sns a')
                                if '&id=' in xx.get('href')][0]
        except:
            if not self.session.suppress_parse_exceptions:
                raise

        # favorite
        info_kws = ['anime', 'manga', 'character', 'people']
        for category in info_kws:
            # key for characater is 'favorite_characters
            key = (
                'favorite_{}'.format(category)
                if category != 'character'
                else 'favorite_{}s'.format(category)
            )
            try:
                user_info[key] = self._get_favorite(user_page, category)
            except:
                if not self.session.suppress_parse_exceptions:
                    raise

        return user_info

    def _get_last_list_updates(self, user_page):
        """last list updates."""
        # regex for progress text
        pg_regex = r'(?P<status>[A-Za-z]+)(  at (?P<episodes>[0-9]+)'
        pg_regex += r' of (?P<total_episodes>[0-9]+))?'

        section_headings = user_page.find_all(u'div', {u'class': u'normal_header'})
        list_updates_header = list(filter(
            lambda x: u'Last List Updates' in x.text, section_headings
        ))
        last_list_updates = None
        if list_updates_header:
            list_updates_header = list_updates_header[0]
            list_updates_table = list_updates_header.findNext(u'table')
            if list_updates_table:
                last_list_updates = {}
                for row in list_updates_table.find_all(u'tr'):
                    cols = row.find_all(u'td')
                    info_col = cols[1]
                    media_link = info_col.find(u'a')
                    link_parts = media_link.get(u'href').split(u'/')
                    # of the form /(anime|manga)/10087/Fate/Zero
                    if link_parts[1] == u'anime':
                        media = (
                            self.session.anime(int(link_parts[2])).set(
                                {u'title': media_link.text}
                            )
                        )
                    else:
                        media = (
                            self.session.manga(int(link_parts[2])).set({u'title': media_link.text})
                        )
                    list_update = {}
                    progress_div = info_col.find(u'div', {u'class': u'spaceit_pad'})
                    if progress_div:
                        progress_match = re.match(pg_regex, progress_div.text).groupdict()
                        list_update[u'status'] = progress_match[u'status']
                        if progress_match[u'episodes'] is None:
                            list_update[u'episodes'] = None
                        else:
                            list_update[u'episodes'] = int(progress_match[u'episodes'])
                        if progress_match[u'total_episodes'] is None:
                            list_update[u'total_episodes'] = None
                        else:
                            list_update[u'total_episodes'] = int(progress_match[u'total_episodes'])
                    time_div = info_col.find(u'div', {u'class': u'lightLink'})
                    if time_div:
                        list_update[u'time'] = utilities.parse_profile_date(time_div.text)
                    last_list_updates[media] = list_update

    def _get_user_stats(self, user_page, stats_type, type_txt):
        """get user stats."""
        assert stats_type in ['birthday', 'last_online', 'gender', 'join_date', 'location']

        # get tags and try to filter it
        user_stats_tag = user_page.select_one('.user-status')
        stats_tags = [
            x for x in user_stats_tag.select('li > span')
            if type_txt in x.text
        ]

        # return default value if nothing found
        if not stats_tags:
            if stats_type == 'gender':
                return 'Not specified'

        # process the html tag
        stats_tag = stats_tags[0].parent
        stats_text = stats_tag.text.split(type_txt)[1].strip()

        # parse the end result based on stats type
        if stats_type in ['birthday', 'last_online', 'join_date']:
            return utilities.parse_profile_date(stats_text)
        else:
            return stats_text

    def parse(self, user_page):
        """Parses the DOM and returns user attributes in the main-content area.

        :type user_page: :class:`bs4.BeautifulSoup`
        :param user_page: MAL user page's DOM

        :rtype: dict
        :return: User attributes.

        """
        user_info = self.parse_sidebar(user_page)

        try:
            access_rank_tag = user_page.select_one('span.profile-team-title')
            if access_rank_tag:
                access_rank = access_rank_tag.text.strip()
            else:
                access_rank = 'Member'
            user_info[u'access_rank'] = access_rank
        except:
            if not self.session.suppress_parse_exceptions:
                raise

        # information keywords dict is made with stats_type as its type and  type_txt as the value
        info_kws = {
            'birthday': 'Birthday',
            'last_online': 'Last Online',
            'gender': 'Gender',
            'join_date': 'Joined',
            'location': 'Location',
        }
        for key in info_kws:
            try:
                user_info[key] = self._get_user_stats(user_page, key, info_kws[key])
            except:
                if not self.session.suppress_parse_exceptions:
                    raise

        # get user site
        try:
            user_site_tag = user_page.select_one('.user-profile-sns a')
            user_site = user_site_tag.text.strip()
            if user_site_tag and (not user_site.startswith('Recent')) and user_site != 'Blog Feed':
                user_info[u'website'] = user_site
        except:
            if not self.session.suppress_parse_exceptions:
                raise

        # num forum posts
        try:
            num_forum_posts = [
                x.text for x in user_page.select('.user-status li a')
                if 'Forum Posts' in x.text
            ][0].split('Forum Posts')[1].strip().replace(',', '')
            user_info[u'num_forum_posts'] = int(num_forum_posts)
        except:
            if not self.session.suppress_parse_exceptions:
                raise

        try:
            num_comments = user_page.select_one('.user-comments h2').text
            num_comments = num_comments.split('(')[1].split(')')[0]
            user_info[u'num_comments'] = int(num_comments)
        except:
            if not self.session.suppress_parse_exceptions:
                raise

        try:
            user_info[u'last_list_updates'] = self._get_last_list_updates(user_page)
        except:
            if not self.session.suppress_parse_exceptions:
                raise

        # anime stats.
        try:
            user_info[u'anime_stats'] = self._get_media_stats(user_page, 'anime')

        except:
            if not self.session.suppress_parse_exceptions:
                raise

        try:
            # manga stats.
            user_info[u'manga_stats'] = self._get_media_stats(user_page, 'manga')
        except:
            if not self.session.suppress_parse_exceptions:
                raise

        try:
            user_desc_tag = user_page.select_one('.profile-about-user table')
            if user_desc_tag:
                user_info[u'about'] = user_desc_tag.text.strip()
        except:
            if not self.session.suppress_parse_exceptions:
                raise

        return user_info

    def _get_media_stats(self, user_page, media_type):
        """get media stats."""
        assert media_type in ['manga', 'anime']
        result = {}
        media_tag = user_page.select_one('.stats.{}'.format(media_type))

        # get time days for media_type
        time_tag = media_tag.select_one('span').parent
        time_text = time_tag.text.split(':')[1].strip()
        result['Time (Days)'] = round(float(time_text.replace(',', '')), 1)

        # get total entries for media_type
        entries_tag = [x for x in media_tag.select('li > span') if 'Total Entries' in x.text][0]
        entries_tag = entries_tag.parent
        time_text = entries_tag.text.split('Entries')[1].strip()
        result['Total Entries'] = int(time_text.replace(',', ''))

        return result if result != {} else None

    def parse_reviews(self, reviews_page):
        """Parses the DOM and returns user reviews attributes.

        :type reviews_page: :class:`bs4.BeautifulSoup`
        :param reviews_page: MAL user reviews page's DOM

        :rtype: dict
        :return: User reviews attributes.

        """
        user_info = self.parse_sidebar(reviews_page)
        second_col = \
            reviews_page.find(u'div', {u'id': u'content'}).find(u'table').find(u'tr').find_all(u'td', recursive=False)[
                1]

        try:
            user_info[u'reviews'] = {}
            reviews = second_col.find_all(u'div', {u'class': u'borderDark'}, recursive=False)
            if reviews:
                for row in reviews:
                    review_info = {}
                    try:
                        (meta_elt, review_elt) = row.find_all(u'div', recursive=False)[0:2]
                    except ValueError:
                        raise
                    meta_rows = meta_elt.find_all(u'div', recursive=False)
                    review_info[u'date'] = utilities.parse_profile_date(meta_rows[0].find(u'div').text)
                    media_link = meta_rows[0].find(u'a')
                    link_parts = media_link.get(u'href').split(u'/')
                    # of the form /(anime|manga)/9760/Hoshi_wo_Ou_Kodomo
                    media = getattr(self.session, link_parts[1])(int(link_parts[2])).set({u'title': media_link.text})

                    helpfuls = meta_rows[1].find(u'span', recursive=False)
                    try:
                        helpful_match = re.match(r'(?P<people_helped>[0-9]+) of (?P<people_total>[0-9]+)',
                                                 helpfuls.text).groupdict()
                        review_info[u'people_helped'] = int(helpful_match[u'people_helped'])
                        review_info[u'people_total'] = int(helpful_match[u'people_total'])
                    except AttributeError:
                        # total of people is no longer shown
                        # try another method, not using regex method.
                        # ie: 805 people found this review helpful
                        helpful_match = helpfuls.text.split('people found this review helpful')[0]
                        review_info[u'people_helped'] = int(helpful_match)
                        # review_info[u'people_total'] = int(helpful_match[u'people_total'])
                        review_info[u'people_total'] = None

                    try:
                        consumption_match = re.match(r'(?P<media_consumed>[0-9]+) of (?P<media_total>[0-9?]+)',
                                                     meta_rows[2].text).groupdict()
                        review_info[u'media_consumed'] = int(consumption_match[u'media_consumed'])
                        if consumption_match[u'media_total'] == u'?':
                            review_info[u'media_total'] = None
                        else:
                            review_info[u'media_total'] = int(consumption_match[u'media_total'])
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
                            review_info[u'media_consumed'] = None
                            review_info[u'media_total'] = None
                        else:
                            # temp var for variable media_consumed
                            temp_consumed = user_media_consumption.split('of')[0].strip()
                            # temp var for variable media_total
                            temp_total = user_media_consumption.split('of')[1].strip()
                            if temp_consumed == '?':
                                review_info[u'media_consumed'] = None
                            else:
                                review_info[u'media_consumed'] = int(temp_consumed)
                            if temp_total == '?':
                                review_info[u'media_total'] = None
                            else:
                                review_info[u'media_total'] = int(temp_total)

                    review_info[u'rating'] = int(meta_rows[2].text.replace(u'Overall Rating: ', '').split('Other review')[0])

                    for x in review_elt.find_all([u'div', 'a']):
                        x.extract()

                    try:
                        review_info[u'text'] = review_elt.text.strip()
                    except AttributeError: 
                        # sometime reviw_elt cant produce attribute error
                        # one of the solution is to reparse the tag
                        review_info[u'text'] = BeautifulSoup(str(review_elt),"lxml").text.strip()

                    user_info[u'reviews'][media] = review_info
        except:
            if not self.session.suppress_parse_exceptions:
                raise

        return user_info

    def parse_recommendations(self, recommendations_page):
        """Parses the DOM and returns user recommendations attributes.

        :type recommendations_page: :class:`bs4.BeautifulSoup`
        :param recommendations_page: MAL user recommendations page's DOM

        :rtype: dict
        :return: User recommendations attributes.

        """
        user_info = self.parse_sidebar(recommendations_page)
        second_col = recommendations_page.find(u'div', {u'id': u'content'}).find(u'table').find(u'tr').find_all(u'td',
                                                                                                                recursive=False)[
            1]

        try:
            recommendations = second_col.find_all(u"div", {u"class": u"spaceit borderClass"})
            if recommendations:
                user_info[u'recommendations'] = {}
                for row in recommendations[1:]:
                    anime_table = row.find(u'table')
                    animes = anime_table.find_all(u'td')
                    liked_media_link = animes[0].find(u'a', recursive=False)
                    link_parts = liked_media_link.get(u'href').split(u'/')
                    # of the form /anime|manga/64/Rozen_Maiden
                    liked_media = getattr(self.session, link_parts[1])(int(link_parts[2])).set(
                        {u'title': liked_media_link.text})

                    recommended_media_link = animes[1].find(u'a', recursive=False)
                    link_parts = recommended_media_link.get(u'href').split(u'/')
                    # of the form /anime|manga/64/Rozen_Maiden
                    recommended_media = getattr(self.session, link_parts[1])(int(link_parts[2])).set(
                        {u'title': recommended_media_link.text})

                    recommendation_text = row.find(u'p').text

                    recommendation_menu = row.find(u'div', recursive=False)
                    utilities.extract_tags(recommendation_menu)
                    recommendation_date = utilities.parse_profile_date(recommendation_menu.text.split(u' - ')[1])

                    user_info[u'recommendations'][liked_media] = {link_parts[1]: recommended_media,
                                                                  'text': recommendation_text,
                                                                  'date': recommendation_date}
        except:
            if not self.session.suppress_parse_exceptions:
                raise

        return user_info

    def parse_clubs(self, clubs_page):
        """Parses the DOM and returns user clubs attributes.

        :type clubs_page: :class:`bs4.BeautifulSoup`
        :param clubs_page: MAL user clubs page's DOM

        :rtype: dict
        :return: User clubs attributes.

        """
        user_info = self.parse_sidebar(clubs_page)
        second_col = \
            clubs_page.find(u'div', {u'id': u'content'}).find(u'table').find(u'tr').find_all(u'td', recursive=False)[1]

        try:
            user_info[u'clubs'] = []

            club_list = second_col.find(u'ol')
            if club_list:
                clubs = club_list.find_all(u'li')
                for row in clubs:
                    club_link = row.find(u'a')
                    link_parts = club_link.get(u'href').split(u'?cid=')
                    # of the form /clubs.php?cid=10178
                    user_info[u'clubs'].append(self.session.club(int(link_parts[1])).set({u'name': club_link.text}))
        except:
            if not self.session.suppress_parse_exceptions:
                raise
        return user_info

    def parse_friends(self, friends_page):
        """Parses the DOM and returns user friends attributes.

        :type friends_page: :class:`bs4.BeautifulSoup`
        :param friends_page: MAL user friends page's DOM

        :rtype: dict
        :return: User friends attributes.

        """
        user_info = self.parse_sidebar(friends_page)
        second_col = \
            friends_page.find(u'div', {u'id': u'content'}).find(u'table').find(u'tr').find_all(u'td', recursive=False)[
                1]

        try:
            user_info[u'friends'] = {}

            friends = second_col.find_all(u'div', {u'class': u'friendHolder'})
            if friends:
                for row in friends:
                    block = row.find(u'div', {u'class': u'friendBlock'})
                    cols = block.find_all(u'div')

                    friend_link = cols[1].find(u'a')
                    friend = self.session.user(friend_link.text)

                    friend_info = {}
                    if len(cols) > 2 and cols[2].text != u'':
                        friend_info[u'last_active'] = utilities.parse_profile_date(cols[2].text.strip())

                    if len(cols) > 3 and cols[3].text != u'':
                        friend_info[u'since'] = utilities.parse_profile_date(
                            cols[3].text.replace(u'Friends since', '').strip())
                    user_info[u'friends'][friend] = friend_info
        except:
            if not self.session.suppress_parse_exceptions:
                raise

        return user_info

    def load(self):
        """Fetches the MAL user page and sets the current user's attributes.

        :rtype: :class:`.User`
        :return: Current user object.

        """
        user_profile = self.session.session.get(
            u'http://myanimelist.net/profile/' + utilities.urlencode(self.username)).text
        self.set(self.parse(utilities.get_clean_dom(user_profile)))
        return self

    def load_reviews(self):
        """Fetches the MAL user reviews page and sets the current user's reviews attributes.

        :rtype: :class:`.User`
        :return: Current user object.

        """
        page = 0
        # collect all reviews over all pages.
        review_collection = []
        while True:
            user_reviews = self.session.session.get(u'http://myanimelist.net/profile/' + utilities.urlencode(
                self.username) + u'/reviews&' + urlencode({u'p': page})).text
            parse_result = self.parse_reviews(utilities.get_clean_dom(user_reviews))
            if page == 0:
                # only set attributes once the first time around.
                self.set(parse_result)
            if len(parse_result[u'reviews']) == 0:
                break
            review_collection.append(parse_result[u'reviews'])
            page += 1

        # merge the review collections into one review dict, and set it.
        self.set({
            'reviews': {k: v for d in review_collection for k, v in d.items()}
        })
        return self

    def load_recommendations(self):
        """Fetches the MAL user recommendations page and sets the current user's recommendations attributes.

        :rtype: :class:`.User`
        :return: Current user object.

        """
        user_recommendations = self.session.session.get(
            u'http://myanimelist.net/profile/' + utilities.urlencode(self.username) + u'/recommendations').text
        self.set(self.parse_recommendations(utilities.get_clean_dom(user_recommendations)))
        return self

    def load_clubs(self):
        """Fetches the MAL user clubs page and sets the current user's clubs attributes.

        :rtype: :class:`.User`
        :return: Current user object.

        """
        user_clubs = self.session.session.get(
            u'http://myanimelist.net/profile/' + utilities.urlencode(self.username) + u'/clubs').text
        self.set(self.parse_clubs(utilities.get_clean_dom(user_clubs)))
        return self

    def load_friends(self):
        """Fetches the MAL user friends page and sets the current user's friends attributes.

        :rtype: :class:`.User`
        :return: Current user object.

        """
        user_friends = self.session.session.get(
            u'http://myanimelist.net/profile/' + utilities.urlencode(self.username) + u'/friends').text
        self.set(self.parse_friends(utilities.get_clean_dom(user_friends)))
        return self

    @property
    @loadable(u'load')
    def id(self):
        """User ID.
        """
        return self._id

    @property
    @loadable(u'load')
    def picture(self):
        """User's picture.
        """
        return self._picture

    @property
    @loadable(u'load')
    def favorite_anime(self):
        """A list of :class:`myanimelist.anime.Anime` objects containing this user's favorite anime.
        """
        return self._favorite_anime

    @property
    @loadable(u'load')
    def favorite_manga(self):
        """A list of :class:`myanimelist.manga.Manga` objects containing this user's favorite manga.
        """
        return self._favorite_manga

    @property
    @loadable(u'load')
    def favorite_characters(self):
        """A dict with :class:`myanimelist.character.Character` objects as keys and :class:`myanimelist.media.Media` as values.
        """
        return self._favorite_characters

    @property
    @loadable(u'load')
    def favorite_people(self):
        """A list of :class:`myanimelist.person.Person` objects containing this user's favorite people.
        """
        return self._favorite_people

    @property
    @loadable(u'load')
    def last_online(self):
        """A :class:`datetime.datetime` object marking when this user was active on MAL.
        """
        return self._last_online

    @property
    @loadable(u'load')
    def gender(self):
        """This user's gender.
        """
        return self._gender

    @property
    @loadable(u'load')
    def birthday(self):
        """A :class:`datetime.datetime` object marking this user's birthday.
        """
        return self._birthday

    @property
    @loadable(u'load')
    def location(self):
        """This user's location.
        """
        return self._location

    @property
    @loadable(u'load')
    def website(self):
        """This user's website.
        """
        return self._website

    @property
    @loadable(u'load')
    def join_date(self):
        """A :class:`datetime.datetime` object marking when this user joined MAL.
        """
        return self._join_date

    @property
    @loadable(u'load')
    def access_rank(self):
        """This user's access rank on MAL.
        """
        return self._access_rank

    @property
    @loadable(u'load')
    def anime_list_views(self):
        """The number of times this user's anime list has been viewed.
        """
        return self._anime_list_views

    @property
    @loadable(u'load')
    def manga_list_views(self):
        """The number of times this user's manga list has been viewed.
        """
        return self._manga_list_views

    @property
    @loadable(u'load')
    def num_comments(self):
        """The number of comments this user has made.
        """
        return self._num_comments

    @property
    @loadable(u'load')
    def num_forum_posts(self):
        """The number of forum posts this user has made.
        """
        return self._num_forum_posts

    @property
    @loadable(u'load')
    def last_list_updates(self):
        """A dict of this user's last list updates, with keys as :class:`myanimelist.media.Media` objects, and values as dicts of attributes, e.g. {'status': str, 'episodes': int, 'total_episodes': int, 'time': :class:`datetime.datetime`}
        """
        return self._last_list_updates

    @property
    @loadable(u'load')
    def about(self):
        """This user's self-bio.
        """
        return self._about

    @property
    @loadable(u'load')
    def anime_stats(self):
        """A dict of this user's anime stats, with keys as strings, and values as numerics.
        """
        return self._anime_stats

    @property
    @loadable(u'load')
    def manga_stats(self):
        """A dict of this user's manga stats, with keys as strings, and values as numerics.
        """
        return self._manga_stats

    @property
    @loadable(u'load_reviews')
    def reviews(self):
        """A dict of this user's reviews, with keys as :class:`myanimelist.media.Media` objects, and values as dicts of attributes, e.g.

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
    @loadable(u'load_recommendations')
    def recommendations(self):
        """A dict of this user's recommendations, with keys as :class:`myanimelist.media.Media` objects, and values as dicts of attributes, e.g.

          {

            'anime|media': :class:`myanimelist.media.Media`,

            'text': str,

            'date': :class:`datetime.datetime`

          }
        """
        return self._recommendations

    @property
    @loadable(u'load_clubs')
    def clubs(self):
        """A list of :class:`myanimelist.club.Club` objects containing this user's club memberships.
        """
        return self._clubs

    @property
    @loadable(u'load_friends')
    def friends(self):
        """A dict of this user's friends, with keys as :class:`myanimelist.user.User` objects, and values as dicts of attributes, e.g.

          {

            'last_active': :class:`datetime.datetime`,

            'since': :class:`datetime.datetime`

          }
        """
        return self._friends

    def anime_list(self):
        """This user's anime list.

        :rtype: :class:`myanimelist.anime_list.AnimeList`
        :return: The desired anime list.
        """
        return self.session.anime_list(self.username)

    def manga_list(self):
        """This user's manga list.

        :rtype: :class:`myanimelist.manga_list.MangaList`
        :return: The desired manga list.
        """
        return self.session.manga_list(self.username)
