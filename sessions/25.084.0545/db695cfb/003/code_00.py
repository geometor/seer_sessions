"""
1.  **Identify Background:** Find the most frequent color in the input grid. This is the background color.

2.  **Identify Objects:** Locate all pixels that *do not* have the background color. These pixels form one or more objects.

3.  **Object Color Count:** Determine the number of distinct colors present in these non-background pixels.

4. **Determine the expansion rule**:

    *   **Single Non-Background Color:** If there's only one non-background color, each object expands diagonally.  Each pixel of that color in the object shifts one position up and one position right, repeatedly.
    *    **Multiple Non-Background Colors:** If there are two or more non-background colors, the colors expand in a cross-spiral pattern:
        - Find the pixels with a non-background color.
        - From each non-background pixel expand up, down, left and right by one cell, with each step.
        - Repeat the expansion using the newly expanded pixels, until no new pixels can be filled in this way.
        - Note that colors appear to interact.

5.  **Construct Output Grid:** Create a new grid with the same dimensions as the input grid, initially filled with the background color.

6.  **Apply Expansion:** Apply the determined expansion rule.

7.  **Color Interaction**: If multiple non-background color pixels meet, one takes the place of the other (exact rule for replacement to be determined)

8.  **Populate Output:** Place the expanded objects (with possibly modified colors) onto the output grid.
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

def expand_single_color(grid, start_pos, color):
    # Diagonal expansion for single color
    rows, cols = grid.shape
    r, c = start_pos
    while r < rows and c < cols:
        grid[r, c] = color
        r += 1
        c += 1

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
                
            

def transform(input_grid):
    # Convert input_grid to numpy array
    input_grid = np.array(input_grid)

    # 1. Identify the Background
    background_color = get_background_color(input_grid)

    # 2. Identify Objects and their colors
    non_background_pixels = get_non_background_pixels(input_grid, background_color)
    unique_colors = set([color for _, color in non_background_pixels])

    # 3. Construct Output Grid (initialize with background)
    output_grid = np.full(input_grid.shape, background_color, dtype=input_grid.dtype)

    # 4. Apply Expansion
    if len(unique_colors) == 1:
        # Single color: diagonal expansion
        for (r, c), color in non_background_pixels:
            expand_single_color(output_grid, (r, c), color)
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