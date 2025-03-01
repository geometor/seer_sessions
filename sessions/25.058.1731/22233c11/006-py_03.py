"""
1.  **Identify Green Pixels:** Locate all pixels colored green (value 3) in the input grid.
2.  **Check for Diagonal Pairs (Down-Right):** Determine if pairs of green pixels are positioned diagonally from each other, specifically where one is down and to the right of the other.
3. **Place Azure Diagonally:** For each pair identified in step 2, fill the spaces between the green pixels on that diagonal with azure (value 8) pixels.
4.  **Maintain Original Pixels:** Ensure all pixels from the original input grid, other than those filled with azure in step 3, remain unchanged in the output grid.
"""

import numpy as np

def find_pixels_by_color(grid, color):
    # Find coordinates of all pixels with the specified color.
    return np.argwhere(grid == color)

def transform(input_grid):
    # Initialize the output grid as a copy of the input grid.
    output_grid = np.copy(input_grid)
    
    # Find all green pixels.
    green_pixels = find_pixels_by_color(input_grid, 3)
    
    # Iterate through all pairs of green pixels.
    for i in range(len(green_pixels)):
        for j in range(i + 1, len(green_pixels)):
            row1, col1 = green_pixels[i]
            row2, col2 = green_pixels[j]
            
            # Check if the second pixel is down and to the right of the first.
            if row2 > row1 and col2 > col1:
                # Calculate diagonal offsets.
                row_diff = row2 - row1
                col_diff = col2 - col1

                # Check if they are on the same diagonal.
                if row_diff == col_diff:
                    # Fill the spaces between with azure.
                    for d in range(1, row_diff):
                        output_grid[row1 + d, col1 + d] = 8

    return output_grid