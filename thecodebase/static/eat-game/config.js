/*--- CONFIG + RUNNING THE GAME ---*/

//Define the game config once everything else is defined
var config = {
    type: Phaser.AUTO,
    width: 640,
    height: 480,
    pixelArt: true,
    physics: {
        default: "arcade",
        arcade: {
        gravity: { y: 0 },
        debug: false
        }
    },
    scene: gamePlay,
    canvas: gameCanvas,
    };

//Instantiate the game with the config
var game = new Phaser.Game(config);