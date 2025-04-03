
## train_1

**input:**
```
0 2 2 2 2 2 0 0 3 0
```


**output:**
```
0 0 0 2 2 2 2 2 3 0
```


## train_2

**input:**
```
4 4 4 4 4 4 0 0 3 0
```


**output:**
```
0 0 4 4 4 4 4 4 3 0
```


## train_3

**input:**
```
8 8 8 8 0 0 3 0 0 0
```


**output:**
```
0 0 8 8 8 8 3 0 0 0
```

*   **Perception**: The task operates on a single row (1D grid). The transformation involves rearranging segments of the row based on the position of a specific 'marker' pixel, which is green (3). A contiguous block of non-white pixels located to the left of the green pixel is identified. All white pixels (0) also located to the left of the green pixel are collected. In the output, these collected white pixels are placed first, followed by the identified non-white block, then the green pixel, and finally any pixels that were originally to the right of the green pixel. The relative order and content of the segment to the right of the green pixel remain unchanged. The core operation is a conditional rearrangement of elements preceding the green pixel, consolidating white space at the beginning and pushing the main colored block rightward until it's adjacent to the green pixel.

*   **Facts YAML**:
    
```yaml
    task_type: rearrangement_1d
    grid_dimensionality: 1
    elements:
      - pixels:
          colors_present: [white(0), red(2), green(3), yellow(4), azure(8)] # Based on all examples
          marker_pixel: green(3)
      - blocks:
          definition: contiguous sequence of same-colored pixels
          types:
            - white_block: consists of white(0) pixels
            - colored_block: consists of non-white, non-green pixels
    marker_properties:
      - color: green(3)
      - function: partition_marker
        description: Divides the grid into a left part and a right part (including the marker itself). The transformation primarily affects the left part.
    transformation:
      scope: affects only the part of the grid to the left of the green(3) marker.
      input_left_part:
        - identify: largest contiguous block of non-white pixels (main_block)
        - identify: all white(0) pixels (whitespace_pixels)
      output_left_part_construction:
        - place: all identified whitespace_pixels at the beginning.
        - append: the identified main_block.
      output_grid_construction:
        - concatenate: [output_left_part, green(3)_marker, original_right_part]
    relationships:
      - adjacency: used to define blocks and relative positions.
      - partitioning: the green(3) pixel acts as a separator.
    invariants:
      - the green(3) pixel itself does not change color or relative position concerning the right part of the grid.
      - the sequence and colors of pixels to the right of the green(3) pixel remain unchanged.
      - the content (colors and count) of the main_block remains unchanged, only its position shifts.
      - the total count of white(0) pixels remains unchanged.
    ```


*   **Natural Language Program**:
    1.  Locate the green pixel (color 3) in the input row. If no green pixel exists, return the input unchanged (assumption based on observed pattern; needs confirmation if such cases exist).
    2.  Define the 'left part' of the row as all pixels strictly to the left of the green pixel.
    3.  Define the 'right part' of the row as all pixels strictly to the right of the green pixel.
    4.  Within the 'left part', identify the largest contiguous block of pixels that are not white (color 0). Call this the 'main block'. If there are multiple such blocks of the same largest size, select the rightmost one (based on examples). If no non-white block exists in the left part, the 'main block' is empty.
    5.  Count the total number of white pixels (color 0) present in the 'left part'.
    6.  Construct the output row:
        a.  Start with a sequence of white pixels (color 0) equal to the count obtained in step 5.
        b.  Append the 'main block' identified in step 4.
        c.  Append the green pixel (color 3).
        d.  Append the 'right part' identified in step 3, maintaining its original sequence of pixels.
