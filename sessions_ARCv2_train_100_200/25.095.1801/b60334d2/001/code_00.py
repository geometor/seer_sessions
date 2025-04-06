import copy

"""
Transforms an input grid based on the locations of the value 5.

For each cell containing the value 5 in the input grid, a specific 3x3 pattern 
is applied to the output grid, centered at the location of the input 5. 
The pattern is:
[[5, 1, 5],
 [1, 0, 1],
 [5, 1, 5]]
The center of the pattern (corresponding to the original 5's location) 
results in a 0 in the output. Non-zero values (1s and 5s) from the pattern 
overwrite existing values in the output grid if they fall within the grid boundaries. 
Overlapping patterns from multiple input 5s will result in the latest non-zero 
pattern value being written to the overlapping cell.
"""

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies the 3x3 pattern transformation based on input grid's '5's.

    Args:
        input_grid: A 2D list of integers representing the input state.

    Returns:
        A 2D list of integers representing the transformed output state.
    """
    # Get dimensions of the input grid
    rows = len(input_grid)
    if rows == 0:
        return []
    cols = len(input_grid[0])
    if cols == 0:
        return [[] for _ in range(rows)]

    # Initialize output_grid with zeros, same dimensions as input_grid
    output_grid = [[0 for _ in range(cols)] for _ in range(rows)]

    # Define the 3x3 pattern to apply
    pattern = [
        [5, 1, 5],
        [1, 0, 1],
        [5, 1, 5]
    ]
    pattern_size = 3
    pattern_center_offset = pattern_size // 2 # This is 1 for a 3x3 pattern

    # Iterate through each cell of the input grid
    for r in range(rows):
        for c in range(cols):
            # Check if the current cell contains the trigger value (5)
            if input_grid[r][c] == 5:
                # If triggered, apply the pattern centered at (r, c)
                for pattern_r in range(pattern_size):
                    for pattern_c in range(pattern_size):
                        # Calculate the target coordinates in the output grid
                        target_r = r + (pattern_r - pattern_center_offset)
                        target_c = c + (pattern_c - pattern_center_offset)

                        # Check if the target coordinates are within the grid bounds
                        if 0 <= target_r < rows and 0 <= target_c < cols:
                            # Get the value from the pattern
                            pattern_value = pattern[pattern_r][pattern_c]
                            # Only update the output grid if the pattern value is non-zero
                            if pattern_value != 0:
                                output_grid[target_r][target_c] = pattern_value

    # Return the final transformed grid
    return output_grid