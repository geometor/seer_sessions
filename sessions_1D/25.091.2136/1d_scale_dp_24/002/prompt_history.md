
## train_1

**input:**
```
0 0 0 0 0 0 2 2 2 2 2 2 2 2 2 2 2 2 0 0 9 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 2 2 2 2 2 2 2 2 2 2 2 2 2 2 9 0 0 0 0 0
```


## train_2

**input:**
```
0 0 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 0 0 0 9 0 0
```


**output:**
```
0 0 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 9 0 0
```


## train_3

**input:**
```
0 0 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 0 0 9 0 0 0 0 0
```


**output:**
```
0 0 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 9 0 0 0 0 0
```

*   **Perception:** The task operates on a 1-dimensional array of pixels. Each example contains a single maroon (9) pixel and a contiguous block of another non-white color (red, orange, or gray). There are white (0) pixels separating the colored block and the maroon pixel. The transformation involves moving the maroon pixel leftwards until it is immediately adjacent to the right end of the colored block. The white pixels originally between the block and the maroon pixel are shifted to the right, filling the space vacated by the maroon pixel and ending up immediately to its right. The relative order and position of all other pixels remain unchanged.

*   **YAML Facts:**
    
```yaml
    task_type: array_manipulation_1d
    components:
      - type: contiguous_block
        color: non-white (varies: red, orange, gray in examples)
        description: A sequence of identical non-white pixels.
      - type: target_pixel
        color: maroon (9)
        count: 1
        description: A single specific pixel to be moved.
      - type: separator_pixels
        color: white (0)
        location: Between the contiguous_block and the target_pixel.
        description: Pixels separating the main block and the target.
      - type: background_pixels
        color: white (0)
        location: Outside the block, separator, and target region.
        description: Pixels forming the rest of the array.
    relationships:
      - type: spatial
        description: The target_pixel is initially located to the right of the contiguous_block, potentially separated by separator_pixels.
    transformation:
      - action: find
        target: target_pixel (maroon 9)
        result: target_index
      - action: find
        target: rightmost pixel of the contiguous_block to the left of target_index
        result: block_end_index
      - action: move
        target: target_pixel
        destination: position immediately right of block_end_index (index = block_end_index + 1)
      - action: move
        target: separator_pixels (originally between block_end_index and target_index)
        destination: positions immediately right of the new target_pixel location.
      - constraint: All other pixels retain their relative order and value.
    ```


*   **Natural Language Program:**
    1.  Locate the index of the single maroon (9) pixel (`maroon_index`).
    2.  Scan leftwards from the position just before the maroon pixel (`maroon_index - 1`) to find the index of the first non-white (non-zero) pixel encountered. This is the rightmost boundary of the contiguous colored block (`block_end_index`).
    3.  Construct the output array by concatenating the following segments:
        a.  The portion of the input array from the beginning up to and including `block_end_index`.
        b.  The maroon (9) pixel.
        c.  The sequence of white (0) pixels that were originally located in the input array between `block_end_index` and `maroon_index` (specifically, from index `block_end_index + 1` to `maroon_index - 1`).
        d.  The portion of the input array starting from the position immediately after the original maroon pixel (`maroon_index + 1`) to the end of the array.
```python
import numpy as np
from typing import List

"""
Locate the single maroon (9) pixel. Find the rightmost non-white pixel to its left.
Move the maroon pixel immediately to the right of this non-white pixel.
Shift the white pixels originally between the non-white block and the maroon pixel 
to the position immediately to the right of the moved maroon pixel. Keep all 
other pixels in their original relative positions.
"""

def find_pixel_index(data: List[int], color: int) -> int:
    """Finds the index of the first occurrence of a specific color."""
    try:
        return data.index(color)
    except ValueError:
        return -1 # Not found

def find_last_non_white_before(data: List[int], before_index: int) -> int:
    """Finds the index of the rightmost non-white pixel before a given index."""
    for i in range(before_index - 1, -1, -1):
        if data[i] != 0:
            return i
    return -1 # No non-white pixel found before the index

def transform(input_grid: List[List[int]]) -> List[List[int]]:
    """
    Applies the transformation rule to the input grid.
    
    Args:
        input_grid: A list containing a single list of integers representing the 1D input.

    Returns:
        A list containing a single list of integers representing the transformed 1D output.
    """
    # Input is expected to be 1D, represented as a list containing one list
    if not input_grid or len(input_grid) != 1:
        # Handle unexpected input format if necessary, maybe raise error or return input
        return input_grid 

    input_row = input_grid[0]
    
    # 1. Locate the index of the single maroon (9) pixel (`maroon_index`).
    maroon_index = find_pixel_index(input_row, 9)
    if maroon_index == -1:
        # Handle case where maroon pixel is not found
        return input_grid # Or raise an error

    # 2. Scan leftwards from the position just before the maroon pixel (`maroon_index - 1`) 
    #    to find the index of the first non-white (non-zero) pixel encountered. 
    #    This is the rightmost boundary of the contiguous colored block (`block_end_index`).
    block_end_index = find_last_non_white_before(input_row, maroon_index)
    if block_end_index == -1:
         # Handle case where no non-white block is found to the left
         # This might mean the maroon pixel is already at the start or only preceded by white
         # Based on examples, there's always a block. If not, could return input or error.
         # Let's assume based on examples it's always found.
         pass # Or raise error if this shouldn't happen based on task constraints

    # 3. Construct the output array by concatenating segments:
    output_row = []
    
    # a. The portion of the input array from the beginning up to and including `block_end_index`.
    output_row.extend(input_row[0 : block_end_index + 1])
    
    # b. The maroon (9) pixel.
    output_row.append(9)
    
    # c. The sequence of white (0) pixels that were originally located in the input array 
    #    between `block_end_index` and `maroon_index`.
    output_row.extend(input_row[block_end_index + 1 : maroon_index])
    
    # d. The portion of the input array starting from the position immediately after 
    #    the original maroon pixel (`maroon_index + 1`) to the end of the array.
    output_row.extend(input_row[maroon_index + 1 :])

    # Return the result in the required format (list of lists)
    return [output_row]

```
