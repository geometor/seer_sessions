
## train_1

**input:**
```
0 0 0 0 0 0 2 2 2 2 2 2 2 2 2 2 2 2 0 0 3 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 2 2 2 2 2 2 2 2 2 2 2 2 3 0 0 0 0 0
```


## train_2

**input:**
```
0 0 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 0 0 3 0 0 0
```


**output:**
```
0 0 0 0 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 3 0 0 0
```


## train_3

**input:**
```
0 0 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 0 0 3 0 0 0 0 0
```


**output:**
```
0 0 0 0 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 3 0 0 0 0 0
```

Okay, let's analyze the provided task example (`train_1`).

**Perception of the Elements:**

1.  **Input/Output Format:** Both input and output are presented as 1D arrays (or single rows) of integers representing colors. The length remains constant (26 elements).
2.  **Key Colors/Objects:**
    *   **White Pixels (0):** These act as the background or empty space.
    *   **Red Block (2):** In the input, there's a contiguous block of 12 red pixels (`2 2 2 2 2 2 2 2 2 2 2 2`).
    *   **Green Pixel (3):** There is a single green pixel. It appears relatively late in the array.
3.  **Spatial Relationships (Input):**
    *   The red block starts after 6 white pixels.
    *   There are 2 white pixels between the end of the red block and the single green pixel.
    *   The green pixel is followed by 5 white pixels.
4.  **Transformation:**
    *   The red block's position changes between input and output.
    *   The green pixel's position remains the same (index 20 in both).
    *   The number and color of pixels in the red block remain unchanged (12 red pixels).
    *   The number of white pixels remains unchanged overall, but their distribution shifts.
5.  **Observed Change Detail:** The red block shifts 2 positions to the right. In the input, it spans indices 6-17. In the output, it spans indices 8-19. The 2 white pixels originally between the red block and the green pixel (at indices 18, 19) are effectively relocated to the positions previously occupied by the start of the red block (indices 6, 7). The result is that the red block becomes immediately adjacent to the green pixel on its left.

**YAML Facts:**


```yaml
task_type: array_manipulation_1d
components:
  - type: background
    color: white (0)
  - type: target_marker
    color: green (3)
    quantity: 1
    role: static anchor point
  - type: movable_block
    description: A contiguous block of non-white pixels immediately preceding the target_marker (potentially separated by background pixels).
    properties:
      color: variable (red=2 in example)
      contiguity: required
      position: left of target_marker
  - type: gap
    description: Contiguous block of background (white) pixels between the movable_block and the target_marker.
    properties:
      color: white (0)
      size: variable (2 in example)
      role: determines shift distance
actions:
  - name: identify_target
    actor: system
    target: target_marker (green=3)
  - name: identify_movable_block
    actor: system
    target: non-white block left of target_marker
  - name: measure_gap
    actor: system
    target: white pixels between movable_block and target_marker
  - name: shift_block
    actor: movable_block
    direction: right
    distance: size of the gap
    effect: closes the gap, makes movable_block adjacent to target_marker
relationships:
  - type: adjacency
    entity1: movable_block
    entity2: target_marker
    state: initially separated by gap, finally adjacent
  - type: dependency
    variable: shift_distance
    depends_on: size of the gap
```


**Natural Language Program:**

1.  Scan the input array from left to right to locate the unique green (3) pixel. This is the 'target pixel'.
2.  Starting from the position immediately to the left of the target pixel, scan leftwards.
3.  Identify the first sequence of one or more white (0) pixels encountered. This is the 'gap'. Record its size (number of white pixels). If no white pixels are found before a non-white pixel, the gap size is 0.
4.  Continue scanning leftwards from the beginning of the gap (or from the position left of the target pixel if the gap size was 0) to identify the contiguous block of non-white pixels. This is the 'movable block'. Record its start index, end index, and the sequence of colors within it.
5.  Construct the output array:
    a.  Copy all pixels from the start of the input array up to (but not including) the start index of the movable block.
    b.  Append a sequence of white (0) pixels equal in length to the recorded gap size.
    c.  Append the sequence of pixels corresponding to the movable block.
    d.  Append the target pixel (green = 3).
    e.  Append all remaining pixels from the input array that were originally positioned after the target pixel.
