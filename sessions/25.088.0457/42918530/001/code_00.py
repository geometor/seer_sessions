import numpy as np
import collections

"""
The transformation identifies 5x5 squares based on their single-pixel non-white borders. 
Squares are grouped by their border color. Within each color group, if there is at least 
one square with a non-white pattern in its 3x3 inner area (a 'source pattern'), this pattern 
is copied into the 3x3 inner area of all other squares in the same color group whose 
inner areas are initially all white ('empty'). Squares that already have a pattern, or 
squares belonging to a color group without any patterned squares, remain unchanged. 
The background also remains unchanged.
"""

def _find_squares(grid):
    """
    Finds all 5x5 squares in the grid based on their border.

    Args:
        grid (np.ndarray): The input grid.

    Returns:
        list: A list of dictionaries, each containing:
              'top_left': (row, col) tuple of the top-left corner.
              'color': The border color.
              'inner_area': A 3x3 numpy array of the inner area.
    """
    squares = []
    height, width = grid.shape
    for r in range(height - 4):
        for c in range(width - 4):
            color = grid[r, c]
            # Potential top-left corner must be non-white
            if color == 0:
                continue

            is_square = True
            # Check corners
            if not (grid[r+4, c] == color and grid[r, c+4] == color and grid[r+4, c+4] == color):
                is_square = False
            
            # Check top and bottom border
            if is_square:
                for i in range(1, 4):
                    if not (grid[r, c+i] == color and grid[r+4, c+i] == color):
                        is_square = False
                        break
            
            # Check left and right border
            if is_square:
                 for i in range(1, 4):
                    if not (grid[r+i, c] == color and grid[r+i, c+4] == color):
                        is_square = False
                        break

            # Check inner area is not the border color (unless it's part of a pattern)
            # More importantly, check if the *immediate* inner border is white, to distinguish from solid blocks
            # A simpler check might be sufficient given the structure: just confirm the border integrity.
            # Let's assume the structure implies the inside isn't the same as the border unless patterned.

            if is_square:
                # Extract inner 3x3 area
                inner_area = grid[r+1:r+4, c+1:c+4]
                squares.append({
                    'top_left': (r, c),
                    'color': color,
                    'inner_area': inner_area
                })
                # Optional: Skip ahead if a square is found to avoid redundant checks?
                # No, overlapping squares aren't expected based on examples.

    return squares

def _is_empty(inner_area):
    """Checks if a 3x3 inner area is all white (0)."""
    return np.all(inner_area == 0)

def transform(input_grid):
    """
    Applies the pattern propagation transformation to the input grid.

    Args:
        input_grid (list of lists or np.ndarray): The input grid.

    Returns:
        np.ndarray: The transformed grid.
    """
    input_grid_np = np.array(input_grid, dtype=int)
    output_grid = input_grid_np.copy()
    
    # 1. Find all 5x5 squares
    found_squares = _find_squares(input_grid_np)

    # 2. Group squares by border color
    color_groups = collections.defaultdict(list)
    for square in found_squares:
        color_groups[square['color']].append(square)

    # 3. Process each color group
    for color, squares_in_group in color_groups.items():
        source_pattern = None
        
        # 3a. Find the source pattern for this color
        for square in squares_in_group:
            if not _is_empty(square['inner_area']):
                source_pattern = square['inner_area']
                break # Assume only one source pattern type per color group

        # 3b. If a source pattern exists, apply it to empty squares
        if source_pattern is not None:
            for square in squares_in_group:
                if _is_empty(square['inner_area']):
                    r, c = square['top_left']
                    # Apply the pattern to the output grid
                    output_grid[r+1:r+4, c+1:c+4] = source_pattern

    return output_grid.tolist() # Return as list of lists as per ARC standard
