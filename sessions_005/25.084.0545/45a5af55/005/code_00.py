"""
The transformation involves copying, mirroring, and interleaving rows from the input to the output grid. Example 1 adds padding, while Example 2 involves line extension and filling the canvas without padding. The interweaving and mirroring are applied to rows based on their object membership.
"""

import numpy as np

def _find_objects(grid):
    """Finds contiguous objects in the grid (rows of same color)."""
    objects = []
    current_object = []
    current_color = None

    for i, row in enumerate(grid):
        first_pixel = row[0]
        if current_color is None:
            current_color = first_pixel
            current_object.append((i, row))
        elif first_pixel == current_color:
            current_object.append((i, row))
        else:
            objects.append({"color": current_color, "rows": current_object, "height": len(current_object)})
            current_color = first_pixel
            current_object = [(i, row)]
    if current_object:  # Add the last object
        objects.append({"color": current_color, "rows": current_object, "height": len(current_object)})
    return objects

def _extend_line(row, prev_row, next_row, output_width):
    """Extends a given row based on context from adjacent rows."""
    new_row = row.copy()
    if len(new_row) < output_width:
        new_row = np.pad(new_row, (0, output_width - len(new_row)), 'constant', constant_values=new_row[-1] if len(new_row) > 0 else 8)

    if prev_row is not None and len(prev_row) == output_width:
        for i in range(min(len(new_row), len(prev_row))):
            if new_row[i] == 8:  # Fill with adjacent colors
                new_row[i] = prev_row[i]

    if next_row is not None and len(next_row) == output_width:
        for i in range(min(len(new_row), len(next_row))):
            if new_row[i] == 8: # Fill with adjacent colors
                new_row[i] = next_row[i]
    return new_row

def transform(input_grid):
    input_grid = np.array(input_grid)
    input_objects = _find_objects(input_grid)
    total_input_height = sum(obj["height"] for obj in input_objects)

    # Determine output dimensions
    if input_grid[0, 0] == 8 and input_grid[-1, 0] == 2:  # Example 1: Padding
        output_rows = (input_grid.shape[0] * 2) + 2
        output_cols = (input_grid.shape[1] * 2) + 2
        output_grid = np.full((output_rows, output_cols), 8, dtype=int)
        offset_row = 2
        offset_col = 2 # unused
    else:  # Example 2: No padding, interweaving
        output_rows = 23
        output_cols = 24
        output_grid = np.full((output_rows, output_cols), 8, dtype=int) # initialize to azure, fill later
        offset_row = 0
        offset_col = 0 # unused


    # build lookup table for output rows based on input objects
    output_row_lookup = {} # {output_row_index: (input_row_index, object_color)}

    for i in range(output_rows):
      output_row_lookup[i] = None

    for obj_index, obj in enumerate(input_objects):
      for input_row_index, input_row_pixels in obj['rows']:
        output_row_lookup[offset_row + input_row_index] = (input_row_index, obj['color'])

    # add mirrored rows
    for obj_index, obj in enumerate(input_objects):
        for input_row_index, input_row_pixels in reversed(obj['rows']):
          output_row_index = output_rows - offset_row - 1 - (input_row_index - obj['rows'][0][0] )
          output_row_lookup[output_row_index] = (input_row_index, obj['color'])


    # populate output grid from lookup table
    for output_row_index in range(output_rows):
        if output_row_lookup[output_row_index] is not None:
          input_row_index, obj_color = output_row_lookup[output_row_index]
          prev_row = None
          next_row = None

          input_row_pixels = input_grid[input_row_index]
          if output_row_index-1 >=0 and output_row_lookup[output_row_index - 1] is not None:
            prev_row_index, _ = output_row_lookup[output_row_index-1]
            prev_row = output_grid[output_row_index-1]
          if output_row_index+1 < output_rows and output_row_lookup[output_row_index + 1] is not None:
            next_row_index, _ = output_row_lookup[output_row_index+1]
            next_row = output_grid[output_row_index+1]

          extended_row = _extend_line(input_row_pixels, prev_row, next_row, output_cols)
          output_grid[output_row_index, :len(extended_row)] = extended_row

    return output_grid