6.  The resulting array is the final output.
```python
import numpy as np
from typing import List

"""
Transformation Rule:
1. Locate the unique target pixel (green=3).
2. Identify the contiguous block of non-background (non-white=0) pixels immediately to the left of the target pixel. This is the 'movable block'.
3. Identify the contiguous block of background (white=0) pixels, if any, situated between the movable block and the target pixel. This is the 'gap'.
4. Determine the size of the gap (number of white pixels).
5. Shift the 'movable block' to the right by a distance equal to the size of the gap, effectively closing the gap and making the movable block adjacent to the target pixel.
6. The relative order and content of all other pixels (background pixels before the movable block, the target pixel itself, and pixels after the target pixel) remain unchanged.
"""

def find_target_pixel(grid: List[int], target_color: int) -> int:
    """Finds the index of the first occurrence of the target color."""
    try:
        return grid.index(target_color)
    except ValueError:
        raise ValueError(f"Target color {target_color} not found in grid.")

def find_movable_block_and_gap(grid: List[int], target_index: int) -> tuple[int, int, int]:
    """
    Finds the start and end indices of the movable block and the size of the gap.
    Scans leftwards from the target pixel.
    Returns (block_start_index, block_end_index, gap_size).
    """
    block_end_index = -1
    gap_size = 0
    
    # Scan left from the target to find the end of the block and the gap
    current_index = target_index - 1
    while current_index >= 0 and grid[current_index] == 0:
        gap_size += 1
        current_index -= 1
        
    # If we found non-background pixels, the last non-background index is the block end
    if current_index >= 0 and grid[current_index] != 0:
        block_end_index = current_index
        block_color = grid[block_end_index]
    else:
        # No movable block found immediately preceded by only background
        # Or the block is at the very beginning after background
        if current_index >= 0 : # found non-zero block_color before potential gap
             block_end_index = current_index
        else: # reached beginning of array while only seeing 0s
            # This case might indicate no movable block or an error in assumptions
            # Based on examples, there's always a block. Let's assume block_end_index must be >= 0.
            # If block_end_index remains -1, it implies no block was found left of the target separated only by optional whitespace.
            # This shouldn't happen based on provided examples.
             raise ValueError("Could not find end of movable block.")


    # Scan left from the block end to find the start of the block
    block_start_index = block_end_index
    block_color = grid[block_end_index]
    current_index = block_end_index - 1
    while current_index >= 0 and grid[current_index] == block_color:
        block_start_index = current_index
        current_index -= 1
        
    return block_start_index, block_end_index, gap_size

def transform(input_grid: List[int]) -> List[int]:
    """
    Applies the transformation rule to the input grid (1D list).
    Finds a target pixel (3), identifies a block to its left, measures the gap
    between them, and shifts the block right to close the gap.
    """
    
    # Configuration
    target_color = 3
    background_color = 0

    # 1. Find the target pixel
    try:
        target_index = find_target_pixel(input_grid, target_color)
    except ValueError as e:
        print(f"Error: {e}")
        # Decide how to handle missing target: return input? raise error?
        return input_grid # Or raise e

    # 2. Find the movable block and the gap size
    try:
        block_start_index, block_end_index, gap_size = find_movable_block_and_gap(input_grid, target_index)
    except ValueError as e:
         print(f"Error: {e}")
         # Handle case where block/gap structure isn't as expected
         return input_grid # Or raise e

    # If gap_size is 0, the block is already adjacent, no transformation needed
    if gap_size == 0:
        return input_grid[:] # Return a copy

    # 3. Extract the different segments of the input grid
    pixels_before_block = input_grid[:block_start_index]
    movable_block_pixels = input_grid[block_start_index : block_end_index + 1]
    # Gap pixels are implicitly handled by the gap_size
    target_pixel = [input_grid[target_index]] # Should be [target_color]
    pixels_after_target = input_grid[target_index + 1:]

    # 4. Construct the output grid
    # New arrangement: pixels before block + new gap (at original block location) + block + target + pixels after target
    
    # Create the filler for the space originally occupied by the block start
    newly_empty_space = [background_color] * gap_size 
    
    output_grid = pixels_before_block + newly_empty_space + movable_block_pixels + target_pixel + pixels_after_target

    return output_grid

```
```python
import numpy as np
from typing import List, Tuple, Optional

"""
Transformation Rule:
1. Locate the unique target pixel (green=3) in the 1D input NumPy array.
2. Identify the block of two background pixels (white=0) immediately to the left of the target pixel. This is the 'fixed gap'.
3. Identify the contiguous block of a single non-white, non-green color located immediately to the left of the fixed gap. This is the 'movable block'.
4. Determine the start and end indices of the movable block.
5. Construct the output array by rearranging segments:
   a. Pixels originally before the movable block.
   b. The two white background pixels (representing the gap shifted left).
   c. The movable block pixels.
   d. The target pixel.
   e. Pixels originally after the target pixel.
Essentially, the movable block shifts right by two positions, closing the gap next to the target pixel, and the gap (two white pixels) fills the space where the block started its shift.
"""

def find_target_pixel_np(grid: np.ndarray, target_color: int) -> Optional[int]:
    """
    Finds the index of the first occurrence of the target color in a 1D NumPy array.
    Returns the index or None if not found.
    """
    indices = np.where(grid == target_color)[0]
    if len(indices) > 0:
        return indices[0]  # Return the first index found
    return None

def find_movable_block_np(grid: np.ndarray, target_index: int, background_color: int) -> Optional[Tuple[int, int]]:
    """
    Finds the start and end indices of the movable block based on its expected position
    relative to the target pixel and the fixed gap of size 2.
    Returns (start_index, end_index) or None if the structure is not found.
    """
    # Expected end of the block is 3 positions left of the target
    expected_block_end_index = target_index - 3
    
    # Basic boundary checks
    if expected_block_end_index < 0:
        print(f"Error: Expected block end index {expected_block_end_index} is out of bounds.")
        return None
        
    # Check if the gap pixels are indeed background color
    if target_index < 2 or grid[target_index - 1] != background_color or grid[target_index - 2] != background_color:
        print(f"Error: Expected gap pixels at {target_index - 1}, {target_index - 2} are not background color.")
        return None
        
    # Get the color of the block
    block_color = grid[expected_block_end_index]
    
    # Check if block color is valid (not background, not target)
    # Note: target_color check isn't strictly needed based on problem description, but good practice.
    if block_color == background_color: # or block_color == target_color:
        print(f"Error: Pixel at expected block end {expected_block_end_index} is background color.")
        return None

    # Scan left from the block end to find the start of the block
    block_start_index = expected_block_end_index
    current_index = expected_block_end_index - 1
    while current_index >= 0 and grid[current_index] == block_color:
        block_start_index = current_index
        current_index -= 1
        
    return block_start_index, expected_block_end_index


def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Applies the transformation rule to the input 1D NumPy array.
    Finds a target pixel (3), identifies a block to its left separated by a gap of 2,
    and shifts the block right by 2 positions to close the gap.
    """
    
    # Configuration
    target_color = 3
    background_color = 0
    gap_size = 2

    # 1. Find the target pixel index
    target_index = find_target_pixel_np(input_grid, target_color)
    
    if target_index is None:
        print(f"Error: Target color {target_color} not found.")
        return input_grid.copy() # Return a copy of the input if target not found

    # 2. Find the movable block's start and end indices
    block_indices = find_movable_block_np(input_grid, target_index, background_color)

    if block_indices is None:
         print(f"Error: Could not find the expected movable block structure.")
         # Handle case where block/gap structure isn't as expected
         return input_grid.copy() # Return a copy of the input

    block_start_index, block_end_index = block_indices

    # 3. Extract the different segments of the input grid using NumPy slicing
    pixels_before_block = input_grid[:block_start_index]
    movable_block_pixels = input_grid[block_start_index : block_end_index + 1]
    # The gap pixels are implicitly input_grid[block_end_index + 1 : target_index]
    target_pixel = input_grid[target_index:target_index+1] # Use slice to keep it as an array
    pixels_after_target = input_grid[target_index + 1:]

    # 4. Define the new gap segment (to be placed where the block started shifting)
    new_gap_segment = np.full(gap_size, background_color, dtype=input_grid.dtype)

    # 5. Construct the output grid by concatenating segments in the new order
    # Order: (Pixels before block) + (New gap) + (Movable block) + (Target pixel) + (Pixels after target)
    output_grid = np.concatenate((
        pixels_before_block,
        new_gap_segment,
        movable_block_pixels,
        target_pixel,
        pixels_after_target
    ))

    return output_grid
```
