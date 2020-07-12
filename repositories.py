import requests


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


def calculate_languages(languages: dict):
    """ Calculate percentage of each language"""
    total_bytes = sum(languages.values())
    sorted_langs = sorted(languages.items(), key=lambda item: item[1])
    new_dict = {lang: byte_cnt/total_bytes for lang, byte_cnt in sorted_langs}
    print(new_dict)


repositories = get_repos()
print(repositories)
langs = get_languages(repositories)
calculate_languages(langs)
