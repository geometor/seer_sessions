
## train_1

**input:**
```
0 9 9 9 0 0 0 0 9 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 9 9 9 0 0 0 9 9 9 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 2 2 2 0 0 0 0 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 2 2 2 0 0 0 2 2 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


## train_3

**input:**
```
0 2 2 2 0 0 2 0 0 0 0 0 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 2 2 2 0 2 2 2 0 0 0 2 2 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

*   **Perception:**
    *   The input and output grids appear to be 1-dimensional arrays or single rows.
    *   Each grid contains objects composed of non-white pixels (maroon '9' or red '2') separated by white '0' pixels.
    *   In each example, there is one object that is larger (3 pixels wide) than the others (1 pixel wide). The color of the larger object is the same as the smaller objects within that example.
    *   The transformation seems to identify the largest object as a "pattern".
    *   It then finds all single-pixel objects of the *same color* as the pattern object.
    *   Each of these single-pixel objects is replaced by a copy of the pattern object.
    *   The replacement is centered: the copied pattern is placed such that its center pixel occupies the position of the original single pixel.
    *   The original pattern object and the background pixels remain unchanged.

*   **Facts:**
    
```yaml
    task_type: object_transformation
    grid_dimensionality: 1D # Based on examples, appears effectively 1D
    background_color: white (0)
    objects:
      - type: contiguous_block
        color: non-white (varies per example, e.g., maroon, red)
        properties:
          - size (pixel count)
          - position (indices)
    relationships:
      - pattern_object: The object with the largest size (pixel count). Assumed unique in these examples.
      - target_objects: Objects consisting of a single pixel with the same color as the pattern_object.
    actions:
      - identify: Find all non-white objects.
      - identify: Determine the pattern_object (largest).
      - identify: Find all target_objects (single pixel, same color as pattern).
      - replace: For each target_object, replace it with a copy of the pattern_object.
      - positioning: Center the copied pattern_object at the index of the original target_object.
      - preserve: Keep the original pattern_object and background pixels unchanged.
    constraints:
      - Replacement only occurs for single-pixel objects matching the pattern color.
      - The pattern object itself is not modified or replaced.
    ```


*   **Natural Language Program:**
    1.  Parse the input grid to identify all contiguous objects of non-white pixels, noting their color, size (number of pixels), and position (indices).
    2.  Find the object with the largest size. Designate this as the `pattern_object`. Record its shape/pixel sequence and color.
    3.  Identify all objects that consist of exactly one pixel and have the same color as the `pattern_object`. Designate these as `target_objects`. Record their positions (indices).
    4.  Create a copy of the input grid to serve as the output grid.
    5.  For each `target_object` identified in step 3:
        a.  Determine the index `i` of the `target_object`.
        b.  Determine the length `L` of the `pattern_object`.
        c.  Calculate the start index for the replacement: `start_index = i - floor(L / 2)`.
        d.  Calculate the end index for the replacement: `end_index = i + floor(L / 2)`.
        e.  Place the `pattern_object` into the output grid spanning the indices from `start_index` to `end_index`. Ensure boundary conditions are handled if necessary (though not apparent in these examples).
    6.  Return the modified output grid.
