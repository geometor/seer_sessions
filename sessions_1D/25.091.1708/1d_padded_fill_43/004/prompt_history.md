
## train_1

**input:**
```
0 0 2 0 0 0 0 2 0 0 0 0 0 2 0 0 0 0 2 0 0 0 0 0 2 0 0 0 0 2 0 0 0
```


**output:**
```
0 0 2 2 2 2 2 2 0 0 0 0 0 2 2 2 2 2 2 0 0 0 0 0 2 2 2 2 2 2 0 0 0
```


## train_2

**input:**
```
0 0 0 0 3 0 0 0 3 0 0 0 0 0 0 3 0 0 0 3 0 0 0 0 0 0 3 0 0 0 3 0 0
```


**output:**
```
0 0 0 0 3 3 3 3 3 0 0 0 0 0 0 3 3 3 3 3 0 0 0 0 0 0 3 3 3 3 3 0 0
```


## train_3

**input:**
```
2 0 0 0 0 0 2 0 0 0 0 2 0 0 0 0 0 2 0 0 0 0 2 0 0 0 0 0 2 0 0 0 0
```


**output:**
```
2 2 2 2 2 2 2 0 0 0 0 2 2 2 2 2 2 2 0 0 0 0 2 2 2 2 2 2 2 0 0 0 0
```

*   **Perception of the elements:**
    *   The input and output are presented as sequences (1D arrays) of integers representing colors. White (0) is the background color.
    *   Each input sequence contains multiple occurrences of a single non-white color (e.g., red=2, green=3). These non-white pixels are separated by white pixels.
    *   The transformation identifies the span covered by the non-white pixels.
    *   The output sequence fills the gap between the first and last non-white pixel with that same non-white color. Pixels outside this span remain white.

*   **YAML documenting facts:**
    
```yaml
    task_type: sequence_manipulation
    components:
      - item: sequence
        attributes: [input, output, 1D_array, colors, fixed_length]
      - item: pixel
        attributes: [color_value, position_index]
      - item: non_white_pixel
        attributes: [color_value_C > 0]
      - item: background_pixel
        attributes: [color_value=0, white]
    transformation:
      type: fill_segment
      steps:
        - identify: non_white_color_C_in_input
        - find: first_occurrence_index_of_C (start_index)
        - find: last_occurrence_index_of_C (end_index)
        - generate_output: copy_input
        - modify_output: fill_range_from_start_index_to_end_index_inclusive_with_color_C
    relationships:
      - input_length == output_length
      - output_color_fill depends on input_non_white_color
      - output_fill_range depends on input_first_and_last_non_white_pixel_indices
    assumptions:
      - Exactly one non-white color exists in the input sequence.
      - At least one non-white pixel exists in the input sequence.
    ```


*   **Natural Language Program:**
    1.  Initialize the output sequence as an identical copy of the input sequence.
    2.  Identify the unique non-white color (let's call it `C`) present in the input sequence.
    3.  Find the index (`start_index`) of the first occurrence of color `C` in the input sequence.
    4.  Find the index (`end_index`) of the last occurrence of color `C` in the input sequence.
    5.  Iterate through all indices `i` from `start_index` to `end_index` (inclusive).
    6.  For each index `i`, set the color of the pixel at that index in the output sequence to color `C`.
    7.  Return the modified output sequence.
```python
import copy

"""
Identifies the unique non-white color C in the input sequence. Finds the index of the first occurrence (start_index) and the last occurrence (end_index) of C. Creates an output sequence by copying the input, then filling the segment from start_index to end_index (inclusive) with color C.
"""

def find_non_white_span(sequence):
    """
    Finds the non-white color, its first index, and its last index.

    Args:
        sequence (list): The input sequence of color values.

    Returns:
        tuple: (non_white_color, start_index, end_index)
               Returns (None, -1, -1) if no non-white color is found.
    """
    non_white_color = None
    start_index = -1
    end_index = -1

    for i, val in enumerate(sequence):
        if val != 0:  # Found a non-white pixel
            if non_white_color is None:
                non_white_color = val  # Store the first non-white color found
            # Ensure we only deal with one non-white color as per assumption
            # In a more robust version, we might handle multiple colors differently
            if val == non_white_color:
                if start_index == -1:
                    start_index = i  # Record the first occurrence index
                end_index = i  # Update the last occurrence index

    return non_white_color, start_index, end_index

def transform(input_sequence):
    """
    Transforms the input sequence by finding the first and last non-white pixel
    of a specific color and filling the space between them (inclusive) with that color.

    Args:
        input_sequence (list): A list of integers representing colors.

    Returns:
        list: The transformed sequence.
    """
    # Initialize output_sequence as a copy of the input
    output_sequence = list(input_sequence) # Use list() for a shallow copy

    # Find the non-white color and its span
    non_white_color, start_index, end_index = find_non_white_span(input_sequence)

    # If a non-white color and its span were found
    if non_white_color is not None and start_index != -1:
        # Iterate through the indices from start_index to end_index (inclusive)
        for i in range(start_index, end_index + 1):
            # Set the color of the pixel at index i in the output sequence to the non-white color
            output_sequence[i] = non_white_color

    # Return the modified output sequence
    return output_sequence
```
```python
import numpy as np

"""
Transforms an input grid by processing each row independently. For each row, it identifies the unique non-white color (if any) and finds the column indices of its first and last occurrences. It then fills the segment between these first and last columns (inclusive) in the output grid's corresponding row with that non-white color. Rows containing only the background color (white=0) remain unchanged.
"""

def find_row_span_and_color(row):
    """
    Finds the non-white color and its start/end column indices in a single row.

    Args:
        row (np.array): A 1D numpy array representing a row of the grid.

    Returns:
        tuple: (non_white_color, start_col, end_col)
               Returns (None, -1, -1) if no non-white color is found in the row.
    """
    non_white_color = None
    start_col = -1
    end_col = -1

    # Find indices of all non-zero elements
    non_zero_indices = np.where(row != 0)[0]

    if len(non_zero_indices) > 0:
        # Get the color of the first non-white pixel (assumption: only one non-white color per row)
        first_nz_index = non_zero_indices[0]
        non_white_color = row[first_nz_index]

        # Find the indices specifically for this color
        color_indices = np.where(row == non_white_color)[0]
        if len(color_indices) > 0:
             start_col = color_indices[0]
             end_col = color_indices[-1]
        # else: # Should not happen based on how non_white_color was found, but good practice
        #     return None, -1, -1

    return non_white_color, start_col, end_col


def transform(input_grid):
    """
    Applies the row-wise fill transformation to the input grid.

    Args:
        input_grid (np.array): A 2D numpy array representing the input grid.

    Returns:
        np.array: The transformed 2D numpy array.
    """
    # Initialize output_grid as a copy of the input grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Iterate through each row of the input grid
    for r in range(rows):
        current_row = input_grid[r, :]

        # Find the non-white color and its span in the current row
        non_white_color, start_col, end_col = find_row_span_and_color(current_row)

        # If a non-white color and a valid span were found in this row
        if non_white_color is not None and start_col != -1:
            # Fill the corresponding segment in the output grid's row
            # Note: Slicing includes start_col but excludes end_col + 1, hence the +1
            output_grid[r, start_col : end_col + 1] = non_white_color

    # Return the modified output grid
    return output_grid
```
