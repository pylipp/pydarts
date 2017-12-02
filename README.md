          ___                                   ___           ___                         ___
         /\  \                   _____         /\  \         /\  \                       /\__\
        /::\  \       ___       /::\  \       /::\  \       /::\  \         ___         /:/ _/_
       /:/\:\__\     /|  |     /:/\:\  \     /:/\:\  \     /:/\:\__\       /\__\       /:/ /\  \
      /:/ /:/  /    |:|  |    /:/  \:\__\   /:/ /::\  \   /:/ /:/  /      /:/  /      /:/ /::\  \
     /:/_/:/  /     |:|  |   /:/__/ \:|__| /:/_/:/\:\__\ /:/_/:/__/___   /:/__/      /:/_/:/\:\__\
     \:\/:/  /    __|:|__|   \:\  \ /:/  / \:\/:/  \/__/ \:\/:::::/  /  /::\  \      \:\/:/ /:/  /
      \::/__/    /::::\  \    \:\  /:/  /   \::/__/       \::/~~/~~~~  /:/\:\  \      \::/ /:/  /
       \:\  \    ~~~~\:\  \    \:\/:/  /     \:\  \        \:\~~\      \/__\:\  \      \/_/:/  /
        \:\__\        \:\__\    \::/  /       \:\__\        \:\__\          \:\__\       /:/  /
         \/__/         \/__/     \/__/         \/__/         \/__/           \/__/       \/__/

# pydarts

>   A Python3 assistant (and library) for playing darts

Play with your friends and keep track of your darts scores!

## Features
- arbitrary start value (501, 301, whatever positive number you like, ...)
- unlimited number of players
- scores can be passed in sum (i.e. the total visit) or throw by throw
- finish suggestions
- player database to keep track of player performance (average, highscore, finishes, etc.)
- no external dependencies for basic functionality

## Upcoming

## TODO
- revisit finish options (e.g. 56, 46)
- make command line program run with Python 2

## Installation

Get the source code

    git clone https://github.com/pylipp/pydarts
    cd pydarts

Install to a virtualenv (I like using virtualenvwrapper)

    mkvirtualenv --python=$(which python3) pydarts
    make install
    make test

ALTERNATIVELY, install to `~/.local` using pip

    pip install --user -e .

OPTIONALLY, you can install sound and histogram support

    pip install simpleaudio==1.0.1
    pip install -e git+https://github.com/pylipp/data_hacks.git@refactoring#egg=data_hacks

Tested on Debian using Python 3.5 and 3.6.

## Usage

### Command line assistant

Execute `pydarts` in the command line to start a classic 501 game. The setup instructions should be self-explanatory.

When the game starts, the program expects a player's score as an input. There are various options:

1. You sum up the three throws of your visit yourself. Say you score 60, 5 and 1, i.e. a total of 66. You type `66d` and hit enter. The suffix `d` indicates that your *d*one.
1. You directly enter after each throw. Say you score a triple 19, so you type 57 and hit enter. The prompt shows that you have two darts left. Repeat or use method 1.
1. You busted. Type `b` and hit enter.
1. Invalid input is not processed, please enter a correct value the next time.
1. The program takes some constraints into account to check if your input is valid (e.g. total visit sum <= 180). Try to trick it and submit an issue if you found a glitch.

When the game is finished (i.e. one player has won the specified number of legs), the program asks whether you want to play again. Answer

1. `y` (YES) if you want a rematch using the same settings
1. `n` (NO) if you want to play again but re-define the settings
1. `q` (QUIT) if you want to quit the application

### Library

`pydarts` provides an API to include the dart assisting functionality into custom projects. Subclass `communication.CommunicatorBase`, create a `game.Game` object and `run()` it! Note that this call blocks until the user decides to quit. You might decide to execute it in a separate thread.

Example: I have a Raspberry/Arduino/ROS [project](https://github.com/pylipp/dartbox). The custom communicator uses a ROS publisher to forward information to an LCD, taking the limited character width into account. Input requests are implemented using ROS client calls to the server (the Arduino listening for keypresses).

I can see a GUI being built on top of the library.

### IMPORTANT

The last visit has to be entered throw by throw. Otherwise, the evaluation of the total number of throws per visit is not correct!

For displaying player statistics, type `pydarts --stats <player_name>`. You can put any number of names. Without any name, information of all players is printed.

Also, see the output of `pydarts --help`.

Have fun!

## Example

Watch MVG casually nailing a 9 darter:

    > pydarts
    Nr of players: 1
    Name of player 1: MVG
    Start value: 501
    Nr of legs: 1
    MVG has 501 and three darts left.
    MVG's score: 180
    MVG has 321 and three darts left.
    MVG's score: 180
    MVG has 141 and three darts left.
    Finish options:
        T20 T19 D12
    MVG's score: 60
    MVG has 81 and two darts left.
    Finish options:
        T19 D12
        T15 D18
    MVG's score: 57
    MVG has 24 and one dart left.
    MVG's score: 24
        MVG:  1
    ================================================================================
    > pydarts -s MVG
    MVG:
    Legs won: 1
    Average: 167.00
    Highscore: 180
    Finishes:
        141: 1
    Darters:
          9-darter: 1

## Credits
- The sound file is generated by [PulseBoy](http://www.pulseboy.com/).
- ASCII art is generated from [this tool](http://patorjk.com/software/taag/#p=display&f=Isometric2&t=pydarts).
