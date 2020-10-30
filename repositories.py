import requests

REPO = "https://github.com/abranhe/programming-languages-logos/blob/master" \
       "/src/{}/{}_64x64.png?raw=true"

LOGOS = {
    'php': REPO.format('php', 'php'),
    'jupyter notebook': "https://upload.wikimedia.org/wikipedia/commons/thumb"
                        "/3/38/Jupyter_logo.svg/1200px-Jupyter_logo.svg.png",
    'c++': REPO.format('cpp', 'cpp'),
    'python': REPO.format('python', 'python'),
    'java': REPO.format('java', 'java'),
    'elixir': 'https://plugins.jetbrains.com/files/7522/88297/icon/pluginIcon'
              '.png ',
    'markdown': 'https://upload.wikimedia.org/wikipedia/commons/thumb/4/48'
                '/Markdown-mark.svg/1280px-Markdown-mark.svg.png',
    'html': REPO.format('html', 'html'),
    'c': REPO.format('c', 'c'),
    'elm': 'https://upload.wikimedia.org/wikipedia/commons/thumb/f/f3'
           '/Elm_logo.svg/512px-Elm_logo.svg.png',
    'css': REPO.format('css', 'css'),
    'makefile': 'https://plugins.jetbrains.com/files/9333/97761/icon/pluginIcon.png'
}


def get_repos():
    """ Get the repositories names."""
    request = requests.get('https://api.github.com/users/nymarya/repos')
    repo_names = [repo['name'] for repo in request.json()]
    return repo_names


def get_languages(repositories):
    """ Get languages present in Github Profile and calculate proportion"""
    languages = {}

    for repository in repositories:
        # Recover languages used in repository
        url = 'https://api.github.com/repos/nymarya/{}/languages'.format(repository)
        response = requests.get(url)
        languages_json = response.json()

        for name, byte_count in languages_json.items():
            if name not in languages:
                languages[name] = int(byte_count)
            else:
                languages[name] += int(byte_count)

    return languages


def calculate_languages(languages: dict) -> dict:
    """ Calculate percentage of use of each language.

    Attributes
    ---------
    languages: dict
        dict with languages and bytes counts.

    Return
    ------
    Dictionary with languages as keys and percentages as values.
    """
    total_bytes = sum(languages.values())
    sorted_tools = sorted(languages.items(), key=lambda item: item[1],
                          reverse=True)
    new_dict = {t: byte_cnt/total_bytes * 100 for t, byte_cnt in sorted_tools}
    return new_dict


def languages_to_html(languages: dict, n: int = 5) -> dict:
    td_tag = '<td> {} </td>'
    img_tag = '<img alt="{}" src="{}" width="50">'
    result = {'logos': [], 'pcts': []}
    for lang, percentage in [*languages.items()][:n]:
        img = img_tag.format(lang, LOGOS[lang.lower()])
        result['logos'].append(td_tag.format(img))
        text = '<sub>{}: <br>{:.2f}%</sub>'.format(lang, percentage)
        result['pcts'].append(td_tag.format(text))

    return result
