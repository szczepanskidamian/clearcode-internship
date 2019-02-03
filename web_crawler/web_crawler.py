from urllib.request import urlopen
import re


def site_map(url, mapping=dict(), all_links=set(), homepage=None):
    """Function making a map of whole site and returns dictionary of urls,
    titles and links on each subsite."""
    if not homepage:
        homepage = url
    _titles, _links = map_link(url, homepage)
    mapping[url] = {'title': _titles[0], 'links': set(_links)}
    for link in _links:
        if link in all_links:
            continue
        all_links.add(link)
        site_map(link, mapping, all_links, homepage)
    return mapping


def map_link(_url, homepage):
    """Function returning titles and links out of given url."""
    html_source = urlopen(_url)
    html_text = html_source.read()

    """Patterns to find titles and links in html."""
    pattern_title = "<title>(.+?)</title>"
    pattern_link = '<a href="(.+?)"'

    """Encoding titles and links from string to bytes."""
    title = re.compile((pattern_title.encode('utf-8')))
    link = re.compile((pattern_link.encode('utf-8')))

    """Searching for every title and link pattern in html source."""
    titles = re.findall(title, html_text)
    links = re.findall(link, html_text)

    """ After decoding for some reason string was in additional quotation marks 
    so I get rid of them with re.sub()."""
    for i in range(len(titles)):
        titles[i] = titles[i].decode('utf-8')
        titles[i] = re.sub('"', '', titles[i])

    for i in range(len(links)):
        links[i] = links[i].decode('utf-8')
        links[i] = re.sub('"', '', links[i])

        if "http" not in links[i]:
            links[i] = homepage + links[i]

        """Removing external urls."""
        if homepage not in links[i]:
            links.remove(links[i])
    return titles, links


# URL = "http://127.0.0.1:8000"
# URL = "http://0.0.0.0:8000"
# print(site_map(URL))
