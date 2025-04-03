```python
"""
Transforms the input grid by shifting a specific colored block two steps
to the right, while keeping a distinct 'anchor' pixel stationary.

1. Create a new output grid of the same size as the input grid, and fill it 
   completely with white (0) pixels.
2. Scan the input grid to find the single, contiguous block of pixels that are 
   neither white (0) nor azure (8). Record the color, starting index, and 
   length of this block.
3. Scan the input grid to find the index of the single azure (8) pixel.
4. In the output grid, place the azure (8) pixel at the same index it 
   occupied in the input grid.
5. Calculate the new starting index for the non-white/non-azure block by 
   adding 2 to its original starting index found in step 2.
6. Copy the block (using its color and length found in step 2) into the 
   output grid, beginning at the new starting index calculated in step 5. 
   Ensure that the placement respects the grid boundaries; do not write pixels 
   beyond the end of the grid.
"""

import numpy as np
from typing import List, Tuple, Optional

# Define color constants used in the logic
WHITE = 0
AZURE = 8

def find_movable_block(grid: np.ndarray) -> Optional[Tuple[int, int, int]]:
    """
    Finds the first contiguous block of pixels whose color is not WHITE or AZURE.

    Args:
        grid: A 1D numpy array representing the input grid.

    Returns:
        A tuple containing (start_index, length, color) of the block,
        or None if no such block is found.
    """
    start_index = -1
    length = 0
    color = -1
    in_block = False

    for i, pixel in enumerate(grid):
        # Check if the pixel is part of the movable block
        if pixel != WHITE and pixel != AZURE:
            if not in_block:
                # Start of a new block
                start_index = i
                color = pixel
                length = 1
                in_block = True
            elif pixel == color:
                # Continuation of the current block
                length += 1
            else:
                # Found a different non-white/non-azure color - stop
                # (assuming only one such block per the task examples)
                 break
        elif in_block:
            # End of the block found (encountered WHITE or AZURE after being in a block)
            break

    if start_index != -1:
        return start_index, length, color
    else:
        # No block found
        return None

def find_anchor_pixel(grid: np.ndarray) -> Optional[int]:
    """
    Finds the index of the AZURE pixel.

    Args:
        grid: A 1D numpy array representing the input grid.

    Returns:
        The index of the AZURE pixel, or None if not found.
    """
    for i, pixel in enumerate(grid):
        if pixel == AZURE:
            return i
    return None # Anchor pixel not found

def transform(input_grid: List[int]) -> List[int]:
    """
    Applies the transformation rule to the input grid.
    """
    # Convert input list to numpy array for efficient processing
    grid_np = np.array(input_grid)
    grid_size = len(grid_np)

    # 1. Initialize an output grid of the same size, filled with WHITE
    output_grid_np = np.full(grid_size, WHITE, dtype=int)

    # 2. Find the movable block details
    block_info = find_movable_block(grid_np)
    if block_info is None:
        # If no movable block is found, potentially return the initial white grid
        # or handle as an error depending on expected behavior for invalid inputs.
        # Based on training examples, a block should always exist.
        print("Warning: Movable block not found. Returning empty grid.")
        return output_grid_np.tolist()
    block_start, block_length, block_color = block_info

    # 3. Find the anchor pixel's index
    anchor_index = find_anchor_pixel(grid_np)
    if anchor_index is None:
        # If no anchor pixel is found, handle as an error or return partially processed grid.
        # Based on training examples, an anchor should always exist.
        print("Warning: Anchor pixel (AZURE) not found. Block will still be moved.")
        # Decide whether to proceed or return early. Here we proceed but skip placing the anchor.
        pass # Anchor index remains None


    # 4. Place the anchor pixel in the output grid (if found)
    if anchor_index is not None:
        if 0 <= anchor_index < grid_size:
             output_grid_np[anchor_index] = AZURE
        else:
             # This case should ideally not happen if find_anchor_pixel works correctly
             print(f"Warning: Anchor index {anchor_index} reported out of bounds.")


    # 5. Calculate the new starting index for the movable block
    new_block_start = block_start + 2

    # 6. Place the movable block in the output grid at the new location, handling boundaries
    # Calculate the actual start and end indices within the grid bounds
    actual_start_index = max(0, new_block_start) # Don't start before index 0
    actual_end_index = min(new_block_start + block_length, grid_size) # Don't go past the grid size

    # Place the block only if the calculated indices are valid and define a non-empty slice
    if actual_start_index < actual_end_index:
         # Determine how many pixels of the block actually fit
         num_pixels_to_place = actual_end_index - actual_start_index
         # Place the block color into the calculated slice
         output_grid_np[actual_start_index : actual_end_index] = block_color


    # Convert the final numpy array back to a list for the expected output format
    output_grid = output_grid_np.tolist()

    return output_grid
```