import numpy as np
import copy

"""
Transforms a 10x10 grid by moving a single, isolated non-zero digit ('Moving Digit') 
adjacent to a line (row or column) of identical non-zero digits ('Blocking Pattern').

The transformation involves:
1. Identifying the Blocking Pattern (a full row or column of identical non-zero digits).
2. Identifying the Moving Digit (an isolated non-zero digit different from the background '0' and the pattern).
3. Determining the target position adjacent to the Blocking Pattern, in the direction perpendicular to the pattern's orientation.
4. Moving the Moving Digit to the target position in the output grid.
5. Replacing the Moving Digit's original position with the background value '0'.
"""

def find_blocking_pattern(grid):
    """
    Finds the blocking pattern (a line of identical non-zero digits).

    Args:
        grid (np.ndarray): The input grid.

    Returns:
        tuple: (value, orientation, index) or None if not found.
               orientation is 'horizontal' or 'vertical'.
               index is the row or column index.
    """
    rows, cols = grid.shape

    # Check for horizontal pattern
    for r in range(rows):
        first_val = grid[r, 0]
        if first_val != 0 and np.all(grid[r, :] == first_val):
            return first_val, 'horizontal', r

    # Check for vertical pattern
    for c in range(cols):
        first_val = grid[0, c]
        if first_val != 0 and np.all(grid[:, c] == first_val):
             return first_val, 'vertical', c
             
    # Fallback/Refined check (in case moving digit is initially *in* the line)
    # This is slightly more robust if the line isn't perfectly uniform initially
    # Check rows again, looking for a dominant non-zero value
    for r in range(rows):
        unique_vals, counts = np.unique(grid[r, :], return_counts=True)
        non_zero_indices = np.where(unique_vals != 0)[0]
        if len(non_zero_indices) == 1: # Exactly one non-zero value in the row
            val_index = non_zero_indices[0]
            pattern_val = unique_vals[val_index]
            # Check if this value dominates the row (e.g., appears >= cols-1 times)
            # This handles the case where the moving digit might initially be in the pattern row/col
            if counts[val_index] >= cols -1: 
                 return pattern_val, 'horizontal', r
                 
    # Check columns again, looking for a dominant non-zero value
    for c in range(cols):
        unique_vals, counts = np.unique(grid[:, c], return_counts=True)
        non_zero_indices = np.where(unique_vals != 0)[0]
        if len(non_zero_indices) == 1: # Exactly one non-zero value in the column
            val_index = non_zero_indices[0]
            pattern_val = unique_vals[val_index]
            if counts[val_index] >= rows -1: 
                 return pattern_val, 'vertical', c


    return None, None, -1 # Should not happen based on examples


def find_moving_digit(grid, pattern_value):
    """
    Finds the single, isolated non-zero digit that is not the background or pattern.

    Args:
        grid (np.ndarray): The input grid.
        pattern_value (int): The value of the blocking pattern digit.

    Returns:
        tuple: (value, row, col) or None if not found.
    """
    rows, cols = grid.shape
    for r in range(rows):
        for c in range(cols):
            val = grid[r, c]
            if val != 0 and val != pattern_value:
                # Check if it's truly isolated (or part of the pattern temporarily)
                # A simple check: is it the only non-zero, non-pattern value?
                # (More sophisticated checks could look at neighbors)
                # For this problem, assuming only one such digit exists simplifies this.
                return val, r, c
    return None, -1, -1 # Should not happen based on examples


def transform(input_grid):
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid (list of lists): The input grid.

    Returns:
        list of lists: The transformed output grid.
    """
    # Convert input to numpy array for easier manipulation
    grid_np = np.array(input_grid, dtype=int)
    output_grid_np = copy.deepcopy(grid_np)
    rows, cols = grid_np.shape

    # --- Identify Grid Components ---
    
    # Find the blocking pattern
    pattern_value, orientation, pattern_index = find_blocking_pattern(grid_np)
    if orientation is None:
        # Handle cases where pattern is not found (though examples suggest it always exists)
        return input_grid # Return original if no pattern identifiable

    # Find the moving digit
    moving_value, initial_r, initial_c = find_moving_digit(grid_np, pattern_value)
    if moving_value is None:
         # Handle cases where moving digit is not found
         return input_grid # Return original if no moving digit

    # --- Determine Target Position ---
    target_r, target_c = -1, -1
    if orientation == 'vertical':
        # Pattern is a column at pattern_index
        # Based on Example 1 (pattern col 9, digit moves from col 2 to col 8)
        # Move horizontally towards the column, stopping adjacent to it.
        target_r = initial_r
        # Check if digit is left or right (though example only shows left)
        if initial_c < pattern_index:
            target_c = pattern_index - 1
        else: # initial_c > pattern_index
             target_c = pattern_index + 1 # Assuming symmetry, though not shown
             
    elif orientation == 'horizontal':
        # Pattern is a row at pattern_index
        # Based on Example 2 (pattern row 0, digit moves from row 7 to row 1)
        # Move vertically towards the row, stopping adjacent to it.
        target_c = initial_c
        # Check if digit is above or below (example shows below)
        if initial_r > pattern_index:
             target_r = pattern_index + 1
        else: # initial_r < pattern_index
            target_r = pattern_index - 1 # Assuming symmetry, though not shown

    # --- Update the Output Grid ---
    if target_r != -1 and target_c != -1: # Check if target was determined
        # Set the initial position of the moving digit to 0 (background)
        output_grid_np[initial_r, initial_c] = 0
        # Place the moving digit at the target position
        output_grid_np[target_r, target_c] = moving_value

    # Convert back to list of lists for the expected output format
    output_grid = output_grid_np.tolist()
    return output_grid