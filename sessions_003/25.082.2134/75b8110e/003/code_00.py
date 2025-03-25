"""
The transformation identifies pixels of colors 4, 6, 5, and 9 in the input grid. Colors 4 and 5 are considered "source" colors, while 6 and 9 are their corresponding "target" colors. The transformation swaps the positions of the source and target colors within each pair (4 with 6, and 5 with 9) and arranges them into a condensed output grid, preserving the relative row and column order of the source pixels.
"""

import numpy as np

def find_pixels(grid, colors):
    # Find coordinates of specified colors
    pixels = {color: [] for color in colors}
    rows, cols = grid.shape
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] in colors:
                pixels[grid[r, c]].append((r, c))
    return pixels

def transform(input_grid):
    # Convert input to numpy array
    grid = np.array(input_grid)

    # Find source and target pixels
    pixels = find_pixels(grid, [4, 6, 5, 9])
    source_pixels = pixels[4] + pixels[5]
    source_pixels.sort() # sort source pixels by row then column

    # Determine output grid size based on the number of source/target pixels
    num_pixels = len(pixels[4]) + len(pixels[6]) + len(pixels[5]) + len(pixels[9])
    
    if num_pixels == 0: # if no source or target colors, return an empty grid
        return []
    
    
    width = 0
    for r, c in pixels[4] + pixels[5]:
        width = max(width, c+1)
    
    width = max(width, len(source_pixels)) # columns
    height = int(num_pixels / width) # rows
    if num_pixels % width != 0:
      height +=1
    
    

    # Initialize output grid with zeros
    output_grid = np.zeros((height, width), dtype=int)

    # Populate output grid with swapped pairs
    
    i = 0
    for r,c in source_pixels:
        
        if grid[r,c] == 4: # swap 4 with 6
            if i < len(pixels[6]):
                target_r, target_c = pixels[6][i]
                output_grid[i//width, i%width] = 6
        elif grid[r,c] == 5: # swap 5 with 9
            if i < len(pixels[9]):
                target_r, target_c = pixels[9][i]
                output_grid[i//width, i%width] = 9
        i+=1
        
    i = 0
    for r,c in source_pixels:
        if grid[r,c] == 4:
            if i < len(pixels[6]):
              output_grid[ (len(pixels[6]) + i)//width, (len(pixels[6]) + i)%width ] = 4
        elif grid[r,c] == 5:
            if i < len(pixels[9]):
                output_grid[ (len(pixels[9]) + i)//width, (len(pixels[9]) + i)%width] = 5
        i+=1
        
    

    return output_grid.tolist()