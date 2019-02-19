
class Leaderboard extends Phaser.Scene {

    constructor () 
    {
        super('Leaderboard')
        
    }

    preload() {
        this.load.bitmapFont('arcade', '/static/platform-game/assets/fonts/bitmap/arcade.png', '/static/platform-game/assets/fonts/bitmap/arcade.xml');
    }

    create() {

    }

    update() {
        if (this.input.space.isDown) {
            this.scene.stop();
            let game = this.scene.get('GamePlay')
            game.scene.resume();
            game.restart_game();
        }
    }

    createLeaderboard(data) 
    {
        this.menuTexts = new Array();
        var rankX = 100;
        var nameX = 400;
        var scoreX = 700;

        var startY = 70;
        var stepY = 40;
        this.addText(400, 20, 'PRESS SPACE');
        this.addText(rankX, startY, 'RANK');
        this.addText(nameX, startY, 'NAME');
        this.addText(scoreX, startY, 'SCORE');

        startY += 20;

        var scoreLines = $.parseJSON(data)

        var rank = 1;
        for (var i = 0; i < scoreLines.length; i++) {
            var line = scoreLines[i];
            var y = startY + (rank * stepY);

            this.addText(rankX, y, rank);
            this.addText(nameX, y, line[0]);
            this.addText(scoreX, y, line[1]);

            rank++;
        }
    }
    addText(x, y, text) 
    {
        this.menuTexts.push(this.add.bitmapText(x, y, 'arcade', text).setTint(0xff00ff).setOrigin(0.5, 0));
    }

    postScore(score) {
        $.ajax({
            type: 'POST',
            url: '/post-score',
            // Add this scene as the scope of the succes callback 
            // so objects can be added to the scene
            context: this,
            data: {
                score: score 
            },
            success: this.createLeaderboard
        });

    }
}

