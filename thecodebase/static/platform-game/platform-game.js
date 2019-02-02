function preload ()
{
    this.load.image('sky', '/static/platform-game/assets/sky.png');
    this.load.image('ground', '/static/platform-game/assets/platform.png');
    this.load.image('star', '/static/platform-game/assets/star.png');
    this.load.image('bomb', '/static/platform-game/assets/bomb.png');
    this.load.spritesheet('dude', 
        '/static/platform-game/assets/dude.png',
        { frameWidth: 32, frameHeight: 48 }
    );
}

var platforms;

function create ()
{
    this.add.image(400, 300, 'sky');

    platforms = this.physics.add.staticGroup();

    platforms.create(400, 568, 'ground').setScale(2).refreshBody();

    platforms.create(600, 400, 'ground');
    platforms.create(50, 250, 'ground');
    platforms.create(750, 220, 'ground');
}

function update ()
{
}