
## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 4 4 4 0 0 6 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 4 4 4 6 0
```


## train_2

**input:**
```
0 0 0 8 8 8 8 8 0 0 0 0 0 0 6 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 8 8 8 8 8 6 0 0 0 0 0 0
```


## train_3

**input:**
```
0 0 0 0 0 0 1 1 1 1 1 1 0 0 0 0 0 0 0 6 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 1 1 1 1 1 1 6 0
```

Okay, let's analyze the provided examples.

## Perception

The input and output are single-row grids (1D arrays) of pixels.
Each input grid contains:
1.  A background of white pixels (color 0).
2.  A single magenta pixel (color 6).
3.  A contiguous horizontal block of pixels of *another* color (yellow, azure, or blue in the examples).

The transformation involves moving the contiguous block horizontally.
Specifically, the block shifts to the right.
The final position of the block is such that its rightmost pixel is immediately adjacent to the left side of the single magenta pixel.
The space originally occupied by the block becomes white (background color).
The magenta pixel and all other white pixels (that were not part of the moved block's original location) remain in their original positions.

## Facts


```yaml
task_type: object_manipulation
grid_dimensionality: 1D (single row)
component_identification:
  - object: background
    properties:
      color: white (0)
      role: static_area
  - object: target_pixel
    properties:
      color: magenta (6)
      shape: single_pixel
      count: 1
      role: anchor_point
  - object: movable_block
    properties:
      color: non-white, non-magenta (variable: yellow, azure, blue in examples)
      shape: contiguous_horizontal_block
      count: 1
      role: object_to_be_moved
transformation:
  action: horizontal_shift
  direction: right
  affected_object: movable_block
  shift_rule: Move the movable_block rightwards until its rightmost pixel is located at the column index immediately preceding the column index of the target_pixel.
  post_action:
    - Fill the original location of the movable_block with background (white) pixels.
relationships:
  - type: spatial_adjacency
    object1: movable_block (rightmost pixel)
    object2: target_pixel
    condition_in_output: object1 is immediately to the left of object2.
