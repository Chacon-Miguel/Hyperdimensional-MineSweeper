#!/usr/bin/env python3
"""6.009 Lab -- Six Double-Oh Mines"""

import typing
import doctest

# NO ADDITIONAL IMPORTS ALLOWED!

translations = [(x-1, y-1) for x in range(3) for y in range(3)]

def dump(game):
    """
    Prints a human-readable version of a game (provided as a dictionary)
    """
    for key, val in sorted(game.items()):
        if isinstance(val, list) and val and isinstance(val[0], list):
            print(f'{key}:')
            for inner in val:
                print(f'    {inner}')
        else:
            print(f'{key}:', val)


# 2-D IMPLEMENTATION

def create_board(num_rows, num_cols, bombs, conditions):
    """
    Creates a 2-d board based on num_rows and num_cols. 
    Uses the bombs list to to check if a bomb is at certain coordinate.
    If so, it gets the first value from conditions, which is '.' and otherwise
    it puts a 0
    """
    board = []
    for r in range(num_rows):
        row = []
        for c in range(num_cols):
            # if there's a bomb
            if (r, c) in bombs:
                # append '.'
                row.append(conditions[0])
            else:
                # if there isn't, append a 0
                row.append(conditions[1])
        board.append(row)
    return board

def get_neighbor_of_bombs(board, bombs, rows, cols):
    """
    Goes through the bombs list to add the number of bombs
    each square is close to
    """
    # for every bomb in the grid...
    for bomb in bombs:
        # for every neighbor of the bomb...
        for t in translations:
            # get the coordinates of the bomb's neighbor...
            n_x, n_y = bomb[0] + t[0], bomb[1] + t[1]
            # if the coordinates are in bounds and the neighbor
            # is a free square, add one to it
            if 0 <= n_x < rows and 0 <= n_y < cols:
                if type(board[n_x][n_y]) == int:
                    board[n_x][n_y] += 1

def new_game_2d(num_rows, num_cols, bombs):
    """
    Start a new game.

    Return a game state dictionary, with the 'dimensions', 'state', 'board' and
    'visible' fields adequately initialized.

    Parameters:
       num_rows (int): Number of rows
       num_cols (int): Number of columns
       bombs (list): List of bombs, given in (row, column) pairs, which are
                     tuples

    Returns:
       A game state dictionary

    >>> dump(new_game_2d(2, 4, [(0, 0), (1, 0), (1, 1)]))
    board:
        ['.', 3, 1, 0]
        ['.', '.', 1, 0]
    bombs: 3
    dimensions: (2, 4)
    state: ongoing
    visible:
        [False, False, False, False]
        [False, False, False, False]
    visited: 0
    """
    board = create_board(num_rows, num_cols, bombs, ['.', 0])
    visible = create_board(num_rows, num_cols, [], [False, False])
    # add the number of bombs every square is close to
    get_neighbor_of_bombs(board, bombs, num_rows, num_cols)

    return {
        'dimensions': (num_rows, num_cols),
        'bombs': len(bombs),
        'board': board,
        'visible': visible,
        'state': 'ongoing',
        'visited': 0
        }


