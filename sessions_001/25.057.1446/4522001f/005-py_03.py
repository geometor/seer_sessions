"""
1.  **Identify Red Pixels:** Locate all pixels in the input grid that are red (color value 2).
2.  **Replace with Green Blocks:** For *each* red pixel found in the input:
    *   Change the color to green (color value 3).
    *   Create a 4x4 block of green pixels.
    *   The top-left corner of this 4x4 block in the output grid corresponds to the original location of the red pixel in the input grid.
3.  **Output Dimensions**: Create an output that can contain these blocks.

    * It is not a simple multiplication of input dimensions.
    * The location of the red pixels in the input grid will define the output shape.
    * The output shape will be different in many cases.
4. All other pixels are black.
"""

import numpy as np

def find_red_pixels(grid):
    """Finds the coordinates of all red pixels in the grid."""
    red_pixels = []
    for row_index, row in enumerate(grid):
        for col_index, pixel in enumerate(row):
            if pixel == 2:
                red_pixels.append((row_index, col_index))
    return red_pixels

def calculate_output_dimensions(red_pixels, input_grid):
    """Calculates output dimensions based on red pixel locations."""
    if not red_pixels:
      return len(input_grid), len(input_grid[0]) # if there are no red pixels, return the input shape
    
    max_row = 0
    max_col = 0
    for row, col in red_pixels:
        max_row = max(max_row, row)
        max_col = max(max_col, col)
        
    output_height = max_row + 4  # Add 4 for block size
    output_width = max_col + 4

    # Ensure minimum dimensions based on original input
    input_height = len(input_grid)
    input_width = len(input_grid[0]) if input_height > 0 else 0
    
    return max(output_height, input_height), max(output_width, input_width)
  

def transform(input_grid):
    """Transforms the input grid by replacing red pixels with 4x4 green blocks."""

    # Find coordinates of red pixels
    red_pixels = find_red_pixels(input_grid)

    # Determine the output grid dimensions
    output_height, output_width = calculate_output_dimensions(red_pixels, input_grid)
    output_grid = np.zeros((output_height, output_width), dtype=int)
    
    # Replace each red pixel with a 4x4 green block
    for row, col in red_pixels:
        output_grid[row:row+4, col:col+4] = 3  # Fill 4x4 block with green

    return output_grid.tolist()