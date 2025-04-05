
## train_1

**input:**
```
0 0 3 0 0
0 0 3 0 0
0 0 3 0 0
0 0 0 0 0
0 0 0 0 0
```


**output:**
```
0 0 0 0 3
0 0 0 3 0
0 0 3 0 0
0 0 0 0 0
0 0 0 0 0
```


## train_2

**input:**
```
0 0 0 0 0
0 0 0 0 0
0 0 3 3 3
0 0 0 0 0
0 0 0 0 0
```


**output:**
```
0 0 0 0 0
0 0 0 0 0
0 0 3 0 0
0 0 0 3 0
0 0 0 0 3
```


## train_3

**input:**
```
0 0 0 0 0
0 0 0 0 0
0 0 3 0 0
0 3 0 0 0
3 0 0 0 0
```


**output:**
```
0 0 0 0 0
0 0 0 0 0
3 3 3 0 0
0 0 0 0 0
0 0 0 0 0
```


## train_4

**input:**
```
3 0 0 0 0
0 3 0 0 0
0 0 3 0 0
0 0 0 0 0
0 0 0 0 0
```


**output:**
```
0 0 3 0 0
0 0 3 0 0
0 0 3 0 0
0 0 0 0 0
0 0 0 0 0
```

Okay, let's analyze the input-output pairs to understand the transformation logic.

**Perception of Task Elements:**

1.  **Grid Structure:** Both input and output are 5x5 grids containing numerical values.
2.  **Values:** The grids contain only two distinct non-zero values: '0' and '3'. '0' appears to represent the background or empty space. '3' represents the active element or object.
3.  **Objects:** The '3' values consistently form lines within the grid. These lines can be vertical, horizontal, or diagonal.
4.  **Transformation:** The core transformation involves changing the *type* or orientation of the line formed by the '3's. The original line is removed, and a new line is created.
5.  **Line Types Observed:**
    *   Vertical (constant column index)
    *   Horizontal (constant row index)
    *   Diagonal (Top-Left to Bottom-Right - constant row minus column difference)
    *   Diagonal (Bottom-Left to Top-Right - constant row plus column sum)
6.  **Mapping:** There's a clear mapping between the input line type and the output line type:
    *   Vertical input transforms into a Diagonal (Bottom-Left to Top-Right) output.
    *   Horizontal input transforms into a Diagonal (Top-Left to Bottom-Right) output.
    *   Diagonal (Bottom-Left to Top-Right) input transforms into a Horizontal output.
    *   Diagonal (Top-Left to Bottom-Right) input transforms into a Vertical output.
7.  **Output Positioning:** The generated output lines seem to have a fixed length (3 cells) and a fixed canonical position based on their type, regardless of the exact position or length of the input line.
    *   Output Vertical line is always at `column 2`, `rows 0, 1, 2`.
    *   Output Horizontal line is always at `row 2`, `columns 0, 1, 2`.
    *   Output Diagonal (TL-BR) line is always at `(2, 2), (3, 3), (4, 4)`.
    *   Output Diagonal (BL-TR) line is always at `(2, 2), (1, 3), (0, 4)`.

**YAML Fact Document:**


```yaml
grid_dimensions:
  rows: 5
  cols: 5
background_value: 0
object_value: 3
objects:
  - type: line
    properties:
      - orientation: vertical | horizontal | diagonal_tl_br | diagonal_bl_tr
      - value: 3
      - elements: list of coordinates (row, col)
actions:
  - identify_line_type:
      input: grid
      output: line_orientation (vertical, horizontal, diagonal_tl_br, diagonal_bl_tr)
  - generate_output_line:
      input: line_orientation (derived from input grid)
      output: new_grid
      process:
        - create empty grid (all 0s)
        - determine target output line type based on input line type mapping
        - draw the target output line with value 3 at its canonical position and length 3
relationships:
  - transformation_mapping:
      vertical -> diagonal_bl_tr
      horizontal -> diagonal_tl_br
      diagonal_bl_tr -> horizontal
      diagonal_tl_br -> vertical
  - canonical_output_positions:
      vertical: [(0, 2), (1, 2), (2, 2)]
      horizontal: [(2, 0), (2, 1), (2, 2)]
      diagonal_tl_br: [(2, 2), (3, 3), (4, 4)]
      diagonal_bl_tr: [(0, 4), (1, 3), (2, 2)] # Corrected order for clarity
```


**Natural Language Program:**

1.  Examine the input grid and locate all cells containing the value '3'.
2.  Determine the geometric arrangement of these '3' cells to identify the type of line they form: check if all '3's share the same column (Vertical), the same row (Horizontal), a constant sum of row and column indices (Diagonal Bottom-Left to Top-Right), or a constant difference between row and column indices (Diagonal Top-Left to Bottom-Right).
3.  Based on the identified input line type, determine the required output line type using the following transformation rules:
    *   If the input line is Vertical, the output line type is Diagonal Bottom-Left to Top-Right.
    *   If the input line is Horizontal, the output line type is Diagonal Top-Left to Bottom-Right.
    *   If the input line is Diagonal Bottom-Left to Top-Right, the output line type is Horizontal.
    *   If the input line is Diagonal Top-Left to Bottom-Right, the output line type is Vertical.
4.  Create a new 5x5 output grid, initially filled entirely with the background value '0'.
5.  Draw the determined output line onto the new grid using the value '3'. The line should consist of exactly three '3's placed in a fixed, canonical position corresponding to its type:
    *   For a Vertical output line, place '3's at coordinates (0, 2), (1, 2), and (2, 2).
    *   For a Horizontal output line, place '3's at coordinates (2, 0), (2, 1), and (2, 2).
    *   For a Diagonal Top-Left to Bottom-Right output line, place '3's at coordinates (2, 2), (3, 3), and (4, 4).
    *   For a Diagonal Bottom-Left to Top-Right output line, place '3's at coordinates (0, 4), (1, 3), and (2, 2).
6.  The resulting grid is the final output.