def dig_2d(game, row, col):
    """
    Reveal the cell at (row, col), and, in some cases, recursively reveal its
    neighboring squares.

    Update game['visible'] to reveal (row, col).  Then, if (row, col) has no
    adjacent bombs (including diagonally), then recursively reveal (dig up) its
    eight neighbors.  Return an integer indicating how many new squares were
    revealed in total, including neighbors, and neighbors of neighbors, and so
    on.

    The state of the game should be changed to 'defeat' when at least one bomb
    is visible on the board after digging (i.e. game['visible'][bomb_location]
    == True), 'victory' when all safe squares (squares that do not contain a
    bomb) and no bombs are visible, and 'ongoing' otherwise.

    Parameters:
       game (dict): Game state
       row (int): Where to start digging (row)
       col (int): Where to start digging (col)

    Returns:
       int: the number of new squares revealed

    >>> game = {'dimensions': (2, 4),
    ...         'board': [['.', 3, 1, 0],
    ...                   ['.', '.', 1, 0]],
    ...         'visible': [[False, True, False, False],
    ...                  [False, False, False, False]],
    ...         'state': 'ongoing',
    ...         'bombs': 3,
    ...         'visited': 1}
    >>> dig_2d(game, 0, 3)
    4
    >>> dump(game)
    board:
        ['.', 3, 1, 0]
        ['.', '.', 1, 0]
    bombs: 3
    dimensions: (2, 4)
    state: victory
    visible:
        [False, True, True, True]
        [False, False, True, True]
    visited: 5
    >>> game = {'dimensions': [2, 4],
    ...         'board': [['.', 3, 1, 0],
    ...                   ['.', '.', 1, 0]],
    ...         'visible': [[False, True, False, False],
    ...                  [False, False, False, False]],
    ...         'state': 'ongoing',
    ...         'visited': 1}
    >>> dig_2d(game, 0, 0)
    1
    >>> dump(game)
    board:
        ['.', 3, 1, 0]
        ['.', '.', 1, 0]
    dimensions: [2, 4]
    state: defeat
    visible:
        [True, True, False, False]
        [False, False, False, False]
    visited: 2
    """
    if game['state'] == 'defeat' or game['state'] == 'victory':
        return 0
    # if the player dug out a mine...
    if game['board'][row][col] == '.':
        # reveal the bomb
        game['visible'][row][col] = True
        game['visited'] += 1
        # change the state to lost
        game['state'] = 'defeat'
        return 1
    # if already revealed, simply return 0
    if game['visible'][row][col]:
        return 0

    # otherwise, use complete DFS to iteratively undig
    # add the starting spot to the queue
    queue = [(row, col)]
    visited = set()
    # add the starting point to the visited set
    visited.add((row, col))
    # while there are still coordinates to check...
    while len(queue) != 0:
        # remove from the queue
        row, col = queue.pop(0)

        # update visible
        game['visible'][row][col] = True

        # if the square has a non-zero int, path has been exhausted so break
        if game['board'][row][col] != 0:
            break
        # for each of the square's neighbors...
        for t in translations:
            # get coordinates of the neighbor
            n_row, n_col = row + t[0], col + t[1]
            # check if the coorindates are in bound
            if 0 <= n_row < game['dimensions'][0] and 0 <= n_col < game['dimensions'][1]:
                # check if we have already seen this square, and if not...
                if (n_row, n_col) not in visited and not game['visible'][n_row][n_col]:
                    # then check if it's a clear square to add it to the queue and visited set
                    if game['board'][n_row][n_col] == 0:
                        queue.append((n_row, n_col))
                        visited.add((n_row, n_col))
                    # otherwise, just add it to visited and update visible
                    else:
                        visited.add((n_row, n_col))
                        game['visible'][n_row][n_col] = True
    # visited holds track of all the squares revealed so add the amount that we
    # revealed in this dig
    game['visited'] += len(visited)

    # if all squares with no mines have been revealed, the game has been won
    if game['visited'] == game['dimensions'][0]*game['dimensions'][1] - game['bombs']:
        game['state'] = 'victory'

    return len(visited)

