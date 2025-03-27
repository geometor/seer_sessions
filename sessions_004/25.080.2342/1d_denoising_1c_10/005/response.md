```python
"""
Finds all contiguous blocks of non-zero pixels in a 1D grid. Identifies the
longest block(s) and sets all other non-zero pixels, not belonging to the
longest block(s) to zero. If there are multiple blocks with the same max
length, keep all such blocks.
"""

import numpy as np

def find_objects(grid):
    """Finds contiguous blocks of the same color (objects) in a 1D grid."""
    objects = []
    current_object = []
    for i, pixel in enumerate(grid):
        if pixel != 0:  # Consider only non-zero pixels as part of objects
            current_object.append((i, pixel))
        elif current_object:
            objects.append(current_object)
            current_object = []
    if current_object:  # Append the last object if it exists
        objects.append(current_object)
    return objects

def transform(input_grid):
    """Transforms the input grid according to the described rule."""

    # Initialize output grid with the same values as the input grid
    output_grid = np.copy(input_grid)
    
    # Find all contiguous blocks (objects)
    objects = find_objects(input_grid)

    # Find the maximum length of the blocks
    max_length = 0
    for obj in objects:
        max_length = max(max_length, len(obj))

    # Set pixels not belonging to the longest blocks to 0
    for i in range(len(input_grid)):
        is_part_of_longest = False
        for obj in objects:
            if len(obj) == max_length:
                for pos, _ in obj:
                    if i == pos:
                        is_part_of_longest = True
                        break
            if is_part_of_longest:
                break
        if input_grid[i] != 0 and not is_part_of_longest:
            output_grid[i] = 0

    return output_grid
```
