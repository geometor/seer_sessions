
## train_1

**input:**
```
0 1 1 1 1 1 1 1 0 0 8 0 0 0 0 0
```


**output:**
```
0 0 0 1 1 1 1 1 1 1 8 0 0 0 0 0
```


## train_2

**input:**
```
0 2 2 2 2 2 2 2 2 0 0 0 0 8 0 0
```


**output:**
```
0 0 0 0 0 2 2 2 2 2 2 2 2 8 0 0
```


## train_3

**input:**
```
0 1 1 1 1 0 0 0 0 0 0 0 0 8 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 1 1 1 1 8 0 0
```

*   **Perception:**
    *   The input and output are single-row grids (1D arrays) of the same size (1x16).
    *   Each input grid contains three types of elements:
        1.  Background pixels (white/0).
        2.  A single, fixed anchor pixel (azure/8).
        3.  A contiguous block of a single color (blue/1 or red/2), which changes position.
    *   The output grid retains the background pixels and the anchor pixel in their original positions.
    *   The colored block (blue or red) is shifted horizontally to the right.
    *   The final position of the colored block in the output grid is always immediately to the left of the anchor (azure/8) pixel. The rightmost pixel of the block becomes adjacent to the anchor pixel.
    *   The color and length of the block remain unchanged during the transformation.

*   **Facts:**
    
```yaml
    task_type: object_manipulation
    grid_dimensionality: 1D (single row)
    objects:
      - type: background
        color: white (0)
        count: variable
        behavior: static (fills empty space)
      - type: anchor
        color: azure (8)
        count: 1
        shape: single_pixel
        behavior: static (position fixed)
      - type: movable_block
        color: non_white_non_azure (e.g., blue/1, red/2)
        count: 1
        shape: contiguous_horizontal_block
        properties:
          - length: variable
          - color: variable (consistent within block)
        behavior: shifts_right
    actions:
      - identify: locate the anchor pixel (azure/8).
      - identify: locate the contiguous movable_block (non-white/0, non-azure/8).
      - determine: record the color and length of the movable_block.
      - calculate: determine the target position for the movable_block. The target end index is the index immediately preceding the anchor pixel's index.
      - transform: place the movable_block at its calculated target position in the output grid, preserving its color and length.
      - transform: place the anchor pixel at its original position in the output grid.
      - transform: fill all other positions with the background color (white/0).
    relationships:
      - adjacency: In the output, the rightmost pixel of the movable_block is adjacent (left side) to the anchor pixel.
      - reference_point: The anchor pixel's position determines the final position of the movable_block.
    ```


*   **Natural Language Program:**
    1.  Initialize an output grid of the same dimensions as the input grid, filled entirely with white (0) pixels.
    2.  Find the index of the single azure (8) pixel in the input grid. Let this be `anchor_index`. Place an azure (8) pixel at `anchor_index` in the output grid.
    3.  Find the contiguous block of pixels in the input grid whose color is not white (0) and not azure (8). Record its color and its length (`block_length`).
    4.  Calculate the target ending index for this block in the output grid as `target_end_index = anchor_index - 1`.
    5.  Calculate the target starting index for this block in the output grid as `target_start_index = target_end_index - block_length + 1`.
    6.  Fill the cells in the output grid from `target_start_index` to `target_end_index` (inclusive) with the recorded color of the block.
```python
import numpy as np

"""
Transforms a 1D input grid by moving a contiguous block of non-background, 
non-anchor color pixels so that its right end is adjacent to the left of a fixed 
anchor pixel (azure/8).

1. Initialize an output grid of the same dimensions as the input grid, 
   filled entirely with white (0) pixels.
2. Find the index of the single azure (8) pixel (anchor) in the input grid. 
   Place an azure (8) pixel at the same index in the output grid.
3. Find the contiguous block of pixels in the input grid whose color is 
   not white (0) and not azure (8). Record its color and its length.
4. Calculate the target position for this block in the output grid such that 
   its rightmost pixel is at the index immediately preceding the anchor pixel's index.
5. Fill the calculated target indices in the output grid with the recorded color 
   of the block.
"""

def find_movable_block(input_array):
    """
    Finds the first contiguous block of color that is not background (0) or anchor (8).
    Returns the color, length, and start index of the block.
    Returns (None, 0, -1) if no such block is found.
    """
    block_color = None
    block_length = 0
    block_start_index = -1
    in_block = False

    for i, pixel in enumerate(input_array):
        is_movable_color = (pixel != 0 and pixel != 8)

        if not in_block and is_movable_color:
            # Start of a new block
            in_block = True
            block_color = pixel
            block_start_index = i
            block_length = 1
        elif in_block:
            if pixel == block_color:
                # Continue the current block
                block_length += 1
            else:
                # End of the block (hit 0, 8, or different color)
                break 
                
    return block_color, block_length, block_start_index

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid: A list of integers representing the 1D input grid.

    Returns:
        A list of integers representing the transformed 1D output grid.
    """
    # Ensure input is a 1D numpy array
    # The input examples are flat lists, directly usable as 1D arrays.
    input_array = np.array(input_grid, dtype=int)
    grid_width = len(input_array)

    # 1. Initialize output grid with background color (0)
    output_grid = np.zeros(grid_width, dtype=int)

    # 2. Find the anchor pixel (azure/8) and place it in the output
    anchor_indices = np.where(input_array == 8)[0]
    if len(anchor_indices) == 0:
        # No anchor found, return the empty grid or handle as error
        # Based on examples, anchor is always present.
        print("Error: Anchor pixel (8) not found.")
        return output_grid.tolist() 
    anchor_index = anchor_indices[0]
    output_grid[anchor_index] = 8

    # 3. Find the contiguous movable block (non-0, non-8)
    block_color, block_length, _ = find_movable_block(input_array)

    if block_color is None:
        # No movable block found, only the anchor is placed.
        # This happens if the input only contains 0s and 8s.
        return output_grid.tolist()

    # 4. Calculate the target end index for the block
    target_end_index = anchor_index - 1

    # 5. Calculate the target start index for the block
    target_start_index = target_end_index - block_length + 1

    # 6. Place the block at the target position in the output grid
    # Ensure indices are within bounds before slicing
    if target_start_index >= 0 and target_end_index < grid_width:
        output_grid[target_start_index : target_end_index + 1] = block_color
    else:
        # Handle cases where the block might partially or fully go out of bounds
        # Based on examples, this doesn't seem to happen, but good to be aware.
        # For now, we only write if the full block fits within valid indices starting >= 0.
        # A more robust solution might clip the block if necessary.
        print(f"Warning: Block placement ({target_start_index} to {target_end_index}) might be out of bounds.")
        # Example: Place only the part that fits
        actual_start = max(0, target_start_index)
        actual_end = min(grid_width - 1, target_end_index)
        length_to_place = actual_end - actual_start + 1
        if length_to_place > 0:
             # Need to figure out which part of the block color sequence to use if clipped
             # Simplest: if start is < 0, fill from 0 up to target_end_index
             if target_start_index < 0:
                 output_grid[0 : target_end_index + 1] = block_color 
             # If end is >= grid_width, fill from target_start_index to end
             elif target_end_index >= grid_width:
                 output_grid[target_start_index : grid_width] = block_color


    # Return the result as a standard Python list
    return output_grid.tolist()
```
