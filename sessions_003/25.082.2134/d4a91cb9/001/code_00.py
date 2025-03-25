"""
1.  **Identify**: Locate the two non-black pixels in the input grid. Let's call the pixel whose color is changed to yellow in the next step as pixel A, and the other pixel at the corner as pixel B.
2.  **Extend**: Change pixel A to yellow. Extend the yellow region from pixel A, either vertically or horizontally to the row or column that aligns with the start of the yellow region based on input pixel B position.
3.  **Fill Rectangle**: Fill the space between the extended line, and up to input pixel B, making a rectangle of yellow color (value 4).
4. **Keep second pixel**: Keep pixel B with the same input value in the output.
5. **Everything else**: The rest of pixels are black.
"""

import numpy as np

def find_non_black_pixels(grid):
    # Find coordinates of non-black pixels
    non_black_indices = np.argwhere(grid != 0)
    return non_black_indices

def transform(input_grid):
    # initialize output_grid
    output_grid = np.zeros_like(input_grid)
    
    # Find the two non-black pixels
    non_black_pixels = find_non_black_pixels(input_grid)
    if len(non_black_pixels) != 2:
      return output_grid # Handles cases not fitting the expected pattern
    
    pixel_a_coords = non_black_pixels[0]
    pixel_b_coords = non_black_pixels[1]
    
    # Determine which pixel is A and which is B based on their relative output positions
    if input_grid[pixel_a_coords[0],pixel_a_coords[1]] == input_grid[pixel_b_coords[0],pixel_b_coords[1]]:
        return input_grid
    
    if input_grid[pixel_a_coords[0], pixel_a_coords[1]] != input_grid[pixel_b_coords[0], pixel_b_coords[1]]:
        #pixel that extends
        output_grid[pixel_a_coords[0], pixel_a_coords[1]] = 4 # Color pixel A yellow

        # Extend yellow region, horizontally or vertically
        if pixel_a_coords[0] == pixel_b_coords[0]:  # Same row: extend horizontally
            min_col = min(pixel_a_coords[1], pixel_b_coords[1])
            max_col = max(pixel_a_coords[1], pixel_b_coords[1])
            for col in range(min_col, max_col + 1):
                output_grid[pixel_a_coords[0], col] = 4
        elif pixel_a_coords[1] == pixel_b_coords[1]:  # Same column: extend vertically
             min_row = min(pixel_a_coords[0], pixel_b_coords[0])
             max_row = max(pixel_a_coords[0], pixel_b_coords[0])
             for row in range(min_row, max_row + 1):
                output_grid[row, pixel_a_coords[1]] = 4
        else:  # different row, different column. Check which extends
          
          if input_grid[pixel_a_coords[0]][pixel_a_coords[1]] != input_grid[pixel_b_coords[0]][pixel_b_coords[1]]:
            min_row = min(pixel_a_coords[0], pixel_b_coords[0])
            max_row = max(pixel_a_coords[0], pixel_b_coords[0])
            min_col = min(pixel_a_coords[1], pixel_b_coords[1])
            max_col = max(pixel_a_coords[1], pixel_b_coords[1])
            
            for row in range(min_row, max_row + 1):
              for col in range(min_col, max_col + 1):
                output_grid[row,col] = 4

    #keep pixel B color.
    output_grid[pixel_b_coords[0], pixel_b_coords[1]] = input_grid[pixel_b_coords[0], pixel_b_coords[1]]

    return output_grid