
## train_1

**input:**
```
0 0 0 5 5 5 5 5 5 0 9 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 9 0 5 5 5 5 5 5 0 0 0 0
```


## train_2

**input:**
```
6 6 6 6 6 0 0 9 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 9 0 0 6 6 6 6 6 0 0 0 0 0 0 0
```


## train_3

**input:**
```
0 0 0 0 7 7 7 7 7 7 0 9 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 9 0 7 7 7 7 7 7 0 0 0
```

*   **Perception:** The task involves manipulating a 1-dimensional sequence of pixels. Each example consists of an input sequence and a corresponding output sequence of the same length (22 pixels). The sequences contain three types of elements: a background of white pixels (0), a single maroon pixel (9) acting as a fixed marker, and a contiguous line of pixels of another single color (gray-5, magenta-6, or orange-7). The transformation involves moving the colored line relative to the fixed maroon marker. The line's original position is filled with white pixels. The line's new position is determined by the location of the maroon marker and the number of white pixels immediately preceding the marker.

*   **YAML Facts:**
    
```yaml
    task_type: array_manipulation_1d
    components:
      - type: background
        color: white (0)
      - type: marker
        color: maroon (9)
        count: 1
        properties:
          - fixed_position: true
      - type: object
        name: colored_line
        properties:
          - contiguous: true
          - uniform_color: true (varies per example: gray, magenta, orange)
          - variable_length: true
          - variable_position: true
    relationships:
      - type: sequence
        description: The input generally follows a pattern like [optional background] -> [colored_line] -> [gap_before] -> [marker] -> [gap_after] -> [optional background].
        elements: [colored_line, marker]
        intervening:
          - gap_before: sequence of white pixels between colored_line and marker
          - gap_after: sequence of white pixels immediately following the marker
    actions:
      - action: identify
        target: marker (maroon pixel)
        result: marker_index
      - action: identify
        target: colored_line
        result: [line_color, line_length, line_start_index, line_end_index]
      - action: identify
        target: gap_before (white pixels between line_end_index and marker_index)
        result: gap_before_length
      - action: identify
        target: first white pixel after marker
        result: first_white_after_marker_index
      - action: calculate
        target: new_line_start_index
        formula: first_white_after_marker_index + gap_before_length
      - action: modify_grid
        steps:
          - Step 1: Create a copy of the input array.
          - Step 2: Replace the original colored_line segment in the copy with white pixels.
          - Step 3: Place the colored_line (same color and length) at the calculated new_line_start_index in the copy.
    invariants:
      - marker position
      - colored_line color and length
      - array length
    ```


*   **Natural Language Program:**
    1.  Identify the single maroon pixel (9) and record its index (`marker_index`).
    2.  Identify the contiguous sequence of non-white, non-maroon pixels (the `colored_line`). Record its color (`line_color`), length (`line_length`), start index (`line_start_index`), and end index (`line_end_index`).
    3.  Calculate the length of the sequence of white pixels (0) located strictly between the end of the `colored_line` and the `marker_index`. This is `gap_before_length = marker_index - (line_end_index + 1)`.
    4.  Find the index of the first white pixel (0) that occurs immediately after the `marker_index`. This is `first_white_after_marker_index`.
    5.  Calculate the new starting index for the `colored_line`: `new_line_start_index = first_white_after_marker_index + gap_before_length`.
    6.  Create the output array by first making a copy of the input array.
    7.  In the output array, replace the pixels from `line_start_index` to `line_end_index` (the original position of the `colored_line`) with white pixels (0).
    8.  In the output array, place the `colored_line` (using `line_color` and `line_length`) starting at the calculated `new_line_start_index`.
    9.  Return the modified array.
