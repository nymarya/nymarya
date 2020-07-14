import re
import pathlib
import os
from posts import get_posts

root = pathlib.Path(__file__).parent.resolve()

post_eng_re = {
    'regex': re.compile(r"<!-- posts starts -->.*<!-- posts ends -->",
                        re.DOTALL),
    'replace': '<!-- posts starts -->\n {} \n<!-- posts ends -->'}
post_ptbr_re = {
    'regex': re.compile(r"<!-- posts inicio -->.*<!-- posts fim -->",
                        re.DOTALL),
    'replace': '<!-- posts inicio -->\n {} \n<!-- posts fim -->'}

REGEXES = [post_eng_re, post_ptbr_re]

if __name__ == "__main__":
    readme = root / "README.md"

    # Retrieve most recent posts for each language
    posts = get_posts(2)

    post_eng_re['replace'] = post_eng_re['replace'].format('\n '.join(
        posts['eng']))
    post_ptbr_re['replace'] = post_ptbr_re['replace'].format('\n '.join(
        posts['pt-br']))

    # Write posts
    readme_path = os.getcwd() + '/README.md'
    for reg in REGEXES:
        readme_contents = readme.open().read()
        readme.open("w").write(reg['regex'].sub(reg['replace'],
                                                readme_contents))
