*   **Perception:** The task involves processing grids of single-digit integers. The transformation rule appears to depend on the grid's aspect ratio (number of rows vs. columns). Based on this ratio, the grid is scanned either row-by-row (horizontally) or column-by-column (vertically). Within each row or column, the most frequent number (the dominant number) is identified. Consecutive rows or columns sharing the same dominant number form a "band". The final output is the sequence of dominant numbers corresponding to these bands, ordered as they appear (top-to-bottom for horizontal bands, left-to-right for vertical bands). The output format (newline vs. space separated) also seems correlated with the scan direction.

*   **YAML Facts:**
    
```yaml
    task_type: grid_transformation
    input_type: grid_of_integers
    output_type: sequence_of_integers
    objects:
      - name: input_grid
        properties:
          - rows: integer
          - columns: integer
          - cells: containing single digits
      - name: scan_direction
        properties:
          - orientation: horizontal | vertical
            determination: based on grid aspect ratio (rows >= columns -> horizontal, columns > rows -> vertical)
      - name: line_scan # Represents a single row or column depending on scan_direction
        properties:
          - elements: list of integers
          - dominant_number: integer (most frequent number in the line_scan)
      - name: dominant_sequence # Sequence of dominant numbers for all lines
        properties:
          - elements: list of integers
      - name: bands # Groups of consecutive identical dominant numbers
        properties:
          - dominant_number: integer
          - extent: range of rows or columns
      - name: output_sequence
        properties:
          - elements: list of unique dominant numbers from consecutive bands
          - order: preserved from band sequence (top-to-bottom or left-to-right)
          - format: newline-separated (horizontal scan) | space-separated (vertical scan)
    actions:
      - name: determine_scan_direction
        inputs: input_grid dimensions
        outputs: scan_direction (horizontal or vertical)
      - name: calculate_dominant_number
        inputs: line_scan (row or column)
        outputs: dominant_number
      - name: generate_dominant_sequence
        inputs: input_grid, scan_direction
        outputs: dominant_sequence
      - name: identify_bands
        inputs: dominant_sequence
        outputs: list of bands (each represented by its dominant number)
      - name: format_output
        inputs: list of band dominant numbers, scan_direction
        outputs: formatted output_sequence
    relationships:
      - scan_direction depends on input_grid aspect ratio.
      - dominant_number is derived from the frequency of elements in a line_scan.
      - dominant_sequence is ordered list of dominant_numbers for each line_scan.
      - bands are identified by grouping consecutive identical numbers in dominant_sequence.
      - output_sequence is derived from the unique dominant numbers of the identified bands, in order.
      - output_format depends on scan_direction.
    ```


*   **Natural Language Program:**
    1.  Read the input grid and determine its dimensions: `R` rows and `C` columns.
    2.  Compare `R` and `C` to determine the scan direction:
        *   If `R` >= `C`, set scan direction to `horizontal`.
        *   If `C` > `R`, set scan direction to `vertical`.
    3.  Initialize an empty list called `dominant_numbers`.
    4.  If the scan direction is `horizontal`:
        *   Iterate through each row of the grid from top to bottom.
        *   For each row, find the integer that appears most frequently (the dominant number).
        *   Append this dominant number to the `dominant_numbers` list.
    5.  If the scan direction is `vertical`:
        *   Iterate through each column of the grid from left to right.
        *   For each column, find the integer that appears most frequently (the dominant number).
        *   Append this dominant number to the `dominant_numbers` list.
    6.  Initialize an empty list called `output_sequence`.
    7.  If `dominant_numbers` is not empty:
        *   Add the first number from `dominant_numbers` to `output_sequence`.
        *   Iterate through `dominant_numbers` starting from the second element.
        *   If the current number is different from the last number added to `output_sequence`, add the current number to `output_sequence`.
    8.  Format the `output_sequence` based on the scan direction:
        *   If scan direction was `horizontal`, join the numbers in `output_sequence` with newline characters.
        *   If scan direction was `vertical`, join the numbers in `output_sequence` with space characters.
    9.  Return the formatted string.