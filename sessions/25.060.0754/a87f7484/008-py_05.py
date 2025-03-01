"""
1.  **Check for Azure Region:** If the input grid contains a contiguous 3x3 block of azure (color 8), extract that 3x3 block as the output. The last occurance (bottom-most) is the target.

2.  **Check for Center-Surrounded Pattern:** If the input grid is 5x5 and has a single azure (color 8) pixel in the center (2,2) surrounded by gray (color 5), create an 11x11 output grid. Replicate input to output, with the central 3x3 sub grid following an inversion rule:
    - swap the gray and the azure pixels on every other grid

3. **Check Diagonal Pattern:** If the grid contains all blue, except for a single line of green, find the largest square that can be fit in the grid, and output that grid with all blue changed to green.
"""

import numpy as np

def find_last_region_center(grid, color):
    # Find all pixels of the target color
    target_pixels = np.argwhere(grid == color)
    
    if target_pixels.size == 0:
        return None
    
    #assume the last occurance will be the bottom region, since that is our target
    last_occurance = target_pixels[-1]

    return (last_occurance[0], last_occurance[1])

def extract_subgrid(grid, center, size):
    # Calculate the boundaries of the sub-grid
    row_start = max(0, center[0] - size // 2)
    row_end = min(grid.shape[0], center[0] + size // 2 + 1)
    col_start = max(0, center[1] - size // 2)
    col_end = min(grid.shape[1], center[1] + size // 2 + 1)
    
    # Extract the sub-grid
    return grid[row_start:row_end, col_start:col_end]

def transform_type_1(input_grid):
    # Convert input grid to a NumPy array
    input_grid_np = np.array(input_grid)
    
    # Find the center of the last region of azure (8) pixels
    center = find_last_region_center(input_grid_np, 8)
    
    if center is None:
        return None  # Or handle the case where no azure region is found

    # Define the size of the sub-grid to extract
    sub_grid_size = 3
        
    # Extract the sub-grid
    output_grid = extract_subgrid(input_grid_np, center, sub_grid_size)
    
    return output_grid.tolist()

def transform_type_2(input_grid):
    # Convert to numpy array
    input_grid_np = np.array(input_grid)

    # Check if the input grid matches the pattern: central colored region surrounded by another color
    center_color = input_grid_np[2, 2]
    border_color = input_grid_np[0, 0]

    # Create an output grid that's 11x11
    output_grid = np.full((11, 11), border_color)

    # Create a 3x3 subgrid for easier color inversion.
    subgrid = np.full((3, 3), border_color)
    subgrid[1,1] = center_color
    
    # Place subgrids, inverting center where i+j is even
    for i in range(3):
        for j in range(3):
            # Calculate the offset for this block of input
            row_offset = i * 3 + 1
            col_offset = j * 3 + 1

            if (i + j) % 2 == 0:
                temp_grid = np.where(subgrid == center_color, border_color, subgrid)
                temp_grid = np.where(temp_grid == border_color, center_color, temp_grid)
            else:
                temp_grid = subgrid

             # Place in the output grid
            output_grid[row_offset:row_offset + 3, col_offset:col_offset+3] = temp_grid
    
    return output_grid.tolist()

def get_largest_square(input_grid_np):
    # find the largest possible square
    rows, cols = input_grid_np.shape
    return min(rows, cols)

def transform_type_3(input_grid):

    input_grid_np = np.array(input_grid)

    # find largest square
    size = get_largest_square(input_grid_np)
    
    # extract grid
    output_grid = extract_subgrid(input_grid_np, (input_grid_np.shape[0] // 2, input_grid_np.shape[1] // 2), size)    
    output_grid = np.where(output_grid == 1, 3, output_grid)

    return output_grid.tolist()


def transform(input_grid):
    # initialize output_grid
    output_grid = None
    
    # Attempt Type 1
    output_grid = transform_type_1(input_grid)
    if output_grid is not None:
        return output_grid    
    
    # Attempt Type 2 (check central region surrounded)
    input_grid_np = np.array(input_grid)
    if input_grid_np.shape == (5,5) and input_grid_np[2,2] == 8 and input_grid_np[0,0] == 5:
         return transform_type_2(input_grid)

    # Attempt Type 3
    return transform_type_3(input_grid)