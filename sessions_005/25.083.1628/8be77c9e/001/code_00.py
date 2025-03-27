"""
The input grid is duplicated, and then the duplicate is vertically reflected. The output grid is a combination of the original input grid and its reflected duplicate.
"""

import numpy as np

def reflect_rows(grid):
    """Reflects the rows of a grid."""
    return np.flipud(grid)

def transform(input_grid):
    """Transforms the input grid by duplicating and reflecting it vertically."""
    # Convert input_grid to numpy array
    input_np = np.array(input_grid)

    # Duplicate the input grid
    duplicated_grid = np.copy(input_np)

    # Reflect the duplicated grid
    reflected_grid = reflect_rows(duplicated_grid)
    
    # Combine the original and reflected grids vertically
    output_grid = np.concatenate((input_np, reflected_grid), axis=0)

    return output_grid.tolist()