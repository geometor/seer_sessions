import numpy as np

"""
1. Read the input grid and determine its dimensions, N x N.
2. Identify the single non-white color, C, present in the input grid.
3. Create a "template" grid, T, of size N x N. Populate T by taking the 
   original input grid and replacing every white pixel (0) with color C, 
   and every pixel of color C with white (0).
4. Create the output grid with dimensions (N * N) x (N * N), and 
   initialize all its pixels to white (0).
5. Iterate through each pixel of the input grid at row `r` and column `c`.
6. Check the color of the input pixel `input[r][c]`:
   a. If `input[r][c]` is equal to the non-white color C, then copy the 
      entire template grid T into the output grid, placing its top-left 
      corner at `output[r * N][c * N]`.
   b. If `input[r][c]` is white (0), do nothing (the corresponding N x N 
      block in the output grid remains white).
7. Return the completed output grid.
"""

def find_non_white_color(grid):
    """Finds the first non-white (non-zero) color in the grid."""
    for row in grid:
        for pixel in row:
            if pixel != 0:
                return pixel
    return 0 # Should not happen based on task description, but handle defensively

def create_inverted_template(grid, color_c):
    """Creates a template by swapping white (0) and color_c in the grid."""
    template = grid.copy()
    white_mask = (template == 0)
    color_c_mask = (template == color_c)
    template[white_mask] = color_c
    template[color_c_mask] = 0
    return template

def transform(input_grid):
    """
    Transforms the input grid based on a pattern tiling rule where blocks
    in the output correspond to pixels in the input, and non-white pixels
    trigger the placement of a color-inverted version of the input pattern.
    """
    # Convert input to numpy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)

    # 1. Determine dimensions (N x N)
    n = input_np.shape[0]
    if n == 0 or input_np.shape[1] != n:
        # Handle potential empty or non-square input, although ARC constraints likely prevent this
        return [] 

    # 2. Identify the non-white color C
    color_c = find_non_white_color(input_np)
    if color_c == 0:
         # Handle case where input is all white (output should be all white)
         output_size = n * n
         return np.zeros((output_size, output_size), dtype=int).tolist()


    # 3. Create the template grid T (color inverted input)
    template_t = create_inverted_template(input_np, color_c)

    # 4. Initialize the output grid (N*N x N*N) with white (0)
    output_size = n * n
    output_grid = np.zeros((output_size, output_size), dtype=int)

    # 5. Iterate through the input grid
    for r in range(n):
        for c in range(n):
            # 6. Check input pixel color
            input_pixel = input_np[r, c]

            # 6a. If input pixel is color C, place the template
            if input_pixel == color_c:
                # Calculate the top-left corner for the block
                start_row = r * n
                start_col = c * n
                # Calculate the bottom-right corner (exclusive)
                end_row = start_row + n
                end_col = start_col + n
                # Copy the template into the output grid block
                output_grid[start_row:end_row, start_col:end_col] = template_t
            # 6b. If input pixel is white (0), do nothing (block remains white)

    # 7. Return the completed output grid (convert back to list of lists if needed)
    return output_grid.tolist()