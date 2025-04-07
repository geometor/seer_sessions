```python
import copy

"""
Transforms a 2D grid by replacing specific '8' values with '4'.
An '8' is changed to a '4' if and only if it is the central '8' 
within a horizontal sequence of `[1, 1, 8, 8, 8, 1, 1]` in the input grid.
"""

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid: A list of lists representing the 2D input grid.

    Returns:
        A list of lists representing the transformed 2D output grid.
    """
    # Initialize output_grid as a deep copy of the input to avoid modifying the original
    output_grid = copy.deepcopy(input_grid)

    # Get grid dimensions
    num_rows = len(input_grid)
    if num_rows == 0:
        return output_grid  # Handle empty grid case
    num_cols = len(input_grid[0])
    if num_cols == 0:
        return output_grid # Handle empty row case

    # Define the specific horizontal pattern to search for
    pattern = [1, 1, 8, 8, 8, 1, 1]
    pattern_len = len(pattern)
    # Define the index within the pattern corresponding to the '8' that needs changing
    target_index_in_pattern = 3 # The middle '8'

    # If the grid columns are fewer than the pattern length, no transformation is possible
    if num_cols < pattern_len:
        return output_grid

    # Iterate through each row of the grid
    for r in range(num_rows):
        # Iterate through possible starting columns for the pattern
        # The loop stops early enough so the pattern fits within the row bounds
        for c in range(num_cols - pattern_len + 1):
            # Extract the sequence (window) from the input grid at the current position
            window = input_grid[r][c : c + pattern_len]

            # Check if the extracted window matches the target pattern
            if window == pattern:
                # If the pattern matches, find the column index of the target '8'
                target_col_index = c + target_index_in_pattern
                # Modify the corresponding cell in the output grid to 4
                output_grid[r][target_col_index] = 4

    # Return the modified grid
    return output_grid
```