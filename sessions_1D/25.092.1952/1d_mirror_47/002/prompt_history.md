
## train_1

**input:**
```
0 0 0 0 0 0 5 5 5 5 5 5 5 0 0 9 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 9 0 0 5 5 5 5 5 5 5 0
```


## train_2

**input:**
```
0 0 0 0 5 5 5 5 5 5 5 0 0 9 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 9 0 0 5 5 5 5 5 5 5 0 0 0
```


## train_3

**input:**
```
0 0 0 6 6 6 6 6 6 0 9 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 9 0 6 6 6 6 6 6 0 0 0 0 0 0 0 0
```

*   **Perception:** The input consists of a 1D array (representing a row or flattened grid) containing mostly white pixels (0), a single maroon pixel (9), and a contiguous block of another color (gray '5' or magenta '6'). The transformation involves rearranging these elements. The maroon pixel seems to act as a pivot or marker. The colored block and the maroon pixel swap their relative order, while maintaining the number of white pixels that originally separated them.

*   **YAML Facts:**
    
```yaml
    task_description: Rearrange elements in a 1D array based on relative positions.
    elements:
      - type: background
        color: white (0)
      - type: marker
        color: maroon (9)
        count: 1
        shape: single pixel
      - type: colored_block
        color: non-white, non-maroon (e.g., gray '5', magenta '6')
        shape: contiguous horizontal block
        count: 1
    relationships:
      - In the input, the colored_block is separated from the marker by a sequence of zero or more background pixels.
      - The order can be [colored_block] [background_gap] [marker] or potentially the reverse (though only the first case is shown).
    actions:
      - Identify the marker pixel and its index.
      - Identify the colored_block, its color, start index, and end index.
      - Identify the sequence of background pixels between the colored_block and the marker (the gap).
      - Reconstruct the array:
        - Start with a background-filled array of the same size.
        - Place the marker at its original index.
        - Place the identified background_gap sequence immediately after the marker.
        - Place the colored_block immediately after the background_gap sequence.
    transformation_result:
      - The relative order of the colored_block and the marker is swapped.
      - The background_gap sequence that was between them in the input is now placed between them in the output, but following the marker instead of preceding it.
      - The absolute position of the marker pixel remains unchanged.
      - The absolute position of the colored_block changes.
    ```


*   **Natural Language Program:**
    1.  Initialize the output grid as a copy of the input grid, filled entirely with the background color (white, 0).
    2.  Find the index (`marker_index`) and color (`marker_color`, which is always maroon, 9) of the single marker pixel in the input grid.
    3.  Find the contiguous block of pixels that are not background (white, 0) and not the marker color (maroon, 9). Record its color (`block_color`), starting index (`block_start_index`), and ending index (`block_end_index`).
    4.  Determine the sequence of background pixels (the `gap`) located between the end of the colored block and the marker pixel in the input grid. Specifically, identify the pixels from `block_end_index + 1` up to `marker_index - 1`. Record the length of this gap (`gap_length`).
    5.  Place the marker pixel (`marker_color`) in the output grid at the `marker_index`.
    6.  Place the `gap` sequence ( `gap_length` background pixels) in the output grid starting at `marker_index + 1`.
    7.  Place the colored block (using `block_color`) in the output grid starting at the index immediately following the gap, which is `marker_index + 1 + gap_length`. The block will extend for the same length as the original block (`block_end_index - block_start_index + 1`).
```python
"""
Transforms a 1D input grid by swapping the relative positions of a single marker 
pixel (color 9) and a contiguous block of another color (non-0, non-9). 
The marker pixel maintains its original absolute position. The block of color 
is moved to the position immediately following the marker, preserving any 
gap of background pixels (color 0) that originally existed between the block 
and the marker. The gap is placed immediately after the marker, followed by 
the block.
"""

import numpy as np

def find_marker(grid):
    """Finds the index and color of the marker pixel (9)."""
    for i, pixel in enumerate(grid):
        if pixel == 9:
            return i, pixel
    return -1, -1 # Should not happen based on examples

def find_colored_block(grid, marker_index):
    """Finds the start index, end index, and color of the non-background, non-marker block."""
    block_start = -1
    block_end = -1
    block_color = -1
    
    for i, pixel in enumerate(grid):
        if pixel != 0 and pixel != 9:
            if block_start == -1:
                block_start = i
                block_color = pixel
            # Continue until the color changes or we hit the marker or end of grid
            if i + 1 == len(grid) or grid[i+1] != block_color:
                 block_end = i
                 break # Found the end of the block
                 
    return block_start, block_end, block_color


def transform(input_grid):
    """
    Applies the transformation rule to the input grid.
    """
    # Convert input to numpy array for easier handling
    input_array = np.array(input_grid, dtype=int)
    grid_size = len(input_array)
    
    # Initialize output_grid with background color (0)
    output_grid = np.zeros_like(input_array)

    # 1. Find the marker pixel
    marker_index, marker_color = find_marker(input_array)
    if marker_index == -1:
        # Handle error case or return input if marker not found? 
        # Based on examples, marker always exists.
        return input_grid # Or raise error

    # 2. Find the colored block
    block_start_index, block_end_index, block_color = find_colored_block(input_array, marker_index)
    if block_start_index == -1:
        # Handle error case or return input if block not found?
        # Based on examples, block always exists.
        return input_grid # Or raise error
        
    block_length = block_end_index - block_start_index + 1

    # 3. Determine the gap between the block and the marker
    # Assuming block is always before marker as per examples
    gap_start_index = block_end_index + 1
    gap_end_index = marker_index - 1
    gap_length = 0
    if gap_start_index <= gap_end_index:
         gap_length = gap_end_index - gap_start_index + 1

    # 4. Place the marker in the output grid
    output_grid[marker_index] = marker_color
    
    # 5. The gap (background pixels) is implicitly placed by filling with 0s initially.
    # The space from marker_index + 1 to marker_index + gap_length will remain 0.

    # 6. Calculate the new starting position for the block
    new_block_start_index = marker_index + 1 + gap_length
    new_block_end_index = new_block_start_index + block_length -1

    # 7. Place the colored block in the output grid
    if new_block_end_index < grid_size: # Ensure block fits within bounds
        output_grid[new_block_start_index : new_block_end_index + 1] = block_color
    else:
        # Handle cases where the moved block might exceed grid boundaries 
        # (though not seen in examples)
        # For now, just place what fits
        placeable_length = grid_size - new_block_start_index
        if placeable_length > 0:
             output_grid[new_block_start_index : new_block_start_index + placeable_length] = block_color


    # Convert back to list format if needed, otherwise return numpy array
    return output_grid.tolist() 
```