def render_2d_locations(game, xray=False):
    """
    Prepare a game for display.

    Returns a two-dimensional array (list of lists) of '_' (hidden squares),
    '.' (bombs), ' ' (empty squares), or '1', '2', etc. (squares neighboring
    bombs).  game['visible'] indicates which squares should be visible.  If
    xray is True (the default is False), game['visible'] is ignored and all
    cells are shown.

    Parameters:
       game (dict): Game state
       xray (bool): Whether to reveal all tiles or just the ones allowed by
                    game['visible']

    Returns:
       A 2D array (list of lists)

    >>> render_2d_locations({'dimensions': (2, 4),
    ...         'state': 'ongoing',
    ...         'board': [['.', 3, 1, 0],
    ...                   ['.', '.', 1, 0]],
    ...         'visible':  [[False, True, True, False],
    ...                   [False, False, True, False]]}, False)
    [['_', '3', '1', '_'], ['_', '_', '1', '_']]

    >>> render_2d_locations({'dimensions': (2, 4),
    ...         'state': 'ongoing',
    ...         'board': [['.', 3, 1, 0],
    ...                   ['.', '.', 1, 0]],
    ...         'visible':  [[False, True, False, True],
    ...                   [False, False, False, True]]}, True)
    [['.', '3', '1', ' '], ['.', '.', '1', ' ']]
    """
    output = []
    # if we can see everything, don't even bother
    # with the visible 2-d list
    if xray:
        # for every row in the board...
        for b_row in game['board']:
            row = []
            # for every value in the current row...
            for val in b_row:
                # if there are no bombs near the square, return
                # space. Otherwise, return string of the number or '.' for bomb
                if val == 0:
                    row.append(' ')
                else:
                    row.append(str(val))
            output.append(row)
    else:
        # for every row in the board and the visible 2-d list
        for b_row, v_row in zip(game['board'], game['visible']):
            row = []
            # for every value and boolean in the current rows...
            for val, visible in zip(b_row, v_row):
                # if we can see the square, check if it's 0 to place a space
                # or return a string of whatever's on the square
                if visible:
                    if val == 0:
                        row.append(' ')
                    else:
                        row.append(str(val))
                # if not visible, then return an underscore
                else:
                    row.append('_')
            output.append(row)
    return output



def render_2d_board(game, xray=False):
    """
    Render a game as ASCII art.

    Returns a string-based representation of argument 'game'.  Each tile of the
    game board should be rendered as in the function
        render_2d_locations(game)

    Parameters:
       game (dict): Game state
       xray (bool): Whether to reveal all tiles or just the ones allowed by
                    game['visible']

    Returns:
       A string-based representation of game

    >>> render_2d_board({'dimensions': (2, 4),
    ...                  'state': 'ongoing',
    ...                  'board': [['.', 3, 1, 0],
    ...                            ['.', '.', 1, 0]],
    ...                  'visible':  [[True, True, True, False],
    ...                            [False, False, True, False]]})
    '.31_\\n__1_'
    """
    # get 2-d list representation
    board = render_2d_locations(game, xray)
    output = ""

    for row in board:
        # combine the entire row values into a string and
        # add it to the ouput string plus and new line character
        output += "".join(row) + "\n"
    # return the output string except the last character
    return output[:-1]



# N-D IMPLEMENTATION

def create_nd_board(dimensions, val):
    """
    Recursively builds an N-dimensional array that represent the n-dimensional board
    """
    # base case
    if len(dimensions) == 1:
        return [val for numb in range(dimensions[0])]
    return [create_nd_board(dimensions[1:], val) for numb in range(dimensions[0])]

def get_neighbor_of_bombs_nd(board, bombs, dims):
    """
    Gets the coordinates of every bomb and the bomb's neighboring squares. If the square
    is a safe square, the number of bombs it has near it is updated by one. Does not return new board
    but rather mutates board.
    """
    # for every bomb...
    for bomb in bombs:
        # add the '.' symbolizing the bomb
        set_val(board, bomb, ".")
        # get list that holds all neighbors of the current bomb
        neighbors = get_neighbors(board, bomb, dims)
        for neighbor in neighbors:
            # check if the neighbor is a safe square
            # and if so update the number of bombs near it by 1
            val = get_val(board, neighbor)
            if type(val) == int:
                set_val(board, neighbor, val+1)


def set_val(board, coords, val):
    """
    Sets the value of at the coordinates given using recursion
    """
    # base case
    if len(coords) == 1:
        board[coords[0]] = val
    else:
        set_val(board[coords[0]], coords[1:], val)

def get_val(board, coords):
    """
    Gets the value at the coordinates given using recursion
    """
    # base case
    if len(coords) == 1:
        return board[coords[0]]
    return get_val(board[coords[0]], coords[1:])

