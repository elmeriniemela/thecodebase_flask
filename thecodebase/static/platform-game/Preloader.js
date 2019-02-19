

class Preloader extends Phaser.Scene {

    constructor () 
    {
        super('Preloader'); 
    }

    preload() 
    {
        this.load.image('sky', '/static/platform-game/assets/sky.png');
        this.load.image('ground', '/static/platform-game/assets/platform.png');
        this.load.image('star', '/static/platform-game/assets/star.png');
        this.load.image('bomb', '/static/platform-game/assets/bomb.png');
        this.load.spritesheet('dude', 
            '/static/platform-game/assets/dude.png',
            { frameWidth: 32, frameHeight: 48 }
        );
        this.load.image('sky', '/static/platform-game/assets/sky.png');
        this.load.bitmapFont('arcade', '/static/platform-game/assets/fonts/bitmap/arcade.png', '/static/platform-game/assets/fonts/bitmap/arcade.xml');
    }

    create() 
    {
        this.anims.create({
            key: 'left',
            frames: this.anims.generateFrameNumbers('dude', { start: 0, end: 3 }),
            frameRate: 10,
            repeat: -1
        });

        this.anims.create({
            key: 'turn',
            frames: [ { key: 'dude', frame: 4 } ],
            frameRate: 20
        });

        this.anims.create({
            key: 'right',
            frames: this.anims.generateFrameNumbers('dude', { start: 5, end: 8 }),
            frameRate: 10,
            repeat: -1
        });

        this.scene.start('GamePlay');
    }

}
