# Snake - a simple game in Python
A simple game Snake written in Python and PyGame.<br>
I've created this project as a first major project in Python. For me creating games is the easiest way to undestand the basics of progamming language.<br>

### Screenshots

<img src="/img/Sclip1.jpg" width="400"> <img src="/img/Sclip2.jpg" width="400">
<img src="/img/Sclip3.jpg" width="400"> <img src="/img/Sclip4.jpg" width="400">

### Setup
| Name   | Version |
| :--:   | :--:    |
| Python | 3.6.5   |
| PyGame | 1.9.4   |

Download into one folder:
- main font: alpha_echo.ttf
- png files: apple.png, ball.png, head.png,
- code file: snake.py

and run with `python snake.py`.

### How to play

* The main menu can be operated with the mouse and keyboard (LEFT, RIGHT, ENTER keys)
* You control the snake with LEFT, RIGHT, UP and DOWN keys
* During the game press P for Pause or Q for Quit (if the score is the best one, the programm saves it)
* Levels:
  * EASY - slow speed, no borders to hit, snake can go through the window
  * MEDIUM - slow speed, there is a border which the snake
  * HARD - high speed, no borders to hit, snake can go through the window   

### Saving and loading of your best score

The programme saves and loads the score using [shelve](https://docs.python.org/3/library/shelve.html) module. When the player ends the game (crashes / eats itself / quits) three files *score.txt.bak*, *score.txt.dat*, *score.txt.dir* storing best score of each level are automatically created within the same folder.

### Author

Piotr Mucha

### License

This project is licensed under the MIT License - (LICENSE.md file to be updated)

# Acknowledgments

* The mechanism of the game is based on tutorial of Al Sweigart http://inventwithpython.com/pygame
* http://stackoverflow.com community where I found solutions for:
  - implementing shelve module to save/load best score to a file
  - how to use *.png* graphics of the apple and snake instead of simple shapes