def get_neighbors(board, coords, dimensions):
    """
    Returns list of all neighbors of the given coordinate
    """
    neighbors = []

    # recursively find the neighbors
    def recursive_func(board, coords, dimensions, i):
        """
        Uses an index i to keep track of what dimensions were getting the neighbors for.
        For instance, if the board were a 3-D array with dimensions (2,4,2) that looked like this:
            [[3, '.'], [3, 3], [1, 1], [0, 0]]
            [['.', 3], [3, '.'], [1, 1], [0, 0]]
        and say we want the neighbors of the coordinate [0, 0, 1]:
        1. we would first change the x-coordinate by adding one and subtracting one so that we
            check the followings coordinates:
            [-1, 0, 1],
            [0, 0, 1],
            [1, 0, 1]
            if they're in bounds, then they're added as a neighbor. Otherwise we move on.
        2. Then, we change the y-coordinate of every coordinate we found in step 1 by doing 
            adding one and subtracting one as well:
            [-1, -1, 1],
            [0, -1, 1],
            [1, -1, 1]
            [-1, 0, 1],
            [0, 0, 1],
            [1, 0, 1]
            [-1, 1, 1],
            [0, 1, 1],
            [1, 1, 1]
        3. And lastly, the same is done for the last dimension, which is the z-coordinate. We simply 
            check if the coordinate is in bounds and then add it as a neighbor.

        """
        # base case:
        if i == len(coords) - 1:
            # for every possible neighbor...
            for change in (-1, 0, 1):
                # get its coordinates
                poss_neighbor = list(coords[:i]) + [ coords[i]+change ] + list(coords[i+1:])
                # if the coordinates are in bound, add it neighbors
                if 0 <= poss_neighbor[i] < dimensions[i]:
                    neighbors.append(poss_neighbor)
        else:
            # for every possible neighbor in this dimension...
            for change in (-1, 0, 1):
                # get its coordinates
                poss_neighbor = list(coords[:i]) + [ coords[i]+change ] + list(coords[i+1:])
                # if in bounds...
                if 0 <= poss_neighbor[i] < dimensions[i]:
                    # decrease the search space by one dimension by updating i
                    recursive_func(board, poss_neighbor, dimensions, i+1)
    recursive_func(board, coords, dimensions, 0)
    return neighbors        



def new_game_nd(dimensions, bombs):
    """
    Start a new game.

    Return a game state dictionary, with the 'dimensions', 'state', 'board' and
    'visible' fields adequately initialized.


    Args:
       dimensions (tuple): Dimensions of the board
       bombs (list): Bomb locations as a list of lists, each an
                     N-dimensional coordinate

    Returns:
       A game state dictionary

    >>> g = new_game_nd((2, 4, 2), [(0, 0, 1), (1, 0, 0), (1, 1, 1)])
    >>> dump(g)
    board:
        [[3, '.'], [3, 3], [1, 1], [0, 0]]
        [['.', 3], [3, '.'], [1, 1], [0, 0]]
    bombs: 3
    dimensions: (2, 4, 2)
    state: ongoing
    visible:
        [[False, False], [False, False], [False, False], [False, False]]
        [[False, False], [False, False], [False, False], [False, False]]
    visited: 0
    """
    board = create_nd_board(dimensions, 0)
    visible = create_nd_board(dimensions, False)
    # add the amount of bombs that are near every safe square
    get_neighbor_of_bombs_nd(board, bombs, dimensions)
    return {
        'dimensions': dimensions,
        'state': 'ongoing',
        'board': board,
        'visible': visible,
        'bombs': len(bombs),
        'visited': 0
    }


