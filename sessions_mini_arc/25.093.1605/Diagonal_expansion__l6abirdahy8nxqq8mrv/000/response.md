## Perception of Task Elements

1.  **Input/Output Format:** Both input and output are 5x5 grids containing single non-negative integers.
2.  **Key Objects:** The non-zero integers in the input grid are the primary objects of interest. The zero values represent the background.
3.  **Transformation:** The transformation involves mapping each non-zero input digit to a diagonal line segment in the output grid.
4.  **Diagonal Pattern:** Each input digit `d` at `(r, c)` corresponds to a specific diagonal in the output, defined by the rule `column - row = c - r` (modulo 5).
5.  **Segment Length:** The length of the diagonal segment generated by an input digit depends on its row position `r`. The length `L` follows the pattern `L = 5 - 2 * abs(r - 2)`, where 2 is the middle row index (0-based).
    *   Row 0 or 4: Length 1
    *   Row 1 or 3: Length 3
    *   Row 2: Length 5
6.  **Segment Placement:** The diagonal segment of length `L` is placed such that it is centered vertically around the original input row `r`.
7.  **Overwriting/Merging:** Multiple input digits might map segments onto the same output cell. When this happens, the output cell takes the value of the *largest* digit among those mapped to it. If only one digit maps to a cell, that digit's value is used. If no non-zero digits map to a cell, it remains zero.

## YAML Facts


```yaml
task_context:
  grid_size: 5x5
  value_range: non-negative integers (single digits observed in examples)
  background_value: 0

input_elements:
  - object: grid
    properties:
      - dimensions: [5, 5]
  - object: cell
    properties:
      - row_index: integer (0-4)
      - col_index: integer (0-4)
      - value: integer
  - object: non_zero_digit
    properties:
      - value: integer > 0
      - position: [row, col]

output_elements:
  - object: grid
    properties:
      - dimensions: [5, 5]
  - object: cell
    properties:
      - row_index: integer (0-4)
      - col_index: integer (0-4)
      - value: integer

transformation_rules:
  - rule: identify_inputs
    description: Find all cells in the input grid with non-zero values.
  - rule: calculate_segment_length
    description: For each non-zero input digit `d` at `(r_in, c_in)`, calculate the length `L` of its corresponding output segment using the formula `L = 5 - 2 * abs(r_in - 2)`.
  - rule: determine_diagonal
    description: For each non-zero input digit `d` at `(r_in, c_in)`, determine the target diagonal `D = (c_in - r_in) mod 5`.
  - rule: generate_segment_coords
    description: >
      For each non-zero input digit `d` at `(r_in, c_in)` with length `L` and diagonal `D`,
      determine the set of output coordinates `(r_out, c_out)` for the segment.
      The segment spans `L` rows centered vertically at `r_in`.
      For each row `r_out` in the segment's row range, the column `c_out` is calculated as `(D + r_out) mod 5`.
  - rule: populate_output
    description: >
      Initialize the output grid with zeros.
      For each output cell `(r_out, c_out)`, determine all input digits `d` whose generated segments include this coordinate.
      Set the value of the output cell `(r_out, c_out)` to the maximum value among these input digits `d`. If no segments cover the cell, its value remains 0.

relationships:
  - type: mapping
    from: input non_zero_digit position `(r_in, c_in)`
    to: output diagonal segment
    properties:
      - diagonal_index: `(c_in - r_in) mod 5`
      - segment_length: `5 - 2 * abs(r_in - 2)`
      - vertical_centering: segment rows centered around `r_in`
  - type: merging
    description: Output cell value is the maximum of values from all input digits whose segments cover that cell.
```


## Natural Language Program

1.  Initialize an empty 5x5 output grid, filled with zeros.
2.  Create a temporary data structure (e.g., another 5x5 grid or a dictionary mapping coordinates to potential values) to store the maximum value proposed for each output cell. Initialize with zeros or empty.
3.  Iterate through each cell `(r_in, c_in)` of the input grid.
4.  If the value `d` at `(r_in, c_in)` is non-zero:
    a.  Calculate the segment length `L = 5 - 2 * abs(r_in - 2)`.
    b.  Calculate the diagonal index `D = (c_in - r_in) mod 5`.
    c.  Determine the range of output rows for the segment. The central row is `r_in`. The number of rows above the center is `floor((L-1)/2)`, and below is `ceil((L-1)/2)`. The row range is from `r_in - floor((L-1)/2)` to `r_in + ceil((L-1)/2)`.
    d.  For each `r_out` in this calculated row range:
        i.  Calculate the corresponding output column `c_out = (D + r_out) mod 5`.
        ii. Access the temporary storage for the cell `(r_out, c_out)`. Update its value to be the maximum of its current value and the input digit `d`. `storage[r_out][c_out] = max(storage[r_out][c_out], d)`.
5.  After iterating through all input cells, copy the values from the temporary storage to the final output grid.
6.  Return the final output grid.