# Hyperdimensional Minesweeper
 The game minesweeper on steroids

## Contents of Each File
DON'T FORGET THISSSSSSSSSS

## Mines
_Mines_ is played on a rectangular $n \times m$ board (where $n$ indicates the number of rows and $m$ the number of columns), covered with $1\times 1$ square tiles. Some of these tiles hide secretly buried mines; all the other squares are safe (and, generally, relative to the size of the board, only a small number of squares contain bombs). On each turn, the player removes one tile, revealing either a mine or a safe square. The game is won when all safe tiles have been removed, without revealing a single mine, and it is lost if a mine is revealed.

The game wouldn't be much of a game at all if it only involved random guessing, so the following twist is added: when a safe square is revealed, that square is additionally inscribed with a number between 0 and 8, indicating the number of surrounding mines (when rendering the board, `0` is replaced by a blank). Additionally, any time a `0` is revealed (a square surrounded by no mines), the surrounding squares are also automatically revealed (they are, by definition, safe).

## An Implementation of Mines
### Game State 
The state of an ongoing _Mines_ game is represented as a dictionary with the following four keys:
* `'dimensions'`: a tuple containing the board's dimensions `(nrows, ncolumns)`
* `'board'`: a 2-dimensional array (implemented using nested lists) of integers and strings. `game['board'][r][c]` is `'.'` is square _(r,c)_ contains a bomb, and it is a number indicating the number of neighboring bombs otherwise.
* `'visible'`: a 2-dimensional array (implemented using nested lists) of Booleans. `game[visible][r][c]` indicates whether the contents of square _(r,c)_ are visible to the player.
* `'state'`: a string containing the state of the game (`'ongoing'` if the game is in progress, `'victory'` if the game has been won, and `'defeat'` if the game has been lost). The state of a new game is _always_ `'ongoing'`.

For example, the following is a valid _Mines_ game state:
```
{
    'dimensions': (4, 3),
    'board': [[1,  '.',  2], [1,   2,  '.'], [1,   2,   1], ['.', 1,   0]],
    'visible': [[True, False, False], [False, True, False], [False, True, True], [False, True, True]],
    'state': 'ongoing',
}
```

### Game Logic
The game is implemented via four functions in `lab.py`:
* `new_game_2d` creates a new object to represent a game, given board dimensions and mine coordinates.

* `dig_2d` implements the digging logic (updating the game state if necessary) and returns the number of new tiles revealed from that move.

* `render_2d_locations` renders the game into a 2D grid (for display).

* `render_2d_board` renders a game state as ASCII art.

Each of these functions is documented in detail in lab.py. 

## An Example Game
This section runs through an example game.

Calling new_game_2d produces a new game object as described above:
```
>>> game = new_game_2d(6, 6, [(3, 0), (0, 5), (1, 3), (2, 3)])
>>> dump(game)
board:
    [0, 0, 1, 1, 2, '.']
    [0, 0, 2, '.', 3, 1]
    [1, 1, 2, '.', 2, 0]
    ['.', 1, 1, 1, 1, 0]
    [1, 1, 0, 0, 0, 0]
    [0, 0, 0, 0, 0, 0]
dimensions: (6, 6)
visible:
    [False, False, False, False, False, False]
    [False, False, False, False, False, False]
    [False, False, False, False, False, False]
    [False, False, False, False, False, False]
    [False, False, False, False, False, False]
    [False, False, False, False, False, False]
state: ongoing
>>> render_2d_locations(game)
[['_', '_', '_', '_', '_', '_'],
 ['_', '_', '_', '_', '_', '_'],
 ['_', '_', '_', '_', '_', '_'],
 ['_', '_', '_', '_', '_', '_'],
 ['_', '_', '_', '_', '_', '_'],
 ['_', '_', '_', '_', '_', '_']]
```

Assume the player first digs at (1, 0) by invoking the dig_2d method. The return value 9 indicates that 9 squares were revealed.

```
>>> dig_2d(game, 1, 0)
9
>>> dump(game)
board:
    [0, 0, 1, 1, 2, '.']
    [0, 0, 2, '.', 3, 1]
    [1, 1, 2, '.', 2, 0]
    ['.', 1, 1, 1, 1, 0]
    [1, 1, 0, 0, 0, 0]
    [0, 0, 0, 0, 0, 0]
dimensions: (6, 6)
visible:
    [True, True, True, False, False, False]
    [True, True, True, False, False, False]
    [True, True, True, False, False, False]
    [False, False, False, False, False, False]
    [False, False, False, False, False, False]
    [False, False, False, False, False, False]
state: ongoing
>>> render_2d_locations(game)
[[' ', ' ', '1', '_', '_', '_'],
 [' ', ' ', '2', '_', '_', '_'],
 ['1', '1', '2', '_', '_', '_'],
 ['_', '_', '_', '_', '_', '_'],
 ['_', '_', '_', '_', '_', '_'],
 ['_', '_', '_', '_', '_', '_']]
```

…then at (5, 4) (which reveals 21 new squares):
```
>>> dig_2d(game, 5, 4)
21
>>> dump(game)
board:
    [0, 0, 1, 1, 2, '.']
    [0, 0, 2, '.', 3, 1]
    [1, 1, 2, '.', 2, 0]
    ['.', 1, 1, 1, 1, 0]
    [1, 1, 0, 0, 0, 0]
    [0, 0, 0, 0, 0, 0]
dimensions: (6, 6)
visible:
    [True, True, True, False, False, False]
    [True, True, True, False, True, True]
    [True, True, True, False, True, True]
    [False, True, True, True, True, True]
    [True, True, True, True, True, True]
    [True, True, True, True, True, True]
state: ongoing
>>> render_2d_locations(game)
[[' ', ' ', '1', '_', '_', '_'],
 [' ', ' ', '2', '_', '3', '1'],
 ['1', '1', '2', '_', '2', ' '],
 ['_', '1', '1', '1', '1', ' '],
 ['1', '1', ' ', ' ', ' ', ' '],
 [' ', ' ', ' ', ' ', ' ', ' ']]
```

