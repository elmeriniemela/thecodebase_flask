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

    this.load.bitmapFont('arcade', '/static/platform-game/assets/fonts/bitmap/arcade.png', '/static/platform-game/assets/fonts/bitmap/arcade.xml');
}