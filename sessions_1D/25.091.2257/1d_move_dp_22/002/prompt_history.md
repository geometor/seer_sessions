
## train_1

**input:**
```
3 3 3 3 0 0 0 0 6 0 0 0 0 0
```


**output:**
```
0 0 0 0 3 3 3 3 6 0 0 0 0 0
```


## train_2

**input:**
```
0 7 7 7 7 7 7 7 7 0 0 0 6 0
```


**output:**
```
0 0 0 0 7 7 7 7 7 7 7 7 6 0
```


## train_3

**input:**
```
0 0 0 0 3 3 3 3 3 0 0 0 6 0
```


**output:**
```
0 0 0 0 0 0 0 3 3 3 3 3 6 0
```

**Perception**

1.  **Input Grid Structure:** All input examples are 1x14 grids (single rows).
2.  **Key Objects:**
    *   A contiguous horizontal block of a single color (green or orange). Let's call this the "main block".
    *   A single magenta pixel (color 6), acting as a marker or boundary.
    *   White pixels (color 0) filling the remaining space.
3.  **Relationships:** The main block and the magenta pixel are separated by zero or more white pixels in the input.
4.  **Output Grid Structure:** The output grids are also 1x14, containing the same colors and objects as the input.
5.  **Transformation:** The primary transformation is the horizontal shift (translation) of the "main block". Its final position appears to be determined by the position of the magenta pixel. Specifically, the main block moves rightwards until its rightmost pixel is immediately to the left of the magenta pixel. The magenta pixel itself does not move. The relative order of pixels within the main block remains unchanged. White pixels fill the space not occupied by the shifted main block or the magenta pixel.

**Facts**


```yaml
task_type: object_manipulation
grid_dimensions:
  input: 1x14
  output: 1x14
objects:
  - id: main_block
    description: A contiguous horizontal sequence of identical non-white, non-magenta pixels.
    properties:
      color: Varies (green '3' or orange '7' in examples).
      shape: Horizontal line segment.
      length: Varies.
      position: Varies in the input.
  - id: marker
    description: A single magenta pixel.
    properties:
      color: magenta '6'
      shape: Single pixel.
      position: Varies in the input, but remains fixed relative to the grid boundaries during transformation.
  - id: background
    description: Pixels filling the rest of the grid.
    properties:
      color: white '0'
actions:
  - action: shift
    target: main_block
    constraints:
      - type: relative_positioning
        reference_object: marker
        details: The main_block is moved horizontally such that its rightmost pixel becomes adjacent to the left side of the marker pixel.
relationships:
  - type: adjacency
    object1: main_block (right end)
    object2: marker (left side)
    state: established in output
  - type: immutability
    object: marker
    property: position
    state: maintained between input and output
```


**Natural Language Program**

1.  Initialize the output grid as a copy of the input grid, filled entirely with white pixels (color 0).
2.  Identify the single magenta pixel (color 6) in the input grid and record its column index. Place this magenta pixel at the same column index in the output grid.
3.  Identify the contiguous horizontal block of non-white (color > 0), non-magenta (color != 6) pixels in the input grid. Record its color and its length (number of pixels).
4.  Determine the target starting column index for this block in the output grid. This index is calculated as: `(magenta_pixel_column_index - block_length)`.
5.  Place the identified block (using its recorded color and length) into the output grid, starting at the calculated target starting column index and extending to the right until the column index `(magenta_pixel_column_index - 1)`.
```python
import numpy as np
from typing import List, Tuple

"""
Transformation rule:
1. Identify the magenta pixel (6) and its position.
2. Identify the contiguous horizontal block of a color other than white (0) or magenta (6). Note its color and length.
3. Initialize an output grid of the same dimensions as the input, filled with white (0).
4. Place the magenta pixel in the output grid at its original position.
5. Calculate the target start position for the block: (magenta position - block length).
6. Place the identified block into the output grid starting at the calculated target position, ensuring it ends immediately to the left of the magenta pixel.
"""

def find_marker_position(grid_row: List[int], marker_color: int) -> int:
    """Finds the column index of the first occurrence of the marker color."""
    for idx, color in enumerate(grid_row):
        if color == marker_color:
            return idx
    return -1 # Should not happen based on task description

def find_main_block(grid_row: List[int], background_color: int, marker_color: int) -> Tuple[int, int, int]:
    """Finds the main block's start index, length, and color."""
    block_start_idx = -1
    block_color = -1
    block_len = 0
    in_block = False

    for idx, color in enumerate(grid_row):
        is_block_pixel = (color != background_color and color != marker_color)
        
        if is_block_pixel and not in_block:
            # Start of the block
            in_block = True
            block_start_idx = idx
            block_color = color
            block_len = 1
        elif is_block_pixel and in_block:
            # Continuation of the block
            if color == block_color:
                 block_len += 1
            else: 
                 # This case (block of different color) shouldn't happen per examples
                 # but if it did, we'd stop the current block count here.
                 # For this task, we assume only one block color exists.
                 break 
        elif not is_block_pixel and in_block:
            # End of the block
            break # Stop searching once the block ends

    if block_start_idx == -1:
        raise ValueError("Main block not found in input grid row.")
        
    return block_start_idx, block_len, block_color

def transform(input_grid: List[List[int]]) -> List[List[int]]:
    """
    Shifts a contiguous block of color horizontally so its right edge
    is adjacent to the left side of a fixed magenta marker pixel.
    Assumes input is a 1xN grid.
    """
    # Assume input is always 1 row based on examples
    if not input_grid or len(input_grid) != 1:
        # Handle unexpected input format if necessary, though examples are 1xN
        return input_grid 

    input_row = input_grid[0]
    height = 1
    width = len(input_row)
    
    # Define colors
    background_color = 0
    marker_color = 6

    # Initialize output grid with background color
    output_row = [background_color] * width
    
    # 1. Find the marker position
    marker_idx = find_marker_position(input_row, marker_color)
    if marker_idx == -1:
         raise ValueError("Magenta marker (6) not found in input grid row.")

    # 4. Place the marker in the output grid (step done early for clarity)
    output_row[marker_idx] = marker_color

    # 2. Find the main block properties
    _, block_len, block_color = find_main_block(input_row, background_color, marker_color)

    # 5. Calculate the target start position for the block
    # The block should end at index marker_idx - 1
    # So it starts at marker_idx - block_len
    target_start_idx = marker_idx - block_len

    # Check for bounds (shouldn't be negative based on examples)
    if target_start_idx < 0:
        # Handle case where block wouldn't fit - maybe raise error or adjust?
        # Based on examples, this shouldn't happen.
         raise ValueError("Calculated block start position is out of bounds.")

    # 6. Place the block in the output grid
    for i in range(block_len):
        current_idx = target_start_idx + i
        if 0 <= current_idx < width: # Ensure we stay within grid bounds
             # Check if we are overwriting the marker - should not happen if logic is correct
             if current_idx == marker_idx:
                  raise ValueError("Block placement overlaps with marker position.")
             output_row[current_idx] = block_color
        else:
             # Handle cases where part of the block might go off-grid if rules allowed
             # For this task, seems unlikely based on fixed marker position.
             pass 

    # Return the output grid (as list of lists)
    return [output_row]

```
