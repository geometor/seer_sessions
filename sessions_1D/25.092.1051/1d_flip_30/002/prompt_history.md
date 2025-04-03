
## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 4 2 2 2 2 2 2 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 2 2 2 2 2 2 4 0 0
```


## train_2

**input:**
```
0 0 0 0 0 0 6 8 8 8 8 8 8 8 8 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 8 8 8 8 8 8 8 8 6 0 0 0 0 0
```


## train_3

**input:**
```
4 7 7 7 7 7 7 7 7 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
7 7 7 7 7 7 7 7 4 0 0 0 0 0 0 0 0 0 0 0
```

*   **Perception of Elements:**
    *   The task operates on 1-dimensional grids (single rows).
    *   Each input contains a contiguous sequence of non-white pixels, potentially flanked by white pixels (0).
    *   Within this non-white sequence, there are exactly two distinct colors present.
    *   One color appears as a single pixel (the "singleton").
    *   The other color appears as a contiguous sequence of multiple pixels (the "sequence").
    *   The singleton pixel is always located at one end of the non-white sequence, adjacent to the start or end of the multi-pixel sequence.
    *   The transformation modifies only the non-white sequence. The surrounding white pixels remain unchanged.
    *   The transformation moves the singleton pixel to the opposite end of the multi-pixel sequence.

*   **YAML Facts:**
    
```yaml
    task_type: array_manipulation_1d
    grid_dimensionality: 1
    background_color: white (0)
    objects:
      - name: non_white_block
        description: A contiguous sequence of non-white pixels.
        properties:
          colors: Contains exactly two distinct non-white colors.
          location: Can be anywhere within the row, possibly touching the edges.
      - name: singleton_pixel
        description: A single pixel within the non_white_block whose color appears only once in the block.
        properties:
          color: Any non-white color.
          count: 1 within the non_white_block.
          location: Always at one of the two ends of the non_white_block.
      - name: sequence_pixels
        description: A contiguous sequence of pixels within the non_white_block, all having the same color, which is different from the singleton_pixel's color.
        properties:
          color: Any non-white color, different from singleton_pixel color.
          count: > 1 within the non_white_block.
          location: Forms the rest of the non_white_block adjacent to the singleton_pixel.
    relationships:
      - type: adjacency
        object1: singleton_pixel
        object2: sequence_pixels
        details: The singleton_pixel is directly adjacent to one end of the sequence_pixels.
    action:
      - type: move
        object: singleton_pixel
        details: The singleton_pixel is moved from its original end of the non_white_block to the opposite end. The relative order of the sequence_pixels remains unchanged.
    invariants:
      - The background white pixels remain unchanged.
      - The colors and number of pixels within the non_white_block remain the same, only their order changes.
      - The length of the grid remains unchanged.
    ```


*   **Natural Language Program:**
    1.  Identify the contiguous block of non-white pixels within the input row. If no such block exists or the block contains fewer than two pixels or more than two distinct colors, return the input unchanged (though this case is not shown in examples).
    2.  Within this non-white block, identify the color that appears only once (the singleton color) and the color that appears multiple times (the sequence color). Determine the single pixel with the singleton color and the sequence of pixels with the sequence color.
    3.  Determine the position of the singleton pixel relative to the sequence pixels (i.e., is it at the start or the end of the combined non-white block?).
    4.  Construct the new non-white block by placing the sequence of pixels first, followed by the singleton pixel, if the singleton was originally at the start.
    5.  Construct the new non-white block by placing the singleton pixel first, followed by the sequence of pixels, if the singleton was originally at the end. (This case doesn't appear in the examples but follows the observed "move to other end" logic).
    6.  Reconstruct the output row by replacing the original non-white block with the newly constructed block, keeping all surrounding white pixels in their original positions.
```python
import collections
import numpy as np # Although not strictly necessary for 1D, it's common in ARC tasks

