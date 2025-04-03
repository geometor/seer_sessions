
## train_1

**input:**
```
0 0 0 0 0 4 5 5 5 5 5 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 5 5 5 5 5 4 0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 0 0 1 2 2 2 2 2 2 2 0 0 0 0 0
```


**output:**
```
0 0 0 0 2 2 2 2 2 2 2 1 0 0 0 0 0
```


## train_3

**input:**
```
0 0 5 3 3 3 3 3 3 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 3 3 3 3 3 3 5 0 0 0 0 0 0 0 0
```

*   **Perception:**
    The input and output are 1D grids (or 1xN arrays). Each input contains a sequence of pixels, mostly white (0), but also includes two distinct non-white objects placed adjacent to each other. One object is always a single pixel of one color, and the other object is a contiguous block of pixels of another color. The output grid is identical to the input grid, except that the positions of the single non-white pixel and the adjacent block of non-white pixels are swapped. The white background pixels remain unchanged.

*   **Facts:**
    
```yaml
    examples:
      train_1:
        input: [0, 0, 0, 0, 0, 4, 5, 5, 5, 5, 5, 0, 0, 0, 0, 0, 0] # 1x17 grid
        output: [0, 0, 0, 0, 0, 5, 5, 5, 5, 5, 4, 0, 0, 0, 0, 0, 0] # 1x17 grid
        objects_input:
          - color: 4 (yellow)
            pixels: [[0, 5]] # (row, col) assuming 1 row
            shape: single pixel
          - color: 5 (gray)
            pixels: [[0, 6], [0, 7], [0, 8], [0, 9], [0, 10]]
            shape: horizontal block (length 5)
        relationship: The yellow pixel is immediately to the left of the gray block.
        action: Swap the positions of the yellow pixel and the gray block.
      train_2:
        input: [0, 0, 0, 0, 1, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0] # 1x17 grid
        output: [0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 1, 0, 0, 0, 0, 0] # 1x17 grid
        objects_input:
          - color: 1 (blue)
            pixels: [[0, 4]]
            shape: single pixel
          - color: 2 (red)
            pixels: [[0, 5], [0, 6], [0, 7], [0, 8], [0, 9], [0, 10], [0, 11]]
            shape: horizontal block (length 7)
        relationship: The blue pixel is immediately to the left of the red block.
        action: Swap the positions of the blue pixel and the red block.
      train_3:
        input: [0, 0, 5, 3, 3, 3, 3, 3, 3, 0, 0, 0, 0, 0, 0, 0, 0] # 1x17 grid
        output: [0, 0, 3, 3, 3, 3, 3, 3, 5, 0, 0, 0, 0, 0, 0, 0, 0] # 1x17 grid
        objects_input:
          - color: 5 (gray)
            pixels: [[0, 2]]
            shape: single pixel
          - color: 3 (green)
            pixels: [[0, 3], [0, 4], [0, 5], [0, 6], [0, 7], [0, 8]]
            shape: horizontal block (length 6)
        relationship: The gray pixel is immediately to the left of the green block.
        action: Swap the positions of the gray pixel and the green block.
    grid_properties:
      dimensionality: 1D (or 1xN 2D)
      background_color: 0 (white)
      transformation_type: object rearrangement
    object_properties:
      - Two non-background objects per grid.
      - Objects are contiguous blocks of a single color.
      - One object is always a single pixel.
      - The other object is a block of one or more pixels.
      - The two objects are always adjacent.
    ```


*   **Natural Language Program:**
    1.  Initialize the output grid as a copy of the input grid.
    2.  Iterate through the input grid to find the start and end indices of all contiguous blocks of non-white (non-zero) pixels. Store these blocks along with their colors and pixel indices.
    3.  Identify the two adjacent non-white blocks. Let Block A be the block that appears first (leftmost) and Block B be the block that appears second (rightmost).
    4.  Determine the pixel indices occupied by Block A and Block B.
    5.  In the output grid, place the pixels corresponding to Block B into the indices originally occupied by Block A.
    6.  In the output grid, place the pixels corresponding to Block A into the indices originally occupied by Block B.
    7.  Return the modified output grid.
```python
import numpy as np
from typing import List, Dict, Tuple

"""
Identifies two adjacent, non-background colored objects in a 1D grid. 
One object is a single pixel, and the other is a contiguous block.
The transformation swaps the positions of these two objects while preserving 
the background.
"""

def find_contiguous_objects(grid: List[int]) -> List[Dict]:
    """
    Finds all contiguous blocks of non-background (non-zero) pixels.

    Args:
        grid: A list of integers representing the 1D grid.

    Returns:
        A list of dictionaries, where each dictionary represents an object
        with keys 'color', 'start' (index), 'end' (index), and 'len'.
    """
    objects = []
    current_object = None
    for i, pixel in enumerate(grid):
        if pixel != 0:
            # Non-background pixel found
            if current_object is None:
                # Start of a new object
                current_object = {'color': pixel, 'start': i, 'count': 1}
            elif pixel == current_object['color']:
                # Continuation of the current object
                current_object['count'] += 1
            else:
                # Different color, end the previous object and start a new one
                current_object['end'] = i - 1
                current_object['len'] = current_object['end'] - current_object['start'] + 1
                # sanity check count vs len
                # assert current_object['len'] == current_object['count']
                objects.append(current_object)
                current_object = {'color': pixel, 'start': i, 'count': 1}
        else:
            # Background pixel found
            if current_object is not None:
                # End of the current object
                current_object['end'] = i - 1
                current_object['len'] = current_object['end'] - current_object['start'] + 1
                # assert current_object['len'] == current_object['count']
                objects.append(current_object)
                current_object = None # Reset

    # If the last pixel was part of an object, add it
    if current_object is not None:
        current_object['end'] = len(grid) - 1
        current_object['len'] = current_object['end'] - current_object['start'] + 1
        # assert current_object['len'] == current_object['count']
        objects.append(current_object)
        
    return objects

def transform(input_grid: List[int]) -> List[int]:
    """
    Transforms the input grid by swapping two adjacent non-background objects.

    Args:
        input_grid: A list of integers representing the 1D input grid.

    Returns:
        A list of integers representing the 1D output grid with objects swapped.
    """
    # Initialize output_grid as a copy of the input
    output_grid = list(input_grid)

    # Find the non-background objects
    objects = find_contiguous_objects(input_grid)

    # Based on the examples, we expect exactly two adjacent objects
    # Add basic validation, though ARC tasks usually guarantee valid inputs
    if len(objects) != 2:
        # Or raise an error, but returning input copy might be safer for ARC runner
        print(f"Warning: Expected 2 objects, found {len(objects)}. Returning copy.")
        return output_grid 
        
    obj1 = objects[0]
    obj2 = objects[1]

    # Check for adjacency (optional but good practice)
    if obj1['end'] + 1 != obj2['start']:
         print(f"Warning: Objects are not adjacent. Obj1 ends at {obj1['end']}, Obj2 starts at {obj2['start']}. Returning copy.")
         return output_grid

    # Determine the starting position for the swap
    swap_start_index = obj1['start']

    # Place the second object (obj2) where the first object (obj1) was
    for i in range(obj2['len']):
        output_grid[swap_start_index + i] = obj2['color']

    # Place the first object (obj1) immediately after the new position of obj2
    for i in range(obj1['len']):
        output_grid[swap_start_index + obj2['len'] + i] = obj1['color']

    return output_grid
```