def dig_nd(game, coordinates):
    """
    Recursively dig up square at coords and neighboring squares.

    Update the visible to reveal square at coords; then recursively reveal its
    neighbors, as long as coords does not contain and is not adjacent to a
    bomb.  Return a number indicating how many squares were revealed.  No
    action should be taken and 0 returned if the incoming state of the game
    is not 'ongoing'.

    The updated state is 'defeat' when at least one bomb is visible on the
    board after digging, 'victory' when all safe squares (squares that do
    not contain a bomb) and no bombs are visible, and 'ongoing' otherwise.

    Args:
       coordinates (tuple): Where to start digging

    Returns:
       int: number of squares revealed

    >>> g = {'dimensions': (2, 4, 2),
    ...      'board': [[[3, '.'], [3, 3], [1, 1], [0, 0]],
    ...                [['.', 3], [3, '.'], [1, 1], [0, 0]]],
    ...        'bombs': 3,
    ...      'visible': [[[False, False], [False, True], [False, False],
    ...                [False, False]],
    ...               [[False, False], [False, False], [False, False],
    ...                [False, False]]],
    ...      'state': 'ongoing',
    ...      'visited': 0}
    >>> dig_nd(g, (0, 3, 0))
    8
    >>> dump(g)
    board:
        [[3, '.'], [3, 3], [1, 1], [0, 0]]
        [['.', 3], [3, '.'], [1, 1], [0, 0]]
    bombs: 3
    dimensions: (2, 4, 2)
    state: ongoing
    visible:
        [[False, False], [False, True], [True, True], [True, True]]
        [[False, False], [False, False], [True, True], [True, True]]
    visited: 8
    >>> g = {'dimensions': (2, 4, 2),
    ...      'board': [[[3, '.'], [3, 3], [1, 1], [0, 0]],
    ...                [['.', 3], [3, '.'], [1, 1], [0, 0]]],
    ...            'bombs': 3,
    ...      'visible': [[[False, False], [False, True], [False, False],
    ...                [False, False]],
    ...               [[False, False], [False, False], [False, False],
    ...                [False, False]]],
    ...      'state': 'ongoing',
    ...      'visited': 0}
    >>> dig_nd(g, (0, 0, 1))
    1
    >>> dump(g)
    board:
        [[3, '.'], [3, 3], [1, 1], [0, 0]]
        [['.', 3], [3, '.'], [1, 1], [0, 0]]
    bombs: 3
    dimensions: (2, 4, 2)
    state: defeat
    visible:
        [[False, True], [False, True], [False, False], [False, False]]
        [[False, False], [False, False], [False, False], [False, False]]
    visited: 1
    """
    if game['state'] == 'defeat' or game['state'] == 'victory':
        return 0

    # if a bomb has been uncovered
    if get_val(game['board'], coordinates) == '.':
        # reveal it
        set_val(game['visible'], coordinates, True)
        # change the state of the game to lost
        game['state'] = 'defeat'
        game['visited'] += 1
        return 1

    # if we've already uncovered the given square, then don't do anything
    if get_val(game['visible'], coordinates):
        return 0
    
    # otherwise, use complete BFS to undig all valid squares
    # add starting point to queue
    queue = [coordinates]
    visited = set()
    # add starting point to visited set
    visited.add(frozenset((tuple(coordinates),)))
    # while there are still coordinates to check...
    while len(queue) != 0:
        # remove the current coordinates from the queue
        coords = queue.pop(0)
        
        # update visible
        set_val(game['visible'], coords, True)

        # if the square has a non-zero int, path has been exhausted so break
        if get_val(game['board'], coords) != 0:
            break
        # for each of the square's neighbors...
        for neighbor in get_neighbors(game['board'], coords, game['dimensions']):
            f_neighbor = frozenset((tuple(neighbor),))
            # if another clear square, add it to queue
            if f_neighbor not in visited and not get_val(game['visible'], neighbor):
                if get_val(game['board'], neighbor) == 0:
                    queue.append(neighbor)
                    visited.add(f_neighbor)
                else:
                    visited.add(f_neighbor)
                    set_val(game['visible'], neighbor, True)
    
    # get total amount of squares by multiplying all dimensions
    total_squares = 1
    for d in game['dimensions']:
        total_squares *= d
    # visited keeps track of the safe squares revealed, so add the ones we just revealed
    game['visited'] += len(visited)

    # if all safe squares have been revealed, the game has been won!
    if game['visited'] == total_squares - game['bombs']:
        game['state'] = 'victory'
    return len(visited)