```python
import numpy as np

def find_marker(grid):
    """
    Finds the index of the first occurrence of the marker color (maroon, 9).

    Args:
        grid (np.array): The 1D input grid.

    Returns:
        int: The index of the marker, or None if not found.
    """
    marker_indices = np.where(grid == 9)[0]
    if len(marker_indices) > 0:
        return marker_indices[0]
    else:
        return None # Marker not found

def find_colored_line(grid):
    """
    Finds the first contiguous block of non-white (0) and non-maroon (9) pixels.

    Args:
        grid (np.array): The 1D input grid.

    Returns:
        tuple: (line_color, line_length, line_start_index, line_end_index)
               or None if no such line is found.
    """
    line_color = -1
    line_length = 0
    line_start_index = -1
    line_end_index = -1
    in_line = False

    for i, pixel in enumerate(grid):
        # A pixel is part of the line if it's not white (0) and not maroon (9)
        is_line_pixel = pixel != 0 and pixel != 9
        
        if is_line_pixel and not in_line:
            # Start of a potential line
            in_line = True
            line_color = pixel
            line_start_index = i
            line_length = 1
        elif is_line_pixel and in_line:
            # Continuing the line
            if pixel == line_color: # Ensure it's the same color
                line_length += 1
            else: 
                # Found a different color - this indicates the end of the first line
                line_end_index = i - 1
                # We only care about the first contiguous line based on examples
                break 
        elif not is_line_pixel and in_line:
            # End of the line (transitioned to white or maroon)
            line_end_index = i - 1
            in_line = False
            # Found the line, stop searching
            break
            
    # Handle case where the line goes to the very end of the grid
    if in_line:
        line_end_index = len(grid) - 1

    if line_start_index != -1:
        return line_color, line_length, line_start_index, line_end_index
    else:
        return None # Line not found

def transform(input_grid):
    """
    Transforms the input grid based on the following rules:
    1. Identify the single maroon pixel (9) marker.
    2. Identify the contiguous sequence of non-white, non-maroon pixels (the colored line).
    3. Calculate the gap (number of white pixels) between the end of the line and the marker.
    4. Find the index of the first white pixel immediately after the marker.
    5. Calculate the new starting position for the line: first white index after marker + gap size.
    6. Create the output grid by copying the input.
    7. Erase the original line by setting its pixels to white (0).
    8. Draw the line (same color and length) at the new calculated position.
    """
    # Ensure input is a numpy array for efficient operations
    grid_np = np.array(input_grid, dtype=int)
    output_grid = grid_np.copy()
    
    # 1. Identify the marker
    marker_index = find_marker(grid_np)
    if marker_index is None:
        print("Error: Marker (9) not found.")
        return input_grid # Return original if marker is missing

    # 2. Identify the colored line
    line_info = find_colored_line(grid_np)
    if line_info is None:
        print("Error: Colored line not found.")
        return input_grid # Return original if line is missing
    line_color, line_length, line_start_index, line_end_index = line_info

    # 3. Calculate the gap length before the marker
    # Gap is the number of white pixels between line_end_index and marker_index
    # If the line is right before the marker, the difference is 1, gap is 0.
    gap_before_length = marker_index - (line_end_index + 1)
    # Ensure gap is not negative (shouldn't happen with valid inputs)
    gap_before_length = max(0, gap_before_length) 

    # 4. Find the index of the first white pixel after the marker
    # Based on examples, the pixel immediately after the marker is always white (0)
    # and is where the new positioning calculation starts.
    first_white_after_marker_index = marker_index + 1
    
    # Basic check if marker is at the very end
    if first_white_after_marker_index >= len(grid_np):
         print("Warning: Marker is at the end, cannot place line after it based on logic.")
         # Or maybe the logic implies wrapping or stopping? Let's proceed but be aware.
         # Based on train cases, there's always space after marker.
         # If logic requires placing part of the line, calculation below handles it.
         pass # Allow calculation to proceed, might result in out-of-bounds below

    # 5. Calculate the new starting index for the colored line
    new_line_start_index = first_white_after_marker_index + gap_before_length

    # 6. Output grid is already a copy

    # 7. Erase the original colored line by filling with white (0)
    output_grid[line_start_index : line_end_index + 1] = 0

    # 8. Place the colored line at the new position
    new_line_end_index = new_line_start_index + line_length
    # Ensure the placement does not exceed grid bounds
    # Only place the part of the line that fits within the grid
    actual_end_index = min(new_line_end_index, len(output_grid))
    actual_length = actual_end_index - new_line_start_index
    
    if actual_length > 0:
        output_grid[new_line_start_index : actual_end_index] = line_color
    
    # If actual_length < line_length, the line was truncated. This doesn't happen in examples.

    # 9. Return the modified grid as a list
    return output_grid.tolist()
```
