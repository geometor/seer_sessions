
## train_1

**input:**
```
3 2 1 4
5 5 5 5
0 0 0 0
0 0 0 0
0 0 0 0
0 0 0 0
0 0 0 0
0 0 0 0
0 0 0 0
0 0 0 0
```


**output:**
```
3 2 1 4
5 5 5 5
3 3 3 3
2 2 2 2
1 1 1 1
4 4 4 4
3 3 3 3
2 2 2 2
1 1 1 1
4 4 4 4
```


## train_2

**input:**
```
2 1 4
5 5 5
0 0 0
0 0 0
0 0 0
0 0 0
0 0 0
0 0 0
```


**output:**
```
2 1 4
5 5 5
2 2 2
1 1 1
4 4 4
2 2 2
1 1 1
4 4 4
```


## train_3

**input:**
```
8 3
5 5
0 0
0 0
0 0
0 0
```


**output:**
```
8 3
5 5
8 8
3 3
8 8
3 3
```

Okay, let's analyze the provided examples to understand the transformation rule.

**Perception of Task Elements:**

1.  **Input Structure:** Each input grid consists of several rows. The top part has distinct features:
    *   A row containing a sequence of different colors (non-white, non-gray).
    *   Immediately below that, a row filled entirely with gray (color 5).
    *   Below the gray row, several rows filled entirely with white (color 0).
2.  **Output Structure:** The output grid retains the top two rows (the color sequence row and the gray separator row) exactly as they were in the input. The rows that were white in the input are now filled with solid colors.
3.  **Transformation:** The core transformation happens in the lower part of the grid (the initially white rows). These rows are filled row-by-row using the colors found in the very first row of the input. The sequence of colors from the first row is repeated cyclically to determine the fill color for each subsequent white row.

**Observations:**

*   The first row in the input acts as a "pattern" or "template" defining a sequence of colors.
*   The second row, always gray, acts as a separator between the pattern and the area to be filled.
*   The white rows below the gray separator are the target area for the transformation.
*   The transformation fills each target row completely with a single color.
*   The color used for filling is determined by iterating through the color sequence from the first row. The first white row gets the first color from the sequence, the second white row gets the second color, and so on. If the end of the sequence is reached, it cycles back to the beginning.

**YAML Facts:**


```yaml
task_description: Fill white rows below a gray separator using a repeating color sequence from the first row.
grid_properties:
  width: variable
  height: variable

elements:
  - object: pattern_row
    description: The first row of the input grid. Contains the sequence of colors to be used for filling. Excludes gray and white.
    properties:
      - colors: A sequence of non-white (0) and non-gray (5) colors.
      - position: Row index 0.
  - object: separator_row
    description: A row filled entirely with gray (color 5).
    properties:
      - color: gray (5)
      - position: Row index 1 (immediately below pattern_row).
  - object: fill_area
    description: Rows below the separator_row initially filled entirely with white (color 0).
    properties:
      - initial_color: white (0)
      - position: Rows starting from index 2 to the bottom of the grid.

transformation:
  - action: identify_pattern_sequence
    input: pattern_row
    output: sequence_of_colors (e.g., [3, 2, 1, 4] for train_1)
  - action: identify_fill_rows
    input: input_grid
    criteria: Rows below separator_row that are entirely white (0).
    output: list_of_row_indices_to_fill
  - action: apply_fill
    input: 
      - fill_rows (from identify_fill_rows)
      - pattern_sequence (from identify_pattern_sequence)
    process: |
      Iterate through the identified fill rows.
      For each fill row, determine the next color from the pattern sequence, cycling back to the start if needed.
      Fill the entire row with that single color.
    output_grid_modification: The identified fill rows in the output grid are filled according to the pattern sequence.
  - action: preserve_upper_rows
    input: input_grid
    process: Copy the pattern_row and separator_row from the input grid to the output grid without modification.
    output_grid_modification: The first two rows of the output grid are identical to the input grid.

relationships:
  - separator_row is always directly below pattern_row.
  - fill_area is always below separator_row.
  - The width of the filled rows matches the width of the pattern_row and separator_row.
  - The color sequence from pattern_row dictates the fill colors for the fill_area rows in a cyclical order.
```


**Natural Language Program:**

1.  Identify the sequence of colors present in the first row of the input grid. Let this be the `pattern_sequence`.
2.  Locate the row immediately below the first row, which should be entirely gray. This is the `separator_row`.
3.  Identify all rows below the `separator_row` that are composed entirely of white pixels. These are the `target_rows`.
4.  Initialize an index for the `pattern_sequence` to 0.
5.  Create the output grid, initially identical to the input grid.
6.  Iterate through each `target_row` in the input grid, identified by its row index.
7.  For the current `target_row`:
    a.  Get the color from the `pattern_sequence` at the current index.
    b.  Fill the entire corresponding row in the output grid with this color.
    c.  Increment the `pattern_sequence` index. If the index goes beyond the end of the sequence, reset it to 0 (cycle).
8.  The final output grid contains the unchanged `pattern_row` and `separator_row` from the input, followed by the newly filled rows.
