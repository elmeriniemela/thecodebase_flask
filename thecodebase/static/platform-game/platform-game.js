
class GamePlay extends Phaser.Scene {

    constructor () 
    {
        super('GamePlay')
        this.score = 0;
        this.gameOver = false;
    }

    preload ()
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

    create ()
    {
        //  A simple background for our game
        this.add.image(400, 300, 'sky');

        //  The this.platforms group contains the ground and the 2 ledges we can jump on
        this.platforms = this.physics.add.staticGroup();

        //  Here we create the ground.
        //  Scale it to fit the width of the game (the original sprite is 400x32 in size)
        this.platforms.create(400, 568, 'ground').setScale(2).refreshBody();

        //  Now let's create some ledges
        this.platforms.create(600, 400, 'ground');
        this.platforms.create(50, 250, 'ground');
        this.platforms.create(750, 220, 'ground');

        // The this.player and its settings
        this.player = this.physics.add.sprite(100, 450, 'dude');

        //  Player physics properties. Give the little guy a slight bounce.
        this.player.setBounce(0.2);
        this.player.setCollideWorldBounds(true);

        //  Our this.player animations, turning, walking left and walking right.
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

        //  Input Events
        this.cursors = this.input.keyboard.createCursorKeys();

        //  Some this.stars to collect, 12 in total, evenly spaced 70 pixels apart along the x axis
        this.stars = this.physics.add.group({
            key: 'star',
            repeat: 11,
            setXY: { x: 12, y: 0, stepX: 70 }
        });

        this.stars.children.iterate(function (child) {

            //  Give each star a slightly different bounce
            child.setBounceY(Phaser.Math.FloatBetween(0.4, 0.8));

        });

        this.bombs = this.physics.add.group();
        var x = (this.player.x < 400) ? Phaser.Math.Between(400, 800) : Phaser.Math.Between(0, 400);
        var bomb = this.bombs.create(x, 16, 'bomb');
        bomb.setBounce(1);
        bomb.setCollideWorldBounds(true);
        bomb.setVelocity(Phaser.Math.Between(-200, 200), 20);
        bomb.allowGravity = false;

        //  The this.score
        this.scoreText = this.add.text(16, 16, 'Score: 0', { fontSize: '32px', fill: '#000' });

        //  Collide the this.player and the this.stars with the this.platforms
        this.physics.add.collider(this.player, this.platforms);
        this.physics.add.collider(this.stars, this.platforms);
        this.physics.add.collider(this.bombs, this.platforms);

        //  Checks to see if the this.player overlaps with any of the this.stars, if he does call the collectStar function
        this.physics.add.overlap(this.player, this.stars, this.collectStar, null, this);

        this.physics.add.collider(this.player, this.bombs, this.hitBomb, null, this);
    }

    update ()
    {
        if (this.gameOver)
        {
            return;
        }

        if (this.cursors.left.isDown)
        {
            this.player.setVelocityX(-160);

            this.player.anims.play('left', true);
        }
        else if (this.cursors.right.isDown)
        {
            this.player.setVelocityX(160);

            this.player.anims.play('right', true);
        }
        else
        {
            this.player.setVelocityX(0);

            this.player.anims.play('turn');
        }

        if (this.cursors.up.isDown && this.player.body.touching.down)
        {
            this.player.setVelocityY(-330);
        }
    }

    collectStar (player, star)
    {
        star.disableBody(true, true);

        //  Add and update the this.score
        this.score += 10;
        this.scoreText.setText('Score: ' + this.score);

        if (this.stars.countActive(true) === 0)
        {
            //  A new batch of this.stars to collect
            this.stars.children.iterate(function (child) {

                child.enableBody(true, child.x, 0, true, true);

            });

            var x = (player.x < 400) ? Phaser.Math.Between(400, 800) : Phaser.Math.Between(0, 400);

            var bomb = this.bombs.create(x, 16, 'bomb');
            bomb.setBounce(1);
            bomb.setCollideWorldBounds(true);
            bomb.setVelocity(Phaser.Math.Between(-200, 200), 20);
            bomb.allowGravity = false;

        }

        

    }

    hitBomb (player, bomb)
    {
        this.physics.pause();

        player.setTint(0xff0000);

        player.anims.play('turn');

        this.gameOver = true;
        var rankX = 100;
        var nameX = 400;
        var scoreX = 700;

        var startY = 70;
        var stepY = 40;
        
        var text;
        text = this.add.bitmapText(0, startY, 'arcade', 'RANK').setTint(0xff00ff);
        text.setX(rankX - text.width / 2);

        text = this.add.bitmapText(0, startY, 'arcade', 'NAME').setTint(0xff00ff);
        text.setX(nameX - text.width / 2);

        text = this.add.bitmapText(0, startY, 'arcade', 'SCORE').setTint(0xff00ff);
        text.setX(scoreX - text.width / 2);
        startY += 20;

        var scoreLines;
        $.ajax({
            async: false,
            type: 'POST',
            url: '/post-score',
            data: {
                score: this.score 
            },
            success: function(data) {
                scoreLines = $.parseJSON(data);
        }
        });
        

        
        var rank = 1;
        for (var i = 0; i < scoreLines.length; i++) {
            var line = scoreLines[i];
            var y = startY + (rank * stepY);
            text = this.add.bitmapText(0, y, 'arcade', rank).setTint(0xff00ff);
            text.setX(rankX - text.width / 2);

            text = this.add.bitmapText(0, y, 'arcade', line[0]).setTint(0xff00ff);
            text.setX(nameX - text.width / 2);

            text = this.add.bitmapText(0, y, 'arcade', line[1]).setTint(0xff00ff);
            text.setX(scoreX - text.width / 2);


            rank++;
        }
        
    }

}







