import numpy as np

"""
Identify columns containing a vertical transition from blue (1) to magenta (6) below the first row.
Find the column where this transition occurs earliest (minimum row index, rightmost column in case of ties). Draw a yellow (4) vertical line in this column from row 1 up to the row before the transition.
Find the column where this transition occurs latest (maximum row index, leftmost column in case of ties). Draw a maroon (9) vertical line in this column from row 1 up to the row before the transition.
All other pixels remain unchanged.
"""

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid (list of lists): The input grid represented as a list of lists of integers.

    Returns:
        list of lists: The transformed output grid.
    """
    input_np = np.array(input_grid, dtype=int)
    output_grid = np.copy(input_np)
    height, width = input_np.shape

    # Initialize variables to track the earliest and latest transitions
    min_transition_row = float('inf')
    min_transition_col = -1
    max_transition_row = -1
    max_transition_col = -1

    # Iterate through each column to find transitions
    for c in range(width):
        # Iterate through rows, starting from the second row (index 1)
        for r in range(1, height):
            # Check for a transition from blue (1) to magenta (6)
            if input_np[r, c] == 6 and input_np[r-1, c] == 1:
                transition_row = r # Record the row where magenta starts

                # Check if this transition is earlier than the current minimum
                if transition_row < min_transition_row:
                    min_transition_row = transition_row
                    min_transition_col = c
                # If it's the same as the minimum, update column to the rightmost one
                elif transition_row == min_transition_row:
                    min_transition_col = c

                # Check if this transition is later than the current maximum
                if transition_row > max_transition_row:
                    max_transition_row = transition_row
                    max_transition_col = c
                # If it's the same as the maximum, keep the leftmost column (do nothing here)
                # elif transition_row == max_transition_row:
                    # pass

                # Once a transition is found in a column, no need to check further down
                break 

    # Draw the yellow line for the earliest transition (rightmost tie)
    if min_transition_col != -1:
        for r in range(1, min_transition_row):
            # Ensure we don't try to draw outside the grid (shouldn't happen with r>0)
            if r < height:
                 output_grid[r, min_transition_col] = 4 # Yellow

    # Draw the maroon line for the latest transition (leftmost tie)
    if max_transition_col != -1:
        for r in range(1, max_transition_row):
             # Ensure we don't try to draw outside the grid (shouldn't happen with r>0)
             if r < height:
                # Avoid overwriting the yellow line if columns happen to be the same
                # (though the logic should prevent this unless only one transition column exists)
                if output_grid[r, max_transition_col] != 4:
                    output_grid[r, max_transition_col] = 9 # Maroon
                # If the yellow line is already there, we need to decide priority.
                # Based on the examples, it seems the lines don't overlap if min!=max.
                # If min==max, the example isn't given, but let's assume maroon overwrites yellow if necessary,
                # although the column selection logic (leftmost for max, rightmost for min) should prevent this
                # unless there is only *one* column with a transition.
                # In the case of one column, max_col == min_col, max_row == min_row.
                # The loops will draw yellow first, then maroon overwrites it. Let's stick to maroon.
                elif output_grid[r, max_transition_col] == 4 and max_transition_col == min_transition_col:
                     output_grid[r, max_transition_col] = 9 # Maroon


    # Convert back to list of lists for the standard ARC output format
    return output_grid.tolist()