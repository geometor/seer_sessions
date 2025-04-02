
## train_1

**input:**
```
0 0 0 0 6 6 6 0 0 0 0 0 0 0 0 0 3 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 6 6 6 6 6 6 6 6 6 6 6 6 3 0 0 0 0 0 0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 0 0 0 3
```


**output:**
```
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 3
```


## train_3

**input:**
```
0 0 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 0 0 0 0 0 0 0 3 0
```


**output:**
```
0 0 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 3 0
```

*   **Perception:** The task involves processing single-row grids. Each input grid contains a contiguous block of a single color (other than white or green) and a single green pixel located somewhere to the right of the block. There are typically white pixels separating the block and the green pixel. The transformation extends the colored block to the right, filling the gap of white pixels between the original end of the block and the position just before the green pixel. The green pixel acts as a boundary marker, stopping the extension. The color of the block being extended varies between examples.

*   **Facts:**
    
```yaml
    task_type: grid_transformation
    grid_dimensionality: 1D (single row)
    input_features:
      - object_type: contiguous_block
        color: non-white (0), non-green (3)
        quantity: 1
        properties: [variable_color, variable_start_index, variable_end_index]
      - object_type: single_pixel
        color: green (3)
        quantity: 1
        properties: [fixed_color, variable_index]
      - object_type: background_pixels
        color: white (0)
        quantity: variable
        properties: [fixed_color]
    relationships:
      - type: spatial
        description: The contiguous block is always located to the left of the green pixel.
      - type: separation
        description: White pixels exist between the right edge of the block and the green pixel.
    actions:
      - action: identify
        target: contiguous block (non-white, non-green)
        details: Determine its color and end index.
      - action: identify
        target: green pixel (3)
        details: Determine its index.
      - action: modify_pixels
        target: white pixels (0)
        condition: Located between the end index of the block + 1 and the index of the green pixel - 1.
        effect: Change their color to the color of the contiguous block.
    output_features:
      - object_type: contiguous_block
        description: The original block is extended rightward.
        properties: [original_color, original_start_index, new_end_index]
        new_end_index: index of the green pixel - 1
      - object_type: single_pixel
        color: green (3)
        description: Remains unchanged in position and color.
      - object_type: background_pixels
        color: white (0)
        description: Pixels to the left of the original block start and to the right of the green pixel remain unchanged.
    ```


*   **Natural Language Program:**
    1.  Identify the single contiguous horizontal block of a color that is not white (0) or green (3). Note its color and the index of its rightmost pixel (end index).
    2.  Identify the index of the single green (3) pixel.
    3.  Iterate through the grid from the position immediately to the right of the block's end index up to, but not including, the index of the green pixel.
    4.  For each pixel in this range, change its color to the color identified in step 1.
    5.  Leave all other pixels in the grid unchanged.
    6.  The output is the modified grid.
```python
import numpy as np

"""
Identify the single contiguous horizontal block of a non-white (0) and non-green (3) color.
Find the index of the rightmost pixel of this block (block_end_index) and note its color (block_color).
Find the index of the single green (3) pixel (green_index).
Fill the pixels between block_end_index + 1 and green_index - 1 (inclusive) with block_color.
Leave all other pixels unchanged.
"""

def find_block(grid):
    """
    Finds the contiguous block of non-white, non-green color.

    Args:
        grid: A 1D numpy array representing the input grid row.

    Returns:
        A tuple (block_color, block_start_index, block_end_index)
        or None if no such block is found.
    """
    block_color = -1
    block_start_index = -1
    block_end_index = -1
    in_block = False

    for i, pixel in enumerate(grid):
        if pixel != 0 and pixel != 3:
            if not in_block:
                # Start of a potential block
                block_color = pixel
                block_start_index = i
                block_end_index = i
                in_block = True
            elif pixel == block_color:
                # Continue the block
                block_end_index = i
            else:
                # Found a different color, the previous block ends
                # Since the problem implies only one block, we can break
                # or just return the first one found. Let's assume the first.
                return block_color, block_start_index, block_end_index
        elif in_block:
             # End of the block (hit white or green)
             return block_color, block_start_index, block_end_index

    # If the block extends to the end of the grid
    if in_block:
        return block_color, block_start_index, block_end_index

    return None # Should not happen based on examples

def find_pixel(grid, color):
    """
    Finds the index of the first pixel with the specified color.

    Args:
        grid: A 1D numpy array representing the input grid row.
        color: The integer color value to find.

    Returns:
        The index of the pixel, or -1 if not found.
    """
    try:
        # np.where returns a tuple of arrays, get the first element's first index
        index = np.where(grid == color)[0][0]
        return index
    except IndexError:
        return -1 # Color not found


def transform(input_grid):
    """
    Transforms the input grid by extending a colored block up to a green pixel marker.

    1. Identify the single contiguous horizontal block of a color that is not white (0) or green (3).
       Note its color and the index of its rightmost pixel (end index).
    2. Identify the index of the single green (3) pixel.
    3. Iterate through the grid from the position immediately to the right of the block's end index
       up to, but not including, the index of the green pixel.
    4. For each pixel in this range, change its color to the color identified in step 1.
    5. Leave all other pixels in the grid unchanged.
    6. The output is the modified grid.
    """
    # Ensure input is a numpy array for easier processing
    grid = np.array(input_grid)

    # Initialize output_grid as a copy of the input
    output_grid = grid.copy()

    # 1. Identify the block
    block_info = find_block(grid)
    if block_info is None:
        # Handle error or return input if no block found (based on task constraints, shouldn't happen)
        return output_grid
    block_color, block_start_index, block_end_index = block_info

    # 2. Identify the green pixel
    green_index = find_pixel(grid, 3)
    if green_index == -1:
        # Handle error or return input if no green pixel found (based on task constraints, shouldn't happen)
        return output_grid

    # 3. & 4. Iterate and fill pixels
    # The fill range starts one position after the block ends
    fill_start = block_end_index + 1
    # The fill range ends one position before the green pixel
    fill_end = green_index

    # Modify the output grid in the specified range
    if fill_start < fill_end: # Only fill if there's space between block and green
        output_grid[fill_start:fill_end] = block_color

    # 5. Other pixels are already unchanged because we started with a copy.
    # 6. Return the modified grid
    return output_grid.tolist() # Return as list to match typical ARC format if needed

```
