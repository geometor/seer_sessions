"""
1. **Identify the Central Region:** Find the largest, contiguous, centrally located block of a single color within the input grid. Note this color - it will act as the background color of the output grid.
2. **Determine the Secondary Color** There is one other constant color present in the output. Identify this value.
3. **Construct the Output Grid Shell:** Create an output grid. Its size is determined based on the central block from the Input Grid. It consists of a grid with alternating pixels, either in a checkerboard style or a cross style, of the two colors.
4. **Populate Output:** Fill in the output grid with the two colors alternating in the pattern selected from the input grid.
"""

import numpy as np

def find_largest_contiguous_block(grid):
    """Finds the largest contiguous block of the same color in a grid."""
    rows, cols = grid.shape
    visited = np.zeros((rows, cols), dtype=bool)
    max_size = 0
    max_color = -1
    max_block_coords = []

    def dfs(row, col, color, block_coords):
        """Depth-first search to explore contiguous block."""
        if (
            row < 0
            or row >= rows
            or col < 0
            or col >= cols
            or visited[row, col]
            or grid[row, col] != color
        ):
            return 0
        visited[row, col] = True
        block_coords.append((row, col))
        size = 1
        size += dfs(row + 1, col, color, block_coords)
        size += dfs(row - 1, col, color, block_coords)
        size += dfs(row, col + 1, color, block_coords)
        size += dfs(row, col - 1, color, block_coords)
        return size

    for r in range(rows):
        for c in range(cols):
            if not visited[r, c]:
                block_coords = []
                color = grid[r, c]
                size = dfs(r, c, color, block_coords)
                if size > max_size:
                    max_size = size
                    max_color = color
                    max_block_coords = block_coords

    return max_color, max_block_coords

def get_center_and_dimensions(coords):
     """Calculates the center and dimensions of a block given its coordinates"""
     if not coords:
          return (0,0), (0,0)
     
     rows = [r for r, _ in coords]
     cols = [c for _, c in coords]

     min_row, max_row = min(rows), max(rows)
     min_col, max_col = min(cols), max(cols)

     center_row = (min_row + max_row) // 2
     center_col = (min_col + max_col) // 2

     height = max_row - min_row + 1
     width = max_col - min_col + 1

     return (center_row, center_col), (height, width)



def get_output_grid_dimensions_and_pattern(input_grid, central_block_coords):
    """
    Determines the dimensions and pattern (checkerboard or cross) of output
    based on central region of input grid.
    """
    center, (h,w) = get_center_and_dimensions(central_block_coords)
    
    rows, cols = input_grid.shape

    # try and detect the repeating pattern in the output
    # examine around center

    patterns = []

    # sample 3x3 around the center pixel
    for r_offset in [-1,0,1]:
      for c_offset in [-1,0,1]:
        r = center[0] + r_offset
        c = center[1] + c_offset
        if 0 <= r < rows and 0 <= c < cols:
          patterns.append((r_offset,c_offset,input_grid[r,c]))

    
    unique_colors = sorted(list(set([c for _,_,c in patterns])))

    if len(unique_colors) != 2:
      # we have to assume there is some pattern so pick the most popular value as primary
      # and select the colors that way
      color_counts = {}
      for _, _, color in patterns:
        if color not in color_counts:
            color_counts[color] = 0
        color_counts[color] += 1
      primary_color = max(color_counts, key=color_counts.get)
      
      secondary_color = -1 # none
      for color in color_counts:
        if color != primary_color:
          secondary_color = color
          break
      if secondary_color == -1:
        secondary_color = primary_color # if no difference default the colors
      
      unique_colors = [primary_color, secondary_color]

    # check if its across
    center_color = input_grid[center[0], center[1]]
    cross = False
    if input_grid[center[0]-1, center[1]] == center_color and \
       input_grid[center[0]+1, center[1]] == center_color and \
       input_grid[center[0], center[1]-1] == center_color and \
       input_grid[center[0], center[1]+1] == center_color:
        
        cross = True

    # choose the smaller dimension as one side of output grid
    # if its odd, use exactly
    # otherwise add one
    output_size = min(h,w)
    if output_size % 2 == 0:
       output_size += 1 # ensure odd
       
    if cross:
      output_h = output_size
      output_w = 2 * output_size - (output_size % 2)
      if h < w:
         # rotate 90
         output_w, output_h = output_h, output_w
    else:
       output_h = output_size
       output_w = 3 * output_size - (2 * (output_size%2)) # make it wider to accomodate
    
    return (output_h, output_w), unique_colors, cross

def transform(input_grid):
    # Find the largest contiguous block and its color
    max_color, max_block_coords = find_largest_contiguous_block(input_grid)

    # Determine output grid dimensions and pattern type
    output_dims, output_colors, cross_pattern = get_output_grid_dimensions_and_pattern(input_grid, max_block_coords)
    
    # Initialize the output grid
    output_grid = np.zeros(output_dims, dtype=int)

    primary_color = output_colors[0]
    secondary_color = output_colors[1]
    
    # Populate based on pattern
    for r in range(output_dims[0]):
        for c in range(output_dims[1]):
          if cross_pattern:
             if r == output_dims[0] // 2 or c == output_dims[1] // 2:
                 output_grid[r,c] = secondary_color # center row or center col
             elif (r + c) % 2 == 0:
                output_grid[r, c] = primary_color
             else:
                output_grid[r, c] = secondary_color

          else: # checkerboard
            if (r + c) % 2 == 0:
                output_grid[r, c] = primary_color
            else:
                output_grid[r, c] = secondary_color

    return output_grid