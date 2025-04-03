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