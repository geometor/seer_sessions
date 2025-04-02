```python
import numpy as np

"""
Identifies a boundary line (horizontal or vertical) and a single 'mover' pixel of a different color.
Moves the 'mover' pixel in a straight line (horizontally or vertically) towards the boundary line.
The movement stops when the 'mover' pixel reaches the cell immediately adjacent to the boundary line along its path.
The original position of the mover pixel becomes background (white, 0).
All other pixels remain unchanged.
"""

def find_boundary(grid):
    """
    Finds a solid horizontal or vertical line of a single non-white color.

    Args:
        grid (np.ndarray): The input grid.

    Returns:
        tuple: (orientation, index, color)
               orientation (str): 'horizontal' or 'vertical'.
               index (int): Row index if horizontal, column index if vertical.
               color (int): The color of the boundary line.
               Returns (None, -1, -1) if no boundary is found.
    """
    rows, cols = grid.shape

    # Check for horizontal boundary
    for r in range(rows):
        row_colors = np.unique(grid[r, :])
        non_white_colors = row_colors[row_colors != 0]
        # Check if the row consists of exactly one non-white color
        if len(non_white_colors) == 1 and np.all(grid[r, :] == non_white_colors[0]):
            # Check if it spans the full width (or is at least substantial)
            # In the examples, they span the full width/height.
             if np.all(grid[r,:] == non_white_colors[0]): # Full row check
                 return 'horizontal', r, non_white_colors[0]


    # Check for vertical boundary
    for c in range(cols):
        col_colors = np.unique(grid[:, c])
        non_white_colors = col_colors[col_colors != 0]
         # Check if the col consists of exactly one non-white color
        if len(non_white_colors) == 1 and np.all(grid[:, c] == non_white_colors[0]):
             # Check if it spans the full height
             if np.all(grid[:, c] == non_white_colors[0]): # Full col check
                 return 'vertical', c, non_white_colors[0]

    return None, -1, -1 # No boundary found

def find_mover(grid, boundary_color):
    """
    Finds the single pixel that is not background (0) and not the boundary color.

    Args:
        grid (np.ndarray): The input grid.
        boundary_color (int): The color of the boundary line.

    Returns:
        tuple: (position, color)
               position (tuple): (row, col) of the mover pixel.
               color (int): The color of the mover pixel.
               Returns (None, -1) if no mover is found.
    """
    rows, cols = grid.shape
    for r in range(rows):
        for c in range(cols):
            pixel_color = grid[r, c]
            # Check if the pixel is not background and not the boundary color
            if pixel_color != 0 and pixel_color != boundary_color:
                # Assuming there's only one such pixel based on examples
                return (r, c), pixel_color
    return None, -1 # No mover found


def transform(input_grid):
    """
    Moves a single pixel towards a boundary line, stopping one step before it.

    Args:
        input_grid (list of lists): The input grid represented as a 2D list.

    Returns:
        list of lists: The transformed grid.
    """
    # Convert input to numpy array for easier manipulation
    grid = np.array(input_grid, dtype=int)
    output_grid = np.copy(grid)
    rows, cols = grid.shape

    # 1. Identify the boundary object
    orientation, boundary_index, boundary_color = find_boundary(grid)

    # Handle case where boundary isn't found as expected
    if orientation is None:
        print("Warning: Boundary not found.")
        return input_grid # Return original grid if no boundary

    # 2. Identify the single 'mover' pixel
    mover_pos, mover_color = find_mover(grid, boundary_color)

    # Handle case where mover isn't found as expected
    if mover_pos is None:
        print("Warning: Mover pixel not found.")
        return input_grid # Return original grid if no mover

    mover_row, mover_col = mover_pos

    # 3. Determine the direction of movement (implicit in target calculation)
    # 4. Determine the target position
    target_row, target_col = -1, -1 # Initialize target coordinates

    if orientation == 'vertical':
        # Move horizontally towards the boundary column
        target_row = mover_row # Row remains the same
        # Stop one step before the boundary
        if mover_col < boundary_index:
            target_col = boundary_index - 1
        else: # mover_col > boundary_index (though examples only show left-to-right)
            target_col = boundary_index + 1
            
    elif orientation == 'horizontal':
        # Move vertically towards the boundary row
        target_col = mover_col # Column remains the same
        # Stop one step before the boundary
        if mover_row < boundary_index: # Mover is above boundary (not in examples)
             target_row = boundary_index - 1
        else: # mover_row > boundary_index (as in example 2)
             target_row = boundary_index + 1

    # Check if target position is valid
    if 0 <= target_row < rows and 0 <= target_col < cols:
        # 5. Create the output grid (already done via np.copy)
        # 6. Set the pixel at the mover's initial position to white (0)
        output_grid[mover_row, mover_col] = 0
        # 7. Set the pixel at the calculated target position to the mover's color
        output_grid[target_row, target_col] = mover_color
    else:
        # Handle cases where target is out of bounds (shouldn't happen with current logic/examples)
        print(f"Warning: Calculated target position ({target_row}, {target_col}) is out of bounds.")
        return input_grid # Return original grid if target is invalid

    # Convert the result back to a list of lists
    return output_grid.tolist()
```