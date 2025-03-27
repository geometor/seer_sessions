
## train_1

**input:**
```
2 9 2
4 4 4
9 9 9
```


**output:**
```
0 0 0
5 5 5
5 5 5
```


## train_2

**input:**
```
7 3 3
6 6 6
3 7 7
```


**output:**
```
0 0 0
5 5 5
0 0 0
```


## train_3

**input:**
```
2 2 4
2 2 4
1 1 1
```


**output:**
```
0 0 0
0 0 0
5 5 5
```


## train_4

**input:**
```
4 4 4
2 3 2
2 3 3
```


**output:**
```
5 5 5
0 0 0
0 0 0
```

## Perception

1.  **Grid Structure:** Both input and output grids are 3x3.
2.  **Color Palette:** The input grids use various colors (red, maroon, yellow, green, blue, magenta, orange). The output grids only use white (0) and gray (5).
3.  **Transformation Focus:** The transformation appears to operate on entire rows independently. The output for a given row depends solely on the content of the corresponding input row.
4.  **Row Analysis:**
    *   Some input rows consist of a single color repeated across all columns (e.g., `4 4 4`, `9 9 9`, `6 6 6`, `1 1 1`).
    *   Other input rows contain multiple different colors (e.g., `2 9 2`, `7 3 3`, `3 7 7`, `2 2 4`, `2 3 2`, `2 3 3`).
5.  **Output Pattern:**
    *   Input rows containing a single repeated color are transformed into output rows filled entirely with gray (5).
    *   Input rows containing multiple different colors are transformed into output rows filled entirely with white (0).

## YAML Facts


```yaml
task_description: Analyze each row of the input grid to determine if it consists of a single repeated color or multiple colors. Based on this analysis, generate the corresponding output row.

elements:
  - element: grid
    description: A 2D array of pixels representing colors.
    properties:
      - height: Varies (3 in examples)
      - width: Varies (3 in examples)
      - pixels: Cells containing color values (0-9).

  - element: row
    description: A horizontal line of pixels within the grid.
    properties:
      - content: Sequence of color values.
      - homogeneity: Whether all pixels in the row have the same color value.

actions:
  - action: analyze_row
    input: row (from input grid)
    output: boolean (true if homogeneous, false otherwise)
    description: Determine if all pixels in the row have the same color value.

  - action: generate_output_row
    input: boolean (result of analyze_row)
    output: row (for output grid)
    description: >
      Create a new row of the same width as the input row.
      If the input boolean is true (row was homogeneous), fill the output row with gray (5).
      If the input boolean is false (row was not homogeneous), fill the output row with white (0).

  - action: construct_output_grid
    input: List of generated output rows.
    output: grid (output grid)
    description: Assemble the generated output rows in order to form the final output grid, maintaining the original height and width.

relationships:
  - relationship: row_mapping
    source: Input grid row
    target: Output grid row
    description: Each input grid row maps directly to the output grid row at the same vertical position.
    condition: The content of the output row depends on the homogeneity of the corresponding input row.
```


## Natural Language Program

1.  Initialize an empty output grid with the same dimensions as the input grid.
2.  Iterate through each row of the input grid, from top to bottom.
3.  For the current input row:
    a.  Check if all pixels in the row have the same color value.
    b.  If all pixels have the same color value, fill the corresponding row in the output grid entirely with gray (5).
    c.  If the pixels have different color values, fill the corresponding row in the output grid entirely with white (0).
4.  Return the completed output grid.
