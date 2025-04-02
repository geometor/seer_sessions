
## train_1

**input:**
```
0 6 6 6 6 6 6 6 6 6 6 0 0 0 0 0 3 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 3 0 0 0 0 0 0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 0 0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 0 0 0 0 3 0 0 0 0
```


**output:**
```
0 0 0 0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 3 0 0 0 0
```


## train_3

**input:**
```
0 0 0 0 5 5 5 5 5 5 5 5 0 0 0 3 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 5 5 5 5 5 5 5 5 5 5 5 3 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

*   **Perception:**
    *   The input and output grids are single rows (1xN).
    *   Each input grid contains a contiguous horizontal block of a single non-white color (magenta, blue, gray).
    *   Each input grid also contains a single green pixel (color 3).
    *   The non-white, non-green block is always located to the left of the green pixel.
    *   There are white pixels (color 0) between the colored block and the green pixel.
    *   The transformation involves extending the colored block to the right.
    *   The extension stops just before the green pixel.
    *   The white pixels between the original end of the colored block and the green pixel are replaced by the color of the block.
    *   The green pixel itself, and any pixels to its right, remain unchanged.
    *   Pixels to the left of the original colored block also remain unchanged.

*   **Facts YAML:**
    
```yaml
    task_type: array_manipulation_1d
    grid_dimensions: 1xN (single row)
    objects:
      - object_type: contiguous_block
        properties:
          color: non-white (0), non-green (3) # e.g., magenta (6), blue (1), gray (5)
          location: left of the green pixel
          shape: horizontal line segment
          identifier: fill_block
      - object_type: single_pixel
        properties:
          color: green (3)
          location: right of the fill_block
          identifier: boundary_pixel
      - object_type: background_pixels
        properties:
          color: white (0)
          location: between fill_block and boundary_pixel, and potentially elsewhere
    actions:
      - action_type: extend
        actor: fill_block
        direction: right
        target: boundary_pixel (exclusive)
        affected_pixels: background_pixels between fill_block and boundary_pixel
        result: affected_pixels change color to match fill_block color
    relationships:
      - type: spatial
        subject: fill_block
        relation: left_of
        object: boundary_pixel
      - type: boundary
        subject: boundary_pixel
        role: stops the extension of fill_block
    invariants:
      - boundary_pixel color and position
      - pixels to the right of boundary_pixel
      - pixels to the left of the original fill_block
      - color of the fill_block (used for filling)
    ```


*   **Natural Language Program:**
    1.  Identify the column index of the single green pixel (color 3). Let this be `green_col`.
    2.  Find the contiguous horizontal block of a single non-white, non-green color located to the left of `green_col`. Identify its color (let's call it `fill_color`) and the column index of its rightmost pixel (let's call it `fill_end_col`).
    3.  Iterate through the columns from `fill_end_col + 1` up to `green_col - 1`.
    4.  For each column index in this range, change the pixel's color to `fill_color`.
    5.  Leave all other pixels unchanged.
```python
"""
1. Identify the column index of the single green pixel (color 3). Let this be `green_col`.
2. Find the contiguous horizontal block of a single non-white, non-green color located to the left of `green_col`. Identify its color (let's call it `fill_color`) and the column index of its rightmost pixel (let's call it `fill_end_col`).
3. Iterate through the columns from `fill_end_col + 1` up to `green_col - 1`.
4. For each column index in this range, change the pixel's color to `fill_color`.
5. Leave all other pixels unchanged.
"""

import numpy as np

def find_first_occurrence(arr, value):
    """Finds the index of the first occurrence of a value in a 1D numpy array."""
    indices = np.where(arr == value)[0]
    if len(indices) > 0:
        return indices[0]
    return -1 # Indicate not found

def find_last_occurrence(arr, value):
    """Finds the index of the last occurrence of a value in a 1D numpy array."""
    indices = np.where(arr == value)[0]
    if len(indices) > 0:
        return indices[-1]
    return -1 # Indicate not found

def find_colored_block(arr, boundary_col):
    """Finds the fill color and end column of the block left of the boundary."""
    fill_color = -1
    fill_end_col = -1
    for col in range(boundary_col -1, -1, -1): # Iterate backwards from boundary
        pixel_value = arr[col]
        if pixel_value != 0 and pixel_value != 3: # Found a pixel of the block
            fill_color = pixel_value
            # Now find the rightmost extent of this block
            current_col = col
            while current_col < boundary_col and arr[current_col] == fill_color:
                fill_end_col = current_col
                current_col += 1
            break # Found the block, no need to search further left
    return fill_color, fill_end_col


