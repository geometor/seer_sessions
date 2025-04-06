import copy

"""
Transforms the input grid based on a specific local pattern. It identifies 
occurrences of the horizontal sequence [1, 1, 8, 8, 8, 1, 1] in each row. 
If such a sequence is found starting at column 'c' in row 'r', and the cell 
directly above the middle '8' of the pattern (at position (r-1, c+3)) is also 
an '8', then this constitutes a valid pattern match. If multiple valid patterns 
are found within the same row, only the rightmost one (the one starting at the 
largest column index 'c') is considered. For the selected valid pattern in a 
row, the middle '8' (at position (r, c+3)) in the output grid is changed to '4'. 
All other cells remain unchanged.
"""

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid: A list of lists representing the input 2D grid of integers.

    Returns:
        A list of lists representing the transformed 2D grid.
    """
    # Initialize output_grid as a deep copy of the input grid
    output_grid = copy.deepcopy(input_grid)

    # Get grid dimensions
    num_rows = len(input_grid)
    if num_rows == 0:
        return output_grid # Return copy if grid is empty
    num_cols = len(input_grid[0])

    # Define the pattern to search for and its length
    pattern = [1, 1, 8, 8, 8, 1, 1]
    pattern_len = len(pattern)
    
    # The index within the pattern of the cell to potentially change (the middle 8)
    target_pattern_index = 3 

    # Check if the grid is wide enough for the pattern
    if num_cols < pattern_len:
        return output_grid # Pattern cannot exist, return the copy

    # Dictionary to store the column index of the cell to modify for each row.
    # We store the target column index (c + target_pattern_index).
    # Since we iterate columns left-to-right, later matches in the same row will
    # automatically overwrite earlier ones, effectively selecting the rightmost.
    row_modification_targets = {}

    # Iterate through each row, starting from the second row (index 1)
    # as we need to check the cell above.
    for r in range(1, num_rows):
        # Iterate through columns, stopping early enough to allow for a full pattern match
        for c in range(num_cols - pattern_len + 1):
            # Extract the horizontal slice from the input grid
            horizontal_slice = input_grid[r][c : c + pattern_len]

            # Check if the slice matches the horizontal pattern
            if horizontal_slice == pattern:
                # Calculate the column index of the target cell (the middle 8)
                target_col = c + target_pattern_index
                
                # Check the value of the cell directly above the target cell
                if input_grid[r-1][target_col] == 8:
                    # If both pattern matches and cell above is 8, record this target column for the current row.
                    # Overwriting ensures only the rightmost valid target is stored.
                    row_modification_targets[r] = target_col

    # After checking all rows and columns, apply the modifications based on the selected targets
    for r, target_c in row_modification_targets.items():
        # Change the value in the output grid
        output_grid[r][target_c] = 4

    # Return the modified grid
    return output_grid