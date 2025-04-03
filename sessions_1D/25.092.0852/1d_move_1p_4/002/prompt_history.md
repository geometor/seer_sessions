
## train_1

**input:**
```
0 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 0 0 0 0 0
```


**output:**
```
0 0 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 0 0 0 0
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 5 5 5 5 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 5 5 5 5 0 0 0
```


## train_3

**input:**
```
0 0 0 1 1 1 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 1 1 1 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

*   **Perception:** The task operates on single-row grids (1D arrays). Each input contains a single contiguous block of a non-white color surrounded by white pixels. The transformation involves shifting this colored block one position to the right within the row. The size and color of the block remain unchanged.

*   **YAML Facts:**
    
```yaml
    task_type: grid_manipulation
    grid_dimensionality: 1D # Effectively 1 row
    input_features:
      - name: background
        color: white (0)
        property: fills space not occupied by the object
      - name: object
        property: single contiguous block of non-white pixels
        attributes:
          - color: varies (green, gray, blue in examples)
          - shape: horizontal line segment
          - size: varies
          - position: varies
    transformation:
      - action: identify
        target: non-white object
        details: find start index, end index, and color
      - action: shift
        target: non-white object
        direction: right
        distance: 1 pixel
      - action: maintain
        target: size and color of the object
      - action: fill
        details: position vacated by the left end of the object becomes white
    output_features:
      - name: background
        color: white (0)
      - name: object
        property: same as input object but shifted right by 1
    relationship: The output grid is the input grid with the single non-white object shifted horizontally one position to the right.
    ```


*   **Natural Language Program:**
    1.  Identify the contiguous segment of non-white pixels within the input row. Determine its color, its starting column index, and its ending column index.
    2.  Create a new output row with the same length as the input row, initially filled with white pixels (0).
    3.  Copy the identified non-white segment into the output row, placing it starting at (input starting column index + 1) and ending at (input ending column index + 1). Ensure the color is preserved.
    4.  Return the newly created output row.
```python
import numpy as np
from typing import List

# COLOR_MAP = {
#     0: (238, 238, 238),  # white
#     1: (30, 147, 255),  # blue
#     2: (220, 50, 40),  # red
#     3: (79, 204, 48),  # green
#     4: (230, 200, 0),  # yellow
#     5: (85, 85, 85),  # gray
#     6: (229, 58, 163),  # magenta
#     7: (230, 120, 20),  # orange
#     8: (135, 216, 241),  # azure
#     9: (146, 18, 49),  # maroon
# }

Grid = List[List[int]]

def find_object_segment(row: List[int]) -> tuple[int, int, int] | None:
    """
    Finds the start index, end index, and color of the first contiguous
    non-white segment in a row.
    Returns None if no non-white segment is found.
    """
    start_index = -1
    end_index = -1
    object_color = 0
    in_segment = False

    for i, pixel in enumerate(row):
        if pixel != 0:
            if not in_segment:
                start_index = i
                object_color = pixel
                in_segment = True
            end_index = i # Keep updating end index while in segment
        elif in_segment:
            # We've reached the end of the segment
            break 
            
    if start_index != -1:
        return start_index, end_index, object_color
    else:
        return None # No object found

def transform(input_grid: Grid) -> Grid:
    """
    Identifies a single contiguous segment of non-white pixels in a 1D input grid (single row)
    and shifts this segment one position to the right, preserving its color and size.
    The background is white (0).
    """
    # Input is expected to be a single row grid
    if not input_grid or len(input_grid) != 1:
        # Handle invalid input if necessary, maybe return input or raise error
        # For now, assume valid input based on examples
        return input_grid 
        
    input_row = input_grid[0]
    width = len(input_row)

    # Initialize the output row with the background color (white)
    output_row = [0] * width

    # 1. Identify the contiguous segment of non-white pixels
    object_info = find_object_segment(input_row)

    # If an object segment is found
    if object_info:
        start_index, end_index, object_color = object_info
        
        # 2. Determine the new position (shifted right by 1)
        new_start_index = start_index + 1
        new_end_index = end_index + 1
        
        # 3. Copy the segment to the new position in the output row
        # Ensure the new indices are within the bounds of the row
        # Iterate through the segment length
        for i in range(end_index - start_index + 1):
            current_output_index = new_start_index + i
            # Check if the index is valid before writing
            if 0 <= current_output_index < width:
                output_row[current_output_index] = object_color
                
    # If no object was found, output_row remains all white, which is correct.

    # 4. Return the newly created output row, wrapped as a grid
    output_grid = [output_row]
    return output_grid

```
