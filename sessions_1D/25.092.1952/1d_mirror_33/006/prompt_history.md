
## train_1

**input:**
```
0 1 1 1 1 1 1 0 0 0 9 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 9 0 0 0 1 1 1 1 1 1 0 0 0 0
```


## train_2

**input:**
```
0 0 5 5 5 5 5 5 5 0 0 9 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 9 0 0 5 5 5 5 5 5 5 0 0 0
```


## train_3

**input:**
```
2 2 2 2 2 2 2 0 0 9 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 9 0 0 2 2 2 2 2 2 2 0 0 0 0 0
```

*   **Perception:**
    *   The input and output are single-row grids (1D arrays).
    *   Each grid contains exactly one maroon pixel (color 9).
    *   Each grid contains one contiguous horizontal line object of a single color (blue, gray, or red in the examples), different from maroon and white.
    *   The rest of the grid cells are white (color 0).
    *   The maroon pixel's position remains unchanged between the input and output.
    *   The colored line object moves from one side of the maroon pixel to the other.
    *   The distance (number of white pixels) between the colored line object and the maroon pixel is preserved during the move. The object essentially reflects across the maroon pixel, maintaining the gap.

*   **Facts:**
    
```yaml
    task_type: object_manipulation
    grid_dimensionality: 1D (single row)
    objects:
      - type: pivot
        color: 9 (maroon)
        count: 1
        shape: single_pixel
        properties:
          - fixed_position: true
      - type: line
        color: any non-zero, non-maroon color (1, 2, 5 in examples)
        count: 1
        shape: horizontal_line (contiguous block)
        properties:
          - variable_color
          - variable_length
          - moves_relative_to_pivot
    background_color: 0 (white)
    relationships:
      - type: spatial
        description: The line object is located either to the left or right of the pivot object.
      - type: distance
        description: The number of white pixels between the line object and the pivot object is constant.
    actions:
      - type: move/reflect
        target: line_object
        reference: pivot_object
        details: The line object is moved to the opposite side of the pivot object, maintaining the original separation distance (number of white pixels).
    ```


*   **Natural Language Program:**
    1.  Initialize the output grid as a copy of the input grid's dimensions, filled with the background color (white, 0).
    2.  Locate the single maroon pixel (9) in the input grid. This is the pivot point. Place the maroon pixel at the same position in the output grid.
    3.  Locate the contiguous block of non-white, non-maroon pixels in the input grid. Note its color and length.
    4.  Determine the position of this block relative to the pivot point (left or right).
    5.  Count the number of white pixels (0) separating the block from the pivot point in the input grid. Let this count be `distance`.
    6.  Determine the starting position for the block in the output grid:
        *   If the block was to the left of the pivot in the input, its new starting position in the output will be `pivot_index + distance + 1`.
        *   If the block was to the right of the pivot in the input, its new starting position in the output will be `pivot_index - distance - block_length`.
    7.  Place the block (with its original color and length) starting at the calculated position in the output grid.
