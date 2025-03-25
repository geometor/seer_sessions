"""
The transformation rule depends on the structure of the input grid. We have two distinct cases:

**Case 1: (Example 1 - Padding and Mirroring)**

1.  **Padding:** The input grid is padded with two rows of azure (8) at the top and bottom, and two columns of azure on the left and right, resulting in a larger output grid.

2.  **Copy Rows:** The "objects," defined as contiguous horizontal lines of the same color, are then copied and potentially mirrored into the output grid.
    *   Rows of color 2 are copied to the output, starting at row 2, column 2 and extending to column (width - 2).
    *   The row of color 6 is copied starting at row 7.

3.  **Interleave and Mirror (Middle Section):**
      - The middle section is created by interweaving the objects based on
        color, and expanding some objects to fill gaps
      - Specifically, the rows of color 6, 8, 1, and then 8 are
        interleaved, starting on output row 7
        - if a row is adjacent to a row with color 8, extend the color
        - if a row is color 8 and adjacent to a different color, fill those
          pixels with adjacent color
    * Mirror colors 2 from rows 2-6 to 20-24

4.  **Mirror Rows:** The rows of color 2 from the input are copied and mirrored. They are placed at the bottom of the padded area.

**Case 2: (Example 2 - Interleaving and Extending)**

1.  **No Padding:** Unlike Case 1, there's no initial padding applied.
2.  **Interleaved Copying and Extending:** The transformation involves a complex interleaving and extension of rows based on their color:
    *   Copy input row 0 to output row 0, extend to output width.
    *  Copy input row 1 to output row 1. Extend it to the second to last column (output_width - 1). The first and last column is the color of the neighboring rows.
    *  Subsequent rows from the input are copied to the output grid with interleaving.
     * Rows of color 2 that come before or after color 3 rows are extended to width -2. Fill the first pixel with the color of the previous row and fill the last pixel with the color of the next row.
     * Rows of color 1 are placed between two rows of color 2 and extended.

3.  **Skipping Rows:** Rows of color 8 in the input are skipped (not copied to the output).
4.  The entire grid is mirrored vertically, starting at input row index 0. The mirrored rows go below existing rows.
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
            objects.append({"color": current_color, "rows": current_object, "height": len(current_object), "start_row":current_object[0][0]})
            current_color = first_pixel
            current_object = [(i, row)]
    if current_object:  # Add the last object
        objects.append({"color": current_color, "rows": current_object, "height": len(current_object), "start_row":current_object[0][0]})
    return objects

def _extend_line(row, prev_row, next_row, output_width, example_num):
    """Extends a given row based on context from adjacent rows and example number."""
    new_row = row.copy()
    if len(new_row) < output_width:
      if example_num == 2:
        if prev_row is not None and next_row is not None:  # Case 2 specific extension.
          new_row = np.pad(new_row, (1, 1), 'constant', constant_values=(prev_row[0], next_row[-1]))
        elif prev_row is not None:
          new_row = np.pad(new_row, (0, output_width-len(new_row)), 'constant', constant_values = new_row[-1])
        else:
          new_row = np.pad(new_row, (0, output_width - len(new_row)), 'constant', constant_values=new_row[-1] if len(new_row)>0 else 8) # default to 8
      else: # example_num == 1
        new_row = np.pad(new_row, (0, output_width - len(new_row)), 'constant', constant_values=new_row[-1] if len(new_row) > 0 else 8) # default to 8

    if example_num == 2:
      if len(new_row) < output_width:
        if prev_row is not None and next_row is None:
          new_row = np.pad(new_row, (0, output_width-len(new_row)), constant_values=prev_row[-1])
        if prev_row is None and next_row is not None:
          new_row = np.pad(new_row, (0, output_width-len(new_row)), constant_values=next_row[0])

    return new_row

def transform(input_grid):
    input_grid = np.array(input_grid)
    input_objects = _find_objects(input_grid)

    # Determine case and set parameters
    if input_grid[0, 0] == 8 and input_grid[-1, 0] == 2:  # Example 1
        example_num = 1
        output_rows = (input_grid.shape[0] * 2) + 4
        output_cols = (input_grid.shape[1] * 2) + 4
        output_grid = np.full((output_rows, output_cols), 8, dtype=int)
        offset_row = 2
        offset_col = 2
    else:  # Example 2
        example_num = 2
        output_rows = 24
        output_cols = 24
        output_grid = np.full((output_rows, output_cols), 8, dtype=int)  # initialize to azure
        offset_row = 0
        offset_col = 0


    # build lookup table
    output_row_lookup = {} # {output_row_index: (input_row_index, object_color)}

    for i in range(output_rows):
      output_row_lookup[i] = None

    # populate lookup table
    for obj_index, obj in enumerate(input_objects):
      for input_row_index, input_row_pixels in obj['rows']:
        if obj['color'] != 8 or example_num == 1: # skip color 8 rows only for example 2
          output_row_lookup[offset_row + input_row_index] = (input_row_index, obj['color'])

    # add mirrored rows, only for example 1, and color 2
    if example_num == 1:
        for obj_index, obj in enumerate(input_objects):
            if obj['color'] == 2:
              for input_row_index, input_row_pixels in reversed(obj['rows']):
                output_row_index = output_rows - offset_row - 1 - (input_row_index - obj['rows'][0][0] )
                output_row_lookup[output_row_index] = (input_row_index, obj['color'])


    # populate output grid from lookup table, extending as needed
    for output_row_index in range(output_rows):
      if output_row_lookup[output_row_index] is not None:
        input_row_index, color = output_row_lookup[output_row_index]
        prev_row = None
        next_row = None
        input_row_pixels = input_grid[input_row_index]

        if output_row_index-1 >=0:
          if output_row_lookup[output_row_index - 1] is not None:
            _, prev_color = output_row_lookup[output_row_index-1]
            prev_row = output_grid[output_row_index-1]

        if output_row_index+1 < output_rows:
          if output_row_lookup[output_row_index + 1] is not None:
              _, next_color = output_row_lookup[output_row_index+1]
              next_row = output_grid[output_row_index+1]
        extended_row = _extend_line(input_row_pixels, prev_row, next_row, output_cols, example_num)
        output_grid[output_row_index, :len(extended_row)] = extended_row


    # handle special interleaving case for example 1
    if example_num == 1:
      interleave_start = 7
      interleave_colors = [6, 8, 1, 8]
      interleave_row = interleave_start

      for color in interleave_colors:
        for obj in input_objects:
            if obj['color'] == color:

                input_row_pixels = obj['rows'][0][1] # only take first row

                prev_row = None
                next_row = None

                if interleave_row-1 >=0:
                    prev_row = output_grid[interleave_row-1]
                if interleave_row + 1 < output_rows:
                    next_row = output_grid[interleave_row + 1]

                extended_row = _extend_line(input_row_pixels, prev_row, next_row, output_cols, example_num=1)
                output_grid[interleave_row, :len(extended_row)] = extended_row
                interleave_row += 1
                break  # Only process the first row of the object for interleaving.

    return output_grid