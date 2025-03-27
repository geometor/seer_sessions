"""
Transforms an input grid by identifying a single "target" pixel (the non-dominant color) and replacing pixels of the dominant color with '1's, extending outwards from the target pixel to the edges of the grid in all orthogonal directions.
"""

import numpy as np

def find_target_pixel(grid):
    # Find the dominant color
    unique_colors, counts = np.unique(grid, return_counts=True)
    dominant_color_index = np.argmax(counts)
    dominant_color = unique_colors[dominant_color_index]

    # Find the target pixel (non-dominant color)
    rows, cols = grid.shape
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] != dominant_color:
                return (r, c), dominant_color # Return target coordinates and dominant color

    return None, dominant_color #should not happen, based on task definition

def transform(input_grid):
    # Initialize output grid
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # Find target
    target_coords, dominant_color = find_target_pixel(input_grid)

    if target_coords is None:
       return output_grid #should not happen

    target_row, target_col = target_coords

    # Extend Up
    for r in range(target_row -1, -1, -1):
        if output_grid[r, target_col] == dominant_color:
            output_grid[r, target_col] = 1
        else:
            break

    # Extend Down
    for r in range(target_row + 1, rows):
        if output_grid[r, target_col] == dominant_color:
            output_grid[r, target_col] = 1
        else:
            break

    # Extend Left
    for c in range(target_col - 1, -1, -1):
        if output_grid[target_row, c] == dominant_color:
             output_grid[target_row, c] = 1
        else:
            break

    # Extend Right
    for c in range(target_col + 1, cols):
        if output_grid[target_row, c] == dominant_color:
            output_grid[target_row, c] = 1
        else:
            break

    # Extend Up-Left - we can stop at edges
    r, c = target_row, target_col
    while r>0 and c>0:
      r -= 1
      c -= 1
      if output_grid[r,c] == dominant_color:
        output_grid[r,c] = 1
      else:
        break    

    # Extend Up-Right - we can stop at edges
    r, c = target_row, target_col
    while r>0 and c<cols-1:
      r -= 1
      c += 1
      if output_grid[r,c] == dominant_color:
        output_grid[r,c] = 1
      else:
        break

    # Extend Down-Left - we can stop at edges
    r, c = target_row, target_col
    while r<rows-1 and c>0:
      r += 1
      c -= 1
      if output_grid[r,c] == dominant_color:
        output_grid[r,c] = 1
      else:
        break

    # Extend Down-Right - we can stop at edges
    r, c = target_row, target_col
    while r<rows-1 and c<cols-1:
      r += 1
      c += 1
      if output_grid[r,c] == dominant_color:
        output_grid[r,c] = 1
      else:
        break

    # now find the boundaries in each of the four directions and fill
    # Extend Up
    for r in range(target_row -1, -1, -1):
        if output_grid[r, target_col] != 1:
          break;
        # now we've reach the limit in this direction - fill the diagonals
        for d in range(1,target_col+1): #left
          if target_col-d >= 0:
            if output_grid[r,target_col-d] == dominant_color:
              output_grid[r,target_col-d] = 1
        for d in range(1,cols-target_col): #left
          if target_col+d < cols:
            if output_grid[r,target_col+d] == dominant_color:
              output_grid[r,target_col+d] = 1

    # Extend Down
    for r in range(target_row + 1, rows):
        if output_grid[r, target_col] != 1:
          break;
        # now we've reach the limit in this direction - fill the diagonals
        for d in range(1,target_col+1): #left
          if target_col-d >= 0:
            if output_grid[r,target_col-d] == dominant_color:
              output_grid[r,target_col-d] = 1
        for d in range(1,cols-target_col): #left
          if target_col+d < cols:
            if output_grid[r,target_col+d] == dominant_color:
              output_grid[r,target_col+d] = 1
    
    # Extend Left
    for c in range(target_col - 1, -1, -1):
        if output_grid[target_row, c] != 1:
          break;
        # now we've reach the limit in this direction - fill the diagonals
        for d in range(1,target_row+1): #up
          if target_row-d >= 0:
            if output_grid[target_row-d,c] == dominant_color:
              output_grid[target_row-d,c] = 1
        for d in range(1,rows-target_row): #down
          if target_row+d < rows:
            if output_grid[target_row+d,c] == dominant_color:
              output_grid[target_row+d,c] = 1

    # Extend Right
    for c in range(target_col + 1, cols):
        if output_grid[target_row, c] != 1:
          break;
        # now we've reach the limit in this direction - fill the diagonals
        for d in range(1,target_row+1): #up
          if target_row-d >= 0:
            if output_grid[target_row-d,c] == dominant_color:
              output_grid[target_row-d,c] = 1
        for d in range(1,rows-target_row): #down
          if target_row+d < rows:
            if output_grid[target_row+d,c] == dominant_color:
              output_grid[target_row+d,c] = 1

    return output_grid