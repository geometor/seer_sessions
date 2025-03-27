
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

Okay, let's break down the transformation logic for this task.

**Perception:**

1.  **Input Structure:** The input grids consist of three main parts vertically:
    *   A top section containing rows with various non-white colors.
    *   A single row composed entirely of gray (5) pixels acting as a separator.
    *   A bottom section composed entirely of white (0) pixels.
2.  **Output Structure:** The output grids retain the top section and the gray separator row from the input. The bottom white section is replaced with rows filled with solid colors.
3.  **Transformation Focus:** The core transformation happens in the white rows below the gray separator.
4.  **Pattern Source:** The sequence of colors used to fill the bottom rows is determined by the colors present in the row *immediately above* the gray separator row. Let's call this the "pattern row".
5.  **Filling Mechanism:** Each white row in the input corresponds to a filled row in the output. The color used to fill a specific row is taken sequentially from the pattern row. The sequence repeats (wraps around) if there are more white rows than colors in the pattern row. The *entire* row is filled with the single selected color.

**Facts (YAML):**


```yaml
task_description: Fill white rows below a gray separator based on a repeating color pattern from the row above the separator.
elements:
  - type: grid_section
    name: header
    description: One or more rows at the top containing non-white pixels. Persists unchanged in the output.
  - type: grid_row
    name: separator_row
    description: A single row consisting entirely of gray (5) pixels. Located below the header. Persists unchanged in the output.
    properties:
      color: gray (5)
      uniform: true
  - type: grid_row
    name: pattern_row
    description: The single row located immediately above the separator_row.
    properties:
      colors: Sequence of non-white colors defining the fill pattern.
  - type: grid_section
    name: target_area
    description: The section of the input grid below the separator_row, consisting entirely of white (0) pixels.
    properties:
      color: white (0)
      uniform_rows: true
  - type: grid_section
    name: filled_area
    description: The section of the output grid corresponding to the target_area, filled with solid color rows.
    properties:
      rows: Each row is filled uniformly with a single color.
relationships:
  - type: spatial
    relation: below
    subject: separator_row
    object: header
  - type: spatial
    relation: above
    subject: pattern_row
    object: separator_row
  - type: spatial
    relation: below
    subject: target_area
    object: separator_row
  - type: transformation
    relation: determines_fill_color
    subject: pattern_row
    object: filled_area
    details: Colors from pattern_row are used sequentially (modulo length of pattern) to determine the fill color for each row in filled_area.
actions:
  - name: identify_separator
    actor: system
    input: input_grid
    output: index of the first row containing only gray (5) pixels.
  - name: identify_pattern
    actor: system
    input: input_grid, separator_index
    output: sequence of colors from the row at separator_index - 1.
  - name: copy_header_and_separator
    actor: system
    input: input_grid, separator_index
    output: partial_output_grid (containing rows 0 to separator_index).
  - name: fill_target_area
    actor: system
    input: partial_output_grid, pattern_sequence, separator_index, input_grid_height
    output: completed_output_grid
    steps:
      - Iterate through row indices `r` from `separator_index + 1` to `input_grid_height - 1`.
      - Calculate relative row index `i = r - (separator_index + 1)`.
      - Calculate pattern color index `p_idx = i % len(pattern_sequence)`.
      - Get color `c = pattern_sequence[p_idx]`.
      - Fill row `r` of the output grid entirely with color `c`.

```


**Natural Language Program:**

1.  Create a copy of the input grid to serve as the initial output grid.
2.  Locate the row index (`separator_index`) of the first row that consists entirely of gray (5) pixels.
3.  Extract the sequence of colors (`pattern_colors`) from the row directly above the separator row (at `separator_index - 1`).
4.  Iterate through each row index `r` starting from the row immediately below the separator row (`separator_index + 1`) down to the last row of the grid.
5.  For each row `r`:
    a.  Calculate the position of this row relative to the first row being filled: `relative_row_index = r - (separator_index + 1)`.
    b.  Determine the index into the `pattern_colors` sequence by taking the `relative_row_index` modulo the number of colors in the `pattern_colors` sequence: `color_index = relative_row_index % len(pattern_colors)`.
    c.  Select the color (`fill_color`) from `pattern_colors` at the calculated `color_index`.
    d.  Modify the output grid by filling the entire row `r` with the `fill_color`.
6.  Return the modified output grid.
