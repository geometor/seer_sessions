import copy

"""
Identifies a specific horizontal pattern [1, 1, 8, 8, 8, 1, 1] within the input grid.
If the pattern is found in a row, the value of the cell corresponding to the 
middle '8' of the pattern (the 4th element in the sequence) is changed to 4 
in the output grid. All other cells remain unchanged.
"""

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Transforms the input grid by finding a specific horizontal pattern 
    [1, 1, 8, 8, 8, 1, 1] and changing the middle 8 to a 4.

    Args:
        input_grid: A list of lists representing the input 2D grid of integers.

    Returns:
        A list of lists representing the transformed 2D grid.
    """
    # Initialize output_grid as a deep copy of the input grid to avoid modifying the original
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

    # Iterate through each row of the grid
    for r in range(num_rows):
        # Iterate through columns, stopping early enough to allow for a full pattern match
        # The last possible starting column index is num_cols - pattern_len
        for c in range(num_cols - pattern_len + 1):
            # Extract the horizontal slice of the grid corresponding to the pattern length
            # We check against the *original* input_grid values
            horizontal_slice = input_grid[r][c : c + pattern_len]

            # Compare the extracted slice with the target pattern
            if horizontal_slice == pattern:
                # If the pattern matches, modify the cell in the output_grid
                # The column index to modify is the starting column 'c' plus the target index within the pattern
                col_to_modify = c + target_pattern_index
                output_grid[r][col_to_modify] = 4

    # Return the modified grid
    return output_grid