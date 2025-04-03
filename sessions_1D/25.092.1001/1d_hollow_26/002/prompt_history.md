
## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 2 2 2 2 2 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 2 0 0 0 0 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 0 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 0 0
```


**output:**
```
0 0 0 3 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 3 0 0
```


## train_3

**input:**
```
0 0 0 1 1 1 1 1 1 1 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 1 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

*   **Perception:** The task involves processing a single row (1D grid) containing a contiguous block of a single non-white color against a white background. The transformation preserves the first and last pixels of this colored block, changing all intermediate pixels within the block to white. The overall dimensions and the background color remain unchanged.

*   **Facts:**
    
```yaml
    task_type: object_transformation
    grid_dimensionality: 1D # Represented as 1xN arrays
    background_color: white (0)

    objects:
      - type: contiguous_block
        description: A horizontal sequence of identical non-white pixels.
        properties:
          - color: The specific non-white color of the block (e.g., red, green, blue).
          - location: Defined by the start and end indices within the row.
          - length: The number of pixels in the block.

    actions:
      - action: identify_block
        input: input_grid
        output: identified block object (color, start_index, end_index)
        description: Locates the start and end indices of the contiguous non-white block.
      - action: create_output
        input: input_grid dimensions, identified block object
        output: output_grid
        description: Generates the output grid based on the input dimensions and the block's properties.

    transformation:
      - description: Keep endpoints of the block
        details: The output grid retains the color of the identified block only at its original start and end indices. All other positions, including those previously occupied by the middle part of the block, are set to the background color (white).
        input_elements:
          - input_grid
          - identified_block (color, start_index, end_index)
        output_elements:
          - output_grid (same dimensions as input, initialized to white)
          - output_grid[start_index] = block_color
          - output_grid[end_index] = block_color

    relationships:
      - The output grid has the same dimensions as the input grid.
      - The non-white pixels in the output grid correspond directly to the start and end positions of the non-white block in the input grid.
      - The color of the non-white pixels in the output is identical to the color of the block in the input.
    ```


*   **Natural Language Program:**
    1.  Initialize the output grid as a copy of the input grid, filled entirely with white pixels (color 0).
    2.  Scan the input grid to find the first non-white pixel. Record its color and its index (start index).
    3.  Continue scanning from the start index to find the last consecutive pixel of the same color. Record its index (end index).
    4.  Set the pixel in the output grid at the recorded start index to the recorded color.
    5.  Set the pixel in the output grid at the recorded end index to the recorded color.
    6.  Return the modified output grid.
```python
import numpy as np
from typing import List, Tuple, Optional

"""
Transforms a 1D grid by identifying a contiguous block of a single non-white color. 
The output grid retains the color of the block only at its start and end indices, 
with all other pixels set to white (0).
"""

def find_contiguous_block(grid: List[int]) -> Optional[Tuple[int, int, int]]:
    """
    Finds the start index, end index, and color of the first contiguous 
    block of non-white pixels in a 1D grid.

    Args:
        grid: A list of integers representing the 1D grid.

    Returns:
        A tuple (start_index, end_index, color) if a block is found, 
        otherwise None.
    """
    start_index = -1
    end_index = -1
    block_color = 0
    
    # Find the start of the block
    for i, pixel in enumerate(grid):
        if pixel != 0:
            start_index = i
            block_color = pixel
            break
            
    # If no non-white pixel found, return None
    if start_index == -1:
        return None
        
    # Find the end of the block (last consecutive pixel of the same color)
    end_index = start_index
    for i in range(start_index + 1, len(grid)):
        if grid[i] == block_color:
            end_index = i
        else:
            # Stop as soon as the color changes or a white pixel is encountered
            break
            
    return start_index, end_index, block_color

def transform(input_grid: List[int]) -> List[int]:
    """
    Applies the transformation rule to the input grid.
    
    Args:
        input_grid: A list of integers representing the 1D input grid.
        
    Returns:
        A list of integers representing the transformed 1D output grid.
    """
    
    # Find the contiguous block of non-white color
    block_info = find_contiguous_block(input_grid)
    
    # Initialize the output grid with the same size as input, filled with white (0)
    output_grid = [0] * len(input_grid)
    
    # If a block was found, place its color at the start and end indices
    if block_info:
        start_index, end_index, block_color = block_info
        output_grid[start_index] = block_color
        # Ensure we don't write the same pixel twice if the block length is 1
        if start_index != end_index:
             output_grid[end_index] = block_color
             
    return output_grid

```
