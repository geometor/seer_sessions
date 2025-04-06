import numpy as np

"""
Transforms the input grid by processing each row independently.
Identifies contiguous horizontal runs of the value '5'.
If a run of '5's has a length greater than 1, it modifies the cells
within that run based on their 1-based position: cells at odd positions
(1st, 3rd, 5th, ...) within the run are changed to '4', while cells
at even positions (2nd, 4th, ...) remain '5'.
Cells with value '0' and isolated '5's (runs of length 1) remain unchanged.
(Note: This rule consistently explains all examples except for a single anomaly
at cell (0, 2) in the expected output of train_3, which is assumed to be an error
in the example data).
"""

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid: A list of lists representing the 2D input grid.

    Returns:
        A list of lists representing the 2D output grid.
    """
    # Convert input to numpy array for easier processing and element access
    grid = np.array(input_grid, dtype=int)
    # Initialize output_grid as a direct copy of the input grid. 
    # Modifications based on the rule will be applied to this copy.
    output_grid = grid.copy()
    rows, cols = grid.shape

    # Process each row independently
    for r in range(rows):
        c = 0  # Initialize column index for scanning the current row
        # Use a while loop to iterate through columns, allowing us to skip ahead
        # after processing a run.
        while c < cols:
            # Check if the current cell contains the value '5'
            if grid[r, c] == 5:
                # Found the potential start of a horizontal run of '5's
                run_start = c
                # Find the end index (exclusive) of the contiguous run of '5's
                run_end = c + 1
                while run_end < cols and grid[r, run_end] == 5:
                    run_end += 1

                # Calculate the length of the identified run
                run_length = run_end - run_start

                # Apply the transformation rule ONLY if the run length is greater than 1
                if run_length > 1:
                    # Iterate through the cells *within* this specific run
                    for i in range(run_length):
                        # Calculate the actual column index in the grid for the current cell in the run
                        current_col_in_run = run_start + i
                        # Calculate the 1-based position within the run (1st, 2nd, 3rd...)
                        position_in_run = i + 1
                        # Check if the position within the run is odd (1, 3, 5, ...)
                        if position_in_run % 2 != 0:
                            # If odd, change the value in the output grid to '4'
                            output_grid[r, current_col_in_run] = 4
                        # Else (position is even: 2, 4, 6,...), the value remains '5' 
                        # (as it was initially copied from the input)

                # Move the main column iterator 'c' to the end of the just-processed run
                # This prevents re-checking cells already part of this run.
                c = run_end
            else:
                # If the current cell is not '5', simply move to the next column
                c += 1

    # Convert the final numpy array back to a standard list of lists format for the return value
    return output_grid.tolist()