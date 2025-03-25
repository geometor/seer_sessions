"""
The transformation identifies the smallest repeating unit of columns within the input grid. This unit is then extracted and presented as the output grid. The repeating unit is determined by finding the smallest number of columns that consistently repeats across the input grid. The output grid represents a single instance of the repeating pattern.
"""

import numpy as np

def find_repeating_unit(grid):
    """Finds the smallest repeating unit of columns in a grid."""
    grid = np.array(grid)
    num_cols = grid.shape[1]
    
    for unit_width in range(1, num_cols + 1):
        # Check if the grid can be divided into units of this width
        if num_cols % unit_width == 0:
            unit = grid[:, :unit_width]
            repeats = num_cols // unit_width

            # build full_sequence that we think input is
            valid_unit = True
            for i in range(1,repeats):
                if not np.array_equal(unit, grid[:, i*unit_width:(i+1)*unit_width]):
                    valid_unit = False
                    break
            
            if valid_unit:
                return unit

    return grid  # Return original grid if not repeating.

def transform(input_grid):
    """
    Transforms the input grid by extracting the smallest repeating unit of columns.
    """
    # Find the repeating unit of columns.
    repeating_unit = find_repeating_unit(input_grid)

    # The output grid is the repeating unit.
    output_grid = repeating_unit.tolist()

    return output_grid