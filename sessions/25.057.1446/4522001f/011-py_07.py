"""
1.  **Zero Handling:** If the input grid contains *only* white (0) pixels, the output grid is an exact copy of the input grid.
2.  **Green Object Identification:** If the input grid contains any green (3) pixels, identify the green object.
3. **Duplication/Expansion and Shifting:**
    *   If a single green pixel present, create a cross shaped object, the initial object at the top left, and two added green pixels
    *    Otherwise: The original green pixels remains in their original positions relative to the overall output grid, but a copy is created and moved. The direction and magnitude of the move depend on the size and potentially shape of original green. The pattern appears to be one where the green pixels also are placed diagonally down.
4. **Padding:** Empty cells are filled with zeros
"""

import numpy as np

def find_green_object(grid):
    # Find the coordinates of all green pixels (value 3).
    green_pixels = np.argwhere(grid == 3)
    if len(green_pixels) == 0:
        return None  # No green object found.

    # find top-left and bottom-right
    min_row, min_col = np.min(green_pixels, axis=0)
    max_row, max_col = np.max(green_pixels, axis=0)
    return (min_row, min_col), (max_row, max_col)

def transform(input_grid):
    # Zero Handling: If only white pixels, return input grid.
    if np.all(input_grid == 0):
        return input_grid.copy()

    # Find green object.
    green_object_bounds = find_green_object(input_grid)
    if green_object_bounds is None:
        return input_grid.copy()  # Should not happen based on prior rule, but good practice
    
    (min_row, min_col), (max_row, max_col) = green_object_bounds
    green_object_height = max_row - min_row + 1
    green_object_width = max_col - min_col + 1
    
    # Determine output grid size and initialize.
    if green_object_height == 1 and green_object_width == 1:
        output_grid = np.zeros((3,3), dtype=int)
         # create cross
        output_grid[0,0] = 3
        output_grid[2,2] = 3
    
    else:
        output_height = input_grid.shape[0] * 3 - (input_grid.shape[0] - 1)  if input_grid.shape[0] > 1 else 3 #special handle of 1 width input
        output_width = input_grid.shape[1] * 3  - (input_grid.shape[1] - 1) if input_grid.shape[1] > 1 else 3
        
        output_grid = np.zeros((output_height, output_width), dtype=int)

        # Copy the original green object to the top-left corner of its section.
        for r in range(input_grid.shape[0]):
            for c in range(input_grid.shape[1]):
                output_grid[r,c] = input_grid[r,c]
        
        # duplicate green to bottom-right
        output_start_row = output_height - green_object_height
        output_start_col = output_width - green_object_width

        for r in range(green_object_height):
             for c in range(green_object_width):
                if input_grid[min_row+r, min_col+c] == 3:
                    output_grid[output_start_row + r, output_start_col + c] = 3
    
    return output_grid