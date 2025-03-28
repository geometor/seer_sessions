"""
Transforms an input grid into an output grid based on a conditional tiling rule using the input grid itself as the tile or stamp.

The transformation follows these steps:
1. Determine the dimensions of the input grid (Height_in, Width_in).
2. Define a scaling factor (SF), which is 3 for this task. All example inputs are 3x3, matching this factor.
3. Calculate the output grid dimensions (Height_out, Width_out) by multiplying the input dimensions by the scaling factor SF (Height_out = Height_in * SF, Width_out = Width_in * SF).
4. Identify the background color (white, 0).
5. Create a new output grid with dimensions (Height_out, Width_out), initialized entirely with the background color.
6. Iterate through each cell (r_in, c_in) of the input grid.
7. If the input cell input_grid[r_in][c_in] contains a non-background color:
    a. Locate the top-left corner of the target SFxSF (3x3) subgrid region in the output grid, which is at row (r_in * SF) and column (c_in * SF).
    b. Copy the *entire original input grid* (which acts as a stamp) into this target SFxSF subgrid region starting at the calculated top-left corner.
8. If the input cell contains the background color, the corresponding SFxSF subgrid in the output remains filled with the background color (as initialized).
9. Return the completed output grid.
"""

import numpy as np

def transform(input_grid):
    """
    Applies a conditional tiling transformation using the input grid as a stamp.

    Args:
        input_grid (list of lists): The input grid represented as a 2D list of integers.

    Returns:
        list of lists: The transformed output grid.
    """
    # Convert input list of lists to a NumPy array for easier processing
    input_np = np.array(input_grid, dtype=int)
    
    # 1. Determine input dimensions
    h_in, w_in = input_np.shape
    
    # 2. Define scaling factor and background color
    # Based on examples, the output grid is 3x the input grid size.
    sf = 3 
    # Background color is white (0)
    bg_color = 0
    
    # 3. Calculate output dimensions
    h_out = h_in * sf
    w_out = w_in * sf
    
    # 5. Initialize the output grid with the background color
    output_grid = np.full((h_out, w_out), bg_color, dtype=int)
    
    # 6. Iterate through each cell of the input grid
    for r_in in range(h_in):
        for c_in in range(w_in):
            # 7. Check if the current input cell is not the background color
            if input_np[r_in, c_in] != bg_color:
                # 7a. Calculate the top-left corner coordinates for placing the stamp in the output grid
                start_r = r_in * sf
                start_c = c_in * sf
                
                # Calculate the bottom-right corner coordinates for the stamp placement
                # Since the stamp is the input grid itself, its size is h_in x w_in
                end_r = start_r + h_in 
                end_c = start_c + w_in 
                
                # 7b. Copy the entire original input grid (stamp) into the target subgrid region
                # Ensure the placement is within the bounds of the output grid
                # (This check is technically redundant if h_in=w_in=sf, but good practice)
                if end_r <= h_out and end_c <= w_out:
                     output_grid[start_r:end_r, start_c:end_c] = input_np
                else:
                    # Handle potential boundary issues if sf didn't match h_in/w_in
                    # or if calculations were off. For this task's examples,
                    # h_in=w_in=sf=3, so this condition should not be met.
                    # If it were, we'd need clarification on how to handle partial stamps.
                    # As a basic fallback, copy only the overlapping part.
                    copy_h = min(h_in, h_out - start_r)
                    copy_w = min(w_in, w_out - start_c)
                    output_grid[start_r:start_r+copy_h, start_c:start_c+copy_w] = input_np[:copy_h, :copy_w]


    # 9. Convert the final NumPy array back to a list of lists before returning
    return output_grid.tolist()