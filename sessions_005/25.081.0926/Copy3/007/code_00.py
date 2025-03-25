"""
The transformation rule involves identifying "seed" objects (contiguous blocks of the same non-zero color)
within each row of the input grid.  The transformation then proceeds row by row. If a row contains
seed objects, it may undergo insertions of single pixels or sequences of pixels, based on the
properties of these seed objects (color, position).  If a row does *not* contain a seed object,
it checks the row two positions above. If that row has a non-zero pixel, a copy of that pixel is
inserted into the current row.
"""

import numpy as np

def find_objects(row):
    """Finds contiguous objects (same-color blocks) in a row."""
    objects = []
    if not row.any():  # All zeros, no objects
        return objects

    start = -1
    for i, pixel in enumerate(row):
        if pixel != 0:
            if start == -1:
                start = i
        elif start != -1:
            objects.append({
                "color": row[start],
                "col_start": start,
                "col_end": i - 1,
                "length": i - start
            })
            start = -1
    # Handle object at the end of the row
    if start != -1:
        objects.append({
            "color": row[start],
            "col_start": start,
            "col_end": len(row) - 1,
            "length": len(row) - start
        })
    return objects

def transform(input_grid):
    """Transforms the input grid according to the identified rule."""
    input_grid = np.array(input_grid)
    rows, cols = input_grid.shape
    output_grid = np.copy(input_grid)  # Start with a copy

    for r in range(rows):
        input_row = input_grid[r]
        objects = find_objects(input_row)
        new_row = []

        if objects:  # Row contains seed objects
            
            # first pass - find the objects
            for obj in objects:
                new_row.extend([obj['color']] * obj['length'])
                # insert blocks
                if obj['length'] > 1: # multiple elements
                    for i in range(obj["length"]):
                        new_row.extend([obj['color']] * obj['length'])

                # copy whole sequences of same color
                if obj['color'] == input_row[obj['col_start']]:
                    # check for sequence insertions
                    for other_obj in objects:
                        if other_obj['col_start'] > obj['col_end']: # object starts later in row
                            # look at position before object
                            if obj['col_end'] + 1 == other_obj['col_start']:
                                new_row.extend([other_obj['color']] * other_obj['length'])
            # second pass - fill in any gaps
            final_row = []
            in_idx = 0
            for i in range(len(new_row)):
                final_row.append(new_row[i])
                if i < len(input_row) and in_idx < len(input_row) and new_row[i] == input_row[in_idx]:
                    in_idx += 1
                elif i < len(input_row) and in_idx < len(input_row) :
                    # find any gaps
                    obj_in_row = False
                    for o in objects:
                        if o['col_start'] <= in_idx and o['col_end'] >= in_idx:
                            obj_in_row = True

                    if not obj_in_row:
                        #print("found gap", r, in_idx)
                        # look for objects to insert
                        for o in objects:
                            if o['col_end'] < in_idx:
                                # check for adjacent pixels
                                #print("checking gap", r, o['col_end'], in_idx, input_row[o['col_end'] + 1])
                                if o['col_end'] + 1 < len(input_row):
                                    next_obj = find_objects(input_row[o['col_end'] + 1 :])[0]
                                    final_row.extend([next_obj['color']] * next_obj['length'])


            output_grid[r] = np.array(final_row[:cols])

        else:  # Row does not contain seed objects, check two rows above
            if r >= 2:
                row_above = input_grid[r - 2]
                objects_above = find_objects(row_above)
                # find objects and insert single unit below
                for obj in objects_above:
                    # insert single element below
                    output_grid[r-1, obj['col_start'] : obj['col_end']+1] = obj['color']

    return output_grid.tolist()