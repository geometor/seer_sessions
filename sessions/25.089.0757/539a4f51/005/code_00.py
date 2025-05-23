import numpy as np

"""
Transforms an input grid into an output grid based on the following rules:
1.  Determine the input grid dimensions (H x W).
2.  Identify the top-left color (C) at `input_grid[0][0]`.
3.  Create a 'modified input grid' (I'):
    - Start with a copy of the input grid.
    - If the input grid contains white (0), replace all white pixels in I' with color C.
    - Otherwise, I' is identical to the input grid.
4.  Determine the output grid dimensions (2H x 2W). Initialize an output grid.
5.  Construct the output grid by filling four H x W quadrants:
    - Top-Left (TL) [0:H, 0:W]: Copy the modified input grid (I').
    - Top-Right (TR) [0:H, W:2W]: Take the first row of I' (`I'[0, :]`) and repeat it vertically H times.
    - Bottom-Left (BL) [H:2H, 0:W]: Take the first column of I' (`I'[:, 0]`) and repeat it horizontally W times.
    - Bottom-Right (BR) [H:2H, W:2W]: Copy the modified input grid (I').
"""

def transform(input_grid):
    """
    Applies the transformation rules to the input grid.
    """
    # Convert input list of lists to a numpy array for efficient manipulation
    input_array = np.array(input_grid, dtype=int)
    
    # 1. Determine the height H and width W of the input grid.
    input_height, input_width = input_array.shape
    
    # 2. Identify the color C located at the top-left corner (0,0).
    top_left_color = input_array[0, 0]
    
    # 3. Create a 'modified input grid' (I').
    modified_input_grid = input_array.copy()
    # Check if the input grid contains any white pixels (0).
    if 0 in input_array:
        # If yes, replace all white (0) pixels with the top-left color C.
        modified_input_grid[modified_input_grid == 0] = top_left_color
        
    # 4. Calculate the dimensions of the output grid and initialize it.
    output_height = input_height * 2
    output_width = input_width * 2
    # Use the same data type as the input
    output_array = np.zeros((output_height, output_width), dtype=input_array.dtype)
    
    # 5. Construct the output grid by filling the four quadrants:

    # - Top-Left (TL): Copy the modified input grid (I').
    output_array[0:input_height, 0:input_width] = modified_input_grid
    
    # - Top-Right (TR): Take the first row of I' and repeat it vertically H times.
    first_row = modified_input_grid[0, :] # Get the first row
    tr_quadrant = np.tile(first_row, (input_height, 1)) # Repeat row H times vertically
    output_array[0:input_height, input_width:output_width] = tr_quadrant
    
    # - Bottom-Left (BL): Take the first column of I' and repeat it horizontally W times.
    first_col = modified_input_grid[:, 0] # Get the first column
    # Reshape to a column vector (Hx1) before tiling horizontally
    first_col_reshaped = first_col.reshape(-1, 1) 
    bl_quadrant = np.tile(first_col_reshaped, (1, input_width)) # Repeat column W times horizontally
    output_array[input_height:output_height, 0:input_width] = bl_quadrant
    
    # - Bottom-Right (BR): Copy the modified input grid (I').
    output_array[input_height:output_height, input_width:output_width] = modified_input_grid
    
    # Convert the output numpy array back to a list of lists for the required format.
    output_grid = output_array.tolist()
    
    return output_grid
