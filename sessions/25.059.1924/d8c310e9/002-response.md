# d8c310e9 • 002 • example_3 • investigate_coder

---
```python
"""
The transformation rule is:
1. Identify Objects: Find all contiguous, horizontally arranged, non-zero colored pixel sequences (objects) in the last row of the input grid.
2. Repeat Objects: For each object, repeat that *entire object* to the end of the output grid row. Ensure there is a padding of one or more 0s to avoid objects from merging into one another.
3. Maintain the sequence in which they appear.
4. Keep the upper rows as it is.
"""

import numpy as np

def find_objects(row):
    # Find contiguous non-zero sequences in a row
    objects = []
    current_object = []
    for pixel in row:
        if pixel != 0:
            current_object.append(pixel)
        elif current_object:
            objects.append(current_object)
            current_object = []
    if current_object:  # Append the last object if it exists
        objects.append(current_object)
    return objects

def transform(input_grid):
    """Transforms the input grid according to the described rule."""
    input_grid = np.array(input_grid)
    output_grid = np.copy(input_grid)
    height, width = input_grid.shape

    # 1. Identify Objects in the last row
    last_row = input_grid[-1]
    objects = find_objects(last_row)

    # 2. & 3. Repeat Objects horizontally, preserving order
    output_row = []
    
    # build the repeated last row object by object, adding a 0 between each
    current_pos = 0
    while current_pos < width:
      for obj in objects:
        if current_pos + len(obj) <= width:
            output_row.extend(obj)
            current_pos += len(obj)
          
            #add zero padding but only if there is room for another obj
            if current_pos < width:
              output_row.append(0)
              current_pos += 1
        else:
          break
          
    #pad remaining with 0
    while current_pos < width:
        output_row.append(0)
        current_pos+=1

    output_grid[-1] = output_row

    return output_grid.tolist()
```
