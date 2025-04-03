
## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 4 2 2 2 2 2 2 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 2 2 2 2 2 2 4 0 0
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 8 4 4 4 4 4 4 4 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 4 4 4 4 4 4 4 8 0 0 0 0
```


## train_3

**input:**
```
0 0 0 0 0 0 0 8 9 9 9 9 9 9 9 9 9 9 9 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 9 9 9 9 9 9 9 9 9 9 9 8 0 0 0 0 0 0
```

*   **Perception:**
    *   The input and output are single rows (1D grids) of pixels.
    *   Each example contains a single contiguous block of non-white (non-zero) pixels surrounded by white (zero) pixels.
    *   This non-white block consists of two distinct colors: a single pixel of one color at the beginning, followed by a sequence of one or more pixels of a second color.
    *   The transformation moves the initial single pixel to the end of the sequence of the second color.
    *   The surrounding white pixels remain unchanged in their positions.

*   **Facts:**
    
```yaml
    task_type: object_transformation
    components:
      - name: background
        type: pixels
        properties:
          color: white (0)
          location: surrounding the active sequence
      - name: active_sequence
        type: object (contiguous non-white pixels)
        properties:
          location: embedded within the background
          composition: consists of two parts:
            - marker_pixel: the first pixel in the sequence (unique color within sequence)
            - body_pixels: the remaining pixels in the sequence (all of the same color)
    transformation:
      action: rearrangement
      target: active_sequence
      rule: move the marker_pixel to the position immediately following the last body_pixel
      constraints: the background pixels remain unchanged
    ```


*   **Natural Language Program:**
    1.  Identify the contiguous sequence of non-white pixels in the input row. Define this as the "active sequence". Note its start and end indices.
    2.  Isolate the first pixel of the "active sequence". This is the "marker pixel".
    3.  Isolate the remaining pixels of the "active sequence" (from the second pixel to the end). This is the "body sequence".
    4.  Create a new sequence by concatenating the "body sequence" followed by the "marker pixel". This is the "transformed sequence".
    5.  Construct the output row by taking the portion of the input row before the "active sequence", appending the "transformed sequence", and then appending the portion of the input row after the "active sequence".
```python
import numpy as np
from typing import List

# Helper functions (not strictly necessary for this simple case but good practice)

def find_contiguous_non_zero_sequence(row: List[int]) -> tuple[int, int]:
    """
    Finds the start and end+1 indices of the first contiguous non-zero sequence in a list.

    Args:
        row: A list of integers representing a row of the grid.

    Returns:
        A tuple (start_index, end_index). Returns (-1, -1) if no sequence is found.
        end_index points to the element *after* the last element of the sequence.
    """
    start_index = -1
    end_index = -1
    n = len(row)
    for i, pixel in enumerate(row):
        # Find the start of a potential sequence
        if pixel != 0 and start_index == -1:
            start_index = i
        # Find the end of the sequence (first zero after start)
        elif pixel == 0 and start_index != -1:
            end_index = i
            break # Found the first sequence, stop searching

    # Handle case where sequence goes to the end of the row
    if start_index != -1 and end_index == -1:
        end_index = n

    return start_index, end_index

def transform(input_grid: List[List[int]]) -> List[List[int]]:
    """
    Identifies a contiguous sequence of non-white (non-zero) pixels in the 
    single input row. It then moves the first pixel (marker) of this sequence 
    to the position immediately following the last pixel of the sequence. 
    The surrounding white (zero) pixels remain unchanged.
    Assumes the input grid contains exactly one row.
    """
    # Ensure input is a list of lists and extract the single row
    if not isinstance(input_grid, list) or not input_grid:
         raise ValueError("Input grid must be a non-empty list of lists.")
    if len(input_grid) != 1:
        # This specific task seems designed for 1-row inputs based on examples
        # If multi-row inputs are possible, the logic needs clarification.
        # For now, assume only 1 row as per examples.
        print("Warning: Expected a grid with a single row based on examples.")
        # Or raise an error: raise ValueError("Expected grid with a single row.")

    input_row = input_grid[0]
    
    # Initialize output_row as a copy of input_row
    output_row = list(input_row) 

    # 1. Identify the contiguous sequence of non-white pixels
    start_index, end_index = find_contiguous_non_zero_sequence(input_row)

    # If no sequence found or sequence is too short (e.g., length < 1), return input unchanged
    # A sequence of length 1 doesn't change when its first element moves to the end.
    if start_index == -1 or (end_index - start_index) <= 1:
        return [output_row] # Return copy in original grid format

    # 2. Isolate the "marker pixel" (the first one)
    marker_pixel = input_row[start_index]
    
    # 3. Isolate the "body sequence" (the rest of the sequence)
    body_sequence = input_row[start_index + 1 : end_index]

    # 4. Create the "transformed sequence" by appending the marker to the body
    transformed_sequence = body_sequence + [marker_pixel]

    # 5. Construct the output row
    # Get parts before and after the original sequence
    before_sequence = input_row[:start_index]
    after_sequence = input_row[end_index:]

    # Assemble the final output row
    output_row = before_sequence + transformed_sequence + after_sequence
    
    # Return the result in the expected grid format [[...]]
    return [output_row]

```
