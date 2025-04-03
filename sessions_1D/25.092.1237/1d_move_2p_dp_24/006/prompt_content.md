
Previous Code:
```python
import numpy as np
from typing import Tuple, Optional

"""
Transformation Rule:
1. Locate the unique target pixel (green=3) in the 1D input NumPy array.
2. Scan leftwards from the target pixel to identify a contiguous block of background pixels (white=0). This is the 'gap'. Determine its start index, end index, and size. If no gap exists immediately to the left of the target, the transformation is not applied.
3. Identify the contiguous block of a single non-background, non-target color located immediately to the left of the gap's start index. This is the 'movable block'. Determine its start and end indices.
4. If both a gap (size > 0) and a movable block are found in the expected adjacent configuration:
   a. Extract four segments:
      i. Pixels before the movable block.
      ii. The pixels of the movable block.
      iii. The pixels of the gap.
      iv. Pixels from the target pixel to the end of the array.
   b. Reconstruct the array by concatenating the segments in the order: (pixels before block) + (gap pixels) + (movable block pixels) + (pixels from target onwards).
5. If no gap is found (size == 0) or the expected block/gap structure is not present, return the original input array unchanged.
"""

def find_target_pixel(grid: np.ndarray, target_color: int) -> Optional[int]:
    """Finds the index of the first occurrence of the target color."""
    indices = np.where(grid == target_color)[0]
    if len(indices) > 0:
        return indices[0]
    return None

def find_gap(grid: np.ndarray, target_index: int, background_color: int) -> Tuple[Optional[int], Optional[int], int]:
    """
    Finds the contiguous block of background pixels immediately left of the target index.
    Returns (gap_start_index, gap_end_index, gap_size).
    Returns (None, None, 0) if no gap is found immediately left.
    """
    gap_end_index = target_index - 1
    gap_start_index = None
    gap_size = 0

    if gap_end_index < 0: # Target is at the beginning
        return None, None, 0

    current_index = gap_end_index
    while current_index >= 0 and grid[current_index] == background_color:
        gap_start_index = current_index
        gap_size += 1
        current_index -= 1

    if gap_size > 0:
        return gap_start_index, gap_end_index, gap_size
    else:
        # No background pixel found immediately left of target
        return None, None, 0

def find_movable_block(grid: np.ndarray, gap_start_index: Optional[int], background_color: int, target_color: int) -> Tuple[Optional[int], Optional[int]]:
    """
    Finds the contiguous block of non-background, non-target color immediately left of the gap's start index.
    Returns (block_start_index, block_end_index).
    Returns (None, None) if no block is found or gap_start_index is None/0.
    """
    if gap_start_index is None or gap_start_index == 0:
        # Gap doesn't exist or is at the very beginning, no space for a block before it
        return None, None

    block_end_index = gap_start_index - 1
    block_color = grid[block_end_index]

    # Check if the potential block color is valid
    if block_color == background_color or block_color == target_color:
        return None, None # Found background or target color where block should be

    # Scan left from the block end to find the start of the block
    block_start_index = block_end_index
    current_index = block_end_index - 1
    while current_index >= 0 and grid[current_index] == block_color:
        block_start_index = current_index
        current_index -= 1

    return block_start_index, block_end_index


def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Applies the transformation rule to swap a colored block and a background gap
    located immediately to the left of a target pixel (3).
    """
    # Configuration
    target_color = 3
    background_color = 0

    # Ensure input is a NumPy array
    if not isinstance(input_grid, np.ndarray):
        input_grid = np.array(input_grid)

    # Make a copy to avoid modifying the original input if no transformation occurs
    output_grid = input_grid.copy()

    # 1. Find the target pixel
    target_index = find_target_pixel(output_grid, target_color)
    if target_index is None:
        # print(f"Debug: Target color {target_color} not found.")
        return output_grid # Return copy of original input

    # 2. Find the gap immediately left of the target
    gap_start_index, gap_end_index, gap_size = find_gap(output_grid, target_index, background_color)

    # 3. If no gap exists, return the original grid unchanged
    if gap_size == 0:
        # print(f"Debug: No gap found left of target at index {target_index}.")
        return output_grid # Return copy of original input

    # 4. Find the movable block immediately left of the gap
    block_start_index, block_end_index = find_movable_block(output_grid, gap_start_index, background_color, target_color)

    # 5. If no valid block is found before the gap, return the original grid unchanged
    if block_start_index is None:
        # print(f"Debug: No valid movable block found left of gap starting at index {gap_start_index}.")
        return output_grid # Return copy of original input

    # 6. Extract the segments for rearrangement
    pixels_before_block = output_grid[:block_start_index]
    movable_block_pixels = output_grid[block_start_index : block_end_index + 1]
    gap_pixels = output_grid[gap_start_index : gap_end_index + 1]
    # Include the target pixel and everything after it
    pixels_after_inclusive = output_grid[target_index:]

    # 7. Construct the output grid by concatenating segments in the new order
    # Order: (Pixels before block) + (Gap pixels) + (Movable block pixels) + (Pixels from target onwards)
    transformed_grid = np.concatenate((
        pixels_before_block,
        gap_pixels,
        movable_block_pixels,
        pixels_after_inclusive
    ))

    return transformed_grid
```
Results for code_00.py:

Train Set Results:

## Example 1:
Input:
```
0 0 0 0 0 0 2 2 2 2 2 2 2 2 2 2 2 2 0 0 3 0 0 0 0 0
```
Expected Output:
```
0 0 0 0 0 0 0 0 2 2 2 2 2 2 2 2 2 2 2 2 3 0 0 0 0 0
```
Transformed Output:
```
0 0 0 0 0 0 2 2 2 2 2 2 2 2 2 2 2 2 0 0 3 0 0 0 0 0
```
Match: False
Pixels Off: 4
Size Correct: True
Color Palette Correct: True
Color Count Correct: True
Score: 15.384615384615387

## Example 2:
Input:
```
0 0 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 0 0 3 0 0 0
```
Expected Output:
```
0 0 0 0 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 3 0 0 0
```
Transformed Output:
```
0 0 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 0 0 3 0 0 0
```
Match: False
Pixels Off: 4
Size Correct: True
Color Palette Correct: True
Color Count Correct: True
Score: 15.384615384615387

## Example 3:
Input:
```
0 0 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 0 0 3 0 0 0 0 0
```
Expected Output:
```
0 0 0 0 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 3 0 0 0 0 0
```
Transformed Output:
```
0 0 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 0 0 3 0 0 0 0 0
```
Match: False
Pixels Off: 4
Size Correct: True
Color Palette Correct: True
Color Count Correct: True
Score: 15.384615384615387
