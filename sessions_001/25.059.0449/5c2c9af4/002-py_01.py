"""
1. **Identify key pixels:** Find all non-white pixels, these are the seeds
2. **Grow L shapes:** For each seed, grow an "L" shape of the same color.
3. **Combine:** Where two L shapes would intersect, combine them, creating longer
   lines or spirals.
"""

import numpy as np

def get_seeds(grid):
    """Finds the coordinates of all non-white pixels."""
    seeds = []
    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            if grid[r, c] != 0:
                seeds.append((r, c, grid[r,c]))
    return seeds

def grow_l_shape(grid, seed, max_attempts=100):
   
    output_grid = np.zeros_like(grid)
    r, c, color = seed
    output_grid[r, c] = color

    
    # Define possible L-shape directions (dr, dc) for each orientation
    l_shapes = [
      ( (0, 1), (1, 0) ), # original
      ( (0, -1), (1, 0) ), # flip on y
      ( (0, 1), (-1, 0) ), # flip on x
      ( (0, -1), (-1, 0) ),  # 180 flip      
      ( (1, 0), (0, 1) ),
      ( (-1, 0), (0, 1) ),      
      ( (1, 0), (0, -1) ),
      ( (-1, 0), (0, -1) )
    ]
    
    for _ in range(max_attempts): #Limit expansion
        
        # choose random directions
        np.random.shuffle(l_shapes)        
        
        for directions in l_shapes:           
            
            valid_move = True
            temp_grid = output_grid.copy()
            
            # grow a single L
            curr_r, curr_c = r, c
            for dr, dc in directions:                                
                
                for i in range(1, 10):
                  next_r, next_c = curr_r + dr*i, curr_c + dc*i
                  
                  if (0 <= next_r < temp_grid.shape[0] and
                      0 <= next_c < temp_grid.shape[1] ):
                      
                      # check for collisions with other colors
                      if temp_grid[next_r, next_c] != 0 and temp_grid[next_r, next_c] != color:
                        valid_move = False
                        break
                      else:
                          temp_grid[next_r, next_c] = color # mark for expansion
                  else:
                      valid_move = False # moved out of bounds
                      break

                if valid_move == False:
                  break

            if valid_move:          
                output_grid = temp_grid # Update the actual grid if move successful
            
    return output_grid
    
def combine_grids(grid1, grid2):
    """Combines two grids, prioritizing non-zero pixels from grid2."""
    combined_grid = grid1.copy()
    for r in range(grid1.shape[0]):
        for c in range(grid1.shape[1]):
            if grid2[r, c] != 0:
                combined_grid[r, c] = grid2[r, c]
    return combined_grid

def transform(input_grid):
    """Transforms the input grid according to the described rule."""

    # 1. Identify key pixels (seeds)
    seeds = get_seeds(input_grid)

    # Initialize output grid as all white
    output_grid = np.zeros_like(input_grid)

    # 2. & 3. Grow L shapes and combine
    for seed in seeds:
      l_grid = grow_l_shape(input_grid, seed)      
      output_grid = combine_grids(output_grid, l_grid)

    return output_grid