Emboldened by this success, the player then makes a fatal mistake and digs at (0, 5), revealing a bomb:
```
>>> dig_2d(game, 0, 5)
1
>>> dump(game)
board:
    [0, 0, 1, 1, 2, '.']
    [0, 0, 2, '.', 3, 1]
    [1, 1, 2, '.', 2, 0]
    ['.', 1, 1, 1, 1, 0]
    [1, 1, 0, 0, 0, 0]
    [0, 0, 0, 0, 0, 0]
dimensions: (6, 6)
visible:
    [True, True, True, False, False, True]
    [True, True, True, False, True, True]
    [True, True, True, False, True, True]
    [False, True, True, True, True, True]
    [True, True, True, True, True, True]
    [True, True, True, True, True, True]
state: defeat
>>> render_2d_locations(game)
[[' ', ' ', '1', '_', '_', '.'],
 [' ', ' ', '2', '_', '3', '1'],
 ['1', '1', '2', '_', '2', ' '],
 ['_', '1', '1', '1', '1', ' '],
 ['1', '1', ' ', ' ', ' ', ' '],
 [' ', ' ', ' ', ' ', ' ', ' ']]
```

## HyperMines (N-dimensional Mines)
Now that we've mastered 2-dimensional Mines, we're going to add a little twist `:)`

Rather than playing on 2-dimensional boards, we're going to extend our _Mines_ game to work on higher-dimensional boards. In this variant, which we'll call _HyperMines_, everything works just the same as in _Mines_, except for the fact that each cell has up to $3^{n}-1$ neighbors, instead of 8 (where _n_ is the dimensionality of the space we're playing in).

### Game Representation and Flow
#### Game State
Similarly to our 2-D representation, we will represent games as dictionaries, each of which should contain the following four keys:
* `'dimension'`, the board's dimensions (an arbitrary tuple of positive integers)
* `'board'`, an N-dimensional array (implemented using nested lists) of integers and strings. In an game called `g`, `g['board'][x_0][...][x_k]` is `"."` if the square with coordinate $(x_{0}, ..., x_{k})$ contains a bomb.
* `'visible'`, an N-dimensional array (implemented using nested lists) of Booleans. In a game called `g`, `g['visible'][x_0][...][x_k]` indicates whether the contents of square $(x_{0}, ..., x_{k})$ are visible to the player.
* `'state'`, a string containing the state of the game: `'ongoing'` if the game is in progress, `'victory'` if the game has been won, and `'defeat'` if the game has been lost. The state of a new game is always 'ongoing'.

For example, the following is a valid HyperMines game state:
```
{
    'dimensions': (4, 3, 2),
    'board': [[[1, 1], ['.', 2], [2, 2]], [[1, 1], [2, 2], ['.', 2]],
             [[1, 1], [2, 2], [1, 1]], [[1, '.'], [1, 1], [0, 0]]],
    'visible': [[[True, False], [False, False], [False, False]], [[False, False], [True, False], [False, False]],
            [[False, False], [True, True], [True, True]], [[False, False], [True, True], [True, True]]],
    'state': 'ongoing',
}
```

## An Example Game
This section runs through an example game in 3D.
```
>>> game = new_game_nd((3,3,2),[(1,2,0)])
>>> dump(game)
board:
    [[0, 0], [1, 1], [1, 1]]
    [[0, 0], [1, 1], ['.', 1]]
    [[0, 0], [1, 1], [1, 1]]
dimensions: (3, 3, 2)
visible:
    [[False, False], [False, False], [False, False]]
    [[False, False], [False, False], [False, False]]
    [[False, False], [False, False], [False, False]]
state: ongoing
```

The player tries digging at (2,1,0), which reveals 1 tile.

```
>>> dig_nd(game, (2,1,0))
1
>>> dump(game)
board:
    [[0, 0], [1, 1], [1, 1]]
    [[0, 0], [1, 1], ['.', 1]]
    [[0, 0], [1, 1], [1, 1]]
dimensions: (3, 3, 2)
visible:
    [[False, False], [False, False], [False, False]]
    [[False, False], [False, False], [False, False]]
    [[False, False], [True, False], [False, False]]
state: ongoing
```

… then at (0,0,0) which reveals 11 new tiles:

```
>>> dig_nd(game, (0,0,0))
11
>>> dump(game)
board:
    [[0, 0], [1, 1], [1, 1]]
    [[0, 0], [1, 1], ['.', 1]]
    [[0, 0], [1, 1], [1, 1]]
dimensions: (3, 3, 2)
visible:
    [[True, True], [True, True], [False, False]]
    [[True, True], [True, True], [False, False]]
    [[True, True], [True, True], [False, False]]
state: ongoing
```

Emboldened by this success, the player then makes a fatal mistake and digs at (1,2,0), revealing a bomb:

```
>>> dig_nd(game, (1,2,0))
1
>>> dump(game)
board:
    [[0, 0], [1, 1], [1, 1]]
    [[0, 0], [1, 1], ['.', 1]]
    [[0, 0], [1, 1], [1, 1]]
dimensions: (3, 3, 2)
visible:
    [[True, True], [True, True], [False, False]]
    [[True, True], [True, True], [True, False]]
    [[True, True], [True, True], [False, False]]
state: defeat
```