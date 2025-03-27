"""
1.  **Identify Background:** Determine the most frequent color in the input grid. This is the background color.
2.  **Identify Objects:** Locate all contiguous regions of non-background color. These are the objects. Record initial positions of object pixels.
3.  **Cross Expansion** From each non-background pixel, fill the background adjacent pixels (up, down, left and right) with the same color.
4. **Interaction**: If two colors want to fill the same background pixel during the expansion, color 6 appears to overwrite color 1.
5. **Boundaries**: expansion should stop at edges of the grid.
6. **Single object shift**: For a single isolated object with only one starting location, perform a shift of each object pixel, rather than expansion:
    - up to the top row
    - if there are two start locations, shift each of them.
"""

import numpy as np
from collections import Counter

def get_background_color(grid):
    flat_grid = grid.flatten()
    color_counts = Counter(flat_grid)
    return color_counts.most_common(1)[0][0]

def get_non_background_pixels(grid, background_color):
    non_background_pixels = []
    rows, cols = grid.shape
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] != background_color:
                non_background_pixels.append(((r, c), grid[r, c]))
    return non_background_pixels

def expand_multi_color(grid, start_pos, color, bg_color):
    # one unit cell expansion, colors interact
    rows, cols = grid.shape
    r, c = start_pos
    new_pixels = []

    if r - 1 >= 0 and grid[r-1,c] == bg_color:
        new_pixels.append( ((r-1,c),color) )
    if r + 1 < rows and grid[r+1, c] == bg_color:
        new_pixels.append( ((r+1,c),color) )
    if c - 1 >= 0 and grid[r,c-1] == bg_color:
        new_pixels.append( ((r,c-1),color) )
    if c + 1 < cols and grid[r,c+1] == bg_color:
        new_pixels.append( ((r,c+1),color) )
    
    # color interaction when expanding to a pixel
    for (new_r,new_c),new_color in new_pixels:
        if grid[new_r,new_c] == bg_color:
           grid[new_r,new_c] = new_color
        elif grid[new_r, new_c] != new_color:
            # if the pixel where we want to write, is not background
            # color, and is different that the color we want to write
            # it seems that color 6 "wins" over color 1
            if new_color == 6:
                grid[new_r,new_c] = 6
            elif grid[new_r,new_c] == 6:
                grid[new_r,new_c] = 6

def shift_object(grid, non_background_pixels, background_color):
    # shift object up
    new_grid = np.full(grid.shape, background_color, dtype=grid.dtype)
    
    for (r,c), color in non_background_pixels:
        new_grid[0:r,c] = color
    
    return new_grid


def transform(input_grid):
    # Convert input_grid to numpy array
    input_grid = np.array(input_grid)

    # 1. Identify the Background
    background_color = get_background_color(input_grid)

    # 2. Identify Objects and their colors
    non_background_pixels = get_non_background_pixels(input_grid, background_color)
    unique_colors = set([color for _, color in non_background_pixels])
    object_locations = {}
    for (r,c), color in non_background_pixels:
        if color not in object_locations:
            object_locations[color] = []
        object_locations[color].append((r,c))

    # 3. Construct Output Grid (initialize with background)
    output_grid = np.full(input_grid.shape, background_color, dtype=input_grid.dtype)

    # Check for single object and single location for shifting
    if len(object_locations) == 1 and len(object_locations[list(object_locations.keys())[0]]) <= 2 :
         output_grid = shift_object(input_grid, non_background_pixels, background_color)
    else:
        # Multiple colors: cross-spiral expansion with color interaction
        # first copy initial object locations
        output_grid = np.copy(input_grid)
        
        prev_grid = np.copy(output_grid)
        current_grid = np.copy(output_grid)
        while True: # expand iteratively
            non_background_pixels = get_non_background_pixels(current_grid, background_color)
            for (r, c), color in non_background_pixels:
                expand_multi_color(current_grid, (r,c), color, background_color)
            if np.array_equal(current_grid, prev_grid):
                break;
            else:
                prev_grid = np.copy(current_grid)
        output_grid = np.copy(current_grid)
    return output_grid.tolist()