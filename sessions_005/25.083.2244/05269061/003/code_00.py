"""
The transformation identifies a core pattern within the input grid and replicates it both horizontally and vertically to fill the output grid. The core pattern is the smallest repeating sequence of numbers, that can reconstruct the input when replicated. The position of zeros matters.
"""

import numpy as np

def get_core_pattern(grid):
    """Extracts the core pattern of non-zero values from the input grid."""
    rows, cols = grid.shape
    grid_flat = grid.flatten()
    non_zero_indices = np.where(grid_flat != 0)[0]

    if not non_zero_indices.size:  # Handle the case where the input is all zeros
         return []
    
    first_non_zero_index = non_zero_indices[0]
    
    # Initialize pattern starting from the first non_zero element
    pattern = [grid_flat[first_non_zero_index]]
    
    for length in range(1, len(non_zero_indices) +1 ):
        pattern = grid_flat[non_zero_indices[0]:non_zero_indices[0]+length]

        valid_pattern = True
        
        for start in range(len(non_zero_indices)):
          
          projected_pattern_index = start % len(pattern)
            
          if grid_flat[non_zero_indices[start]] != pattern[projected_pattern_index]:
              valid_pattern = False
              break
        
        if valid_pattern:
            return pattern.tolist()


    return pattern #should not reach here
    

def transform(input_grid):
    """Transforms the input grid according to the observed rule."""
    input_grid = np.array(input_grid)
    rows, cols = input_grid.shape
    output_grid = np.zeros_like(input_grid)
    
    # 1. Identify the Core Pattern
    core_pattern = get_core_pattern(input_grid)
    pattern_len = len(core_pattern)

    if not core_pattern:   #if empty return empty grid
        return output_grid.tolist()

    # 2. Expand Horizontally and 3. Expand Vertically
    pattern_index = 0
    for r in range(rows):
        for c in range(cols):
            output_grid[r,c] = core_pattern[pattern_index % pattern_len]
            pattern_index += 1

    return output_grid.tolist()