"""
The transformation takes a seed sequence of non-zero numbers from the input grid and replicates it both horizontally and vertically to fill the entire output grid, replacing the initial zeros in the process. The replication maintains the order and arrangement of the seed sequence.
"""

import numpy as np

def get_core_pattern(grid):
    """Extracts the core pattern of non-zero values from the input grid."""
    rows, cols = grid.shape
    pattern = []
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] != 0:
                pattern.append(grid[r, c])
            if grid[r,c] != 0 and (c+1 >= cols or grid[r,c+1] == 0):
                return pattern

    return pattern
    

def transform(input_grid):
    """Transforms the input grid according to the observed rule."""
    input_grid = np.array(input_grid)
    rows, cols = input_grid.shape
    output_grid = np.zeros_like(input_grid)
    
    # 1. Identify the Core Pattern
    core_pattern = get_core_pattern(input_grid)
    #print(f"Core pattern: {core_pattern}")
    pattern_len = len(core_pattern)

    # 2. Expand Horizontally and 3. Expand Vertically
    pattern_index = 0
    for r in range(rows):
        for c in range(cols):
            output_grid[r,c] = core_pattern[pattern_index % pattern_len]
            pattern_index +=1

    return output_grid.tolist()