import numpy as np

def transform(input_grid):
    """
    The input grid is 12x6 and is conceptually divided vertically into four 3x6 subgrids (rows 0-2, 3-5, 6-8, 9-11).
    The output grid is a 3x6 grid.
    Each pixel (r, c) in the output grid is determined by examining the pixels at the same relative position (r, c) within each of the four input subgrids: input_grid[r][c], input_grid[r+3][c], input_grid[r+6][c], and input_grid[r+9][c].
    The color of the output pixel output_grid[r][c] is the color with the highest priority among the four corresponding input pixels, excluding white (0) unless all four are white.
    The priority order of colors is: gray (5) > yellow (4) > azure (8) > red (2).
    If all four corresponding input pixels are white (0), the output pixel is white (0).
    """

    input_np = np.array(input_grid, dtype=int)
    input_height, input_width = input_np.shape

    # Calculate output dimensions
    output_height = input_height // 4
    output_width = input_width
    
    # Initialize output grid with zeros (white)
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # Define the number of subgrids
    num_subgrids = 4
    subgrid_height = output_height

    # Iterate through each cell of the output grid
    for r in range(output_height):
        for c in range(output_width):
            # Get the corresponding pixels from the four input subgrids
            corresponding_pixels = [
                input_np[r + i * subgrid_height][c] for i in range(num_subgrids)
            ]

            # Determine the output color based on priority
            output_color = 0 # Default to white
            if 5 in corresponding_pixels:
                output_color = 5
            elif 4 in corresponding_pixels:
                output_color = 4
            elif 8 in corresponding_pixels:
                output_color = 8
            elif 2 in corresponding_pixels:
                output_color = 2
            # If none of the priority colors are present, it remains 0 (white)
                
            # Assign the determined color to the output grid cell
            output_grid[r, c] = output_color

    # Convert numpy array back to list of lists for the expected output format
    return output_grid.tolist()
