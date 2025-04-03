import copy

"""
Transforms a 1D input grid based on a specific pattern.
The transformation identifies sequences of four pixels in the input grid matching the pattern [white, C, white, white], where C is any non-white color (1-9).
For each identified pattern starting at index k, the corresponding pixels in the output grid at indices k, k+1, and k+2 are set to color C. The pixel at index k+3 remains white (0).
The changes are applied based on the initial state of the input grid. Pixels not part of a matched pattern remain unchanged in the output grid.
"""

# Constants for colors (optional, but good practice)
WHITE = 0

def transform(input_grid):
    """
    Applies the pattern-based transformation to the input grid.

    Args:
        input_grid: A list of integers representing the 1D input grid.

    Returns:
        A list of integers representing the transformed 1D output grid.
    """
    # Initialize output_grid as a copy of the input_grid
    # This ensures that pixels not affected by the transformation remain the same
    output_grid = list(input_grid) # Use list() to ensure it's a mutable copy
    grid_length = len(input_grid)

    # Iterate through the input grid to find the pattern
    # The loop needs to stop early enough to allow checking 4 consecutive pixels (k, k+1, k+2, k+3)
    for k in range(grid_length - 3):
        # Check if the sequence starting at k matches the pattern [white, C, white, white]
        # where C is any non-white color (1-9)
        pixel1 = input_grid[k]
        pixel2 = input_grid[k+1]
        pixel3 = input_grid[k+2]
        pixel4 = input_grid[k+3]

        if pixel1 == WHITE and pixel2 != WHITE and pixel3 == WHITE and pixel4 == WHITE:
            # Pattern matched. Identify the color C.
            color_c = pixel2

            # Modify the output grid according to the rule: [C, C, C, white]
            # Note: We modify the output_grid, not the input_grid,
            # to ensure all checks are based on the original input state.
            output_grid[k] = color_c
            output_grid[k+1] = color_c
            output_grid[k+2] = color_c
            # output_grid[k+3] remains white (it's already white based on the pattern match)
            # but explicitly setting it could prevent errors if the copy wasn't perfect, though unnecessary here.
            # output_grid[k+3] = WHITE

    # Return the modified output grid
    return output_grid
