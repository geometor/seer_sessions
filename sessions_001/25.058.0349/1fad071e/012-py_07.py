"""
The output is a 1xN grid, where N is the number of columns in the input grid. Each cell in the
output grid corresponds to a column in the input grid. An output cell is blue (1) if the
corresponding input column contains a contiguous blue object with an area of 2 or greater.
Otherwise, the output cell is white (0).
"""

import numpy as np
from skimage.measure import label, regionprops

def get_blue_objects(grid):
    """
    Identifies contiguous blue regions in a grid and returns their properties.
    """
    grid = np.array(grid)
    blue_mask = (grid == 1)
    labeled_mask = label(blue_mask)
    regions = regionprops(labeled_mask)

    object_data = []
    for region in regions:
        object_data.append({
            'area': region.area,
            'bbox': region.bbox,  # (min_row, min_col, max_row, max_col)
        })
    return object_data

def transform(input_grid):
    """
    Transforms the input grid based on the presence of the largest blue object in each column.
    """
    input_grid = np.array(input_grid)
    num_cols = input_grid.shape[1]
    output_grid = [0] * num_cols  # Initialize output as a list of zeros

    # Get blue objects and their properties
    blue_objects = get_blue_objects(input_grid)

    # Iterate through each column
    for j in range(num_cols):
        # Find blue objects in the current column
        objects_in_column = [obj for obj in blue_objects if obj['bbox'][1] <= j < obj['bbox'][3]]

        # If there are blue objects in the column
        if objects_in_column:
            # Find the largest area
            max_area = max(obj['area'] for obj in objects_in_column)
            
            # Check if the area is greater than or equal to 2
            if max_area >= 2:
                output_grid[j] = 1  # Set output to blue (1)

    return output_grid