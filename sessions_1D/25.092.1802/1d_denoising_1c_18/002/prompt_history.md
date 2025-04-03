
## train_1

**input:**
```
0 0 2 0 0 0 2 0 0 2 2 2 2 2 2 2 2 2 2 2 0 0 0 2 0 0 0 0 2 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 2 2 2 2 2 2 2 2 2 2 2 0 0 0 0 0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 0 0 4 0 0 0 0 0 0 0 0 0 0 0 0 0 4 4 4 4 4 4 4 4 4 4 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 4 4 4 4 4 4 4 4 4 4 0 0 0 0
```


## train_3

**input:**
```
0 0 0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 0 0 0 0 1 0 0 0 1 0 0 1 0 0 0
```


**output:**
```
0 0 0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

*   **Perception:** The input grids are one-dimensional arrays (or 1xN grids) containing mostly white pixels (0) and one other color (red, yellow, or blue in the examples). Each input grid features one large contiguous block of the non-white color and several isolated single pixels of the same color. The output grid retains only the largest contiguous block of the non-white color, positioned exactly as it was in the input. All other pixels, including the previously isolated non-white pixels and all original white pixels, become white in the output. The transformation identifies and isolates the single largest contiguous segment of non-background color, discarding all smaller segments and isolated pixels of that color.

*   **Facts:**
    
```yaml
    task_type: filtering
    grid_dimensionality: 1D # presented as 1xN
    background_color: white (0)
    objects:
      - type: contiguous_block
        color: non-white (variable: red, yellow, blue in examples)
        properties:
          - size: count of pixels in the block
          - location: start and end indices
    relationships:
      - multiple blocks of the same non-white color can exist within one input grid.
      - blocks vary in size (some are size 1, others are larger).
    actions:
      - identify_all_contiguous_blocks: find all groups of adjacent non-white pixels.
      - calculate_block_size: determine the number of pixels in each block.
      - find_largest_block: identify the block with the maximum size. If there's a tie for largest, the examples don't cover this, but assume one is chosen (e.g., the first one encountered).
      - filter_blocks: keep only the largest block.
      - generate_output: create a new grid of the same dimensions as the input, initially filled with the background color (white).
      - place_largest_block: copy the pixels corresponding to the largest block from the input to their original positions in the new output grid.
    result: The output grid contains only the largest contiguous block of non-white color from the input, with all other positions set to white.
    ```


*   **Natural Language Program:**
    1.  Initialize an output grid with the same dimensions as the input grid, filled entirely with the background color (white, 0).
    2.  Identify all contiguous blocks of non-white pixels in the input grid. For each block, record its color, starting position, ending position, and size (number of pixels).
    3.  If no non-white blocks are found, return the initialized white output grid.
    4.  Determine the maximum size among all identified blocks.
    5.  Select the block(s) that have this maximum size. (Based on the examples, there appears to be only one unique largest block per input).
    6.  For the selected largest block, copy its pixels (color and position) from the input grid to the corresponding positions in the output grid.
    7.  Return the final output grid.
```python
import numpy as np
from typing import List, Dict, Tuple

"""
Identify all contiguous blocks of non-background (non-white, non-0) pixels in the 1D input grid.
Determine the size (length) of each block.
Find the block with the maximum size.
Create an output grid of the same dimensions as the input, filled with the background color (white, 0).
Copy the pixels of the largest identified block from the input grid to their original positions in the output grid.
If multiple blocks share the maximum size, the examples suggest only one is present, but implicitly the first one encountered during iteration would be chosen.
If no non-background blocks exist, the output remains entirely background color.
"""

def find_contiguous_blocks(grid_1d: List[int], background_color: int = 0) -> List[Dict]:
    """
    Finds all contiguous blocks of non-background colors in a 1D grid.

    Args:
        grid_1d: A list of integers representing the 1D grid.
        background_color: The integer value representing the background color.

    Returns:
        A list of dictionaries, where each dictionary represents a block
        and contains 'color', 'start' index, 'end' index, and 'size'.
    """
    blocks = []
    current_block = None

    for i, pixel in enumerate(grid_1d):
        if pixel != background_color:
            # Non-background pixel found
            if current_block is None:
                # Start a new block
                current_block = {'color': pixel, 'start': i, 'size': 1}
            elif pixel == current_block['color']:
                # Continue the current block
                current_block['size'] += 1
            else:
                # Different color, finalize previous block and start new one
                current_block['end'] = i - 1
                blocks.append(current_block)
                current_block = {'color': pixel, 'start': i, 'size': 1}
        else:
            # Background pixel found
            if current_block is not None:
                # Finalize the current block
                current_block['end'] = i - 1
                blocks.append(current_block)
                current_block = None

    # Handle case where the grid ends with a block
    if current_block is not None:
        current_block['end'] = len(grid_1d) - 1
        blocks.append(current_block)

    return blocks

def transform(input_grid: List[int]) -> List[int]:
    """
    Transforms the input grid by keeping only the largest contiguous block
    of non-background color.

    Args:
        input_grid: A list of integers representing the 1D input grid.

    Returns:
        A list of integers representing the transformed 1D output grid.
    """
    # Ensure input is treated as a 1D list (as presented in examples)
    # If input were a numpy array, flatten it: grid_1d = input_grid.flatten().tolist()
    # Assuming input is already a list based on example format
    grid_1d = input_grid 
    grid_size = len(grid_1d)
    background_color = 0

    # Initialize output grid with background color
    output_grid = [background_color] * grid_size

    # Find all contiguous blocks of non-background colors
    blocks = find_contiguous_blocks(grid_1d, background_color)

    # If no blocks are found, return the background grid
    if not blocks:
        return output_grid

    # Find the largest block
    largest_block = None
    max_size = 0
    for block in blocks:
        if block['size'] > max_size:
            max_size = block['size']
            largest_block = block
        # Note: If sizes are equal, the first one encountered remains largest_block

    # If a largest block was found (should always happen if blocks list is not empty)
    if largest_block:
        # Copy the largest block to the output grid
        start_index = largest_block['start']
        end_index = largest_block['end']
        color = largest_block['color']
        for i in range(start_index, end_index + 1):
            # Ensure index is within bounds (should be, based on how blocks are found)
            if 0 <= i < grid_size:
                output_grid[i] = color

    return output_grid
```
