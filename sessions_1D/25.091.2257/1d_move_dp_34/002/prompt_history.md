
## train_1

**input:**
```
0 0 0 0 0 0 6 6 6 6 0 0 0 3 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 6 6 6 6 3 0
```


## train_2

**input:**
```
0 2 2 2 0 0 0 0 0 0 3 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 2 2 2 3 0 0 0 0
```


## train_3

**input:**
```
0 8 8 8 8 8 0 0 0 0 0 0 0 0 3
```


**output:**
```
0 0 0 0 0 0 0 0 0 8 8 8 8 8 3
```

**Perception**

1.  **Grid Structure**: The inputs and outputs are single-row grids (1D arrays).
2.  **Background**: The predominant color is white (0), acting as the background.
3.  **Objects**: Each input grid contains two distinct non-white elements:
    *   A contiguous block (or "object") of a single color (magenta 6, red 2, or azure 8). The length of this block varies across examples.
    *   A single green pixel (3).
4.  **Transformation**: The primary transformation is the horizontal movement (translation) of the colored block.
5.  **Movement Rule**: The colored block moves to the right.
6.  **Stopping Condition**: The movement stops when the rightmost pixel of the colored block is positioned immediately to the left of the single green pixel.
7.  **Invariance**: The green pixel's position remains unchanged. The size and color of the moving block remain unchanged. The overall size of the grid remains unchanged. The pixels previously occupied by the block become white (0).

**Facts**


```yaml
task_type: object_manipulation
grid_dimensionality: 1D
background_color: 0 # white
objects:
  - type: contiguous_block
    properties:
      color: any non-white, non-green color (e.g., 6, 2, 8)
      size: variable length (e.g., 4, 3, 5)
      role: mobile_object
  - type: single_pixel
    properties:
      color: 3 # green
      role: boundary_marker
relationship:
  - type: spatial_adjacency
    description: In the output, the rightmost pixel of the mobile_object is immediately to the left of the boundary_marker.
transformation:
  - type: translation
    target: mobile_object
    direction: right
    termination_condition: adjacency to boundary_marker
    properties:
      preserves_shape: True
      preserves_color: True
      overwrites_original_position: True (with background color)
invariants:
  - element: boundary_marker
    property: position
  - element: grid
    property: size
```


**Natural Language Program**

1.  Identify the background color (white, 0).
2.  Identify the single green pixel (3) and note its index; this is the `marker_index`.
3.  Identify the contiguous block of non-white, non-green pixels. Note its color, its starting index (`start_index`), and its ending index (`end_index`). Calculate its length (`length = end_index - start_index + 1`).
4.  Create a new output grid of the same size as the input grid, initially filled with the background color (white, 0).
5.  Place the green pixel (3) in the output grid at the `marker_index`.
6.  Calculate the target ending index for the block in the output grid: `target_end_index = marker_index - 1`.
7.  Calculate the target starting index for the block in the output grid: `target_start_index = target_end_index - length + 1`.
8.  Copy the identified block (using its original color and length) into the output grid starting at `target_start_index` and ending at `target_end_index`.
```python
import numpy as np
from typing import List, Tuple, Optional, Set

"""
Identifies a contiguous block of a single non-white, non-green color and a single green pixel (3) in a 1D input grid.
Moves the colored block to the right until its rightmost edge is immediately adjacent to the left of the green pixel.
The green pixel's position remains fixed. The background is white (0).
"""

def find_contiguous_block(grid_1d: np.ndarray, exclude_colors: Set[int]) -> Optional[Tuple[int, int, int]]:
    """
    Finds the first contiguous block of a single color not in exclude_colors.

    Args:
        grid_1d: 1D numpy array representing the grid row.
        exclude_colors: A set of colors to ignore when searching for the block.

    Returns:
        A tuple (start_index, end_index, color) if a block is found, otherwise None.
    """
    start_index = -1
    block_color = -1
    for i, pixel in enumerate(grid_1d):
        if pixel not in exclude_colors:
            if start_index == -1: # Start of a potential block
                start_index = i
                block_color = pixel
            elif pixel != block_color: # End of the block (different color)
                return start_index, i - 1, block_color
        elif start_index != -1: # End of the block (excluded color encountered)
            return start_index, i - 1, block_color
    # Check if the block extends to the end of the grid
    if start_index != -1:
        return start_index, len(grid_1d) - 1, block_color
    return None

def find_pixel_index(grid_1d: np.ndarray, color: int) -> Optional[int]:
    """
    Finds the index of the first occurrence of a specific color.

    Args:
        grid_1d: 1D numpy array representing the grid row.
        color: The color to find.

    Returns:
        The index of the color if found, otherwise None.
    """
    indices = np.where(grid_1d == color)[0]
    if len(indices) > 0:
        return indices[0]
    return None

def transform(input_grid: List[List[int]]) -> List[List[int]]:
    """
    Transforms the input grid by moving a colored block next to a green marker.

    Args:
        input_grid: A list containing a single list (representing the 1D grid).

    Returns:
        A list containing a single list representing the transformed 1D grid.
    """
    # Ensure input is treated as a 1D array
    if not input_grid or not isinstance(input_grid[0], list):
         # Handle empty or incorrectly formatted input if necessary
         # For this specific task, assuming input is always [[...]]
         # If it could be just [...] then adjust handling.
         # Let's assume valid ARC format [[...]] for 1D row
         if isinstance(input_grid, list) and len(input_grid)>0 and isinstance(input_grid[0],int):
             # handle case of input being just a list of ints
             input_row = np.array(input_grid, dtype=int)
         else:
             # standard case
             input_row = np.array(input_grid[0], dtype=int)
    else:
         input_row = np.array(input_grid[0], dtype=int)


    grid_width = len(input_row)
    background_color = 0
    marker_color = 3

    # 1. Initialize output grid with background color
    output_row = np.full(grid_width, background_color, dtype=int)

    # 2. Find the marker pixel (green)
    marker_index = find_pixel_index(input_row, marker_color)
    if marker_index is None:
        # Should not happen based on examples, but handle defensively
        # Return input or empty grid? Let's return initialized output.
        return [output_row.tolist()] # Return as list of lists

    # 3. Place the marker pixel in the output grid
    output_row[marker_index] = marker_color

    # 4. Find the contiguous colored block (excluding background and marker)
    block_info = find_contiguous_block(input_row, {background_color, marker_color})
    if block_info is None:
        # No block found, return grid with just the marker
        return [output_row.tolist()] # Return as list of lists

    start_index, end_index, block_color = block_info
    block_length = end_index - start_index + 1

    # 5. Calculate the target position for the block in the output grid
    # The block should end right before the marker
    target_end_index = marker_index - 1
    target_start_index = target_end_index - block_length + 1

    # 6. Check if the target position is valid (within grid bounds)
    if target_start_index < 0 or target_end_index >= grid_width:
         # This case shouldn't occur if logic is correct and marker isn't at pos 0
         # or block is too large, but handle defensively.
         print(f"Warning: Calculated target position {target_start_index}-{target_end_index} is out of bounds for grid width {grid_width}.")
         # Decide how to handle: return current output, raise error, etc.
         # For now, proceed but slicing might behave unexpectedly or error out.
         # Let's just place what fits, although problem description implies it always fits.
         pass # Slicing below will handle boundary conditions partially

    # 7. Place the block in the output grid at the target position
    # Ensure indices are valid before slicing
    if target_start_index >= 0 and target_end_index < grid_width and target_start_index <= target_end_index:
         output_row[target_start_index : target_end_index + 1] = block_color


    # Return the result as a list of lists
    return [output_row.tolist()]
```