```python
import numpy as np

"""
Identify the largest contiguous block of non-white pixels (the 'pattern').
Find all single non-white pixels that have the same color as the pattern.
Replace each of these single pixels with a copy of the pattern, centering the pattern over the original pixel's position.
Other pixels remain unchanged.
"""

def find_objects_1d(grid_1d):
    """
    Finds contiguous blocks of non-white pixels in a 1D grid.

    Args:
        grid_1d: A 1D NumPy array representing a row of the grid.

    Returns:
        A list of dictionaries, where each dictionary represents an object
        with keys: 'color', 'size', 'start', 'end'.
    """
    objects = []
    in_object = False
    current_object = {}
    for i, pixel in enumerate(grid_1d):
        if pixel != 0 and not in_object: # Start of a new non-white object
            in_object = True
            current_object = {'color': pixel, 'size': 1, 'start': i, 'end': i}
        elif pixel != 0 and in_object: # Continuing an object
            if pixel == current_object['color']: # Same color, extend object
                current_object['size'] += 1
                current_object['end'] = i
            else: # Different non-white color, end previous object, start new one
                objects.append(current_object)
                current_object = {'color': pixel, 'size': 1, 'start': i, 'end': i}
        elif pixel == 0 and in_object: # End of an object (hit white pixel)
            in_object = False
            objects.append(current_object)
            current_object = {}
        # If pixel is 0 and not in_object, do nothing

    # If the grid ends while inside an object, add the last object
    if in_object:
        objects.append(current_object)
    return objects

def transform(input_grid):
    """
    Transforms the input grid based on the described pattern replacement rule.

    Args:
        input_grid: A list containing a single list (representing the 1D grid).
                    Example: [[0, 9, 9, 9, 0, 0, 9, 0, ...]]

    Returns:
        A list containing a single list representing the transformed 1D grid.
    """
    # Validate input format and extract the 1D row
    if not isinstance(input_grid, list) or len(input_grid) != 1 or not isinstance(input_grid[0], list):
        # Handle invalid input format if necessary, maybe raise error or return default
        return [] # Or return input_grid

    grid_1d_list = input_grid[0]
    # Handle empty row
    if not grid_1d_list:
        return [[]]

    # Convert to NumPy array for easier processing
    grid_np = np.array(grid_1d_list, dtype=int)
    output_grid_np = grid_np.copy()
    grid_len = len(grid_np)

    # Find all non-white objects in the 1D grid
    objects = find_objects_1d(grid_np)

    # If no non-white objects exist, return the original grid
    if not objects:
        return [output_grid_np.tolist()]

    # Identify the pattern object (the one with the largest size)
    try:
        pattern_object_info = max(objects, key=lambda obj: obj['size'])
    except ValueError: # Should not happen if objects list is not empty, but safe practice
         return [output_grid_np.tolist()]

    pattern_color = pattern_object_info['color']
    pattern_size = pattern_object_info['size']
    pattern_start = pattern_object_info['start']
    pattern_end = pattern_object_info['end']

    # Extract the actual pixel sequence of the pattern from the input grid
    pattern_sequence = grid_np[pattern_start : pattern_end + 1]

    # Identify target objects: single pixels (size 1) with the same color as the pattern
    target_objects_indices = [
        obj['start'] for obj in objects
        if obj['size'] == 1 and obj['color'] == pattern_color
    ]

    # Perform the replacement for each target object
    for target_index in target_objects_indices:
        # Calculate the start index for placing the pattern so it's centered
        # The center pixel of the pattern (at index pattern_size // 2 within the pattern)
        # should align with the target_index.
        start_index = target_index - (pattern_size // 2)

        # Calculate the end index (exclusive) for slicing
        end_index = start_index + pattern_size

        # --- Boundary Condition Handling ---
        # Determine the slice of the output grid to modify
        dest_start = max(0, start_index)
        dest_end = min(grid_len, end_index)

        # Determine the corresponding slice of the pattern sequence to use
        # Adjust source slice if pattern placement goes off the left edge
        src_start = max(0, -start_index)
        # Adjust source slice if pattern placement goes off the right edge
        src_end = pattern_size - max(0, end_index - grid_len)
        # --- End Boundary Handling ---


        # Ensure the calculated slices are valid before attempting replacement
        if dest_start < dest_end and src_start < src_end:
            # Place the appropriate part of the pattern sequence into the output grid
            output_grid_np[dest_start:dest_end] = pattern_sequence[src_start:src_end]

    # Return the modified grid in the required list-of-lists format
    return [output_grid_np.tolist()]
```
```python
"""
Identify the largest contiguous block of non-white pixels (the 'pattern') in the first row of the input grid.
Find all single non-white pixels in that row that have the same color as the pattern.
Replace each of these single pixels with a copy of the pattern, centering the pattern over the original pixel's position. Handle boundary conditions where the pattern might extend beyond the grid edges.
Other pixels, including the original pattern object location (unless overwritten by another replacement), remain unchanged.
Return the modified first row within a list-of-lists structure.
"""

import numpy as np
import math

def find_objects_1d(grid_1d):
    """
    Finds contiguous blocks of non-white pixels in a 1D grid (NumPy array).

    Args:
        grid_1d: A 1D NumPy array representing a row of the grid.

    Returns:
        A list of dictionaries, where each dictionary represents an object
        with keys: 'color', 'size', 'start', 'end'. Returns an empty list
        if the input is empty or contains only background pixels.
    """
    if grid_1d is None or len(grid_1d) == 0:
        return []

    objects = []
    in_object = False
    current_object = {}
    for i, pixel in enumerate(grid_1d):
        pixel_val = pixel.item() # Extract scalar value for comparison
        if pixel_val != 0 and not in_object: # Start of a new non-white object
            in_object = True
            current_object = {'color': pixel_val, 'size': 1, 'start': i, 'end': i}
        elif pixel_val != 0 and in_object: # Continuing an object
            if pixel_val == current_object['color']: # Same color, extend object
                current_object['size'] += 1
                current_object['end'] = i
            else: # Different non-white color, end previous object, start new one
                objects.append(current_object)
                current_object = {'color': pixel_val, 'size': 1, 'start': i, 'end': i}
        elif pixel_val == 0 and in_object: # End of an object (hit white pixel)
            in_object = False
            objects.append(current_object)
            current_object = {}
        # If pixel is 0 and not in_object, do nothing

    # If the grid ends while inside an object, add the last object
    if in_object:
        objects.append(current_object)
    return objects

def transform(input_grid):
    """
    Transforms the input grid based on the described pattern replacement rule,
    operating only on the first row.

    Args:
        input_grid: A list containing list(s) representing the grid rows.
                    Expected format: [[row1_data], [row2_data], ...] or just [[row1_data]].

    Returns:
        A list containing a single list representing the transformed first row,
        or the original input if input is invalid or no transformation is applicable.
    """
    # --- Input Validation ---
    if not isinstance(input_grid, list) or not input_grid:
        # Handle empty input list []
        return []
    if not isinstance(input_grid[0], list):
         # Handle cases where input is not list of lists, e.g. [1, 2, 3]
         # Depending on strictness, could raise error or return input
         return input_grid # Or maybe [[ ]] or [] ? Let's return input for now.
    
    # Handle empty first row [[]]
    if not input_grid[0]:
        return [[]]

    # --- Select and Prepare Data ---
    # Select the first row for processing
    grid_1d_list = input_grid[0]
    # Convert to NumPy array for easier processing
    grid_np = np.array(grid_1d_list, dtype=int)
    # Create a copy to modify for the output
    output_grid_np = grid_np.copy()
    grid_len = len(grid_np)

    # --- Find Objects ---
    # Find all non-white objects in the 1D grid
    objects = find_objects_1d(grid_np)

    # If no non-white objects exist, return the original first row (formatted)
    if not objects:
        return [output_grid_np.tolist()]

    # --- Identify Pattern and Targets ---
    # Identify the pattern object (the one with the largest size)
    # Use max with a default value in case objects is empty (though checked above)
    pattern_object_info = max(objects, key=lambda obj: obj['size'], default=None)
    
    # This check is redundant due to the 'if not objects' check above, but safe
    if pattern_object_info is None:
         return [output_grid_np.tolist()]

    pattern_color = pattern_object_info['color']
    pattern_size = pattern_object_info['size']
    pattern_start = pattern_object_info['start']
    pattern_end = pattern_object_info['end']

    # Extract the actual pixel sequence of the pattern from the original input grid
    pattern_sequence = grid_np[pattern_start : pattern_end + 1]

    # Identify target objects: single pixels (size 1) with the same color as the pattern
    target_objects_indices = [
        obj['start'] for obj in objects
        if obj['size'] == 1 and obj['color'] == pattern_color
    ]

    # --- Perform Replacements ---
    # Perform the replacement for each target object
    for target_index in target_objects_indices:
        # Calculate the ideal start index for placing the pattern so it's centered
        # The center pixel of the pattern (at index floor(pattern_size / 2) within the pattern)
        # should align with the target_index.
        start_index = target_index - math.floor(pattern_size / 2)

        # Calculate the ideal end index (exclusive) for slicing
        end_index = start_index + pattern_size

        # --- Boundary Condition Handling ---
        # Determine the actual slice of the output grid to modify (destination)
        dest_start = max(0, start_index)
        dest_end = min(grid_len, end_index)

        # Determine the corresponding slice of the pattern sequence to use (source)
        # Adjust source start if pattern placement starts before the grid (start_index < 0)
        src_start = max(0, -start_index)
        # Adjust source end if pattern placement ends after the grid (end_index > grid_len)
        src_end = pattern_size - max(0, end_index - grid_len)
        # --- End Boundary Handling ---

        # Ensure the calculated slices are valid before attempting replacement
        # (dest_start < dest_end) checks if there's any overlap with the grid
        # (src_start < src_end) checks if the calculated source slice is valid
        if dest_start < dest_end and src_start < src_end:
            # Place the appropriate (potentially clipped) part of the pattern sequence
            # into the output grid
            output_grid_np[dest_start:dest_end] = pattern_sequence[src_start:src_end]

    # --- Format Output ---
    # Return the modified grid in the required list-of-lists format
    return [output_grid_np.tolist()]
```
```python
"""
Processes the input grid row by row. For each row:
1. Identifies all contiguous blocks (objects) of non-white pixels.
2. Determines the largest object in the row, designating it as the 'pattern' for that row.
3. Finds all single-pixel objects within the same row that share the same color as the row's pattern.
4. Creates a copy of the row.
5. Replaces each identified single-pixel object in the copied row with a copy of the pattern, ensuring the pattern is centered over the original pixel's position.
6. Handles boundary conditions: if placing the pattern causes it to extend beyond the row's edges, the pattern is clipped accordingly.
7. The original pattern object location remains unchanged unless it is overwritten by a replacement centered on a different target pixel.
8. Returns a new grid composed of these potentially modified rows, having the same dimensions as the input grid.
"""

import numpy as np
import math

def find_objects_1d(grid_1d):
    """
    Finds contiguous blocks of non-white pixels in a 1D NumPy array (a row).

    Args:
        grid_1d: A 1D NumPy array representing a row of the grid.

    Returns:
        A list of dictionaries, where each dictionary represents an object
        with keys: 'color', 'size', 'start', 'end'. Returns an empty list
        if the input is empty or contains only background pixels (color 0).
    """
    if grid_1d is None or grid_1d.size == 0:
        return []

    objects = []
    in_object = False
    current_object = {}
    for i, pixel in enumerate(grid_1d):
        pixel_val = pixel.item() # Extract scalar value for comparison
        
        if pixel_val != 0 and not in_object: # Start of a new non-white object
            in_object = True
            current_object = {'color': pixel_val, 'size': 1, 'start': i, 'end': i}
        elif pixel_val != 0 and in_object: # Continuing an object
            if pixel_val == current_object['color']: # Same color, extend object
                current_object['size'] += 1
                current_object['end'] = i
            else: # Different non-white color, end previous object, start new one
                objects.append(current_object)
                current_object = {'color': pixel_val, 'size': 1, 'start': i, 'end': i}
                # No need to set in_object=True, it already is.
        elif pixel_val == 0 and in_object: # End of an object (hit white pixel)
            in_object = False
            objects.append(current_object)
            current_object = {}
        # If pixel is 0 and not in_object, do nothing

    # If the grid ends while inside an object, add the last object
    if in_object:
        objects.append(current_object)
        
    return objects

def transform(input_grid):
    """
    Applies the row-wise pattern replacement transformation to the input grid.

    Args:
        input_grid: A list of lists representing the input grid.

    Returns:
        A list of lists representing the transformed output grid.
    """
    # --- Input Validation and Initialization ---
    if not isinstance(input_grid, list) or not input_grid:
        return [] 
    if not all(isinstance(row, list) for row in input_grid):
         # Handle cases where input is not list of lists
         # Return input unmodified as a safe default, though error might be better
         return input_grid 

    input_np = np.array(input_grid, dtype=int)
    output_np = input_np.copy() # Create a copy to modify
    height, width = input_np.shape

    # --- Process Each Row Independently ---
    for r in range(height):
        row_np = input_np[r, :] # Get the current row from the original input
        
        # Handle empty rows within the grid
        if row_np.size == 0:
            continue 

        # --- Find Objects in the Current Row ---
        objects = find_objects_1d(row_np)

        # If no non-white objects exist in this row, skip to the next row
        if not objects:
            continue

        # --- Identify Pattern and Targets for the Row ---
        # Use max with a default value in case objects is empty (safety check)
        pattern_object_info = max(objects, key=lambda obj: obj['size'], default=None)
        
        # This check is redundant due to the 'if not objects' check above, but safe
        if pattern_object_info is None:
            continue # Should not happen if objects list is not empty

        pattern_color = pattern_object_info['color']
        pattern_size = pattern_object_info['size']
        pattern_start = pattern_object_info['start']
        pattern_end = pattern_object_info['end']

        # Extract the actual pixel sequence of the pattern from the original row
        # Ensure indices are within bounds (should be guaranteed by find_objects_1d)
        if pattern_start >= 0 and pattern_end < width:
             pattern_sequence = row_np[pattern_start : pattern_end + 1]
        else:
             # Handle potential error case if find_objects_1d returned invalid indices
             continue # Skip this row if pattern indices are bad


        # Identify target objects: single pixels (size 1) with the same color as the pattern
        target_objects_indices = [
            obj['start'] for obj in objects
            if obj['size'] == 1 and obj['color'] == pattern_color
        ]

        # --- Perform Replacements in the Output Row ---
        # Note: Replacements are done on output_np[r, :]
        for target_index in target_objects_indices:
            # Calculate the ideal start index for placing the pattern so it's centered
            start_index = target_index - math.floor(pattern_size / 2)
            # Calculate the ideal end index (exclusive) for slicing
            end_index = start_index + pattern_size

            # --- Boundary Condition Handling (Clipping) ---
            # Determine the actual slice of the output row to modify (destination)
            dest_start = max(0, start_index)
            dest_end = min(width, end_index)

            # Determine the corresponding slice of the pattern sequence to use (source)
            src_start = max(0, -start_index) 
            src_end = pattern_size - max(0, end_index - width)
            
            # Ensure the calculated slices are valid before attempting replacement
            if dest_start < dest_end and src_start < src_end and src_end <= pattern_sequence.size:
                 # Ensure the source slice doesn't exceed the pattern sequence length
                effective_src_end = min(src_end, src_start + (dest_end - dest_start))

                if src_start < effective_src_end:
                    # Place the appropriate (potentially clipped) part of the pattern sequence
                    # into the corresponding row of the output grid
                    output_np[r, dest_start:dest_end] = pattern_sequence[src_start:effective_src_end]

    # --- Format Output ---
    # Convert the final NumPy array back to a list of lists
    return output_np.tolist()
```
