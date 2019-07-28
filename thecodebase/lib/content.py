

from collections import (
    namedtuple,
    defaultdict,
)

from . import sql
from . import github_integration as github


Card = namedtuple('Card', ['title', 'url', 'image', 'description'])
PhaserGame = namedtuple('PhaserGame', ['title', 'url', 'image', 'description', 'folder', 'files'])


class __content:

    repos = defaultdict(list)

    def __init__(self):
        self.topics = (
            Card(
                title='Python',
                url='python',
                image='images/python_logo.png',
                description="Python is my strongest language. "
                    "It's the main language I've used professionally."
            ),
            Card(
                title='Java',
                url='java',
                image='images/java_logo.png',
                description="I learned Java in University of Helsinki. "
                    "I've also used it in my work at SprintIT.",
            ),
            Card(
                title='Web Development',
                url='web-developmen',
                image='images/web-development.jpg',
                description="This website is an example of my skills with Flask and Bootstrap. "
                    "I've also learned alot about deploying servers from my work at SprintIT.",
            ),
            Card(
                title='C/C++',
                url='c-c-plus',
                image='images/c++.png',
                description="I've studied the basics of C/C++. "
                    "There's alot I'd like to do with C++ for example "
                    "rewrite some of the games I've made with pygame.",
            ),
            Card(
                title='JavaScript',
                url='javascript',
                image='images/javascript.png',
                description="I aspire to master JavaScript, since I've already encountered "
                    "it in my work as an Odoo developer, but also in personal projects.",
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

        self.query_repos()

    def query_repos(self):
        rows = github.get_all_repos()
        for row in rows:
            topic = row.get('topic', 'unidenified')
            self.repos[topic].append(row)

content = __content()    
