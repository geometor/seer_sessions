import copy

"""
Transforms an input grid containing mostly 0s and a single 1 at the bottom-left
corner into an output grid of the same dimensions. The output grid contains 8s
by default. A path starting from the bottom-left cell (corresponding to the input 1)
is traced upwards towards the top row. The path moves diagonally: one step up and
one step horizontally (initially right). When the path hits the left (column 0) or
right (column width-1) boundary, the horizontal direction reverses. All cells visited
by this bouncing path are marked with 1 in the output grid.
"""

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies the bouncing diagonal path transformation to the input grid.

    Args:
        input_grid: A list of lists representing the input grid. Assumed to
                    contain 0s and a single 1 at the bottom-left.

    Returns:
        A list of lists representing the output grid with the path marked by 1s
        and the background filled with 8s.
    """
    
    # Determine grid dimensions
    if not input_grid:
        return []
    height = len(input_grid)
    if height == 0 or not input_grid[0]:
        # Handle empty rows or grid
         return [[] for _ in range(height)] # Return grid with correct number of empty rows if height > 0
        
    width = len(input_grid[0])
    
    # Initialize output grid with default value 8
    output_grid = [[8 for _ in range(width)] for _ in range(height)]

    # If the grid is empty vertically or horizontally after initialization check, return
    if height == 0 or width == 0:
       return output_grid # Should be [] or [[], [], ...] based on previous check

    # Initialize path parameters
    current_row = height - 1
    current_col = 0
    horizontal_direction = 1  # 1 for right, -1 for left

    # Handle the special case of a single-column grid
    if width == 1:
        horizontal_direction = 0 # Path goes straight up

    # Mark the starting cell
    output_grid[current_row][current_col] = 1

    # Trace the path upwards from the second-to-last row to the top row
    # We iterate height-1 times to draw the rest of the path
    for _ in range(height - 1):
        # Check for boundary collision based on the *current* column and direction
        # If we are at a boundary, the direction for the *next* step needs to flip
        if current_col == 0 and width > 1: # Hitting left wall (and not single column)
             horizontal_direction = 1
        elif current_col == width - 1 and width > 1: # Hitting right wall (and not single column)
             horizontal_direction = -1
             
        # Move one step up
        current_row -= 1
        
        # Move one step horizontally based on the (potentially updated) direction
        current_col += horizontal_direction

        # Mark the new cell on the path
        # Ensure row index is valid (should always be >= 0 in this loop)
        if 0 <= current_row < height and 0 <= current_col < width:
             output_grid[current_row][current_col] = 1
        # else: # Should not happen with correct logic, but good for debugging
        #     print(f"Warning: Path went out of bounds at ({current_row}, {current_col})")
        #     break


    return output_grid