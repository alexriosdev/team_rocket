# team_rocket
<b>Repository for Game Dev Class</b><br>

This repo contains the necessary files for the Game Showcase project on February 23, 2017 <br>

<h4>How to run the game</h4> 
  - Make sure to have Python 2.7 and Pygame installed
  - Make sure to have the following included in the game folder:
    - main.py
    - sprite1.py
    - utils.py
    - Images folder
    - Sounds folder
  - Run main.py on Python 2.7 and enjoy!
  
<h3>Notes:</h3>
For this particular demo the following files are included:
  - main.py - (Main file) 
  - sprite1.py
  - utils.py
  - Images
    - background_update.png
    - Floor4.png
    - player1-3.png (player sprites)
    - security1-3.png (enemy sprites)
    - student1-2.png (student sprites)
    - coffee1-3.png (powerup sprites)
    - trash1.png
    - bench1.png
    - long_bench.png  
  - Sounds
    - song.mp3
    - jump.wav
    - bump.wav
    - powerup.wav

<!-- <h4>Reference Files</h4>
  - demo_play.py - (Old main file) 
  - background2.png  
  - player.png  
  - demo_play2.py - (Same as main file, just has the Start Screen added)
  - enemy.png -->


<h4>Progress:</h4> 

  - Background and Player Dimensions have been defined
    - Background resolution has been set to 1024x764
    - Player resolution has been set to 128x100
  - Background is able to loop seamesly
  - Player sprite is able to move with the use of a keyboard
  - Player sprite is able to move with defined speed
  - Implementation of a Start Screen
  - Enemy sprite added
  - Enemy sprite follows player like a shadow
  - Player sprite is able to jump
  - Player sprite does not go outside screen boundaries
  - Player slows down if steps out of paved path
  - Player falls back if doesn't jump obstacle 
  - Potholes have been added as a jumping obstacle
  - Gameover screen appears when user exceeds lower boundary
  - Gameover screen gives option to Restart or Quit the game
  - Player sprite respawns back to initial position once Restart option is selected
  - Student sprites have been added as obstacles
  - Collision rules have been added to student sprites
  - Score system added and displayed
  - Obstacles are added every time score icrements 500 points
  - Running animation added to player sprite
  - Running animation added to enemy and student sprites
  - Powerup sprite added
  - Player moves up when touching a powerup sprite
  - Powerup respawns every 900 points
  - Obstacle class created so as to integrate new object sprites
  - Sound FX added
  - Score system now displays previous player score
  - Movement delay for enemy sprite added
  - Image sprites and sound fx organized in folders
  - Player sprite now has shadow when jumping
    
<h4>To do:</h4>
  - Refine sprite animations
  
<h4>Changes:</h4>
   - SPACEBAR is used to start the game so that users will already be set to jump when game starts
    