invariants:
  - grid_dimensions
  - position_of_target_pixel
  - position_of_background_pixels (excluding those replaced by the moved block or those filling the block's original space)
  - color_of_target_pixel
  - color_of_movable_block
  - length_of_movable_block
```


## Natural Language Program

1.  Identify the grid dimensions (which remain constant).
2.  Locate the position (column index) of the single magenta pixel (color 6). This is the target position's right boundary.
3.  Identify the contiguous horizontal block of non-white, non-magenta pixels. Note its color, starting column index, and ending column index (length).
4.  Create a new grid of the same dimensions, initially filled with the background color (white, 0).
5.  Place the magenta pixel (color 6) in the new grid at its original column index.
6.  Determine the new starting column index for the identified block. This will be `(magenta_pixel_index - block_length)`.
7.  Place the block (using its original color and length) into the new grid starting at this new calculated index and ending at the index immediately before the magenta pixel (`magenta_pixel_index - 1`).
8.  Fill any remaining positions in the new grid with the background color (white, 0), ensuring positions already filled by the block or the magenta pixel are not overwritten. (Step 4 handles most of this, this is just a clarification).
9.  The resulting grid is the output.
```python
import numpy as np
from typing import List, Tuple, Optional

"""
Transforms a 1D input grid by shifting a contiguous block of a non-white, non-magenta color to the right, placing its rightmost edge immediately adjacent to the left of the single magenta pixel. The original position of the block becomes white.
"""

def find_pixel_index(grid: np.ndarray, color: int) -> Optional[int]:
    """Finds the index of the first occurrence of a specific color pixel."""
    indices = np.where(grid == color)[0]
    if len(indices) > 0:
        return indices[0]
    return None

def find_block(grid: np.ndarray, exclude_colors: List[int]) -> Optional[Tuple[int, int, int, int]]:
    """
    Finds the first contiguous block of pixels whose color is not in exclude_colors.
    Returns (start_index, end_index_exclusive, length, color).
    """
    block_color = -1
    start_index = -1
    for i, pixel in enumerate(grid):
        if pixel not in exclude_colors:
            if start_index == -1:
                start_index = i
                block_color = pixel
            elif pixel != block_color: # End of block (different color)
                 end_index = i
                 length = end_index - start_index
                 return start_index, end_index, length, block_color
        elif start_index != -1: # End of block (excluded color encountered)
            end_index = i
            length = end_index - start_index
            return start_index, end_index, length, block_color
    # Check if block runs to the end of the grid
    if start_index != -1:
        end_index = len(grid)
        length = end_index - start_index
        return start_index, end_index, length, block_color
    return None # No block found


def transform(input_grid: List[int]) -> List[int]:
    """
    Shifts a colored block rightwards to be adjacent to the magenta pixel.

    Args:
        input_grid: A list representing the 1D input grid.

    Returns:
        A list representing the transformed 1D output grid.
    """
    # Convert input list to numpy array for easier manipulation
    grid_np = np.array(input_grid)
    grid_length = len(grid_np)

    # --- Identify components ---
    # Find the magenta pixel (anchor point)
    magenta_color = 6
    magenta_index = find_pixel_index(grid_np, magenta_color)
    if magenta_index is None:
        # Handle error: magenta pixel not found (shouldn't happen based on examples)
        print("Error: Magenta pixel not found.")
        return input_grid # Or raise an exception

    # Find the movable block (excluding white 0 and magenta 6)
    block_info = find_block(grid_np, [0, magenta_color])
    if block_info is None:
         # Handle error: movable block not found (shouldn't happen based on examples)
        print("Error: Movable block not found.")
        return input_grid # Or raise an exception

    block_start, block_end, block_length, block_color = block_info

    # --- Create the output grid ---
    # Initialize output grid with background color (white 0)
    output_grid_np = np.zeros(grid_length, dtype=int)

    # Place the magenta pixel in its original position
    output_grid_np[magenta_index] = magenta_color

    # --- Calculate the new position for the block ---
    # The block should end right before the magenta pixel
    new_block_end = magenta_index
    new_block_start = new_block_end - block_length

    # --- Place the block in the new position ---
    if new_block_start >= 0: # Ensure the block fits within the grid bounds
        output_grid_np[new_block_start:new_block_end] = block_color
    else:
        # Handle case where block would shift off the left edge (unlikely given examples)
        print("Warning: Block shifts partially or fully off the grid.")
        actual_start = 0
        visible_length = new_block_end - actual_start
        output_grid_np[actual_start:new_block_end] = block_color # Place the visible part


    # Convert numpy array back to list for the final output
    output_grid = output_grid_np.tolist()

    return output_grid

```
```python
import numpy as np
from typing import List, Tuple, Optional

"""
Transforms a 1D input grid by:
1. Identifying a single 'anchor' pixel (magenta, color 6) which remains stationary.
2. Identifying a contiguous horizontal block of a single color (neither white 0 nor magenta 6).
3. Shifting this block horizontally to the right so that its rightmost pixel is positioned immediately to the left of the anchor pixel.
4. Filling the original location of the shifted block with the background color (white, 0).
The output grid has the same dimensions as the input grid.
"""

def find_pixel_index(grid: np.ndarray, color: int) -> Optional[int]:
    """
    Finds the index of the first occurrence of a specific color pixel in a 1D grid.

    Args:
        grid: The 1D numpy array representing the grid.
        color: The color value to search for.

    Returns:
        The index of the first pixel with the specified color, or None if not found.
    """
    indices = np.where(grid == color)[0]
    if len(indices) > 0:
        return indices[0]
    return None

def find_block(grid: np.ndarray, exclude_colors: List[int]) -> Optional[Tuple[int, int, int, int]]:
    """
    Finds the first contiguous block of pixels in a 1D grid whose color is not in exclude_colors.

    Args:
        grid: The 1D numpy array representing the grid.
        exclude_colors: A list of color values to ignore when searching for the block.

    Returns:
        A tuple (start_index, end_index_exclusive, length, color) of the block,
        or None if no such block is found.
    """
    block_color = -1
    start_index = -1
    for i, pixel_color in enumerate(grid):
        is_excluded = pixel_color in exclude_colors
        if not is_excluded:
            # Found a potential block pixel
            if start_index == -1:
                # Start of a new block
                start_index = i
                block_color = pixel_color
            elif pixel_color != block_color:
                # Found a different non-excluded color, meaning the previous block ended.
                # This scenario assumes only one movable block exists per grid as per examples.
                end_index = i
                length = end_index - start_index
                return start_index, end_index, length, block_color
        elif start_index != -1:
            # Found an excluded color after a block started, meaning the block ended.
            end_index = i
            length = end_index - start_index
            return start_index, end_index, length, block_color

    # Check if a block was found and ran to the end of the grid
    if start_index != -1:
        end_index = len(grid)
        length = end_index - start_index
        return start_index, end_index, length, block_color

    # No block found
    return None


def transform(input_grid: List[int]) -> List[int]:
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid: A list representing the 1D input grid.

    Returns:
        A list representing the transformed 1D output grid.
    """
    # Convert input list to numpy array for easier manipulation
    grid_np = np.array(input_grid, dtype=int)
    grid_length = len(grid_np)
    background_color = 0
    anchor_color = 6

    # --- Initialize Output ---
    # Create a new grid filled with the background color
    output_grid_np = np.full(grid_length, background_color, dtype=int)

    # --- Identify Anchor ---
    # Locate the index of the magenta anchor pixel
    anchor_index = find_pixel_index(grid_np, anchor_color)
    if anchor_index is None:
        # Handle error: anchor pixel not found (should not happen based on examples)
        # Returning the input or an empty grid might be options depending on requirements.
        print(f"Error: Anchor pixel (color {anchor_color}) not found.")
        return input_grid # Return original grid as fallback

    # --- Place Anchor ---
    # Copy the anchor pixel to the output grid at its original position
    output_grid_np[anchor_index] = anchor_color

    # --- Identify Block ---
    # Find the movable block (excluding background and anchor colors)
    block_info = find_block(grid_np, [background_color, anchor_color])
    if block_info is None:
         # Handle error: movable block not found (should not happen based on examples)
        print(f"Error: Movable block not found (excluding colors {background_color}, {anchor_color}).")
        # If no block, the output is just the background + anchor
        return output_grid_np.tolist()

    block_start_in, block_end_in, block_length, block_color = block_info

    # --- Calculate New Position ---
    # Determine the target start index for the block in the output grid.
    # The block ends just before the anchor pixel.
    new_block_end_exclusive = anchor_index
    new_block_start = new_block_end_exclusive - block_length

    # --- Place Block ---
    # Fill the calculated position in the output grid with the block's color.
    # Ensure the calculated start index is valid.
    if new_block_start >= 0:
        output_grid_np[new_block_start:new_block_end_exclusive] = block_color
    else:
        # This case means the block would shift partially or fully off the left edge.
        # Based on examples, this might not occur, but handle defensively.
        # Place only the part of the block that fits on the grid.
        actual_start = 0
        visible_length = new_block_end_exclusive - actual_start
        if visible_length > 0:
             output_grid_np[actual_start:new_block_end_exclusive] = block_color
        print(f"Warning: Block (color {block_color}) shifted partially off-grid.")


    # --- Finalize ---
    # Convert the numpy array back to a list for the final output
    output_grid = output_grid_np.tolist()

    return output_grid
```
