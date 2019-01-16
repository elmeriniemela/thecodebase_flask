from collections import namedtuple

Project = namedtuple('Project', ['title', 'url', 'html_file'])
Topic = namedtuple('Topic', ['title', 'url', 'image'])

def Content():
    return {
        Topic('Python', url='python', image='python_logo.png'): [
            Project('Tower Defence', 'TowerDefence', 'tdgame.html'),
            Project('Bemarifield', 'bem', 'bemarifield.html'),
            Project('Physics 2D', 'physics', 'physics.html'),

            Project('Odoo', 'odoo-portfolio', 'coming-soon.html'),
        ],
        Topic('Java', url='java', image='java_logo.png'): [
            Project('Tic Tac Toe', 'tic-tac-toe', 'tic-tac-toe.html'),
        ],
        Topic('Web Development', url='web-development', image='web-development.jpg'): [
            Project('Flask', 'flask', 'coming-soon.html'),
            Project('Django', 'django', 'coming-soon.html'),
        ],
        Topic('C/C++', url='C-C++', image='c++.png'): [
            Project('C-practice', 'c-practice', 'c-practice.html'),
            Project('Python C-extension', 'c-extension', 'coming-soon.html'),
        ],
        Topic('JavaScript', url='javascript', image='javascript.png'): [
            Project('React.js', 'react-js', 'coming-soon.html'),
            Project('Bacon.js', 'bacon-js', 'coming-soon.html'),
        ]
    }
    
