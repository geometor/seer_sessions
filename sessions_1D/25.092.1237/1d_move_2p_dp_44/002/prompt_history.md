
## train_1

**input:**
```
7 7 7 0 0 6 0
```


**output:**
```
0 0 7 7 7 6 0
```


## train_2

**input:**
```
3 3 3 0 0 6 0
```


**output:**
```
0 0 3 3 3 6 0
```


## train_3

**input:**
```
8 8 8 0 0 6 0
```


**output:**
```
0 0 8 8 8 6 0
```

*   **Perception:**
    *   The input and output are both 1D grids (sequences) of the same length (7 pixels).
    *   The colors present in the examples are Orange (7), Green (3), Azure (8), Magenta (6), and White (0).
    *   The core transformation involves rearranging pixels within the sequence. The number and type of pixels remain unchanged between input and output.
    *   The rearrangement seems localized to the beginning of the sequence. Specifically, the first contiguous block of non-white pixels and the immediately following contiguous block of white pixels appear to swap positions.
    *   Pixels further down the sequence (the Magenta and trailing White pixel in the examples) retain their positions relative to the end of the sequence.

*   **Facts:**
    
```yaml
    task_type: rearrangement
    grid_dimensionality: 1D
    element_type: pixels
    properties:
      - color: (represented by integers 0-9)
      - position: index within the sequence
      - contiguity: groups of adjacent pixels with the same color (or property, e.g., being white/non-white)
    objects:
      - object_type: contiguous_block
        description: A sequence of one or more adjacent pixels sharing a property.
        properties:
          - color_type: (all white (0) or all non-white (>0))
          - start_index: position of the first pixel in the block
          - end_index: position of the last pixel in the block
          - length: number of pixels in the block
    actions:
      - action_type: identify
        description: Locate specific blocks based on criteria.
        criteria:
          - 1: The first contiguous block of non-white pixels starting from the beginning of the sequence.
          - 2: The contiguous block of white pixels immediately following the block identified in step 1.
      - action_type: swap
        description: Exchange the positions of the two identified blocks.
    relationships:
      - relationship_type: adjacency
        description: One block immediately follows another in the sequence.
      - relationship_type: ordering
        description: The relative order of blocks in the sequence.
    constraints:
      - The overall length of the sequence remains constant.
      - The count of each color pixel remains constant.
      - Only the identified non-white block and the adjacent white block change positions. All other pixels retain their original relative order.

    ```


*   **Natural Language Program:**
    1.  Scan the input sequence from the beginning (left to right).
    2.  Identify the first contiguous block (one or more adjacent pixels) of non-white (non-zero color) pixels. Record its start and end indices.
    3.  Identify the contiguous block of white (zero color) pixels that starts immediately after the end index of the non-white block found in step 2. Record its start and end indices.
    4.  Construct the output sequence by:
        a.  Placing the identified white block (from step 3) at the starting index of the identified non-white block (from step 2).
        b.  Placing the identified non-white block (from step 2) immediately after the white block placed in step 4a.
        c.  Appending all remaining pixels from the input sequence, starting from the pixel immediately after the end of the white block identified in step 3, maintaining their original relative order.
```python
import numpy as np
from typing import List

"""
Transformation Rule:
1. Identify the first contiguous block of non-white (non-zero) pixels from the left of the sequence.
2. Identify the contiguous block of white (zero) pixels that immediately follows the non-white block.
3. Swap the positions of these two blocks.
4. Keep all other pixels (leading white pixels and pixels after the swapped blocks) in their original relative positions.
"""

def find_first_non_white_block(grid: List[int]) -> tuple[int, int]:
    """Finds the start and end indices of the first non-white block."""
    start_index = -1
    end_index = -1
    n = len(grid)

    # Find the start of the first non-white block
    for i in range(n):
        if grid[i] != 0:
            start_index = i
            break
            
    # If no non-white pixel found, return (-1, -1)
    if start_index == -1:
        return -1, -1

    # Find the end of the first non-white block
    end_index = start_index
    for i in range(start_index + 1, n):
        if grid[i] != 0:
            end_index = i
        else:
            break # End of the non-white block

    return start_index, end_index

def find_subsequent_white_block(grid: List[int], start_search_index: int) -> tuple[int, int]:
    """Finds the start and end indices of the white block starting at start_search_index."""
    start_index = -1
    end_index = -1
    n = len(grid)

    # Check if the search starts within bounds and if the pixel is white
    if start_search_index >= n or grid[start_search_index] != 0:
        return -1, -1 # No white block starts immediately after

    start_index = start_search_index
    end_index = start_index
    # Find the end of the white block
    for i in range(start_index + 1, n):
        if grid[i] == 0:
            end_index = i
        else:
            break # End of the white block

    return start_index, end_index

def transform(input_grid: List[int]) -> List[int]:
    """
    Applies the transformation rule to the input grid (sequence).
    Finds the first non-white block and the immediately following white block,
    then swaps their positions.
    """
    n = len(input_grid)

    # 1. Find the first contiguous block of non-white pixels.
    nw_start, nw_end = find_first_non_white_block(input_grid)

    # If no non-white block is found, return the original grid
    if nw_start == -1:
        return input_grid

    # 2. Find the contiguous block of white pixels immediately following.
    w_start_search = nw_end + 1
    w_start, w_end = find_subsequent_white_block(input_grid, w_start_search)

    # If no subsequent white block is found, return the original grid
    if w_start == -1:
        return input_grid

    # 3. Extract the different segments of the grid
    leading_pixels = input_grid[0:nw_start]
    non_white_block = input_grid[nw_start : nw_end + 1]
    white_block = input_grid[w_start : w_end + 1]
    remainder = input_grid[w_end + 1 :]

    # 4. Construct the output grid by rearranging the segments
    output_grid = leading_pixels + white_block + non_white_block + remainder

    return output_grid

```
