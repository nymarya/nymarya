import requests
from bs4 import BeautifulSoup


def get_posts(n: int = 1) -> dict:
    """ Get n posts.

    Attributes
    ---------
    n: int
        number of posts to be retrieved. Default values is 1.

    Return
    ------
    Dictionary with list of posts
    """
    # Access blog and get HTML
    response = requests.get('https://nymarya.github.io/categories')
    html_data = response.text

    # Create a BeautifulSoup object from the HTML
    soup = BeautifulSoup(html_data, features="html.parser")

    posts = {}

    # Find categories
    categories = soup.findAll("h2")

    # For each language/category, extract title and link of newest post
    for category in categories:
        lang = category.next_element  # eng/pt-br
        posts[lang] = []

        # Get list under category and all a tags inside
        recent_posts = category.findNext('ul').findAll('a')

        # Get required number of posts
        for i in range(n):
            if i < len(recent_posts):
                recent_post = recent_posts[i]

                # Create string with Markdown link
                posts[lang].append('[{}]({})'. format(recent_post['title'],
                                                  recent_post['href']))

    return posts
