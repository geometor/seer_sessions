import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by creating four-way symmetry around the grid's center.
    
    1. Create a copy of the input grid to serve as the initial output grid.
    2. Determine the height (H) and width (W) of the grid.
    3. Iterate through every cell (pixel) of the input grid, identifying its row r, column c, and color C.
    4. If the color C is not white (i.e., C > 0):
        a. Calculate the horizontally reflected column index: c_h = W - 1 - c. Set the color of the pixel at (r, c_h) in the output grid to C.
        b. Calculate the vertically reflected row index: r_v = H - 1 - r. Set the color of the pixel at (r_v, c) in the output grid to C.
        c. Calculate the diagonally reflected position using the indices from steps 4a and 4b: (r_v, c_h). Set the color of the pixel at (r_v, c_h) in the output grid to C.
    5. After iterating through all input pixels, return the completed output grid.
    """

    # Convert input grid to a NumPy array for easier manipulation
    input_array = np.array(input_grid)
    
    # Initialize output_grid as a copy of the input grid
    output_array = np.copy(input_array)
    
    # Determine the height (H) and width (W) of the grid
    H, W = input_array.shape

    # Iterate through every cell (pixel) of the input grid
    for r in range(H):
        for c in range(W):
            # Identify the color C of the current pixel
            C = input_array[r, c]
            
            # If the color C is not white (0)
            if C != 0:
                # Calculate the horizontally reflected column index
                c_h = W - 1 - c
                # Set the color of the horizontally reflected pixel in the output grid
                output_array[r, c_h] = C
                
                # Calculate the vertically reflected row index
                r_v = H - 1 - r
                # Set the color of the vertically reflected pixel in the output grid
                output_array[r_v, c] = C
                
                # Calculate the diagonally reflected position (combining horizontal and vertical reflections)
                # Set the color of the diagonally reflected pixel in the output grid
                output_array[r_v, c_h] = C

    # Convert the NumPy array back to a list of lists for the final output
    output_grid = output_array.tolist()
    
    return output_grid
