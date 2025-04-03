
## train_1

**input:**
```
0 0 7 3 3 3 3 3 3 3 3 3 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 3 3 3 3 3 3 3 3 3 7 0 0 0 0 0 0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 4 2 2 2 2 2 2 2 2 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 2 2 2 2 2 2 2 2 4 0 0
```


## train_3

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0 2 1 1 1 1 1 1 1 1 1 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0 1 1 1 1 1 1 1 1 1 2 0 0 0
```

*   **Perception:**
    *   The input and output grids are single rows.
    *   Each input grid contains a contiguous sequence of non-white pixels surrounded by white pixels (color 0).
    *   Within this non-white sequence, the first pixel has a unique color, and the subsequent pixels all share a different, repeating color.
    *   The transformation modifies only the non-white sequence.
    *   The first pixel of the non-white sequence is moved to the end of that sequence. The rest of the sequence shifts one position to the left to fill the gap.
    *   Alternatively, the transformation can be seen as swapping the first and the last pixels within the contiguous non-white sequence.

*   **Facts:**
    
```yaml
    task_type: transformation
    grid_dimensionality: 1D (single row)
    objects:
      - type: background
        color: white (0)
        location: surrounds the non-white sequence
      - type: sequence
        color: non-white
        location: contiguous block within the row
        properties:
          - composition: contains exactly two distinct non-white colors
          - structure:
              - starts with a single pixel of one color (color_A)
              - followed by one or more pixels of a second color (color_B)
    actions:
      - action: modify_sequence
        target: non-white sequence
        effect: swap the first and last pixels of the sequence
    relationships:
      - The non-white sequence is always contiguous.
      - The position and color of the background (white pixels) remain unchanged.
    ```


*   **Natural Language Program:**
    1.  Identify the contiguous sequence of non-white pixels in the input row.
    2.  If no non-white sequence is found, return the input unchanged.
    3.  Within the identified non-white sequence, swap the color value of the first pixel with the color value of the last pixel.
    4.  Keep all other pixels (including the surrounding white pixels and the intermediate pixels within the non-white sequence) in their original relative positions.
    5.  Construct the output row using the modified sequence and the unchanged surrounding pixels.
```python
import numpy as np

"""
Identifies the contiguous sequence of non-white pixels in the single-row input grid.
Swaps the color value of the first pixel in this sequence with the color value of the last pixel in the sequence.
Keeps all other pixels (background white pixels and intermediate sequence pixels) unchanged.
If no non-white sequence is found, or the sequence has only one pixel, returns the input grid unchanged.
"""

def transform(input_grid):
    """
    Transforms the input grid according to the described rule.

    Args:
        input_grid: A list of lists representing the input grid (expected to be 1xN).

    Returns:
        A list of lists representing the transformed grid.
    """
    # Ensure input is not empty and is a list of lists
    if not input_grid or not isinstance(input_grid, list) or not isinstance(input_grid[0], list):
        # Handle invalid input if necessary, here returning it unchanged
        return input_grid

    # Convert the first (and only) row to a numpy array for easier processing
    # Using list directly might be simpler here, actually. Let's use list.
    row_list = list(input_grid[0])
    output_row = list(row_list) # Create a copy to modify

    # Find indices of non-white pixels (value != 0)
    non_white_indices = [i for i, pixel in enumerate(row_list) if pixel != 0]

    # Check if there are at least two non-white pixels to form a sequence to swap
    if len(non_white_indices) > 1:
        # Find the start index (first non-white pixel)
        start_index = min(non_white_indices)
        # Find the end index (last non-white pixel)
        end_index = max(non_white_indices)

        # Check if these indices form a contiguous block (optional, but assumed by examples)
        # The logic works even if not strictly contiguous, just swaps first/last non-white found.
        # If contiguity is required:
        # is_contiguous = all(non_white_indices[i] == non_white_indices[0] + i for i in range(len(non_white_indices)))
        # if is_contiguous:
        
        # Swap the values at the start and end indices in the output row
        first_pixel_value = output_row[start_index]
        last_pixel_value = output_row[end_index]
        output_row[start_index] = last_pixel_value
        output_row[end_index] = first_pixel_value

    # Convert the modified row list back into the grid format (list of lists)
    output_grid = [output_row]

    return output_grid
```