```python
import numpy as np
from typing import List, Tuple, Optional

def find_contiguous_blocks(segment: List[int], target_color: int = -1, exclude_color: int = 0) -> List[Tuple[int, int, int]]:
    """
    Finds contiguous blocks of a specific color or any color excluding another.

    Args:
        segment: The list of integers (pixels) to search within.
        target_color: The specific color to look for. If -1, find blocks of any color excluding exclude_color.
        exclude_color: The color to exclude when target_color is -1.

    Returns:
        A list of tuples, where each tuple represents a block: (start_index, end_index, color).
        Returns an empty list if no blocks are found.
    """
    blocks = []
    start_index = -1
    current_color = -1

    for i, pixel in enumerate(segment):
        is_target = False
        if target_color != -1:
            is_target = (pixel == target_color)
        else:
            is_target = (pixel != exclude_color)

        if is_target:
            if start_index == -1:
                # Start of a new potential block
                start_index = i
                current_color = pixel
            elif pixel != current_color and target_color == -1:
                 # If finding any non-excluded color, and color changes, end previous block and start new
                 blocks.append((start_index, i - 1, current_color))
                 start_index = i
                 current_color = pixel

        elif start_index != -1:
            # End of the current block
            blocks.append((start_index, i - 1, current_color))
            start_index = -1
            current_color = -1

    # Check for a block ending at the last element
    if start_index != -1:
        blocks.append((start_index, len(segment) - 1, current_color))

    # Filter blocks if a specific target_color was requested initially but we found multiple colors
    if target_color != -1:
         blocks = [(s, e, c) for s, e, c in blocks if c == target_color]
    elif target_color == -1 and exclude_color is not None:
         # This case is already handled by is_target logic, no extra filter needed.
         pass


    return blocks

def find_largest_rightmost_block(blocks: List[Tuple[int, int, int]]) -> Optional[Tuple[int, int, int]]:
    """
    Finds the largest block among the given blocks. If there are ties in size,
    returns the rightmost one (highest end index).

    Args:
        blocks: A list of blocks, each represented as (start_index, end_index, color).

    Returns:
        The largest, rightmost block tuple, or None if the input list is empty.
    """
    if not blocks:
        return None

    largest_block = None
    max_len = -1

    for block in blocks:
        start, end, color = block
        length = end - start + 1
        if length >= max_len: # Use >= to favor rightmost blocks in case of tie
             # Update if current block is longer OR same length but more to the right
            if length > max_len or (length == max_len and end > largest_block[1]):
                max_len = length
                largest_block = block

    return largest_block


def transform(input_grid: List[List[int]]) -> List[List[int]]:
    """
    Transforms the input grid (a single row) based on the position of the green pixel (3).
    1. Locate the green pixel (color 3).
    2. Divide the row into left, green pixel, and right parts.
    3. In the left part, identify the largest contiguous block of non-white (0) pixels.
       If ties in length, choose the rightmost one.
    4. Count the white (0) pixels in the left part.
    5. Construct the output row by concatenating:
       - White pixels equal to the count from step 4.
       - The identified main block from step 3.
       - The green pixel.
       - The original right part.
    If no green pixel is found, or the input is not a single row, return the input unchanged.
    """
    # Ensure input is a single row
    if len(input_grid) != 1:
        # Or handle potential multi-row cases if the problem evolves
        return input_grid
        
    input_row = input_grid[0]
    
    # 1. Locate the green pixel (color 3)
    green_pixel_index = -1
    try:
        green_pixel_index = input_row.index(3)
    except ValueError:
        # No green pixel found, return input unchanged
        return input_grid

    # 2. Define the 'left part', 'green pixel', and 'right part'
    left_part = input_row[:green_pixel_index]
    green_pixel = [3] # Keep as a list for concatenation
    right_part = input_row[green_pixel_index + 1:]

    # Handle edge case: green pixel is the first element
    if not left_part:
        output_row = green_pixel + right_part
        return [output_row]

    # 3. Within the 'left part', identify the largest contiguous block of non-white pixels.
    # Find all non-white blocks
    non_white_blocks_indices = find_contiguous_blocks(left_part, target_color=-1, exclude_color=0)

    main_block_data = []
    if non_white_blocks_indices:
         # Find the largest (and rightmost in case of ties)
        largest_block_indices = find_largest_rightmost_block(non_white_blocks_indices)
        if largest_block_indices:
            start, end, _ = largest_block_indices
            main_block_data = left_part[start : end + 1]


    # 4. Count the total number of white pixels (color 0) present in the 'left part'.
    white_pixel_count = left_part.count(0)

    # 5. Construct the output row
    # a. Start with a sequence of white pixels
    output_left_part_white = [0] * white_pixel_count
    
    # b. Append the 'main block'
    output_left_part = output_left_part_white + main_block_data
    
    # c. Append the green pixel
    # d. Append the 'right part'
    output_row = output_left_part + green_pixel + right_part

    # Ensure output matches input dimensions (1 row)
    return [output_row]

```
