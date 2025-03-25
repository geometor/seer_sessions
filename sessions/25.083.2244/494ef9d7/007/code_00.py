"""
The transformation rule involves potentially swapping two non-zero pixels within each row of the input grid. A swap occurs only if a row contains exactly two non-zero pixels, and, after sorting these two pixels by their column indices, the value of the first pixel is greater than the value of the second pixel. Rows with zero, one, or more than two non-zero pixels are copied to the output without modification.
"""

import numpy as np

def find_objects(grid):
    """Finds non-zero pixels and their positions in a grid."""
    objects = []
    for row_index, row in enumerate(grid):
        for col_index, pixel in enumerate(row):
            if pixel != 0:
                objects.append({'value': pixel, 'row': row_index, 'col': col_index})
    return objects

def transform(input_grid):
    """Transforms the input grid according to the observed rule."""

    # Initialize output grid with the same dimensions and filled with zeros
    output_grid = np.zeros_like(input_grid)
    
    #Copy input grid to the output grid
    output_grid[:] = input_grid[:]

    # Find objects in the input grid
    objects = find_objects(input_grid)

    # Iterate through rows
    for row_index in range(input_grid.shape[0]):
        row_objects = [obj for obj in objects if obj['row'] == row_index]

        #If only 0 or 1 object is in that row, continue
        if len(row_objects) < 2:
          continue
        elif len(row_objects) > 2:
          continue
        else:
            #Sort objects by column
            row_objects.sort(key=lambda obj: obj['col'])
            
            #Swap two objects if first object value is greater than the second
            obj1 = row_objects[0]
            obj2 = row_objects[1]
            if obj1['value'] > obj2['value']:
              output_grid[obj1['row']][obj1['col']], output_grid[obj2['row']][obj2['col']] = output_grid[obj2['row']][obj2['col']], output_grid[obj1['row']][obj1['col']]

    return output_grid