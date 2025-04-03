
## train_1

**input:**
```
0 0 0 0 0 4 4 4 4 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 4 0 0 4 0 0 0 0 0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 3 3 3 3 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 3 0 0 3 0 0 0 0 0 0 0 0
```


## train_3

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0 3 3 3 3 3 3 3 3 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0 3 0 0 0 0 0 0 3 0
```

*   **Perception:** The input and output are 1D arrays (or single rows/columns of a 2D grid) of pixels. Each input contains a single contiguous block of non-white pixels (yellow or green) surrounded by white pixels. The transformation modifies this block. Specifically, it keeps the first and last pixel of the block unchanged, while changing all the pixels *between* the first and last pixels to white (0). Pixels outside the original block remain white.

*   **YAML Facts:**
    
```yaml
    task_type: array_transformation_1d
    input_features:
      - description: A 1D array of pixels.
      - properties:
          - contains a single contiguous block of non-white pixels.
          - non-white block is surrounded by white pixels (0).
    output_features:
      - description: A 1D array of pixels, same length as the input.
      - properties:
          - derived from the input array.
          - the non-white block from the input is modified.
    transformation:
      - description: Modifies the contiguous non-white block.
      - steps:
          - Identify the start and end indices of the non-white block.
          - Keep the pixel at the start index (color and position).
          - Keep the pixel at the end index (color and position).
          - Replace all pixels strictly between the start and end indices with white (0).
          - Pixels outside the original block remain unchanged (white).
    objects:
      - id: background
        color: white (0)
        role: static background
      - id: block
        color: non-white (e.g., yellow (4), green (3))
        shape: contiguous horizontal segment
        role: object being modified
    relationships:
      - type: spatial
        description: The non-white block is embedded within the white background.
    actions:
      - action: identify_block
        target: input array
        output: start index, end index, color of the block
      - action: modify_block
        target: block identified in the input
        result: A new block where only the first and last pixels retain the original color, and the intermediate pixels become white (0).
      - action: construct_output
        input: original array, identified block info, modification rule
        output: the final output array
    constraints:
      - Only one non-white block per input array in the examples.
      - Block length must be at least 2 for modification to have an effect (a block of length 1 would remain unchanged). If the block length is 2, it also remains unchanged.
    ```


*   **Natural Language Program:**
    1.  Scan the input array to find the first and last indices of the contiguous sequence of non-white pixels (the "block"). Note the color of this block.
    2.  Create a new output array of the same size as the input, initially filled with white pixels (0).
    3.  Copy all white pixels from the input array to the corresponding positions in the output array.
    4.  If a non-white block was found:
        a.  Place the block's original color at the starting index of the block in the output array.
        b.  Place the block's original color at the ending index of the block in the output array.
        c.  Ensure all positions in the output array strictly between the starting and ending indices of the block are filled with white pixels (0).
```python
import numpy as np
from typing import List

"""
Transformation Rule:
1. Identify the contiguous horizontal block of non-white pixels in the input 1D array.
2. Determine the starting index, ending index, and color of this block.
3. Create an output array of the same size, initialized to all white (0).
4. Place the identified block's color at the starting index in the output array.
5. Place the identified block's color at the ending index in the output array.
6. All other pixels in the output array remain white (0).
"""

def find_non_white_block_indices(grid_1d: List[int]) -> tuple[int | None, int | None, int | None]:
    """
    Finds the start index, end index, and color of the first contiguous 
    non-white block in a 1D list. Assumes only one such block exists.
    
    Args:
        grid_1d: A list of integers representing pixels.
        
    Returns:
        A tuple (start_index, end_index, color). Returns (None, None, None) 
        if no non-white block is found.
    """
    start_index = None
    end_index = None
    block_color = None
    
    # Find the first non-white pixel
    for i, pixel in enumerate(grid_1d):
        if pixel != 0:
            start_index = i
            block_color = pixel
            break
            
    # If no non-white pixel found, return None
    if start_index is None:
        return None, None, None
        
    # Find the last non-white pixel (must be the same color for a contiguous block)
    # Iterate backwards to find the last occurrence efficiently,
    # or simply update end_index whenever we see the block_color.
    for i in range(start_index, len(grid_1d)):
         # Update end_index if we are still in the block
         if grid_1d[i] == block_color:
             end_index = i
         # If we encounter a different non-zero color or a zero after starting,
         # the block has ended. (Assumes single contiguous block)
         elif grid_1d[i] != block_color:
              break # Stop searching once the block ends

    # Re-confirm end_index by searching backwards if the forward search felt ambiguous
    # Let's stick to the simpler forward update logic based on the examples.
    # Find the last index matching the block_color starting from the end
    for i in range(len(grid_1d) - 1, start_index - 1, -1):
        if grid_1d[i] == block_color:
            end_index = i
            break
            
    return start_index, end_index, block_color

def transform(input_grid: List[int]) -> List[int]:
    """
    Applies the transformation rule to the input 1D grid.
    Keeps only the first and last pixels of the non-white block, 
    turning the intermediate pixels white.

    Args:
        input_grid: A list of integers representing the input row/column.

    Returns:
        A list of integers representing the transformed row/column.
    """
    
    # Initialize output grid with the same size as input, filled with white (0)
    output_grid = [0] * len(input_grid)
    
    # Find the boundaries and color of the non-white block
    start_index, end_index, block_color = find_non_white_block_indices(input_grid)
    
    # If a block was found, place its endpoints in the output grid
    if start_index is not None and end_index is not None and block_color is not None:
        # Place the color at the start index
        output_grid[start_index] = block_color
        
        # Place the color at the end index (handles blocks of length 1 correctly)
        output_grid[end_index] = block_color
        
    # Pixels outside the original block's start/end indices, 
    # and pixels between start and end (exclusive) remain white (0) 
    # as initialized.
        
    return output_grid

```
