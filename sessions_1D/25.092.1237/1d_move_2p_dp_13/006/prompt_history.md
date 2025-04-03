
## train_1

**input:**
```
0 0 7 7 7 7 7 7 7 7 7 0 0 9 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 7 7 7 7 7 7 7 7 7 9 0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 4 4 4 4 4 4 4 0 0 9 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 4 4 4 4 4 4 4 9 0
```


## train_3

**input:**
```
4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 0 0 9 0
```


**output:**
```
0 0 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 9 0
```

## Perception of Elements:

The task involves transforming a one-dimensional grid of pixels based on the relative positions of colored elements. The input grid contains sequences of white pixels (0), a contiguous block of orange pixels (7), and a single maroon pixel (9). The output grid rearranges these elements while preserving the total count of each color and the overall grid size. The core transformation seems to involve shifting the orange block towards the maroon pixel, eliminating the white space between them, and relocating that white space to the beginning of the grid.

## YAML Facts:


```yaml
task_description: Rearrange elements in a 1D grid based on object proximity.
grid_dimensions:
  input: 1x20
  output: 1x20
objects:
  - object_id: leading_whitespace
    color: white (0)
    location: Indices 0-1 in input, 0-3 in output
    description: Sequence of white pixels at the start of the grid.
  - object_id: mobile_block
    color: orange (7)
    pixels: [7, 7, 7, 7, 7, 7, 7, 7, 7]
    location: Indices 2-10 in input, 4-12 in output
    description: A contiguous block of non-white pixels.
  - object_id: separating_whitespace
    color: white (0)
    pixels: [0, 0]
    location: Indices 11-12 in input, absent between mobile_block and anchor_pixel in output (relocated to beginning)
    description: Sequence of white pixels between the mobile_block and the anchor_pixel.
  - object_id: anchor_pixel
    color: maroon (9)
    pixels: [9]
    location: Index 13 in both input and output
    description: A single non-white pixel, distinct from the mobile_block, acting as a positional reference.
  - object_id: trailing_whitespace
    color: white (0)
    location: Indices 14-19 in both input and output
    description: Sequence of white pixels at the end of the grid.
relationships:
  - type: spatial
    between: [mobile_block, separating_whitespace, anchor_pixel]
    description: In the input, the mobile_block is followed by separating_whitespace, which is followed by the anchor_pixel.
  - type: spatial
    between: [mobile_block, anchor_pixel]
    description: In the output, the mobile_block is immediately adjacent to the anchor_pixel.
actions:
  - action: identify
    target: mobile_block
    criteria: Contiguous block of non-white pixels preceding the anchor_pixel.
  - action: identify
    target: anchor_pixel
    criteria: Single non-white pixel located to the right of the mobile_block.
  - action: identify
    target: separating_whitespace
    criteria: White pixels located between the mobile_block and the anchor_pixel.
  - action: relocate
    target: separating_whitespace
    destination: Prepend to the leading_whitespace at the beginning of the grid.
  - action: shift
    target: mobile_block
    direction: right
    magnitude: Number of pixels in separating_whitespace
    result: mobile_block becomes adjacent to anchor_pixel.
  - action: maintain_position
    target: anchor_pixel
    description: The anchor pixel's absolute position remains unchanged.
  - action: maintain_relative_position
    target: trailing_whitespace
    description: The trailing whitespace remains at the end of the grid.
```


## Natural Language Program:

1.  Identify the main contiguous block of non-white pixels (the "mobile block").
2.  Identify the single, different non-white pixel located to the right of the mobile block (the "anchor pixel").
3.  Identify the sequence of white pixels positioned directly between the end of the mobile block and the anchor pixel (the "separating whitespace").
4.  Count the number of pixels in the separating whitespace.
5.  Construct the output grid:
    a.  Place the separating whitespace at the beginning of the grid.
    b.  Append any white pixels that originally preceded the mobile block in the input grid.
    c.  Append the mobile block.
    d.  Append the anchor pixel.
    e.  Append any white pixels that originally followed the anchor pixel in the input grid.
