assignments = []
rows = 'ABCDEFGHI'
cols = '123456789'

def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [a+b for a in A for b in B]

boxes = cross(rows, cols)
row_units = [cross(r, cols) for r in rows]
col_units = [cross(rows, c) for c in cols]
square_units = [cross(r, c) for r in ('ABC', 'DEF', 'GHI') for c in ('123', '456', '789')]
# Zip rows and cols and rows and reverse cols for diagonal units
diagonal_units = [[a+b for a,b in zip(rows, cols)], [a+b for a,b in zip(rows, cols[::-1])]]

# List of all units
unit_list = row_units + col_units + square_units + diagonal_units

# Dict of units each box belongs to
units = {box: [unit for unit in unit_list if box in unit] for box in boxes}

# Dict of sets of peers each box has
peers = {box: set(s for unit in units[box] for s in unit) - set([box]) for box in boxes}


def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """

    # Don't waste memory appending actions that don't actually change any values
    if values[box] == value:
        return values

    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """

    # Find all instances of naked twins
    for unit in unit_list:
        # Cache occurences of values of length 2
        c = {}

        for box in unit:
            v = values[box]
            # For values of length 2
            if len(v) == 2:
                # If this value already exists in cache, found naked twin
                if v in c:
                    twins = (c[v], box)
                    # Eliminate the naked twins as possibilities for their peers in current unit
                    peers = [box for box in unit if box not in twins]
                    for peer in peers:
                        new_value = values[peer].replace(v[0], '').replace(v[1], '')
                        values = assign_value(values, peer, new_value)
                # Else add the box to cache
                else:
                    c[v] = box

    return values

def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """

    # Convert grid string into list of values
    values = ['123456789' if char == '.' else char for char in grid]

    # Zip boxes with values to create dict
    assert len(values) == 81

    return dict(zip(boxes, values))

def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    # Max width of an entry
    width = 1 + max(len(values[s]) for s in values.keys())

    # Row line separator
    line = '+'.join(['-'*width*3]*3)

    for r in rows:
        # Display values centered on width separated by | for Cols 3 and 6 or space
        print(''.join(values[r+c].center(width) + ('|' if c in '36' else ' ') for c in cols))
        # Rows 3 and 6 separator
        if r in 'CF': print(line)

def eliminate(values):
    # For boxes that have a solved value
    for box in [b for b in boxes if len(values[b]) == 1]:
        v = values[box]
        # For each of this box's peers
        for p in peers[box]:
            # Remove v from this peer's possible values
            values = assign_value(values, p, values[p].replace(v, ''))
    return values

def only_choice(values):
    """Finalize all values that are the only choice for a unit.

    Go through all the units, and whenever there is a unit with a value
    that only fits in one box, assign the value to this box.
    """
    for u in unit_list:
        for d in '123456789':
            # Find occurences of this digit in this unit
            places = [b for b in u if d in values[b]]
            # If there is only one possible place, set that box's value to this digit
            if len(places) == 1:
                values = assign_value(values, places[0], d)

    return values


def reduce_puzzle(values):
    """
    Iterate eliminate() and only_choice(). If at some point, there is a box
    with no available values, return False.
    If the sudoku is solved, return the sudoku.
    If after an iteration of both functions, the sudoku remains the same,
    return the sudoku.
    """
    # Use number of solved values to determine if reduce_puzzle has stalled
    stalled = False
    while not stalled:
        solved_values_before = len([b for b in boxes if len(values[b]) == 1])
        values = eliminate(values)
        values = only_choice(values)
        solved_values_after = len([b for b in boxes if len(values[b]) == 1])
        stalled = solved_values_before == solved_values_after
        if len([b for b in boxes if len(values[b]) == 0]):
            return False
    return values

def search(values):
    "Using depth-first search and propagation, create a search tree and solve the sudoku."
    # First, reduce the puzzle using the eliminate and only_choice strategies
    values = reduce_puzzle(values)

    # Determine if solved
    if values is False:
        return False
    if all(len(values[box]) == 1 for box in boxes):
        return values

    # Choose one of the unfilled squares with the fewest possibilities
    m, min_box = min((len(values[box]), box) for box in boxes if len(values[box]) > 1)

    for digit in values[min_box]:
        attempt_values = values.copy()
        attempt_values = assign_value(attempt_values, min_box, digit)
        # Now use recursion to solve each one of the resulting sudokus, and if one returns a value (not False), return that answer!
        attempt = search(attempt_values)
        if attempt:
            return attempt

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    # Translate string grid to dict of boxes and values
    values = grid_values(grid)

    # Use search strategy on values
    solution = search(values)

    return solution

if __name__ == '__main__':
    diag_sudoku_grid = '9.1....8.8.5.7..4.2.4....6...7......5..............83.3..6......9................'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
