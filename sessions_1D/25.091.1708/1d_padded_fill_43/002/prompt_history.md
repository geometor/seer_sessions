
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