def render_nd(game, xray=False):
    """
    Prepare the game for display.

    Returns an N-dimensional array (nested lists) of '_' (hidden squares), '.'
    (bombs), ' ' (empty squares), or '1', '2', etc. (squares neighboring
    bombs).  The game['visible'] array indicates which squares should be
    visible.  If xray is True (the default is False), the game['visible'] array
    is ignored and all cells are shown.

    Args:
       xray (bool): Whether to reveal all tiles or just the ones allowed by
                    game['visible']

    Returns:
       An n-dimensional array of strings (nested lists)

    >>> g = {'dimensions': (2, 4, 2),
    ...      'board': [[[3, '.'], [3, 3], [1, 1], [0, 0]],
    ...                [['.', 3], [3, '.'], [1, 1], [0, 0]]],
    ...      'visible': [[[False, False], [False, True], [True, True],
    ...                [True, True]],
    ...               [[False, False], [False, False], [True, True],
    ...                [True, True]]],
    ...      'state': 'ongoing'}
    >>> render_nd(g, False)
    [[['_', '_'], ['_', '3'], ['1', '1'], [' ', ' ']],
     [['_', '_'], ['_', '_'], ['1', '1'], [' ', ' ']]]

    >>> render_nd(g, True)
    [[['3', '.'], ['3', '3'], ['1', '1'], [' ', ' ']],
     [['.', '3'], ['3', '.'], ['1', '1'], [' ', ' ']]]
    """
    render = create_nd_board(game['dimensions'], 0)

    def recursive_func(board, coords, dimensions, i):
        # base case
        if i == len(coords) - 1:
            # for every dimension...
            for d in range(dimensions[i]):
                # for every value in that dimension...
                coords = coords[:i] + [d] + coords[i+1:]
                # if xray, always show
                if xray:
                    visible = True
                else:
                    visible = get_val(game['visible'], coords)

                if visible:
                    # get the value
                    val = get_val(game['board'], coords)
                    # return a space if it's an empty square
                    if val == 0:
                        set_val(render, coords, ' ')
                    else:
                        # set the value in output to the integer on the board
                        set_val(render, coords, str(get_val(game['board'], coords)))
                else:
                        # if not visible, set empty underscore
                        set_val(render, coords, '_')
        else:
            # for every value in the current dimension...
            for d in range(game['dimensions'][i]):
                # go through every value in that dimension
                coords = coords[:i] + [d] + coords[i+1:]
                recursive_func(board, coords, dimensions, i+1)

    recursive_func(render, [0 for d in game['dimensions']], game['dimensions'], 0)

    return render



if __name__ == "__main__":
    # Test with doctests. Helpful to debug individual lab.py functions.
    _doctest_flags = doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS
    doctest.testmod(optionflags=_doctest_flags)  # runs ALL doctests

    # Alternatively, can run the doctests JUST for specified function/methods,
    # e.g., for render_2d_locations or any other function you might want.  To
    # do so, comment out the above line, and uncomment the below line of code.
    # This may be useful as you write/debug individual doctests or functions.
    # Also, the verbose flag can be set to True to see all test results,
    # including those that pass.
    #
    # doctest.run_docstring_examples(
    #    dig_nd,
    #    globals(),
    #    optionflags=_doctest_flags,
    #    verbose=False
    # )
    # g = {'dimensions': (2, 4, 2),
    # 'board': [[[3, '.'], [3, 3], [1, 1], [0, 0]],
    #                 [['.', 3], [3, '.'], [1, 1], [0, 0]]],
    #       'visible': [[[False, False], [False, True], [False, False],
    #                 [False, False]],
    #                [[False, False], [False, False], [False, False],
    #             [False, False]]],
    #       'state': 'ongoing',
    #       'bombs': 3,
    #       'visited': 0}
    # print(dig_nd(g, (0, 3, 0)))
    # print(dig_nd(g, (0, 0, 0)))
    g = {'dimensions': (4, 6), 'bombs': 2, 
    'board': [[0, 0, 1, '.', 1, 0], 
              [0, 1, 2, 2, 1, 0], 
              [0, 1, '.', 1, 0, 0], 
              [0, 1, 1, 1, 0, 0]], 
    'visible': [[False, False, False, False, False, False], 
                [False, False, False, False, False, False], 
                [False, False, False, False, False, False], 
                [False, False, False, False, False, False]], 
    'state': 'ongoing', 'visited': 0}
    print(g)
    print(dig_2d(g, 0, 5))
    print(g)
    print(dig_2d(g, 1, 1))
    print(g)
    print(dig_2d(g, 0, 4))
    print(g)
    print(dig_2d(g, 3, 2))
    print(g)
    print(dig_2d(g, 0, 0))
    print(g)