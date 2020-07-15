import re
import pathlib
import os
from posts import get_posts
from repositories import *

root = pathlib.Path(__file__).parent.resolve()

common_re = r"<!-- {} starts -->{}<!-- {} ends -->"

post_eng_re = {
    'regex': re.compile(common_re.format('posts', '.*', 'posts'),
                        re.DOTALL),
    'replace': common_re.format('posts', '\n {} \n', 'posts')}
post_ptbr_re = {
    'regex': re.compile(common_re.format('posts-br', '.*', 'posts-br'),
                        re.DOTALL),
    'replace': common_re.format('posts-br', '\n {} \n', 'posts-br')}

logos_re = {
    'regex': re.compile(common_re.format('logos', '.*', 'logos'),
                        re.DOTALL),
    'replace': common_re.format('logos', '\n {} \n', 'logos')}

pcts_re = {
    'regex': re.compile(common_re.format('pcts', '.*', 'pcts'),
                        re.DOTALL),
    'replace': common_re.format('pcts', '\n {} \n', 'pcts')}

REGEXES = [post_eng_re, post_ptbr_re, logos_re, pcts_re]

if __name__ == "__main__":
    readme = root / "README.md"

    # Retrieve most recent posts for each language
    posts = get_posts(2)

    post_eng_re['replace'] = post_eng_re['replace'].format('\n\n '.join(
        posts['eng']))
    post_ptbr_re['replace'] = post_ptbr_re['replace'].format('\n\n '.join(
        posts['pt-br']))

    # Retrieve profile overview
    repositories = get_repos()
    languages = get_languages(repositories)
    percentages = calculate_languages(languages)
    html = languages_to_html(percentages)

    logos_re['replace'] = logos_re['replace'].format('\n'.join(html['logos']))
    pcts_re['replace'] = pcts_re['replace'].format('\n'.join(html['pcts']))

    # Write posts
    readme_path = os.getcwd() + '/README.md'
    for reg in REGEXES:
        readme_contents = readme.open().read()
        readme.open("w").write(reg['regex'].sub(reg['replace'],
                                                readme_contents))
