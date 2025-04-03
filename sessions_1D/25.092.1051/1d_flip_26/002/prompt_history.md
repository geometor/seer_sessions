
## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 0 6 2 2 2 2 2 2 2 2 2 2 2 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 2 2 2 2 2 2 2 2 2 2 2 6 0 0
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 4 5 5 5 5 5 5 5 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 5 5 5 5 5 5 5 4 0 0 0 0 0 0 0
```


## train_3

**input:**
```
1 4 4 4 4 4 4 4 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
4 4 4 4 4 4 4 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

*   **Perception**: The input and output are single rows of pixels. Each input row contains a sequence of non-background pixels consisting of a single pixel of one color (let's call it the 'marker') immediately followed by a contiguous block of pixels of another color (let's call it the 'block'). The background is white (0). The transformation involves moving the marker pixel from the position *before* the block to the position immediately *after* the block. The pixels within the block shift one position to the left to fill the gap left by the marker.

*   **YAML Facts**:
    
```yaml
    task_description: Move a single 'marker' pixel across an adjacent 'block' of pixels in a 1D grid.

    elements:
      - object: marker_pixel
        description: A single pixel with a color different from the background (white) and the adjacent block.
        properties:
          - color: unique_color_1 (e.g., magenta in ex1, yellow in ex2, blue in ex3)
          - position: index `i`
      - object: pixel_block
        description: A contiguous sequence of one or more pixels, all having the same color, different from the background and the marker pixel.
        properties:
          - color: unique_color_2 (e.g., red in ex1, gray in ex2, yellow in ex3)
          - position: starts at index `i+1`
          - length: `L` (number of pixels in the block)
      - object: background
        description: Pixels representing the empty space.
        properties:
          - color: white (0)

    relationships:
      - type: adjacency
        objects: [marker_pixel, pixel_block]
        details: The marker_pixel is immediately to the left of the first pixel of the pixel_block.

    actions:
      - action: move
        object: marker_pixel
        from_position: index `i`
        to_position: index `i + L` (immediately after the original block)
      - action: shift
        object: pixel_block
        direction: left
        distance: 1 position (occupying indices `i` to `i + L - 1`)
    ```


*   **Natural Language Program**:
    1.  Identify the sequence of non-background pixels in the input row.
    2.  Find the first pixel in this sequence (the 'marker pixel').
    3.  Identify the contiguous block of pixels of a single, different color that immediately follows the marker pixel (the 'pixel block'). Let the length of this block be `L`.
    4.  Create the output row by copying the input row.
    5.  Move the marker pixel from its original position (`i`) to the position immediately following the end of the pixel block (position `i + L`).
    6.  Shift all pixels of the pixel block one position to the left, so they now occupy the original position of the marker pixel and the subsequent `L-1` positions (positions `i` through `i + L - 1`).
    7.  Leave all other pixels (background) unchanged.
```python
import numpy as np
from typing import List, Tuple

"""
Identify a sequence of non-background pixels in the input row. This sequence consists 
of a single 'marker' pixel followed immediately by a contiguous 'block' of pixels 
of a single, different color. Move the marker pixel to the position immediately 
following the end of the block. Shift the pixels of the block one position to the 
left to fill the original position of the marker.
"""

def find_marker_and_block(row: List[int]) -> Tuple[int, int, int, int, int]:
    """
    Finds the marker pixel and the subsequent block in a row.

    Args:
        row: A list of integers representing a row of the grid.

    Returns:
        A tuple containing:
        - marker_idx: The index of the marker pixel.
        - marker_color: The color of the marker pixel.
        - block_start_idx: The starting index of the block.
        - block_color: The color of the block pixels.
        - block_length: The number of pixels in the block.
        Returns (-1, -1, -1, -1, -1) if no marker/block pattern is found.
    """
    marker_idx = -1
    marker_color = -1
    block_start_idx = -1
    block_color = -1
    block_length = 0

    # 1. Find the first non-background pixel (potential marker)
    for i, pixel in enumerate(row):
        if pixel != 0:
            marker_idx = i
            marker_color = pixel
            break

    # If no non-background pixel found, return defaults
    if marker_idx == -1:
        return -1, -1, -1, -1, -1

    # 2. Check if there's a pixel immediately following the marker
    if marker_idx + 1 >= len(row):
        return -1, -1, -1, -1, -1 # Marker is at the very end, no block possible

    # 3. Identify the block
    block_start_idx = marker_idx + 1
    block_color = row[block_start_idx]

    # Check if the block color is different from marker and background
    if block_color == marker_color or block_color == 0:
        return -1, -1, -1, -1, -1 # Not a valid block

    # 4. Calculate block length
    block_length = 0
    for i in range(block_start_idx, len(row)):
        if row[i] == block_color:
            block_length += 1
        else:
            break # Block ends

    # Check if a block was actually found
    if block_length == 0:
        return -1, -1, -1, -1, -1

    return marker_idx, marker_color, block_start_idx, block_color, block_length


def transform(input_grid: List[List[int]]) -> List[List[int]]:
    """
    Transforms the input grid by moving a marker pixel across an adjacent block.

    Args:
        input_grid: A 2D list of integers representing the input grid. 
                      Expected to have only one row based on examples.

    Returns:
        A 2D list of integers representing the transformed grid.
    """
    # Assume input is always a single row, potentially wrapped in a list
    if not input_grid or not input_grid[0]:
        return input_grid # Handle empty case
        
    input_row = input_grid[0]
    output_row = list(input_row) # Create a mutable copy

    # Find the marker and block information
    marker_idx, marker_color, block_start_idx, block_color, block_length = find_marker_and_block(input_row)

    # If the specific pattern wasn't found, return the original grid
    if marker_idx == -1:
        return input_grid

    # Check if the target position for the marker is within bounds
    target_marker_idx = marker_idx + block_length
    if target_marker_idx >= len(output_row):
        # This case shouldn't happen based on examples, but handle defensively
        print(f"Warning: Target marker index {target_marker_idx} is out of bounds for row length {len(output_row)}")
        return input_grid 

    # Perform the transformation
    # 1. Shift the block pixels one step to the left
    for i in range(block_length):
        output_row[marker_idx + i] = block_color

    # 2. Place the marker pixel at the end of the original block position
    output_row[target_marker_idx] = marker_color

    # Return the transformed row, wrapped in a list to match input format
    return [output_row]

```
