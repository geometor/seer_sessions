
## train_1

**input:**
```
0 0 3 3 3 3 3 3 0 9 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 9 0 3 3 3 3 3 3 0 0 0 0
```


## train_2

**input:**
```
0 0 0 0 5 5 5 5 5 0 0 9 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 9 0 0 5 5 5 5 5 0 0
```


## train_3

**input:**
```
0 0 0 4 4 4 4 4 4 0 0 9 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 9 0 0 4 4 4 4 4 4 0
```

*   **Perception:** The task involves manipulating a 1-dimensional grid of pixels. In the provided example, the input grid contains a contiguous block of green pixels and a single maroon pixel, surrounded by white pixels. The maroon pixel appears to act as a stationary pivot point. The green block is located to the left of the maroon pixel in the input. In the output, the green block has moved to the right side of the maroon pixel, maintaining a one-pixel (white) separation. The size and color of the green block remain unchanged. The position of the maroon pixel also remains unchanged. The background remains white.

*   **Facts:**
    
```yaml
    grid_dimensions:
      - rows: 1
      - cols: 21 # Based on linear representation
    objects:
      - id: object_1
        color: green (3)
        representation: contiguous block
        input_location: indices 2-7
        output_location: indices 11-16
        attributes:
          - size: 6 pixels
          - shape: horizontal line segment
      - id: pivot_object
        color: maroon (9)
        representation: single pixel
        input_location: index 9
        output_location: index 9
        attributes:
          - size: 1 pixel
          - stationary: true
      - id: background
        color: white (0)
        representation: remaining pixels
    relationships:
      - type: spatial
        input: object_1 is left of pivot_object, separated by one white pixel (index 8).
        output: object_1 is right of pivot_object, separated by one white pixel (index 10).
    actions:
      - type: move
        target: object_1
        reference: pivot_object
        details: Move object_1 from one side of pivot_object to the other, maintaining a one-pixel separation. The space previously occupied by object_1 becomes background (white).
    ```


*   **Natural Language Program:**
    1.  Identify the single maroon (9) pixel in the input grid and note its position (index). This is the pivot point.
    2.  Identify the contiguous block of pixels that are not white (0) and not maroon (9). Note its color, start index, end index, and length. This is the movable object.
    3.  Create a new output grid of the same dimensions as the input grid, initially filled with white (0) pixels.
    4.  Place the maroon (9) pixel in the output grid at the same position (index) it occupied in the input grid.
    5.  Determine the relative position of the movable object with respect to the pivot point in the input grid (left or right).
    6.  If the movable object was to the left of the pivot point in the input grid:
        *   Calculate the starting position for the object in the output grid as `pivot_index + 2`.
        *   Place the movable object (using its original color and length) into the output grid starting at this calculated position.
    7.  If the movable object was to the right of the pivot point in the input grid:
        *   Calculate the starting position for the object in the output grid as `pivot_index - 1 - object_length`.
        *   Place the movable object (using its original color and length) into the output grid starting at this calculated position.
    8.  The final output grid is the result of these placements.
