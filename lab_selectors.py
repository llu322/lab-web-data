#!/usr/bin/python3
"""Functions for extracting data from HTML."""
from bs4 import BeautifulSoup


def count_matches(html, selector):
    """
    Return how many tags match the CSS selector.

    >>> count_matches('<div><p>a</p><p>b</p><span><p>c</p></span></div>', 'p')
    3
    >>> count_matches('<div><p>a</p><p>b</p><span><p>c</p></span></div>', 'div > p')
    2
    """
    soup = BeautifulSoup(html, "html.parser")
    return len(soup.select(selector))


def select_texts(html, selector):
    """
    Return each matching tag's text, preserving whitespace.

    >>> select_texts('<span class="price">$9.99</span><span class="price">$19.99</span>', '.price')
    ['$9.99', '$19.99']
    >>> select_texts('<div><p>a</p><p>b</p></div>', 'p')
    ['a', 'b']
    """
    soup = BeautifulSoup(html, "html.parser")
    texts = []
    for tag in soup.select(selector):
        texts.append(tag.text)
    return texts


def select_attr(html, selector, attr):
    """
    Return the requested attribute from every matching tag.

    >>> select_attr('<a href="/a">One</a><a href="/b">Two</a>', 'a', 'href')
    ['/a', '/b']
    >>> select_attr('<img src="x.png"><img src="y.png">', 'img', 'src')
    ['x.png', 'y.png']
    """
    soup = BeautifulSoup(html, "html.parser")
    values = []
    for tag in soup.select(selector):
        values.append(tag[attr])
    return values


def extract_titles(html):
    """
    Return listing titles with surrounding whitespace removed.

    >>> extract_titles('<li class="item"><a class="title" href="/1">Mouse</a></li><li class="item"><a class="title" href="/2">Keyboard</a></li>')
    ['Mouse', 'Keyboard']
    """
    soup = BeautifulSoup(html, "html.parser")
    titles = []
    for tag in soup.select(".title"):
        titles.append(tag.text.strip())
    return titles


def extract_prices_cents(html):
    """
    Return every price as an integer number of cents.

    >>> extract_prices_cents('<span class="price">$49.99</span><span class="price">$5.00</span>')
    [4999, 500]
    >>> extract_prices_cents('<span class="price">$8.99</span>')
    [899]
    """
    soup = BeautifulSoup(html, "html.parser")
    prices = []
    for tag in soup.select(".price"):
        dollars = tag.text.strip().replace("$", "").replace(",", "")
        cents = int(round(float(dollars) * 100))
        prices.append(cents)
    return prices


def count_free_shipping(html):
    """
    Return the number of free-shipping badges.

    >>> count_free_shipping('<li class="item"><span class="free-shipping">Free shipping</span></li><li class="item"></li>')
    1
    >>> count_free_shipping('<li class="item"></li><li class="item"></li>')
    0
    """
    soup = BeautifulSoup(html, "html.parser")
    return len(soup.select(".free-shipping"))


def first_link(html):
    """
    Return the first link's href, or None if no links exist.

    >>> first_link('<div><a href="/first">One</a><a href="/second">Two</a></div>')
    '/first'
    >>> first_link('<p>no links here</p>')
    """
    soup = BeautifulSoup(html, "html.parser")
    links = soup.select("a[href]")
    if len(links) == 0:
        return None
    return links[0]["href"]


def extract_listings(html):
    """
    Return one dictionary per item with name, price_cents, and url.

    >>> html = '<li class="item"><a class="title" href="/itm/1">Mouse</a><span class="price">$9.99</span></li><li class="item"><a class="title" href="/itm/2">Keyboard</a><span class="price">$19.99</span></li>'
    >>> extract_listings(html)
    [{'name': 'Mouse', 'price_cents': 999, 'url': '/itm/1'}, {'name': 'Keyboard', 'price_cents': 1999, 'url': '/itm/2'}]
    """
    soup = BeautifulSoup(html, "html.parser")
    listings = []

    for item in soup.select(".item"):
        title = item.select(".title")[0]
        price = item.select(".price")[0]
        dollars = price.text.strip().replace("$", "").replace(",", "")

        listing = {
            "name": title.text.strip(),
            "price_cents": int(round(float(dollars) * 100)),
            "url": title["href"]
        }
        listings.append(listing)

    return listings


if __name__ == "__main__":
    import doctest
    doctest.testmod()