"""
Identifies a contiguous block of non-white pixels in a 1D input grid.
Within this block, it finds a single pixel of one color (singleton) and a sequence of pixels of another color.
The transformation moves the singleton pixel to the opposite end of the sequence within the block, keeping the surrounding white pixels unchanged.
"""

def find_non_white_block(grid_1d):
    """
    Finds the start and end indices of the first contiguous non-white block.
    Args:
        grid_1d: A list representing the 1D grid.
    Returns:
        A tuple (start_index, end_index) or (None, None) if no block is found.
    """
    start_index = -1
    end_index = -1
    for i, pixel in enumerate(grid_1d):
        if pixel != 0:
            if start_index == -1:
                start_index = i
            end_index = i
        elif start_index != -1:
            # Found the end of the first block
            break
    if start_index == -1:
        return None, None
    return start_index, end_index

def analyze_block(block):
    """
    Analyzes a block of non-white pixels to find the singleton and sequence colors.
    Args:
        block: A list representing the non-white block.
    Returns:
        A tuple (singleton_color, sequence_color, singleton_index_in_block)
        or (None, None, None) if the block doesn't fit the pattern.
    """
    if not block or len(block) < 2:
        return None, None, None

    counts = collections.Counter(block)

    # Expect exactly two distinct non-white colors
    if len(counts) != 2:
        return None, None, None

    singleton_color = None
    sequence_color = None
    singleton_index_in_block = -1

    for color, count in counts.items():
        if count == 1:
            singleton_color = color
        else:
            sequence_color = color # Assume the other is the sequence

    if singleton_color is None or sequence_color is None:
        # Did not find one singleton and one sequence
        return None, None, None

    # Find the index of the singleton
    try:
        singleton_index_in_block = block.index(singleton_color)
    except ValueError:
         # Should not happen if counts were correct, but handle defensively
         return None, None, None

    # Verify singleton is at one of the ends
    if singleton_index_in_block != 0 and singleton_index_in_block != len(block) - 1:
        # Singleton is not at an end, which violates the observed pattern
        return None, None, None

    return singleton_color, sequence_color, singleton_index_in_block


def transform(input_grid_list):
    """
    Transforms the input 1D grid according to the described rule.
    Moves a singleton pixel at one end of a non-white block to the other end.
    Args:
        input_grid_list: A list of integers representing the 1D input grid.
    Returns:
        A list of integers representing the transformed 1D output grid.
    """
    # Ensure input is a standard list (if numpy array is passed)
    input_grid = list(input_grid_list)

    # Initialize output_grid as a copy of the input
    output_grid = list(input_grid) # Use list() to ensure it's a copy

    # 1. Find the contiguous block of non-white pixels
    start_index, end_index = find_non_white_block(input_grid)

    # If no block found, return the original grid
    if start_index is None:
        return output_grid

    # Extract the block
    block = input_grid[start_index : end_index + 1]

    # 2. Analyze the block to find singleton and sequence
    singleton_color, sequence_color, singleton_index_in_block = analyze_block(block)

    # If block doesn't match the expected pattern, return original grid
    if singleton_color is None:
        return output_grid

    # 3. Construct the new block based on the singleton's original position
    new_block = []
    if singleton_index_in_block == 0:
        # Singleton was at the start, move it to the end
        sequence_pixels = [p for p in block if p == sequence_color]
        new_block = sequence_pixels + [singleton_color]
    elif singleton_index_in_block == len(block) - 1:
        # Singleton was at the end, move it to the start
        sequence_pixels = [p for p in block if p == sequence_color]
        new_block = [singleton_color] + sequence_pixels
    else:
        # This case should have been caught by analyze_block, but handle defensively
        return output_grid # Return original if singleton wasn't at an end

    # Ensure the new block has the same length as the old one
    if len(new_block) != len(block):
        # Something went wrong in reconstruction
        print(f"Warning: New block length ({len(new_block)}) doesn't match old block length ({len(block)}).")
        return output_grid # Return original grid on error


    # 4. Reconstruct the output grid
    output_grid[start_index : end_index + 1] = new_block

    return output_grid
```
