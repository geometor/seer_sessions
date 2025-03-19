"""
1.  **Identify Corner Pixels:** Locate the four corner pixels (top-left, top-right, bottom-left, bottom-right) in the original 6X6 input image, that do not match the predominant background fill color.
2.  **Extract Colors:** Extract only corner colors.
3.  **Construct Output Grid:** Create a 2x2 output grid.
4. **Fill:** Fill the 2X2 grid using the non-background colors of the corresponding input corners. maintain the position of the original corner pixels.
"""

import numpy as np

def get_background_color(grid):
    # Flatten the grid and find the most frequent color.
    unique, counts = np.unique(grid, return_counts=True)
    return unique[np.argmax(counts)]
    

def transform(input_grid):
    """Transforms a 6x6 grid into a 2x2 grid by extracting the colors of the four corner pixels, excluding the background."""
    rows, cols = input_grid.shape
    background_color = get_background_color(input_grid)

    # Initialize the output grid
    output_grid = np.zeros((2, 2), dtype=int)

    # Extract the four corner pixels, checking for background.
    corners = [(0, 0), (0, cols - 1), (rows - 1, 0), (rows - 1, cols - 1)]
    output_coords = [(0, 0), (0, 1), (1, 0), (1, 1)]

    for (in_r, in_c), (out_r, out_c) in zip(corners, output_coords):
        if input_grid[in_r, in_c] != background_color:
           output_grid[out_r, out_c] = input_grid[in_r, in_c]
        else:
            #find next non-background value going down, right, up, or left
            
            for i in range(1,max(rows,cols)):
                # Check down
                if in_r + i < rows and input_grid[in_r+i,in_c] != background_color:
                    output_grid[out_r, out_c] = input_grid[in_r + i, in_c]
                    break
                #check right
                if in_c + i < cols and input_grid[in_r,in_c+i] != background_color:
                    output_grid[out_r, out_c] = input_grid[in_r, in_c+i]
                    break
                #check up
                if in_r - i >= 0 and input_grid[in_r-i,in_c] != background_color:
                    output_grid[out_r, out_c] = input_grid[in_r-i, in_c]
                    break
                #check left
                if in_c - i >= 0 and input_grid[in_r,in_c-i] != background_color:
                    output_grid[out_r, out_c] = input_grid[in_r, in_c-i]
                    break

    return output_grid