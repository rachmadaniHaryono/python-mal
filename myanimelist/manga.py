#!/usr/bin/python
# -*- coding: utf-8 -*-
from . import utilities
from .base import Base, Error, loadable
from . import media


class MalformedMangaPageError(media.MalformedMediaPageError):
    """Indicates that a manga-related page on MAL has irreparably broken markup in some way.
    """
    pass


class InvalidMangaError(media.InvalidMediaError):
    """Indicates that the manga requested does not exist on MAL.
    """
    pass


class Manga(media.Media):
    """Primary interface to manga resources on MAL.
    """
    _status_terms = [
        'Unknown',
        'Publishing',
        'Finished',
        'Not yet published'
    ]
    _consuming_verb = "read"

    def __init__(self, session, manga_id):
        """Creates a new instance of Manga.

        :type session: :class:`myanimelist.session.Session`
        :param session: A valid MAL session
        :type manga_id: int
        :param manga_id: The desired manga's ID on MAL

        :raises: :class:`.InvalidMangaError`

        """
        if not isinstance(manga_id, int) or int(manga_id) < 1:
            raise InvalidMangaError(manga_id)
        super(Manga, self).__init__(session, manga_id)
        self._volumes = None
        self._chapters = None
        self._published = None
        self._authors = None
        self._serialization = None

    def parse_sidebar(self, manga_page):
        """Parses the DOM and returns manga attributes in the sidebar.

        :type manga_page: :class:`lxml.html.HtmlElement`
        :param manga_page: MAL manga page's DOM

        :rtype: dict
        :return: manga attributes

        :raises: :class:`.InvalidMangaError`, :class:`.MalformedMangaPageError`
        """
        # if MAL says the series doesn't exist, raise an InvalidMangaError.
        if not self._validate_page(manga_page):
            raise InvalidMangaError(self.id)

        title_tag = manga_page.xpath(".//div[@id='contentWrapper']//h1")
        if len(title_tag) == 0:
            raise MalformedMangaPageError(self.id, manga_page, message="Could not find title div")

        # otherwise, begin parsing.
        manga_info = super(Manga, self).parse_sidebar(manga_page)
        info_panel_first = None

        try:
            container = utilities.css_select("#content", manga_page)
            if container is None:
                raise MalformedMangaPageError(self.id, manga_page, message="Could not find the info table")

            info_panel_first = container[0].find(".//table/tr/td")
            temp = info_panel_first.xpath(".//div/span[text()[contains(.,'Volumes:')]]")
            if len(temp) == 0:
                raise Exception("Couldn't find volumes tag.")
            volumes_tag = temp[0].getparent().xpath(".//text()")[-1]
            manga_info['volumes'] = int(volumes_tag.strip()) if volumes_tag.strip() != 'Unknown' else None
        except:
            if not self.session.suppress_parse_exceptions:
                raise

        try:
            temp = info_panel_first.xpath(".//div/span[text()[contains(.,'Chapters:')]]")
            if len(temp) == 0:
                raise Exception("Couldn't find chapters tag.")
            chapters_tag = temp[0].getparent().xpath(".//text()")[-1]
            manga_info['chapters'] = int(chapters_tag.strip()) if chapters_tag.strip() != 'Unknown' else None
        except:
            if not self.session.suppress_parse_exceptions:
                raise

        try:
            temp = info_panel_first.xpath(".//div/span[text()[contains(.,'Published:')]]")
            if len(temp) == 0:
                raise Exception("Couldn't find published tag.")
            published_tag = temp[0].getparent().xpath(".//text()")[-1]
            published_parts = published_tag.strip().split(' to ')
            if len(published_parts) == 1:
                # this published once.
                try:
                    published_date = utilities.parse_profile_date(published_parts[0])
                except ValueError:
                    raise MalformedMangaPageError(self.id, published_parts[0],
                                                  message="Could not parse single publish date")
                manga_info['published'] = (published_date,)
            else:
                # two publishing dates.
                try:
                    publish_start = utilities.parse_profile_date(published_parts[0])
                except ValueError:
                    raise MalformedMangaPageError(self.id, published_parts[0],
                                                  message="Could not parse first of two publish dates")
                if published_parts == '?':
                    # this is still publishing.
                    publish_end = None
                else:
                    try:
                        publish_end = utilities.parse_profile_date(published_parts[1])
                    except ValueError:
                        raise MalformedMangaPageError(self.id, published_parts[1],
                                                      message="Could not parse second of two publish dates")
                manga_info['published'] = (publish_start, publish_end)
        except:
            if not self.session.suppress_parse_exceptions:
                raise

        try:
            temp = info_panel_first.xpath(".//div/span[text()[contains(.,'Authors:')]]")
            if len(temp) == 0:
                raise Exception("Couldn't find authors tag.")
            authors_tags = temp[0].getparent().xpath(".//a")
            manga_info['authors'] = {}
            for author_link in authors_tags:
                link_parts = author_link.get('href').split('/')
                # of the form /people/1867/Naoki_Urasawa
                person = self.session.person(int(link_parts[2])).set({'name': author_link.text})
                role = author_link.xpath("./following-sibling::text()")[0].replace(' (', '').replace(')', '')
                manga_info['authors'][person] = role
        except:
            if not self.session.suppress_parse_exceptions:
                raise

        try:
            temp = info_panel_first.xpath(".//div/span[text()[contains(.,'Serialization:')]]")
            if len(temp) == 0:
                raise Exception("Couldn't find authors tag.")
            serialization_tags = temp[0].getparent().xpath(".//a")

            manga_info['serialization'] = None
            if len(serialization_tags) != 0:
                publication_link = serialization_tags[0]
                link_parts = publication_link.get('href').split('mid=')
                if len(link_parts) != 1:
                    # backwards compatibility
                    # of the form /manga.php?mid=1
                    manga_info['serialization'] = self.session.publication(int(link_parts[1])).set(
                        {'name': publication_link.text})
                else:
                    # of the form /manga/magazine/83/<the_name>
                    link_parts = publication_link.get('href').split('/')
                    manga_info['serialization'] = self.session.publication(int(link_parts[-2])).set(
                        {'name': publication_link.text})
        except:
            if not self.session.suppress_parse_exceptions:
                raise

        return manga_info

    @property
    @loadable('load')
    def volumes(self):
        """The number of volumes in this manga.
        """
        return self._volumes

    @property
    @loadable('load')
    def chapters(self):
        """The number of chapters in this manga.
        """
        return self._chapters

    @property
    @loadable('load')
    def published(self):
        """A tuple(2) containing up to two :class:`datetime.date` objects representing the start and end dates of this manga's publishing.

          Potential configurations:

            None -- Completely-unknown publishing dates.

            (:class:`datetime.date`, None) -- Manga start date is known, end date is unknown.

            (:class:`datetime.date`, :class:`datetime.date`) -- Manga start and end dates are known.
        """
        return self._published

    @property
    @loadable('load')
    def authors(self):
        """An author dict with :class:`myanimelist.person.Person` objects of the authors as keys, and strings describing the duties of these authors as values.
        """
        return self._authors

    @property
    @loadable('load')
    def serialization(self):
        """The :class:`myanimelist.publication.Publication` involved in the first serialization of this manga.
        """
        return self._serialization