```python
"""
Reflects a contiguous block of non-white, non-maroon pixels across a single maroon pivot pixel in a 1D grid (single row), maintaining the separation distance.

1.  Find the index of the maroon pixel (9), the pivot.
2.  Find the contiguous block of non-white (0) and non-maroon pixels. Record its color, start index, and end index.
3.  Calculate the distance (number of white pixels) between the block and the pivot.
4.  Determine if the block is to the left or right of the pivot.
5.  Calculate the new starting position for the block on the opposite side of the pivot, maintaining the distance.
6.  Create an output grid filled with white (0).
7.  Place the pivot pixel (9) at its original position in the output grid.
8.  Place the colored block at its calculated new position in the output grid.
"""

import numpy as np

def find_pivot(grid_1d):
    """Finds the index of the pivot pixel (9)."""
    for i, pixel in enumerate(grid_1d):
        if pixel == 9:
            return i
    return -1 # Should not happen based on task description

def find_object(grid_1d, pivot_index):
    """Finds the start index, end index, and color of the movable object."""
    object_color = -1
    object_start = -1
    object_end = -1
    in_object = False

    for i, pixel in enumerate(grid_1d):
        if pixel != 0 and pixel != 9: # Found a pixel of the object
            if not in_object:
                object_color = pixel
                object_start = i
                in_object = True
            object_end = i # Keep updating end index while in object
        elif in_object: # Just exited the object
            break # Stop searching once the object is found and passed

    if object_start == -1: # Handle case where object might be at the very end
        # Re-scan if not found in the first pass (e.g., object ends at grid end)
        # This simple loop actually covers this, but explicit check might be needed
        # for more complex cases. For this task, the above loop should suffice.
        pass

    return object_start, object_end, object_color


def transform(input_grid):
    """
    Transforms the input grid by reflecting the colored object across the pivot.

    Args:
        input_grid: A list of integers representing the 1D input grid.

    Returns:
        A list of integers representing the transformed 1D output grid.
    """
    # Ensure input is treated as a 1D list/array
    if isinstance(input_grid[0], list): # Handle potential [[...]] format
         grid_1d = np.array(input_grid[0])
    else:
         grid_1d = np.array(input_grid) # Assume already flat list

    grid_size = len(grid_1d)
    output_grid = np.zeros(grid_size, dtype=int) # Initialize with white (0)

    # 1. Find the pivot
    pivot_index = find_pivot(grid_1d)
    if pivot_index == -1:
        # Handle error: Pivot not found (though examples guarantee one)
        return input_grid # Or raise an error

    # 2. Place the pivot in the output
    output_grid[pivot_index] = 9

    # 3. Find the object
    object_start, object_end, object_color = find_object(grid_1d, pivot_index)
    if object_start == -1:
         # Handle error: Object not found (though examples guarantee one)
         return output_grid.tolist() # Return grid with only pivot

    object_length = object_end - object_start + 1

    # 4. Calculate distance and determine relative position
    distance = 0
    is_left = False
    if object_end < pivot_index: # Object is to the left
        is_left = True
        distance = pivot_index - object_end - 1
    else: # Object is to the right
        is_left = False
        distance = object_start - pivot_index - 1

    # Ensure distance is non-negative (can be 0 if adjacent)
    distance = max(0, distance)

    # 5. Calculate new position
    new_object_start = -1
    if is_left:
        # Move to the right
        new_object_start = pivot_index + distance + 1
    else:
        # Move to the left
        new_object_start = pivot_index - distance - object_length

    # 6. Place the object in the output grid
    new_object_end = new_object_start + object_length
    if 0 <= new_object_start < grid_size and 0 <= new_object_end <= grid_size:
        output_grid[new_object_start:new_object_end] = object_color
    else:
        # Handle error: Calculated position is out of bounds
        # This shouldn't happen if input follows the pattern
        print(f"Warning: Calculated object position out of bounds.")
        print(f"Pivot: {pivot_index}, OldStart: {object_start}, OldEnd: {object_end}, Dist: {distance}, Len: {object_length}, NewStart: {new_object_start}")


    # Return as a flat list, matching input/output format
    return output_grid.tolist()
```
```python
"""
Reflects a contiguous block of non-white, non-maroon pixels across a single maroon pivot pixel in a 1D grid (represented as a single row in a 2D grid). The reflection maintains the separation distance (number of white pixels) between the block and the pivot. The input and output are lists containing a single list representing the row.
"""

import numpy as np

def find_pivot(grid_1d):
    """Finds the index of the pivot pixel (9) in a 1D list."""
    for i, pixel in enumerate(grid_1d):
        if pixel == 9:
            return i
    return -1 # Pivot not found

def find_object(grid_1d):
    """
    Finds the start index, end index (inclusive), and color of the 
    contiguous block of non-white (0) and non-maroon (9) pixels in a 1D list.
    Returns (start, end, color) or (-1, -1, -1) if not found.
    """
    object_color = -1
    object_start = -1
    object_end = -1
    in_object = False

    for i, pixel in enumerate(grid_1d):
        if pixel != 0 and pixel != 9: # Found a pixel of the object
            if not in_object:
                # Start of the object
                object_color = pixel
                object_start = i
                in_object = True
            # Update end index while within the object
            object_end = i 
        elif in_object: 
            # Exited the object block, stop searching
            break 
            
    # Check if an object was actually found
    if object_start == -1:
        return -1, -1, -1

    return object_start, object_end, object_color


def transform(input_grid):
    """
    Transforms the input grid by reflecting the colored object across the pivot.

    Args:
        input_grid: A list containing a single list of integers representing the 1D input row. 
                      Example: [[0, 1, 1, 9, 0]]

    Returns:
        A list containing a single list of integers representing the transformed 1D output row.
                      Example: [[0, 9, 1, 1, 0]] (if input was [[0, 1, 1, 9, 0]])
    """
    # 1. Extract the working grid row (assuming standard ARC format [[...]])
    if not input_grid or not isinstance(input_grid[0], list):
        # Handle unexpected input format gracefully
        # In a real scenario, might raise an error or return input_grid
        return input_grid 
    grid_1d = input_grid[0]
    grid_size = len(grid_1d)

    # 2. Create an output row initialized with the background color (0)
    output_grid_1d = np.zeros(grid_size, dtype=int)

    # 3. Locate the pivot point (maroon pixel, 9)
    pivot_index = find_pivot(grid_1d)
    if pivot_index == -1:
        # Pivot not found, maybe return original or empty grid?
        # Returning an empty grid matching size might be safer.
        return [output_grid_1d.tolist()] 

    # 4. Place the pivot in the output row
    output_grid_1d[pivot_index] = 9

    # 5. Identify the movable object (non-white, non-maroon block)
    object_start, object_end, object_color = find_object(grid_1d)
    if object_start == -1:
        # Object not found, return the grid with only the pivot placed
        return [output_grid_1d.tolist()]

    object_length = object_end - object_start + 1

    # 6. Determine object position relative to pivot and calculate distance
    distance = 0
    is_left = False
    if object_end < pivot_index: # Object is to the left
        is_left = True
        distance = pivot_index - object_end - 1
    elif object_start > pivot_index: # Object is to the right
        is_left = False
        distance = object_start - pivot_index - 1
    else:
        # Should not happen if object and pivot don't overlap and are distinct
        # Handle as error or unexpected state if needed
        print("Warning: Object appears to overlap or touch pivot unexpectedly.")
        return [output_grid_1d.tolist()] # Return grid with pivot only

    # Ensure distance is non-negative
    distance = max(0, distance)

    # 7. Calculate the new starting position for the object
    new_object_start = -1
    if is_left:
        # Object was left, move it to the right
        new_object_start = pivot_index + distance + 1
    else:
        # Object was right, move it to the left
        new_object_start = pivot_index - distance - object_length

    # 8. Place the object in the output row at the new position
    new_object_end_exclusive = new_object_start + object_length
    # Check bounds before writing to avoid errors
    if 0 <= new_object_start < grid_size and 0 < new_object_end_exclusive <= grid_size:
         output_grid_1d[new_object_start:new_object_end_exclusive] = object_color
    else:
        # Handle error: Calculated position is out of bounds
        print(f"Warning: Calculated object position out of bounds. Pivot:{pivot_index}, NewStart:{new_object_start}, Length:{object_length}")
        # Return grid with only pivot, or potentially raise error

    # 9. Return the output row wrapped in a list
    return [output_grid_1d.tolist()]
```
```python
"""
Reflects a contiguous block of non-background, non-pivot pixels across a single pivot pixel (9) in a 1D list. The reflection maintains the separation distance (number of background pixels) between the block and the pivot. The block's color and length remain unchanged.
"""

import numpy as np

def find_pivot(grid_1d):
    """
    Finds the index of the pivot element (color 9) in a 1D list.

    Args:
        grid_1d: A list of integers representing the 1D grid.

    Returns:
        The index of the pivot element, or -1 if not found.
    """
    for i, pixel in enumerate(grid_1d):
        if pixel == 9:
            return i
    return -1 # Pivot not found

def find_object(grid_1d):
    """
    Finds the start index, end index (inclusive), and color of the 
    contiguous block of non-background (0) and non-pivot (9) pixels in a 1D list.

    Args:
        grid_1d: A list of integers representing the 1D grid.

    Returns:
        A tuple (start_index, end_index, color) or (-1, -1, -1) if no such object is found.
    """
    object_color = -1
    object_start = -1
    object_end = -1
    in_object = False

    for i, pixel in enumerate(grid_1d):
        if pixel != 0 and pixel != 9: # Found a pixel of the object
            if not in_object:
                # Start of the object
                object_color = pixel
                object_start = i
                in_object = True
            # Update end index while within the object
            object_end = i 
        elif in_object: 
            # Exited the object block, stop searching
            break 
            
    # Check if an object was actually found
    if object_start == -1:
        return -1, -1, -1

    return object_start, object_end, object_color

def transform(input_grid):
    """
    Transforms the input grid by reflecting the colored block across the pivot.

    Args:
        input_grid: A list of integers representing the 1D input grid.

    Returns:
        A list of integers representing the transformed 1D output grid.
    """
    # Ensure input is a list (and potentially handle if it's nested)
    if not isinstance(input_grid, list):
         # Handle error case if needed, maybe return input or raise error
         return input_grid 
    
    # Check if input might be the [[...]] format and extract the inner list if so
    grid_1d = input_grid
    if len(input_grid) == 1 and isinstance(input_grid[0], list):
        grid_1d = input_grid[0] # Work with the inner list

    grid_size = len(grid_1d)

    # 1. Initialize the output list with the background color (0)
    output_grid = np.zeros(grid_size, dtype=int)

    # 2. Locate the pivot element (9)
    pivot_index = find_pivot(grid_1d)
    if pivot_index == -1:
        # Pivot not found, return the empty grid (or handle error appropriately)
        return output_grid.tolist() 

    # 3. Place the pivot element in the output list
    output_grid[pivot_index] = 9

    # 4. Locate the movable block
    object_start, object_end, object_color = find_object(grid_1d)
    if object_start == -1:
        # Object not found, return the grid with only the pivot placed
        return output_grid.tolist()

    object_length = object_end - object_start + 1

    # 5. Determine the block's position relative to the pivot and calculate the separation distance
    distance = 0
    is_left = False
    if object_end < pivot_index: # Block is to the left of the pivot
        is_left = True
        distance = pivot_index - object_end - 1 # Count of background pixels between
    elif object_start > pivot_index: # Block is to the right of the pivot
        is_left = False
        distance = object_start - pivot_index - 1 # Count of background pixels between
    else:
        # This case (overlap or adjacent without separation) shouldn't occur based on examples
        print("Warning: Block is adjacent to or overlapping pivot unexpectedly.")
        return output_grid.tolist() # Return grid with pivot only as a safe default

    # Ensure distance is non-negative (it should be based on logic above)
    distance = max(0, distance)

    # 6. Calculate the new starting index for the block in the output list
    new_object_start = -1
    if is_left:
        # Block was left, move it to the right
        new_object_start = pivot_index + distance + 1
    else:
        # Block was right, move it to the left
        new_object_start = pivot_index - distance - object_length

    # 7. Place the block in the output list at the new position, checking bounds
    new_object_end_exclusive = new_object_start + object_length
    if 0 <= new_object_start < grid_size and 0 < new_object_end_exclusive <= grid_size:
         output_grid[new_object_start:new_object_end_exclusive] = object_color
    else:
        # Handle error: Calculated position is out of bounds
        print(f"Warning: Calculated object position out of bounds. Pivot:{pivot_index}, NewStart:{new_object_start}, Length:{object_length}")
        # Return grid with only pivot placed

    # 8. Return the final output list
    return output_grid.tolist()
```
