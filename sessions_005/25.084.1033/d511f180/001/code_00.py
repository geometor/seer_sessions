"""
Processes an input grid by swapping two specific colors: gray (5) and azure (8).
Iterates through each pixel of the input grid. If a pixel is gray (5), it's changed
to azure (8) in the output grid. If a pixel is azure (8), it's changed to gray (5)
in the output grid. All other pixel colors remain unchanged. The output grid has
the same dimensions as the input grid.
"""

import copy # Although copy isn't strictly needed here as we build a new grid

def transform(input_grid):
    """
    Swaps colors 5 (gray) and 8 (azure) in the input grid.

    Args:
        input_grid: A list of lists representing the input grid where each inner
                    list is a row and each element is an integer color code (0-9).

    Returns:
        A new list of lists representing the output grid with colors 5 and 8 swapped,
        maintaining the original dimensions.
    """
    # 1. Get the dimensions of the input grid
    height = len(input_grid)
    # Handle potential empty input grid case
    if height == 0:
        return []
    width = len(input_grid[0])
    # Handle potential empty row case (though unlikely in ARC standard format)
    if width == 0:
        return [[] for _ in range(height)] # Return grid with empty rows

    # 2. Create a new grid with the same dimensions as the input grid.
    # Initialize with a placeholder value (e.g., 0), as all cells will be explicitly set.
    output_grid = [[0 for _ in range(width)] for _ in range(height)]

    # 3. Iterate through each pixel (cell) of the input grid using row and column indices.
    for r in range(height):
        for c in range(width):
            # Get the color value of the current input pixel
            input_pixel_color = input_grid[r][c]

            # 4. Apply the swapping logic based on the input pixel's color.
            if input_pixel_color == 5:
                # If the input color is gray (5), set the corresponding output pixel to azure (8).
                output_grid[r][c] = 8
            elif input_pixel_color == 8:
                # If the input color is azure (8), set the corresponding output pixel to gray (5).
                output_grid[r][c] = 5
            else:
                # 5. If the color is neither gray (5) nor azure (8), keep the original color.
                # Set the corresponding output pixel to the same color as the input pixel.
                output_grid[r][c] = input_pixel_color

    # 6. Return the newly created grid containing the transformed pixels.
    return output_grid