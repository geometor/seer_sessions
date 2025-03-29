```python
"""
Identifies the largest square subgrid composed entirely of white (0) pixels
in the input grid. If multiple squares share the largest size, selects the
one whose top-left corner is bottom-most, and then right-most among those.
Fills this selected square area with azure (8) pixels in the output grid.
All other pixels remain unchanged. If no white squares exist, the output
is identical to the input.
"""

import numpy as np

def _find_largest_white_square(grid):
    """
    Finds the largest white square, applying bottom-right tie-breaking.

    Args:
        grid (np.ndarray): The input grid.

    Returns:
        tuple: (r, c, size) of the selected square, or None if no white square found.
    """
    rows, cols = grid.shape
    max_size = 0
    largest_squares = [] # Stores {'r': r, 'c': c, 'size': size} for squares of max_size

    # Iterate through possible square sizes, from largest to smallest
    for size in range(min(rows, cols), 0, -1):
        found_at_this_size = False
        current_size_squares = []
        # Iterate through all possible top-left corners (r, c) for this size
        for r in range(rows - size + 1):
            for c in range(cols - size + 1):
                # Check if the current square subgrid is all white (0)
                subgrid = grid[r:r+size, c:c+size]
                if np.all(subgrid == 0):
                    # If this is the first size we've found squares for, it's the max size
                    if max_size == 0:
                        max_size = size
                    # If this square's size matches the max size found so far
                    if size == max_size:
                        current_size_squares.append({'r': r, 'c': c, 'size': size})
                        found_at_this_size = True

        # If we found any squares of the current size 'size', and this size is
        # the largest we've encountered (max_size), store them and break
        # the loop since we started checking from the largest possible size.
        if found_at_this_size:
            largest_squares = current_size_squares
            break # Found the max size, no need to check smaller sizes

    # If no white squares were found
    if not largest_squares:
        return None

    # Apply tie-breaking: bottom-most (max r), then right-most (max c)
    # Sort by row descending, then column descending
    largest_squares.sort(key=lambda s: (s['r'], s['c']), reverse=True)

    # The first element after sorting is the chosen one
    chosen_square = largest_squares[0]
    return chosen_square['r'], chosen_square['c'], chosen_square['size']


def transform(input_grid):
    """
    Transforms the input grid by finding the largest white square (with
    bottom-right tie-breaking) and filling it with azure (8).

    Args:
        input_grid (list of lists): The input grid represented as a list of lists.

    Returns:
        list of lists: The transformed grid.
    """
    # Convert input to numpy array for easier processing
    input_grid_np = np.array(input_grid, dtype=np.int8)
    
    # Initialize output grid as a copy of the input
    output_grid = input_grid_np.copy()

    # Step 1 & 2 & 3: Find the largest white square using the helper function
    # This includes identification, finding max size, and tie-breaking.
    result = _find_largest_white_square(input_grid_np)

    # Step 4: Fill with Azure if a square was found
    if result is not None:
        r, c, size = result
        # Fill the identified square area in the output grid with azure (8)
        output_grid[r:r + size, c:c + size] = 8

    # Step 5: Output the result
    # Convert back to list of lists format for the expected output
    return output_grid.tolist()
```