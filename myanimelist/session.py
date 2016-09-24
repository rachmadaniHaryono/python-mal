#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Module to handle myanimelist session."""
try:  # py3
    from urllib.parse import urlparse, parse_qs
except ImportError:  # py2
    from urlparse import urlparse, parse_qs

import requests

try:
    import anime
    import manga
    import character
    import person
    import user
    import club
    import genre
    import tag
    import publication
    import producer
    import anime_list
    import manga_list
    import utilities
    from base import Error
except ImportError:
    from . import (
        anime,
        manga,
        character,
        person,
        user,
        club,
        genre,
        tag,
        publication,
        producer,
        anime_list,
        manga_list,
        utilities
    )
    from .base import Error


class UnauthorizedError(Error):
    """Indicates that the current session is unauthorized to make the given request."""

    def __init__(self, session, url, result):
        """Create a new instance of UnauthorizedError.

        :type session: :class:`.Session`
        :param session: A valid MAL session.

        :type url: str
        :param url: The requested URL.

        :type result: str
        :param result: The result of the request.

        :rtype: :class:`.UnauthorizedError`
        :return: The desired error.

        """
        super(UnauthorizedError, self).__init__()
        self.session = session
        self.url = url
        self.result = result

    def __str__(self):
        """string representation."""
        return "\n".join([
            super(UnauthorizedError, self).__str__(),
            "URL: " + self.url,
            "Result: " + self.result
        ])


