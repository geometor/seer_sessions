"""
Transforms a 3x3 input grid containing white (0) and one other color (C) into a larger square grid of size S x S.

1. Identify the non-white color (C) in the 3x3 input grid.
2. Determine the horizontal repetition factor (H_rep), vertical repetition factor (V_rep), and output grid size (S) based on C using a predefined mapping:
   - C=2 (Red): H_rep=3, V_rep=1, S=18
   - C=3 (Green): H_rep=3, V_rep=2, S=9
   - C=4 (Yellow): H_rep=4, V_rep=1, S=15
   - C=6 (Magenta): H_rep=4, V_rep=2, S=12
3. Create an S x S output grid initialized with white (0).
4. Tile the 3x3 input grid pattern H_rep times horizontally and V_rep times vertically within the top-left corner of the output grid. The tiled area will have dimensions (V_rep * 3) x (H_rep * 3).
5. The remaining area of the output grid remains white.
"""

import numpy as np

def find_non_white_color(grid):
    """Finds the first non-white (non-zero) color in the grid."""
    for row in grid:
        for cell in row:
            if cell != 0:
                return cell
    return None # Should not happen based on task description

def transform(input_grid):
    """
    Applies the tiling transformation based on the non-white color.
    """
    input_np = np.array(input_grid, dtype=int)
    input_height, input_width = input_np.shape

    # 1. Identify the non-white color (C)
    color_c = find_non_white_color(input_np)

    if color_c is None:
        # Handle cases where no non-white color is found (though not expected)
        # For robustness, perhaps return an empty grid or the input grid?
        # Let's return a default small white grid for now.
        return np.zeros((1, 1), dtype=int).tolist() 
        
    # 2. Determine H_rep, V_rep, and S based on color_c
    if color_c == 2: # Red
        h_rep, v_rep, size_s = 3, 1, 18
    elif color_c == 3: # Green
        h_rep, v_rep, size_s = 3, 2, 9
    elif color_c == 4: # Yellow
        h_rep, v_rep, size_s = 4, 1, 15
    elif color_c == 6: # Magenta
        h_rep, v_rep, size_s = 4, 2, 12
    else:
        # Handle unexpected colors - return default small white grid
        print(f"Warning: Unexpected color {color_c} found.")
        return np.zeros((1, 1), dtype=int).tolist() 

    # 3. Create an S x S output grid initialized with white (0)
    output_grid = np.zeros((size_s, size_s), dtype=int)

    # 4. Tile the input pattern
    tiled_height = v_rep * input_height
    tiled_width = h_rep * input_width

    for v in range(v_rep):
        for h in range(h_rep):
            # Calculate top-left corner for this tile
            start_row = v * input_height
            start_col = h * input_width
            end_row = start_row + input_height
            end_col = start_col + input_width

            # Copy the input grid to the calculated position in the output grid
            output_grid[start_row:end_row, start_col:end_col] = input_np

    # 5. Convert back to list of lists for the expected output format
    return output_grid.tolist()