```python
"""
Identify the single maroon (9) pixel (pivot) and the contiguous block of non-white, non-maroon pixels (object) in the input 1D grid. Move the object from one side of the pivot to the other, maintaining a one-pixel white (0) separation, while keeping the pivot stationary. Fill the original location of the object with white pixels.
"""

import numpy as np

def find_pivot(grid_1d):
    """Finds the index and color of the pivot pixel (maroon, 9)."""
    for i, pixel in enumerate(grid_1d):
        if pixel == 9:
            return i, pixel
    return -1, -1 # Should not happen based on examples

def find_movable_object(grid_1d, pivot_index):
    """Finds the start index, end index, color, and length of the movable object."""
    object_color = -1
    start_index = -1
    end_index = -1
    in_object = False

    for i, pixel in enumerate(grid_1d):
        if pixel != 0 and pixel != 9: # Found a non-background, non-pivot pixel
            if not in_object:
                object_color = pixel
                start_index = i
                in_object = True
            end_index = i # Keep updating end index while in the object
        elif in_object: # Exited the object
            break

    if start_index != -1:
        length = end_index - start_index + 1
        return start_index, end_index, object_color, length
    else:
        return -1, -1, -1, 0 # Object not found

def transform(input_grid):
    """
    Moves a contiguous block of colored pixels from one side of a stationary 
    maroon (9) pixel to the other side, maintaining a one-pixel separation.
    """
    # Assuming input_grid is a list of lists, even for 1D cases (e.g., [[0, 0, 3,...]])
    # Convert to a 1D numpy array for easier processing
    grid_1d = np.array(input_grid[0])
    grid_length = len(grid_1d)

    # Initialize output_grid as a 1D array of zeros (white)
    output_grid_1d = np.zeros(grid_length, dtype=int)

    # 1. Identify the pivot point (maroon pixel)
    pivot_index, pivot_color = find_pivot(grid_1d)
    if pivot_index == -1:
         # Handle error: pivot not found (though examples guarantee it)
         return input_grid # Or raise an error

    # 2. Identify the movable object
    obj_start, obj_end, obj_color, obj_length = find_movable_object(grid_1d, pivot_index)
    if obj_start == -1:
        # Handle error: object not found
        return input_grid # Or raise an error

    # 3. Place the pivot pixel in the output grid
    output_grid_1d[pivot_index] = pivot_color

    # 4. Determine relative position and calculate new position
    if obj_end < pivot_index: # Object is to the left of the pivot
        # 5. Calculate new starting position to the right of the pivot
        new_start_index = pivot_index + 2 # +1 for pivot, +1 for gap
    else: # Object is to the right of the pivot
        # 5. Calculate new starting position to the left of the pivot
        new_start_index = pivot_index - 1 - obj_length # -1 for pivot, -1 for gap start calculation

    # Ensure new position is within bounds (although not strictly needed by examples)
    new_end_index = new_start_index + obj_length - 1
    if 0 <= new_start_index < grid_length and 0 <= new_end_index < grid_length:
         # 6. Place the movable object in the output grid at the new location
         output_grid_1d[new_start_index : new_end_index + 1] = obj_color
    else:
        # Handle case where object goes out of bounds (optional based on task constraints)
        print(f"Warning: Object placement out of bounds: {new_start_index}-{new_end_index}")
        # Decide how to handle: truncate? error? return original?
        # For now, just proceed, potentially causing numpy errors if indexes are invalid

    # Convert back to list of lists format for ARC
    output_grid = [output_grid_1d.tolist()]

    return output_grid
```
```python
"""
Identify the single maroon (9) pixel (pivot) and the contiguous block of non-white, non-maroon pixels (object) in the input 1D grid. Reflect the object across the pivot, maintaining the original distance (number of white pixels) between the object and the pivot. The pivot remains stationary, and the original location of the object becomes white (0).
"""

import numpy as np

def find_pivot(grid_1d):
    """Finds the index of the pivot pixel (maroon, 9)."""
    pivot_indices = np.where(grid_1d == 9)[0]
    if len(pivot_indices) > 0:
        return pivot_indices[0]
    return -1 # Should not happen based on examples

def find_object(grid_1d):
    """Finds the start index, end index, color, and length of the movable object."""
    object_indices = np.where((grid_1d != 0) & (grid_1d != 9))[0]
    if len(object_indices) == 0:
        return -1, -1, -1, 0 # Object not found

    start_index = object_indices[0]
    end_index = object_indices[-1]
    
    # Verify contiguity: check if all indices between start and end are present
    # and that the color is consistent
    object_color = grid_1d[start_index]
    is_contiguous = True
    for i in range(start_index, end_index + 1):
        if grid_1d[i] != object_color:
            is_contiguous = False
            break
            
    if is_contiguous and len(object_indices) == (end_index - start_index + 1):
        length = end_index - start_index + 1
        return start_index, end_index, object_color, length
    else:
        # This handles cases where non-0/9 pixels might not form a single contiguous block
        # or have varying colors within the block, though not present in examples.
        print(f"Warning: Non-contiguous or multi-colored object detected at indices {object_indices}")
        # For simplicity based on examples, let's still return the first block found
        # A more robust solution might need clarification on how to handle multiple objects.
        # Let's assume the first contiguous block IS the object.
        
        # Re-scan to find the first contiguous block
        current_start = -1
        current_color = -1
        first_block = None # (start, end, color, length)
        
        for i, pixel in enumerate(grid_1d):
             if pixel != 0 and pixel != 9:
                 if current_start == -1: # Start of a potential block
                     current_start = i
                     current_color = pixel
                 elif pixel != current_color: # Color changed, previous block ended
                      if first_block is None:
                          first_block = (current_start, i-1, grid_1d[current_start], (i-1)-current_start + 1)
                      current_start = i # Start new block
                      current_color = pixel
             elif current_start != -1: # End of the block (found 0 or 9)
                 if first_block is None:
                      first_block = (current_start, i-1, current_color, (i-1)-current_start + 1)
                 current_start = -1 # Reset block tracking
        
        # Handle block ending at the grid edge
        if current_start != -1 and first_block is None:
             first_block = (current_start, len(grid_1d)-1, current_color, (len(grid_1d)-1)-current_start + 1)

        if first_block:
             return first_block
        else: # No valid object found
             return -1, -1, -1, 0
                 


def calculate_gap(obj_start, obj_end, pivot_index):
    """Calculates the gap size between the object and the pivot."""
    if obj_end < pivot_index: # Object is to the left
        return pivot_index - obj_end - 1
    elif obj_start > pivot_index: # Object is to the right
        return obj_start - pivot_index - 1
    else: # Should not happen if object and pivot don't overlap
        return -1 

def transform(input_grid):
    """
    Moves a contiguous block of colored pixels from one side of a stationary 
    maroon (9) pixel (pivot) to the other side, preserving the gap size.
    """
    # Ensure input is treated as a list of lists, get the first (only) row
    if not isinstance(input_grid, list) or not isinstance(input_grid[0], list):
        raise ValueError("Input grid must be a list of lists.")
    
    grid_1d = np.array(input_grid[0], dtype=int)
    grid_length = len(grid_1d)

    # Initialize output_grid as a 1D array of zeros (white)
    output_grid_1d = np.zeros(grid_length, dtype=int)

    # 1. Identify the pivot point (maroon pixel)
    pivot_index = find_pivot(grid_1d)
    if pivot_index == -1:
         print("Error: Pivot (9) not found.")
         return input_grid # Return original grid if pivot missing

    # Place pivot in output
    output_grid_1d[pivot_index] = 9

    # 2. Identify the movable object
    obj_start, obj_end, obj_color, obj_length = find_object(grid_1d)
    if obj_start == -1:
        print("Warning: Movable object not found. Returning grid with only pivot.")
        # Return grid with just the pivot placed
        output_grid = [output_grid_1d.tolist()]
        return output_grid

    # 3. Calculate the gap size in the input grid
    input_gap_size = calculate_gap(obj_start, obj_end, pivot_index)
    if input_gap_size < 0:
        print("Error: Could not determine gap between object and pivot.")
        return input_grid # Or handle error appropriately

    # 4. Determine new position based on reflection and preserved gap
    if obj_end < pivot_index: # Object was to the left, move to the right
        new_start_index = pivot_index + 1 + input_gap_size
    else: # Object was to the right, move to the left
        new_start_index = pivot_index - 1 - input_gap_size - obj_length + 1 # Calculate start based on where end should be

    new_end_index = new_start_index + obj_length - 1

    # 5. Place the movable object in the output grid at the new location
    # Check bounds before placing
    if 0 <= new_start_index < grid_length and 0 <= new_end_index < grid_length:
         output_grid_1d[new_start_index : new_end_index + 1] = obj_color
    else:
        # Handle case where object goes out of bounds (optional based on task constraints)
        print(f"Warning: New object placement ({new_start_index}-{new_end_index}) out of bounds for grid length {grid_length}.")
        # Decide how to handle: truncate? error? place partially? 
        # For now, we simply won't place it if it's fully out of bounds, 
        # or numpy slicing might handle partial placement implicitly if start/end are adjusted.
        # Let's explicitly clip indices to stay within bounds if any part overlaps.
        clip_start = max(0, new_start_index)
        clip_end = min(grid_length -1, new_end_index)
        offset_start = clip_start - new_start_index # How much the object start is shifted due to left clipping
        
        if clip_start <= clip_end : # Check if any part is within bounds after clipping
             # Create the object array and slice the part that fits
             object_segment = np.full(obj_length, obj_color, dtype=int)
             place_segment = object_segment[offset_start : offset_start + (clip_end - clip_start + 1)]
             output_grid_1d[clip_start : clip_end + 1] = place_segment


    # Convert back to list of lists format for ARC
    output_grid = [output_grid_1d.tolist()]

    return output_grid
```