class Session(object):
    """Class to handle requests to MAL. Handles login, setting HTTP headers, etc."""

    def __init__(self, username=None, password=None, user_agent="iMAL-iOS"):
        """Create a new instance of Session.

        :type username: str
        :param username: A MAL username. May be omitted.

        :type password: str
        :param username: A MAL password. May be omitted.

        :type user_agent: str
        :param user_agent: A user-agent to send to MAL in requests.
        If you have a user-agent assigned to you by Incapsula, pass it in here.

        :rtype: :class:`.Session`
        :return: The desired session.

        """
        self.username = username
        self.password = password
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': user_agent
        })

        """Suppresses any Malformed*PageError exceptions raised during parsing.

        Attributes which raise these exceptions will be set to None.
        """
        self.suppress_parse_exceptions = False

    def logged_in(self):
        """Check the logged-in status of the current session.

        Expensive (requests a page), so use sparingly!
        Best practice is to try a request and catch an UnauthorizedError.

        :rtype: bool
        :return: Whether or not the current session is logged-in.

        """
        if self.session is None:
            return False

        panel_url = 'http://myanimelist.net/panel.php'
        panel = self.session.get(panel_url)

        if 'Logout' in panel.content:
            return True

        return False

    def login(self):
        """Log into MAL and sets cookies appropriately.

        :rtype: :class:`.Session`
        :return: The current session.

        """
        # POSTS a login to mal.
        mal_headers = {
            'Host': 'myanimelist.net',
        }
        mal_payload = {
            'username': self.username,
            'password': self.password,
            'cookie': 1,
            'sublogin': 'Login'
        }
        self.session.headers.update(mal_headers)
        self.session.post('http://myanimelist.net/login.php', data=mal_payload)
        return self

    def anime(self, anime_id):
        """Create an instance of myanimelist.Anime with the given ID.

        :type anime_id: int
        :param anime_id: The desired anime's ID.

        :rtype: :class:`myanimelist.anime.Anime`
        :return: A new Anime instance with the given ID.

        """
        return anime.Anime(self, anime_id)

    def anime_list(self, username):
        """Create an instance of myanimelist.AnimeList belonging to the given username.

        :type username: str
        :param username: The username to whom the desired anime list belongs.

        :rtype: :class:`myanimelist.anime_list.AnimeList`
        :return: A new AnimeList instance belonging to the given username.

        """
        return anime_list.AnimeList(self, username)

    def character(self, character_id):
        """Create an instance of myanimelist.Character with the given ID.

        :type character_id: int
        :param character_id: The desired character's ID.

        :rtype: :class:`myanimelist.character.Character`
        :return: A new Character instance with the given ID.

        """
        return character.Character(self, character_id)

    def club(self, club_id):
        """Create an instance of myanimelist.Club with the given ID.

        :type club_id: int
        :param club_id: The desired club's ID.

        :rtype: :class:`myanimelist.club.Club`
        :return: A new Club instance with the given ID.

        """
        return club.Club(self, club_id)

    def genre(self, genre_id):
        """Create an instance of myanimelist.Genre with the given ID.

        :type genre_id: int
        :param genre_id: The desired genre's ID.

        :rtype: :class:`myanimelist.genre.Genre`
        :return: A new Genre instance with the given ID.

        """
        return genre.Genre(self, genre_id)

    def manga(self, manga_id):
        """Create an instance of myanimelist.Manga with the given ID.

        :type manga_id: int
        :param manga_id: The desired manga's ID.

        :rtype: :class:`myanimelist.manga.Manga`
        :return: A new Manga instance with the given ID.

        """
        return manga.Manga(self, manga_id)

    def manga_list(self, username):
        """Create an instance of myanimelist.MangaList belonging to the given username.

        :type username: str
        :param username: The username to whom the desired manga list belongs.

        :rtype: :class:`myanimelist.manga_list.MangaList`
        :return: A new MangaList instance belonging to the given username.

        """
        return manga_list.MangaList(self, username)

    def person(self, person_id):
        """Create an instance of myanimelist.Person with the given ID.

        :type person_id: int
        :param person_id: The desired person's ID.

        :rtype: :class:`myanimelist.person.Person`
        :return: A new Person instance with the given ID.

        """
        return person.Person(self, person_id)

    def producer(self, producer_id):
        """Create an instance of myanimelist.Producer with the given ID.

        :type producer_id: int
        :param producer_id: The desired producer's ID.

        :rtype: :class:`myanimelist.producer.Producer`
        :return: A new Producer instance with the given ID.

        """
        return producer.Producer(self, producer_id)

    def publication(self, publication_id):
        """Create an instance of myanimelist.Publication with the given ID.

        :type publication_id: int
        :param publication_id: The desired publication's ID.

        :rtype: :class:`myanimelist.publication.Publication`
        :return: A new Publication instance with the given ID.

        """
        return publication.Publication(self, publication_id)

    def tag(self, tag_id):
        """Create an instance of myanimelist.Tag with the given ID.

        :type tag_id: int
        :param tag_id: The desired tag's ID.

        :rtype: :class:`myanimelist.tag.Tag`
        :return: A new Tag instance with the given ID.

        """
        return tag.Tag(self, tag_id)

    def user(self, username):
        """Create an instance of myanimelist.User with the given username.

        :type username: str
        :param username: The desired user's username.

        :rtype: :class:`myanimelist.user.User`
        :return: A new User instance with the given username.

        """
        return user.User(self, username)

    def _check_search_input(self, keyword):
        """check if input is valid for search.

        function will raise error if input is invalid for search.

        :param keyword: keyword to search.
        :type keyword: str
        """
        # check keyword length
        keyword = str(keyword)
        max_len_keyword = 100
        min_len_keyword = 2
        if len(keyword) >= max_len_keyword:
            raise ValueError('Your keyword is too long')
        if len(keyword) <= min_len_keyword:
            raise ValueError('Your keyword is too short')

    def search_manga(self, keyword):
        """search using given keyword and mode.

        :param query: keyword to search.
        :type query: str
        :return: Generator of the anime.
        :rtype: `types.GeneratorType`
        """
        self._check_search_input(keyword)
        base_url_tmpl = 'https://myanimelist.net/manga.php?q={query}'
        page_num = 0
        item_per_page = 50
        is_item_found = None
        while not is_item_found or is_item_found is None:
            is_item_found = False
            # prepare url
            page_num += 1
            item_idx = (page_num - 1) * item_per_page
            if item_idx > 0:
                url_tmpl = base_url_tmpl + '&show={}'.format(item_idx)
            else:
                url_tmpl = base_url_tmpl

            # prepare url
            page_url = url_tmpl.format(**{'query': keyword})
            page = self.session.get(page_url).text
            html_soup = utilities.get_clean_dom(page, fix_html=False)
            a_tags = [x.select_one('a') for x in html_soup.select('tr') if x.select_one('a')]
            a_tags = list(filter(lambda x: x.get('href'), a_tags))
            links = list(filter(lambda x: '/manga/' in x, [x.get('href') for x in a_tags]))

            is_item_found = bool(links)
            if is_item_found:
                objs = [self.load_from_url(x) for x in links]
                for x in objs:
                    yield x

    def search_anime(self, keyword):
        """search using given keyword and mode.

        :param query: keyword to search.
        :type query: str
        :return: Generator of the anime.
        :rtype: `types.GeneratorType`
        """
        self._check_search_input(keyword)
        page_num = 0
        item_per_page = 50
        is_item_found = None
        while not is_item_found or is_item_found is None:
            is_item_found = False

            # prepare url
            url_tmpl = 'https://myanimelist.net/anime.php?q={query}'
            page_num += 1
            item_idx = (page_num - 1) * item_per_page
            if item_idx > 0:
                url_tmpl += '&show={}'.format(item_idx)
            page_url = url_tmpl.format(**{'query': keyword})

            page = self.session.get(page_url).text
            html_soup = utilities.get_clean_dom(page, fix_html=False)
            a_tags = [x.select_one('a') for x in html_soup.select('tr') if x.select_one('a')]
            a_tags = list(filter(lambda x: x.get('href'), a_tags))
            links = list(filter(lambda x: '/anime/' in x, [x.get('href') for x in a_tags]))
            is_item_found = bool(links)
            if is_item_found:
                objs = [self.load_from_url(x) for x in links]
                for x in objs:
                    yield x

    def search(self, keyword, mode='all'):
        """search using given keyword and mode.

        :param keyword: keyword to search.
        :param mode: mode used to search.
        :type keyword: str
        :type mode: str
        :return: list of found media/object.
        :rtype: list
        """
        self._check_search_input(keyword)
        # anime search can received empty keyword but can't 1 or 2 characters.
        # so use the min, max limit used by mode 'all'
        if mode == 'anime':
            return self.search_anime(keyword)
        elif mode == 'manga':
            return self.search_manga(keyword)

        # the query have following format for each mode:
        query_dict = {
            'all': 'search/all?q={query}',
        }
        not_implemented_mode_dict = {
            # already implemented 
            # 'anime': 'anime.php?q={query}',
            # 'manga': 'manga.php?q={query}',

            # not yet implemented.
            'character': 'character.php?q={query}',
            'people': 'people.php?q={query}',
            'clubs': 'clubs.php?action=find&cn={query}',
            'users': 'users.php?q={query}',

            # no object/class created for this search.
            'news': 'news/search?q={query}',
            'featured': 'featured/search?q={query}',
            'forum': 'forum/?action=search&u=&uloc=1&loc=-1&q={query}',
        }
        # check mode
        if mode not in query_dict and mode not in not_implemented_mode_dict:
            raise ValueError('Search mode is not available.')
        elif mode in not_implemented_mode_dict:
            raise NotImplementedError('"{}" category search is not yet implemented.'.format(mode))

        url = 'https://myanimelist.net'
        search_page_url = '/'.join([url, query_dict[mode]])
        search_page_url = search_page_url.format(**{'query': keyword})
        search_page = self.session.get(search_page_url).text
        html_soup = utilities.get_clean_dom(search_page, fix_html=False)

        result = []
        categories = ['characters', 'anime', 'manga', 'people', 'clubs']
        disallowed_url_part = [
            'myanimelist.net/topanime.php',
            'myanimelist.net/login',
            '/login.php',
        ]
        for catg in categories:
            article = html_soup.select_one('#{}'.format(catg)).find_next('article')
            if catg == 'clubs':
                article_divs = [x for x in article.select('div') if x.select_one('a')]
                a_tags = [
                    x.select_one('a') for x in article_divs if x.select_one('a').get('href')]
                links = [x.get('href') for x in a_tags]
                a_tags_result = list(map(self.load_from_url, links))
                result.extend(a_tags_result)
            else:
                a_tags = article.select('.information a')
                # find all link to correct object.
                a_tags_result = []
                for tag in a_tags:
                    link = tag.get('href')
                    # pass the login link
                    is_skipped_url = any(x in link for x in disallowed_url_part)
                    if is_skipped_url:
                        continue
                    a_tags_result.append(self.load_from_url(link))

                # fix the bug on when parsing manga on search page.
                # it is caused by unclosed a tag on 'article > div > div.information > div'
                if catg == 'manga' and len(a_tags_result) == 1:
                    a_tags_hrefs = [x.get('href') for x in html_soup.select('a') if x.get('href')]
                    manga_link = [x for x in a_tags_hrefs if 'myanimelist.net/manga/' in x]
                    a_tags_result = list(map(self.load_from_url, manga_link))

                result.extend(a_tags_result)

        # parse club for all mode search

        return list(set(result))

    def load_from_url(self, url):
        """get media/object from url.

        :param url: myanimelist url.
        :type url: str
        :return: object which match the url.

        user can give the url with or without protocol, e.g.:

         - myanimelist.net/character/15264/Maina
         - http://myanimelist.net/character/15264/Maina
        """
        # check if url-form is valid.
        unknown_url_error_msg = 'Unknown url.'
        parsed_url = urlparse(url)
        if parsed_url.scheme:
            if parsed_url.scheme not in ['http', 'https']:
                raise ValueError('Wrong protocol "{}".'.format(parsed_url.scheme))

        # non-protocol url have following structure
        # myanimelist.net/{obj_category}/{obj_id}/{obj_slug_name}
        # myanimelist.net/character/15264/Maina
        # it could also without slug name
        # myanimelist.net/character/15264
        # but that only for character, anime, manga, people
        # club 'https://myanimelist.net/clubs.php?cid={club_id}'
        allowed_netlocs = ['myanimelist.net' or 'www.myanimelist.net']
        if parsed_url.netloc not in allowed_netlocs:
            raise ValueError('Url format is not recognized.')

        club_url_keyword = 'clubs.php'
        allowed_category = {
            'character': character.Character,
            'anime': anime.Anime,
            'manga': manga.Manga,
            'people': person.Person,
            'club': club.Club,
        }

        path_parts = parsed_url.path.split('/')
        if len(path_parts) > 3 and 'club' in path_parts[1]:
            raise ValueError(unknown_url_error_msg)
        elif len(path_parts) > 3:
            url_domain, obj_category, obj_id = path_parts[:3]
        elif len(path_parts) == 2 and club_url_keyword in path_parts[1]:
            obj_category = 'club'
            url_query = parse_qs(parsed_url.query)
            club_id = url_query['cid'][0]
            return allowed_category[obj_category](self, club_id)
        else:
            raise ValueError(unknown_url_error_msg)

        if obj_category not in allowed_category:
            err_msg = 'The url category "{}" can\'t be loaded.'.format(obj_category)
            raise NotImplementedError(err_msg)
        return allowed_category[obj_category](self, int(obj_id))
