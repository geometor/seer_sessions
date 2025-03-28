import copy

"""
For each row in the input grid, identify the color in the first column (column 0).
Then, iterate through the rest of the row (columns 1 onwards).
If a pixel in the row has the color gray (5), change its color in the output grid to the color identified from the first column of that row.
All other pixels (white, colors in the first column, or non-gray colors in other columns) retain their original color.
"""

def transform(input_grid):
    """
    Transforms the input grid based on the rule: gray pixels in a row are replaced
    by the color found in the first column of that row.

    Args:
        input_grid (list[list[int]]): A 2D list representing the input grid.

    Returns:
        list[list[int]]: A 2D list representing the transformed output grid.
    """
    # Initialize output_grid as a deep copy of the input grid to preserve original values
    output_grid = copy.deepcopy(input_grid)
    
    # Define the target color to be replaced
    target_color = 5 # gray

    # Get grid dimensions
    height = len(input_grid)
    if height == 0:
        return output_grid # Handle empty grid case
    width = len(input_grid[0])
    if width == 0:
        return output_grid # Handle empty row case

    # Iterate through each row
    for r in range(height):
        # Get the replacement color from the first column of the current row in the *input* grid
        replacement_color = input_grid[r][0]

        # No replacement happens if the first column color is white (0)
        # and also no replacement is needed if the target color itself is white (which is not the case here, but good practice)
        # or if the replacement color is the same as the target color (gray replacing gray - no change needed)
        if replacement_color == 0 or replacement_color == target_color:
            continue

        # Iterate through each column in the current row (starting from column 1, as column 0 is the source)
        # Actually, we need to iterate from column 0 as well, in case the first column itself is gray (though unlikely based on examples)
        # Let's iterate through all columns for simplicity, the copy handles column 0 preservation unless it's gray.
        # Re-evaluating: The rule implies column 0 color dictates the change, but column 0 itself doesn't change *based on itself*.
        # The examples show column 0 pixels are preserved. So iterate from column 1.
        for c in range(1, width):
            # Check if the pixel in the *input* grid is the target color (gray)
            if input_grid[r][c] == target_color:
                # If it is gray, change the corresponding pixel in the output grid to the replacement color
                output_grid[r][c] = replacement_color
            # If it's not gray, it retains its original color (already handled by the deepcopy)

    return output_grid