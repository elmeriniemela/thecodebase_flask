

import logging
import re
import json
from collections import (
    namedtuple,
)
from datetime import datetime


import requests
from github import Github
import markdown

from . import sql

    

Topic = namedtuple('Topic', ['title', 'url', 'image', 'description', 'repos'])
PhaserGame = namedtuple('PhaserGame', ['title', 'url', 'image', 'description', 'folder', 'files'])

logger = logging.getLogger(__name__)



def prettify(repo_name):
    words = re.split(r'[ \-_]', repo_name)
    words = [word.capitalize() for word in words]
    return ' '.join(words)



class __content:

    topics = tuple()
    topics = tuple()

    def __init__(self):
        self.topics = (
            Topic(
                title='Python',
                url='python',
                image='images/python_logo.png',
                description="Python is my strongest language. "
                    "It's the main language I've used professionally.",
                repos=[],
            ),
            Topic(
                title='Java',
                url='java',
                image='images/java_logo.png',
                description="I learned Java in University of Helsinki. "
                    "I've also used it in my work at SprintIT.",
                repos=[],
            ),
            Topic(
                title='Web Development',
                url='web-development',
                image='images/web-development.jpg',
                description="This website is an example of my skills with Flask and Bootstrap. "
                    "I've also learned alot about deploying servers from my work at SprintIT.",
                repos=[],
            ),
            Topic(
                title='C/C++',
                url='c-c-plus',
                image='images/c++.png',
                description="I've studied the basics of C/C++. "
                    "There's alot I'd like to do with C++ for example "
                    "rewrite some of the games I've made with pygame.",
                repos=[],
            ),
            Topic(
                title='JavaScript',
                url='javascript',
                image='images/javascript.png',
                description="I aspire to master JavaScript, since I've already encountered "
                    "it in my work as an Odoo developer, but also in personal projects.",
                repos=[],
            ),
        )

        self.games = (
            PhaserGame(
                title='Platform Game',
                url='platform-game',
                image='games/platform-game/docs/platform_game.png',
                description="Collect as many starts as you can, but beware of the bombs! "
                    "See if you can get the highest score.",
                folder='games/platform-game',
                files=['config.js', 'Preloader.js', 'Leaderboard.js', 'GamePlay.js'],
            ),
            PhaserGame(
                title='Eat Game',
                url='eat-game',
                image='games/eat-game/docs/eat_game.png',
                description="Eat the baddies when they are vulnerable, "
                    "but watch out when they're not!",
                folder='games/eat-game',
                files=['config.js', 'eat-game.js']
            ),
        )


    @property
    def repos(self):
        topic_dict = {}
        for topic_tuple in self.topics:
            topic_tuple.repos.clear()
            topic_dict[topic_tuple.url] = topic_tuple


        with sql.Cursor() as cur:
            cur.execute("SELECT * FROM Repo ORDER BY sequence, repo_id")
            columns = [col[0] for col in cur.description]
            rows = [dict(zip(columns, row)) for row in cur.fetchall()]
        for row in rows:
            row['readme_html'] = row['readme_html'].decode()

            topics = json.loads(row.get('topics', '[]'))

            for topic in topics:
                if topic in topic_dict:
                    topic_dict[topic].repos.append(row)

        return rows

    def delete_all_repos(self):
        with sql.Cursor() as cur:
            cur.execute("DELETE FROM Repo")

    def update_repo(self, repo_id, vals):
        data = {
            'display_name': vals['display_name'],
            'readme_html': vals['readme_html'],
            'sequence': vals['sequence'],
            'no_update': bool(vals.get('no_update', False)),
            'update_date': datetime.now()
        }

        sql.update_row('Repo', data, repo_id=repo_id)

    def fetch_repos_from_remote(self, username, password):
        ghub = Github(username, password)
        repos = []
        for repo in ghub.get_user().get_repos():
            if not repo.private and repo.owner.login == username:
                try:
                    readme = repo.get_readme()
                except:
                    continue
                logger.info("Updated repo %s", repo.name)
                readme_str = requests.get(readme.download_url).text
                readme_html = markdown.markdown(readme_str)
                repo.readme_html = readme_html
                repos.append(repo)

        with sql.Cursor() as cur:
            cur.execute("SELECT name, repo_id, no_update FROM Repo")
            existing = {t[0]: (t[1], t[2]) for t in cur.fetchall()}
        
            for repo in repos:
                row = {
                    'readme_html': repo.readme_html,
                    'topics': json.dumps(repo.get_topics()),
                    'update_date': datetime.now(),
                }
                if repo.name in existing:
                    repo_id, no_update = existing[repo.name]
                    if not no_update:
                        sql.update_row('Repo', row, repo_id=repo_id)
                else:
                    row.update(display_name=prettify(repo.name), name=repo.name)
                    sql.insert_row('Repo', row)

content = __content()
