from collections import namedtuple

Project = namedtuple('Project', ['title', 'url', 'html_file', 'image'])
Topic = namedtuple('Topic', ['title', 'url', 'image', 'description'])

def Content():
    python = Topic(
        title='Python', 
        url='python', 
        image='python_logo.png',
        description="Python is my strongest language. It's the main language I've used professionally."
    )

    java = Topic(
        title='Java', 
        url='java', 
        image='java_logo.png',
        description="I learned Java in University of Helsinki. I've also used it in my work at SprintIT.",
    )


    web_development = Topic(
        title='Web Development', 
        url='web-development', 
        image='web-development.jpg',
        description="This website is an example of my skills with Flask and Bootstrap. I've also learned alot about deploying servers from my work at SprintIT.",
    )
    c_c_plus = Topic(
        title='C/C++', 
        url='C-C++', 
        image='c++.png',
        description="I've studied the basics of C/C++. There's still alot I'd like to do with C++ for example rewrite some of the games I've made with pygame.",
    )
    javascript = Topic(
        title='JavaScript', 
        url='javascript', 
        image='javascript.png',
        description="I aspire to master JavaScript, since I've already encountered it in my work as an Odoo developer, but also in personal projects.",
    )

    return {
        python : [
            Project('Tower Defence', 'TowerDefence', 'tdgame.html', 'tdgame.png'),
            Project('Bemarifield', 'Bemarifield', 'bemarifield.html', 'bem1.png'),
            Project('Physics 2D', 'Physics', 'physics.html', 'physics.gif'),

            Project('Odoo', 'odoo-portfolio', False, 'under_construction.png'),
        ],
        java : [
            Project('Tic Tac Toe', 'tic-tac-toe', 'tic-tac-toe.html', 'tic-tac-toe.png'),
            Project('Game Of Life', 'game-of-life', False, 'under_construction.png'),
            Project('Falling Sand', 'falling-sand', False, 'under_construction.png'),
            Project('Asteroids', 'asteroids', False, 'under_construction.png'),
        ],
        web_development : [
            Project('The Codebase', 'thecodebase', 'thecodebase.html', 'server_combined.jpg'),
            Project('Django', 'django', False, 'under_construction.png'),
        ],
        c_c_plus : [
            Project('C-practice', 'c-harjoitus', 'c-practice.html', 'c-practice.png'),
            Project('Python C-extension', 'c-extension', False, 'under_construction.png'),
        ],
        javascript : [
            Project('React.js', 'react-js', False, 'under_construction.png'),
            Project('Bacon.js', 'bacon-js', False, 'under_construction.png'),
        ]
    }
    