def transform(input_grid):
    """
    Extends a colored block to the right until it reaches a green pixel.

    Args:
        input_grid: A list representing the 1xN input grid.

    Returns:
        A list representing the 1xN output grid.
    """
    # Convert list to numpy array for easier manipulation
    # Assuming input is always a flat list representing a single row
    input_arr = np.array(input_grid, dtype=int)
    
    # Initialize output_grid as a copy of the input
    output_arr = input_arr.copy()

    # 1. Find the green pixel (boundary)
    green_col = find_first_occurrence(input_arr, 3)
    if green_col == -1:
        # Should not happen based on examples, but handle defensively
        return output_arr.tolist() 

    # 2. Find the colored block (fill_color and its rightmost edge)
    fill_color = -1
    fill_end_col = -1
    
    # Search for the block to the left of the green pixel
    # Iterate from left up to the green pixel
    for col in range(green_col):
        pixel = input_arr[col]
        # Check if it's a non-white, non-green color
        if pixel != 0 and pixel != 3: 
            fill_color = pixel
            # Find the end of this contiguous block
            current_col = col
            while current_col < green_col and input_arr[current_col] == fill_color:
                 fill_end_col = current_col
                 current_col += 1
            break # Found the first block, assume it's the one we need

    # Check if a valid block was found
    if fill_color == -1 or fill_end_col == -1:
         # Should not happen based on examples
        return output_arr.tolist()

    # 3. & 4. Fill the gap between the block end and the green pixel
    # Iterate from the column *after* the block ends up to *before* the green pixel
    for col_to_fill in range(fill_end_col + 1, green_col):
        output_arr[col_to_fill] = fill_color
        
    # 5. Other pixels remain unchanged (already handled by copying)

    # Convert back to list for the required output format
    return output_arr.tolist()
```
```python
"""
Transforms a 1D grid by finding a contiguous block of a non-white, non-green color 
and extending it to the right, filling the gap with its color until it reaches 
a single green pixel which acts as a boundary.

1. Create a copy of the input row to serve as the output row.
2. Locate the column index of the single green pixel (color 3) in the input row. 
   Let this be `green_col`.
3. Scan the input row from left to right, up to (but not including) `green_col`, 
   to find the *first* contiguous block of pixels with a color that is neither 
   white (0) nor green (3).
4. Identify the color of this block (`fill_color`) and the column index of its 
   rightmost pixel (`fill_end_col`).
5. If such a block is found:
   a. Iterate through the columns from `fill_end_col + 1` up to `green_col - 1`.
   b. For each column index in this range, set the corresponding pixel in the 
      *output* row to `fill_color`.
6. Return the modified output row.
"""

import numpy as np

def find_first_of(arr, values):
    """Finds the index of the first occurrence of any value in `values` within `arr`."""
    for val in values:
        indices = np.where(arr == val)[0]
        if len(indices) > 0:
            return indices[0]
    return -1 # Not found

def find_block_left_of(arr, boundary_col):
    """
    Finds the fill color and end column index of the first non-white, non-green block
    occurring before the specified boundary column.
    """
    fill_color = -1
    fill_end_col = -1
    
    for col in range(boundary_col):
        pixel_value = arr[col]
        # Check if it's a potential start of the block (non-white, non-green)
        if pixel_value != 0 and pixel_value != 3:
            fill_color = pixel_value
            # Find the end of this contiguous block
            current_col = col
            # Continue as long as we are before the boundary and the color matches
            while current_col < boundary_col and arr[current_col] == fill_color:
                fill_end_col = current_col
                current_col += 1
            # Found the first block and its end, no need to search further
            break 
            
    return fill_color, fill_end_col

def transform(input_grid):
    """
    Applies the fill transformation to the input grid.

    Args:
        input_grid: A list representing the 1xN input grid.

    Returns:
        A list representing the transformed 1xN output grid.
    """
    # Convert list to numpy array for efficient operations
    input_arr = np.array(input_grid, dtype=int)
    
    # 1. Create a copy of the input row to serve as the output row.
    output_arr = input_arr.copy()

    # 2. Locate the column index of the single green pixel (color 3).
    green_indices = np.where(input_arr == 3)[0]
    if len(green_indices) == 0:
        # Green pixel not found, return the original grid (as per current understanding)
        return output_arr.tolist() 
    green_col = green_indices[0] # Assume only one green pixel as per examples

    # 3. & 4. Find the fill block's color and its rightmost extent.
    fill_color, fill_end_col = find_block_left_of(input_arr, green_col)

    # 5. If a valid block was found, fill the gap.
    if fill_color != -1 and fill_end_col != -1:
        # Iterate from the column *after* the block ends up to *before* the green pixel
        start_fill_col = fill_end_col + 1
        end_fill_col = green_col # The loop range is exclusive of the end value
        
        for col_to_fill in range(start_fill_col, end_fill_col):
            # Check if the pixel to fill is currently white (optional, but matches examples)
            # if output_arr[col_to_fill] == 0: 
            output_arr[col_to_fill] = fill_color
            
    # 6. Return the modified output row as a list.
    return output_arr.tolist()
```
