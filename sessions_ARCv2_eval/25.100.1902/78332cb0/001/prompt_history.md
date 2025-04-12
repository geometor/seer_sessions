
## train_1

**input:**
```
7 7 7 7 7 6 7 4 7 7 7
7 7 7 7 7 6 7 4 4 4 7
7 7 7 7 7 6 7 7 7 4 7
7 2 2 2 7 6 7 7 7 4 7
7 7 2 7 7 6 7 7 7 4 7
6 6 6 6 6 6 6 6 6 6 6
7 7 7 1 7 6 7 7 3 7 7
7 1 1 1 7 6 7 3 3 7 7
7 1 1 1 7 6 7 3 7 7 7
7 1 1 1 7 6 7 3 7 7 7
7 7 7 7 7 6 7 3 7 7 7
```


**output:**
```
7 7 7 7 7
7 7 7 7 7
7 7 7 7 7
7 2 2 2 7
7 7 2 7 7
6 6 6 6 6
7 7 3 7 7
7 3 3 7 7
7 3 7 7 7
7 3 7 7 7
7 3 7 7 7
6 6 6 6 6
7 4 7 7 7
7 4 4 4 7
7 7 7 4 7
7 7 7 4 7
7 7 7 4 7
6 6 6 6 6
7 7 7 1 7
7 1 1 1 7
7 1 1 1 7
7 1 1 1 7
7 7 7 7 7
```


## train_2

**input:**
```
7 7 7 7 7
7 7 8 8 7
7 7 8 8 7
8 8 8 7 7
7 7 7 7 7
6 6 6 6 6
7 7 7 7 7
2 2 2 7 7
7 7 2 2 7
7 7 7 2 2
7 7 7 7 7
6 6 6 6 6
7 7 7 7 7
7 9 7 9 9
7 9 9 9 7
7 9 7 7 7
7 7 7 7 7
```


**output:**
```
7 7 7 7 7 6 7 7 7 7 7 6 7 7 7 7 7
7 9 7 9 9 6 2 2 2 7 7 6 7 7 8 8 7
7 9 9 9 7 6 7 7 2 2 7 6 7 7 8 8 7
7 9 7 7 7 6 7 7 7 2 2 6 8 8 8 7 7
7 7 7 7 7 6 7 7 7 7 7 6 7 7 7 7 7
```


## train_3

**input:**
```
7 7 7 7 7 6 7 7 1 7 7 6 7 7 9 7 7
7 8 8 8 7 6 7 7 1 7 7 6 7 9 9 9 7
7 7 8 7 7 6 7 7 1 7 7 6 7 7 7 7 7
7 7 8 7 7 6 7 7 1 7 7 6 7 7 7 7 7
7 7 8 7 7 6 7 7 1 7 7 6 7 7 7 7 7
```


**output:**
```
7 7 7 7 7
7 8 8 8 7
7 7 8 7 7
7 7 8 7 7
7 7 8 7 7
6 6 6 6 6
7 7 1 7 7
7 7 1 7 7
7 7 1 7 7
7 7 1 7 7
7 7 1 7 7
6 6 6 6 6
7 7 9 7 7
7 9 9 9 7
7 7 7 7 7
7 7 7 7 7
7 7 7 7 7
```

**Perception of the Elements:**

The task involves rearranging blocks of numbers within a grid. The grids contain numerical values, where '7' appears to be a background or padding color, and '6' acts as a separator. Numbers other than 6 and 7 define distinct shapes or patterns within 5x5 blocks. The transformation depends on the initial arrangement of these blocks and separators in the input grid.

There are three distinct scenarios observed in the training examples:

