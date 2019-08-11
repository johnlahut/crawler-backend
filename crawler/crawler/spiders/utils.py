"""
``utils`` contains helper functions for the ``spider`` classes. Handles general tasks such as
file I/O, URL validation, and log messages.
"""
from urllib.parse import urlsplit
import json

# gets a list of the urls to crawl initially
# -- are prepended to links to ignore
def get_urls(filename):
    """
    Returns a list of URLs from a ``json`` or ``txt`` file. If it is ``json``, file must be formatted
    based on ``OrgSpider``'s contact output.

    Cleans URLs.

    :param filename: file containing URLs
    :return: list of URLs
    """
    ext = str(filename).split('.')[-1]
    urls = []

    # getting URLs from previous iteration
    if ext  == 'json':
        data = json.load(open(filename, 'r'))
        for k,v in data.items():
            urls += [clean_url(url) for url in v['partners']]

    # plain list of text files
    else:
        for url in _read_file(filename):
            if '--' == url[:2]:
                print(f'>>_: Ignoring {url}')
                continue
            urls.append(clean_url(url))

    return urls

# adds protocol to links
def clean_url(url) -> str:
    """
    Returns a cleaned/uniform version of a URL.

    **Example:** google.com -> http://www.google.com.

    It is expected that this will be called in conjunction with ``get_urls``.

    :param url: URL to clean
    :return: properly formatted URL for scrapy to read in.
    """
    if 'http' not in url:
        return f'http://{url}'
    return url

# gets a list of the partner keywords
def get_kws(filename):
    """
    Returns a list of keywords given a filename. File must be list of URLs, one per line.

    :param filename: full absolute path of file
    :return: a ``list`` of URLs. These URLs are *not* cleaned.
    """
    return _read_file(filename)

# reads in filename as read only, returns list of stripped strings from file
def _read_file(filename):
    with open(filename, 'r') as file:
        return [kw.strip() for kw in file.readlines()]

# check to see if any of the partner words are in URL
def partner_match(url, kws, logger=None):
    """
    Checks to see if any the partner keywords are in a given URL.

    :param url: the current URL
    :param kws: list of keywords to match against
    :param logger: If standard logger object is passed, log the match.
    :return: ``True`` if ``kw`` is in ``url``, ``False`` otherwise.
    """

    if not url: return False

    # the elegant solution is this
    if not logger:
        return any(kw in url for kw in kws)

    # but for logging purposes we will be verbose
    for kw in kws:
        if kw in url:
            logger.info(f'✅ {kw} was found in {url}.')
            return True

# check to see if any of the stop words are in URL
def stop_word_match(url, kws, logger=None):
    """
    Checks to see if any of the stop words are in a given URL.

    :param url: the current URL
    :param kws: list of stop words to match against
    :param logger: If standard logger object is passed, log the stop word.
    :return: ``True`` if ``kw`` is in ``url``, ``False`` otherwise.
    """

    if not url: return False

    # the elegant solution is this
    if not logger:
        return any(kw in url for kw in kws)

    # but for logging purposes we will be verbose
    for kw in kws:
        if kw in url:
            logger.info(f'🛑 {kw} was encountered in {url}.')
            return True


# check to see if URL is on path of detecting partner
def valid_partner_url(url, p_kws,  s_kws, logger=None):
    """
    Checks to see if the URL is a valid partner.

    **Note:** This is different to ``partner_match``. Partner match simply returns if a partner keyword
    is in a URL. This function uses both ``stop_word_match`` and ``partner_match`` to validate
    a partner.

    :param url: the current URL
    :param p_kws: list of partner keywords to match against
    :param s_kws: list of stop words to match against
    :param logger: If standard logger object is passed, pass to helper functions.
    :return: ``True`` if ``p_kws`` is in ``url`` and ``s_kws`` not in ``url``, ``False`` otherwise.
    """
    return partner_match(url, p_kws, logger) and not stop_word_match(url, s_kws, logger)

# extracts the hostname of a given website
# i.e. stackoverflow.com/questions/12345 -> www.stackoverflow.com
def get_hostname(url):
    """
    Returns a URLs hostname given a **full** url. The function assumes that URLs are in the form:
    http://google.com/this/is/another-page

    Also appends ``www.`` to the URL. This function is mainly used for output consistency.


    :param url: URL to get hostname of
    :return: hostname of URL.
    """
    hostname =  urlsplit(url).hostname

    # already in good form
    if not hostname:
        return url

    if 'www' not in hostname:
        return f'www.{hostname}'
    return hostname

# validates a URL to see if it is a potential partner link
def valid_partner_link(base, url, kws, logger=None):
    """
    Checks to see if given URL is a valid *link* (**i.e.** ``<a> </a>`` tags) for a partner. When this function
    returns, the link will be flagged a valid partner for the URL.

    Also checks to ensure the base is not the same as the URL as a URL never it a partner for itself.

    :param base: source URL
    :param url: current URL
    :param kws: stop words
    :param logger: logger to pass on to helper functions
    :return: ``True`` if valid partner link, ``False`` otherwise.
    """

    # not a partner of itself, is not an image or telephone link
    return (get_hostname(base) != get_hostname(url) and
            not stop_word_match(url, kws, logger) and
            'tel' not in url and
            'jpg' not in url)

def contact_match(url, logger=None):
    """
    Checks against the listed keywords to check if the spider should follow this URL.

    :param url: URL to check match against
    :param logger: standard ``logger`` object that will keep track of followed URLs
    :return: ``True`` if the spider should follow this URL, ``False`` otherwise.
    """

    keywords = ['contact', 'location', 'join']

    if not url: return False

    url = url.lower()

    # elegant solution
    if not logger:
        return any(kw in url for kw in keywords)

    # for logging
    for kw in keywords:
        if kw in url:
            logger.info(f'✅ {kw} was found in {url}.')
            return True

# debug purposes, simple health checks
# def org_health_check(partner_info, generated_urls, out_file):
#     with open(generated_urls, 'r') as urls, open(out_file, 'r') as output:
#
#         out_data = json.load(output)
#
#         no_urls = len(urls.readlines())
#         no_keys = len(out_data.keys())
#
#         # checks to see if number of base urls matches in read urls
#         if no_urls == no_keys:
#             print(f'✅ URL count validation pass: read: {no_urls} stored: {no_keys}')
#         else:
#             print(f'🚫 Health check fail. Number of URLs read in [{no_urls}] is not the same as output [{no_keys}].')
#
#         # checks to make sure we have an entry for every partner in partner_info
#
#         partners = set()
#         partner_pass = True
#         for entry in out_data.values():
#             [partners.add(partner) for partner in entry['partners']]
#         for partner in partners:
#             if partner not in partner_info:
#                 print(f'🚫 Health check fail. No contact entry for {partner}.')
#                 partner_pass = False
#         if partner_pass:
#             print(f'✅ Health check Pass. All partners have contact entry.')
#
#         for partner_contact in partner_info:
#             if partner_contact not in partners:
#                 print(f'⚠️ Warning: {partner_contact} in contacts but not a partner.')