```python
import numpy as np
from typing import List, Tuple

"""
Transforms a 1D grid by relocating the white space between the first contiguous block of non-white pixels (mobile block) and the next non-white pixel (anchor pixel). This separating white space is moved to the beginning of the grid, effectively shifting the mobile block adjacent to the anchor pixel.

1. Identify the first contiguous block of non-white pixels (mobile block).
2. Identify the first non-white pixel appearing after the mobile block (anchor pixel).
3. Identify the sequence of white pixels between the mobile block and the anchor pixel (separating whitespace).
4. Construct the output grid by concatenating: separating whitespace, original leading whitespace, mobile block, anchor pixel, and original trailing whitespace.
"""

def find_first_non_white_block(grid_1d: List[int]) -> Tuple[int, int, List[int]]:
    """Finds the start index, end index (exclusive), and pixels of the first contiguous non-white block."""
    start_index = -1
    end_index = -1
    block_pixels = []

    for i, pixel in enumerate(grid_1d):
        if start_index == -1 and pixel != 0:
            start_index = i
        if start_index != -1:
            if pixel == 0 or (i > start_index and pixel != grid_1d[start_index]): # Also stops if color changes within block, might need adjustment if blocks can be multicolored
                end_index = i
                break
            block_pixels.append(pixel)
    
    # Handle case where block goes to the end of the grid
    if start_index != -1 and end_index == -1:
        end_index = len(grid_1d)

    # Handle case where no block is found (shouldn't happen based on examples)
    if start_index == -1:
        return -1, -1, []

    # Recalculate block_pixels using indices for certainty, especially if color change logic is refined
    block_pixels = grid_1d[start_index:end_index]
    
    return start_index, end_index, block_pixels

def find_first_non_white_after_index(grid_1d: List[int], start_search_index: int) -> Tuple[int, int]:
    """Finds the index and value of the first non-white pixel at or after start_search_index."""
    for i in range(start_search_index, len(grid_1d)):
        if grid_1d[i] != 0:
            return i, grid_1d[i]
    return -1, -1 # Not found

def transform(input_grid: List[List[int]]) -> List[List[int]]:
    """
    Applies the transformation rule to the input grid.
    """
    
    # Ensure input is treated as 1D
    if not input_grid or len(input_grid) != 1:
        # Handle invalid input if necessary, though ARC tasks usually provide valid examples
        return input_grid 
    grid_1d = input_grid[0]
    grid_len = len(grid_1d)

    # --- Identify Components ---

    # 1. Identify the mobile block
    mobile_start, mobile_end, mobile_block = find_first_non_white_block(grid_1d)
    
    if mobile_start == -1:
         # No mobile block found, return original grid or handle error
         return input_grid

    # 2. Identify the anchor pixel (first non-white after the mobile block)
    anchor_index, anchor_pixel = find_first_non_white_after_index(grid_1d, mobile_end)

    if anchor_index == -1:
        # No anchor pixel found after the mobile block, maybe return original grid?
        # Based on examples, there's always an anchor.
        return input_grid

    # 3. Identify the separating whitespace (pixels between mobile_end and anchor_index)
    separating_whitespace = grid_1d[mobile_end:anchor_index]
    # Verify it's all white (0), though the find_first_non_white_after_index implies it
    # assert all(p == 0 for p in separating_whitespace) 

    # 4. Identify leading whitespace (pixels before mobile_start)
    leading_whitespace = grid_1d[:mobile_start]

    # 5. Identify trailing whitespace (pixels after anchor_index)
    trailing_whitespace = grid_1d[anchor_index+1:]

    # --- Construct Output Grid ---
    
    # Concatenate the parts in the new order:
    # separating_whitespace + leading_whitespace + mobile_block + [anchor_pixel] + trailing_whitespace
    output_grid_1d = separating_whitespace + leading_whitespace + mobile_block + [anchor_pixel] + trailing_whitespace

    # Ensure the output grid has the same length as the input
    # assert len(output_grid_1d) == grid_len

    # Format the output as a list containing one list (1xN grid)
    output_grid = [output_grid_1d]

    return output_grid
```
```python
import numpy as np
from typing import List, Tuple

"""
Transforms a 1D grid by identifying segments: leading white space, the first contiguous block of non-white pixels (mobile block), the white space separating the mobile block from the next non-white pixel (separating whitespace), the first non-white pixel after the mobile block (anchor pixel), and the trailing white space. The transformation reconstructs the grid by rearranging these segments: the separating whitespace is moved to the beginning, followed by the original leading whitespace, the mobile block, the anchor pixel, and finally the trailing whitespace.

1.  Scan the input grid to find the start and end indices of the first contiguous block of non-white pixels (the "mobile block").
2.  Identify the "leading whitespace" as pixels before the mobile block start.
3.  Scan from the end of the mobile block to find the index and value of the next non-white pixel (the "anchor pixel").
4.  Identify the "separating whitespace" as the white pixels between the mobile block's end and the anchor pixel's index.
5.  Identify the "trailing whitespace" as pixels after the anchor pixel.
6.  Construct the output grid by concatenating: separating whitespace, leading whitespace, mobile block pixels, the anchor pixel, and trailing whitespace.
"""


def find_first_non_white_block_indices(grid_1d: List[int]) -> Tuple[int, int]:
    """
    Finds the start index (inclusive) and end index (exclusive) of the 
    first contiguous block of non-white pixels.

    Returns:
        Tuple[int, int]: (start_index, end_index). Returns (-1, -1) if no 
                         non-white block is found.
    """
    start_index = -1
    end_index = -1
    n = len(grid_1d)

    # Find the start of the block
    for i, pixel in enumerate(grid_1d):
        if pixel != 0:
            start_index = i
            break
            
    # If no non-white pixel found, return (-1, -1)
    if start_index == -1:
        return -1, -1

    # Find the end of the block (first white pixel after start_index)
    end_index = start_index # Initialize end_index assume block has length at least 1
    for i in range(start_index, n):
        if grid_1d[i] == 0:
            end_index = i
            break
        # If loop finishes without finding a 0, the block goes to the end
        if i == n - 1 and grid_1d[i] != 0: 
             end_index = n # End index is exclusive

    return start_index, end_index

def find_first_non_white_after_index(grid_1d: List[int], start_search_index: int) -> Tuple[int, int]:
    """
    Finds the index and value of the first non-white pixel at or after 
    start_search_index.

    Returns:
        Tuple[int, int]: (index, value). Returns (-1, -1) if none found.
    """
    for i in range(start_search_index, len(grid_1d)):
        if grid_1d[i] != 0:
            return i, grid_1d[i]
    return -1, -1 # Not found

def transform(input_grid: List[List[int]]) -> List[List[int]]:
    """
    Applies the transformation rule to the input grid.
    """
    # Ensure input is treated as 1D
    if not input_grid or len(input_grid) != 1:
        # Handle invalid input if necessary, though ARC tasks usually provide valid examples
        # Return unchanged grid for robustness
        return input_grid 
        
    grid_1d = input_grid[0]
    grid_len = len(grid_1d)

    # --- 1. Identify Mobile Block ---
    mobile_start, mobile_end = find_first_non_white_block_indices(grid_1d)
    
    # Handle case where no mobile block is found (e.g., all white grid)
    if mobile_start == -1:
         return input_grid # Return original grid if no pattern detected

    # Extract mobile block pixels
    mobile_block = grid_1d[mobile_start:mobile_end]

    # --- 2. Identify Leading Whitespace ---
    leading_whitespace = grid_1d[:mobile_start]

    # --- 3. Identify Anchor Pixel ---
    # Search for the first non-white pixel *after* the mobile block ends
    anchor_index, anchor_pixel = find_first_non_white_after_index(grid_1d, mobile_end)

    # Handle case where no anchor pixel is found after the mobile block
    if anchor_index == -1:
        # This case might imply the mobile block is at the very end, or only trailing whitespace follows.
        # Based on examples, an anchor always exists. If not, maybe return original?
        # For now, assume anchor exists as per examples. If error occurs, this needs review.
         return input_grid # Or potentially handle differently if this case is valid

    # --- 4. Identify Separating Whitespace ---
    # Pixels between the end of the mobile block and the anchor pixel
    separating_whitespace = grid_1d[mobile_end:anchor_index]

    # --- 5. Identify Trailing Whitespace ---
    # Pixels after the anchor pixel
    trailing_whitespace = grid_1d[anchor_index+1:]

    # --- 6. Construct Output Grid ---
    # Concatenate the parts in the new order:
    # separating_whitespace + leading_whitespace + mobile_block + [anchor_pixel] + trailing_whitespace
    output_grid_1d = separating_whitespace + leading_whitespace + mobile_block + [anchor_pixel] + trailing_whitespace

    # Ensure the output grid maintains the original length (sanity check)
    if len(output_grid_1d) != grid_len:
         # Handle potential length mismatch error, though logic should preserve length
         print(f"Warning: Output length {len(output_grid_1d)} differs from input length {grid_len}")
         # Fallback or error handling needed here if this occurs
         return input_grid # Safer to return original if length changes unexpectedly

    # Format the output as a list containing one list (1xN grid)
    output_grid = [output_grid_1d]

    return output_grid
```
```python
import numpy as np
from typing import List, Tuple, Optional

"""
Transforms a 1D grid by identifying five segments: leading white space, the first contiguous block of non-white pixels (mobile block), the white space separating the mobile block from the next non-white pixel (separating whitespace), the first non-white pixel after the mobile block (anchor pixel), and the trailing white space. The transformation reconstructs the grid by rearranging these segments in the order: separating whitespace, leading whitespace, mobile block, anchor pixel, trailing whitespace.

1.  Examine the input grid (a single row of pixels) from left to right.
2.  Identify the pixels constituting the "leading whitespace": the sequence of white (0) pixels from the start of the grid up to the first non-white pixel. If the grid starts with a non-white pixel, the leading whitespace is empty.
3.  Identify the "mobile block": the first contiguous sequence of one or more non-white pixels. Note its start and end positions.
4.  Identify the "anchor pixel": find the *first* non-white pixel that appears *after* the end of the mobile block. Note its value and position.
5.  Identify the "separating whitespace": the sequence of white (0) pixels located strictly between the end of the mobile block and the position of the anchor pixel. This sequence might be empty if the anchor pixel immediately follows the mobile block.
6.  Identify the "trailing whitespace": the sequence of white (0) pixels from the position immediately after the anchor pixel to the end of the grid. This sequence might be empty.
7.  Construct the output grid by concatenating the identified segments in the following order:
    a.  The separating whitespace.
    b.  The leading whitespace.
    c.  The mobile block pixels.
    d.  The anchor pixel.
    e.  The trailing whitespace.
8.  The resulting grid will have the same dimensions and the same count of each pixel color as the input grid, but the segments will be rearranged.
"""


def find_first_non_white_block_indices(grid_1d: List[int]) -> Tuple[int, int]:
    """
    Finds the start index (inclusive) and end index (exclusive) of the 
    first contiguous block of non-white pixels.

    Args:
        grid_1d: The input 1D list of pixels.

    Returns:
        Tuple[int, int]: (start_index, end_index). Returns (-1, -1) if no 
                         non-white block is found.
    """
    start_index = -1
    end_index = -1
    n = len(grid_1d)

    # Find the start of the block
    for i, pixel in enumerate(grid_1d):
        if pixel != 0:
            start_index = i
            break
            
    # If no non-white pixel found, return (-1, -1)
    if start_index == -1:
        return -1, -1

    # Find the end of the block (first white pixel *at or after* start_index)
    # Initialize end_index assuming block might go to the end
    end_index = n 
    for i in range(start_index, n):
        if grid_1d[i] == 0:
            end_index = i
            break
        
    return start_index, end_index

def find_first_non_white_after_index(grid_1d: List[int], start_search_index: int) -> Tuple[int, int]:
    """
    Finds the index and value of the first non-white pixel at or after 
    start_search_index.

    Args:
        grid_1d: The input 1D list of pixels.
        start_search_index: The index from which to start searching (inclusive).

    Returns:
        Tuple[int, int]: (index, value). Returns (-1, -1) if none found.
    """
    for i in range(start_search_index, len(grid_1d)):
        if grid_1d[i] != 0:
            return i, grid_1d[i]
    return -1, -1 # Not found

def transform(input_grid: List[List[int]]) -> List[List[int]]:
    """
    Applies the segment rearrangement transformation to the input grid.
    """
    # Ensure input is treated as 1D list
    if not input_grid or len(input_grid) == 0:
        return [] # Handle empty input
    if len(input_grid) > 1:
         # This task expects 1D input, return unchanged if not 1D
         # Or raise an error depending on desired behavior for invalid input
         return input_grid
        
    # Explicitly convert to list to avoid potential numpy ambiguity issues
    grid_1d = list(input_grid[0])
    grid_len = len(grid_1d)
    
    # --- 1. Identify Mobile Block ---
    mobile_start, mobile_end = find_first_non_white_block_indices(grid_1d)
    
    # Handle case where no mobile block is found (e.g., all white grid)
    if mobile_start == -1:
         # If no block, the grid remains unchanged
         return input_grid 

    # --- 2. Identify Leading Whitespace ---
    leading_whitespace = grid_1d[:mobile_start]

    # Extract mobile block pixels now that we know indices are valid
    mobile_block = grid_1d[mobile_start:mobile_end]

    # --- 3. Identify Anchor Pixel ---
    # Search for the first non-white pixel *after* the mobile block ends
    anchor_index, anchor_pixel = find_first_non_white_after_index(grid_1d, mobile_end)

    # Handle case where no anchor pixel is found after the mobile block
    if anchor_index == -1:
        # If no anchor, the relative structure required for transformation is missing.
        # Return the original grid as no transformation rule applies.
        return input_grid 

    # --- 4. Identify Separating Whitespace ---
    # Pixels between the end of the mobile block and the anchor pixel
    separating_whitespace = grid_1d[mobile_end:anchor_index]

    # --- 5. Identify Trailing Whitespace ---
    # Pixels after the anchor pixel
    trailing_whitespace = grid_1d[anchor_index+1:]

    # --- 6. Construct Output Grid ---
    # Concatenate the parts in the new order:
    # separating_whitespace + leading_whitespace + mobile_block + [anchor_pixel] + trailing_whitespace
    output_grid_1d = separating_whitespace + leading_whitespace + mobile_block + [anchor_pixel] + trailing_whitespace

    # Basic check to ensure length is preserved (should always be true with list concatenation)
    if len(output_grid_1d) != grid_len:
         # This indicates a logic error in segmentation/concatenation
         print(f"Error: Output length {len(output_grid_1d)} differs from input length {grid_len}")
         # Fallback to returning original grid in case of unexpected error
         return input_grid 

    # Format the output as a list containing one list (1xN grid)
    output_grid = [output_grid_1d]

    return output_grid
```