1.  **Quadrant Reordering (train_1):** An 11x11 input grid with a central cross formed by a row and a column of '6's. This divides the grid into four 5x5 quadrants. These quadrants are extracted and stacked vertically in the output in a specific order (Top-Left, Bottom-Right, Top-Right, Bottom-Left), separated by single rows of '6's.
2.  **Vertical Stack to Horizontal Row (train_2):** A tall input grid composed of 5x5 blocks stacked vertically and separated by rows of '6's. These blocks are rearranged into a horizontal row in the output, in reverse order, separated by columns of '6's.
3.  **Horizontal Row to Vertical Stack (train_3):** A wide input grid composed of 5x5 blocks arranged horizontally and separated by columns of '6's. These blocks are rearranged into a vertical stack in the output, preserving the original order, separated by rows of '6's.

**YAML Facts:**


```yaml
elements:
  - object: grid
    properties:
      - type: 2D array of integers
      - contains_numbers: [0-9] # Primarily 1, 2, 3, 4, 6, 7, 8, 9 observed
      - background_color: 7
      - separator_color: 6
  - object: block
    properties:
      - type: subgrid
      - dimensions: 5x5
      - contains: a shape/pattern defined by numbers other than 6 or 7, padded with 7
  - object: shape
    properties:
      - defined_by: numbers other than 6 or 7 (e.g., 1, 2, 3, 4, 8, 9)
      - located_within: a block

relationships:
  - separator (6) divides grid into blocks or quadrants
  - blocks contain shapes
  - blocks are rearranged between input and output

actions:
  - identify_structure: determine if input is quadrant-based, vertical stack, or horizontal row based on dimensions and separator locations
  - extract_blocks: isolate the 5x5 blocks from the input grid
  - rearrange_blocks: arrange extracted blocks in the output grid according to specific rules (order, orientation)
  - insert_separators: add rows or columns of 6s between blocks in the output grid

transformation_types:
  - type_1: Quadrant Reordering (11x11 grid -> vertical stack)
    input_condition: 11x11 grid with central cross of 6s at row 5 and column 5
    output_structure: vertical stack (23x5)
    block_order: TL, BR, TR, BL
    separator: row of 6s
  - type_2: Vertical to Horizontal (stack -> row)
    input_condition: (N*5+N-1)x5 grid with rows of 6s as separators
    output_structure: horizontal row (5x(N*5+N-1))
    block_order: reversed
    separator: column of 6s
  - type_3: Horizontal to Vertical (row -> stack)
    input_condition: 5x(N*5+N-1) grid with columns of 6s as separators
    output_structure: vertical stack ((N*5+N-1)x5)
    block_order: preserved
    separator: row of 6s
```


**Natural Language Program:**

1.  **Analyze Input Structure:** Examine the dimensions of the input grid and the position of the separator color '6'.
2.  **Determine Transformation Type:**
    *   **If** the input grid is 11x11 and has a row of '6's at index 5 and a column of '6's at index 5:
        *   Identify the four 5x5 subgrids (blocks) corresponding to the Top-Left (TL: rows 0-4, cols 0-4), Top-Right (TR: rows 0-4, cols 6-10), Bottom-Left (BL: rows 6-10, cols 0-4), and Bottom-Right (BR: rows 6-10, cols 6-10) quadrants.
        *   Construct the output grid by stacking these blocks vertically in the order: TL, BR, TR, BL.
        *   Insert a single row containing five '6's between each consecutive pair of stacked blocks.
    *   **Else if** the input grid has 5 columns and rows of '6's act as separators (e.g., at row indices 5, 11, ...):
        *   Identify the 5x5 blocks located between the separator rows (and at the start/end).
        *   Construct the output grid by arranging these blocks horizontally, in reverse order compared to their vertical order in the input.
        *   Insert a single column containing five '6's between each consecutive pair of horizontal blocks.
    *   **Else if** the input grid has 5 rows and columns of '6's act as separators (e.g., at column indices 5, 11, ...):
        *   Identify the 5x5 blocks located between the separator columns (and at the start/end).
        *   Construct the output grid by stacking these blocks vertically, in the same order as their horizontal order in the input.
        *   Insert a single row containing five '6's between each consecutive pair of stacked blocks.
3.  **Return** the constructed output grid.
