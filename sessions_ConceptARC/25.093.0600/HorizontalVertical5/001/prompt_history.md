
## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 4 4 4 4 4 0 0 0
0 0 0 0 4 0 0 0 0 0
0 0 0 0 4 0 0 0 0 0
0 0 0 0 4 0 0 0 0 0
0 0 4 4 4 4 4 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
3 3 3 3 3 3 3 3 3 3
0 0 0 0 0 0 0 0 0 0
0 0 4 4 4 4 4 0 0 0
0 0 0 0 4 0 0 0 0 0
0 0 0 0 4 0 0 0 0 0
0 0 0 0 4 0 0 0 0 0
0 0 4 4 4 4 4 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 4 0 0 0 0 0 4 0 0
0 4 4 4 4 4 4 4 0 0
0 4 0 0 0 0 0 4 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 3
0 0 0 0 0 0 0 0 0 3
0 4 0 0 0 0 0 4 0 3
0 4 4 4 4 4 4 4 0 3
0 4 0 0 0 0 0 4 0 3
0 0 0 0 0 0 0 0 0 3
0 0 0 0 0 0 0 0 0 3
0 0 0 0 0 0 0 0 0 3
0 0 0 0 0 0 0 0 0 3
0 0 0 0 0 0 0 0 0 3
```


## train_3

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
4 4 4 4 4 4 4 4 0 0
4 0 4 0 0 0 0 0 0 0
0 4 0 4 0 0 0 0 0 0
0 0 4 0 4 0 0 0 0 0
0 0 0 4 0 4 0 0 0 0
0 0 0 0 4 0 4 0 0 0
0 0 4 4 4 4 4 4 4 0
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
3 3 3 3 3 3 3 3 3 3
0 0 0 0 0 0 0 0 0 0
4 4 4 4 4 4 4 4 0 0
4 0 4 0 0 0 0 0 0 0
0 4 0 4 0 0 0 0 0 0
0 0 4 0 4 0 0 0 0 0
0 0 0 4 0 4 0 0 0 0
0 0 0 0 4 0 4 0 0 0
0 0 4 4 4 4 4 4 4 0
0 0 0 0 0 0 0 0 0 0
```

**Perception:**

The task involves transforming a 10x10 grid containing primarily background cells (color 0) and a shape made of cells with color 4. The transformation preserves the original grid content (the 0s and 4s) but adds a line of cells with color 3. This line is either the entire first row (row index 0) or the entire last column (column index 9). The decision of whether to fill the first row or the last column depends on the properties of the bounding box surrounding the shape formed by the color 4 cells.

**Facts:**


```yaml
# describes the elements and logic of the transformation
# from input grid to output grid

elements:
  - object: grid
    description: A 10x10 matrix of numerical values representing colors.
    properties:
      - rows: 10
      - columns: 10
  - object: cell
    description: An individual element within the grid.
    properties:
      - value: The color code (0, 3, or 4 observed).
      - position: Defined by row and column index (0-9).
  - object: background
    description: Cells with value 0.
  - object: shape
    description: A connected or disconnected group of cells with value 4.
    properties:
      - bounding_box: The smallest rectangle enclosing all cells with value 4.
        attributes:
          - row_min: The minimum row index of any cell in the shape.
          - row_max: The maximum row index of any cell in the shape.
          - col_min: The minimum column index of any cell in the shape.
          - col_max: The maximum column index of any cell in the shape.
          - height: (row_max - row_min + 1)
          - width: (col_max - col_min + 1)
  - object: modification_line
    description: A line of cells filled with value 3 in the output grid.
    properties:
      - color: 3
      - location: Either the first row (row 0) or the last column (column 9).

transformation:
  - action: copy_grid
    description: The output grid initially retains all values from the input grid.
  - action: determine_bounding_box
    description: Find the minimum and maximum row and column indices for all cells with value 4 in the input grid.
  - action: calculate_dimensions
    description: Calculate the height and width of the bounding box.
  - action: apply_modification
    description: Fill either the first row or the last column with value 3 based on conditions.
    conditions:
      - condition: If bounding_box.height equals bounding_box.width
        result: Fill all cells in the first row (row 0) with value 3.
      - condition: If bounding_box.height is less than bounding_box.width
        sub_conditions:
          - condition: If bounding_box.col_min equals 0
            result: Fill all cells in the first row (row 0) with value 3.
          - condition: If bounding_box.col_min is greater than 0
            result: Fill all cells in the last column (column 9) with value 3.
      # Note: The case where height > width is not observed in the examples,
      # but the logic covers the observed cases.

relationships:
  - The location of the modification_line (row 0 or column 9) depends on the comparison between the height and width of the shape's bounding box, and potentially the starting column (col_min) of that bounding box.
```


**Natural Language Program:**

1.  Start with the input grid.
2.  Identify all cells containing the value 4.
3.  Determine the bounding box enclosing all cells with value 4. Calculate its minimum row (`row_min`), maximum row (`row_max`), minimum column (`col_min`), and maximum column (`col_max`).
4.  Calculate the height of the bounding box: `height = row_max - row_min + 1`.
5.  Calculate the width of the bounding box: `width = col_max - col_min + 1`.
6.  Create the output grid as a copy of the input grid.
7.  **Decision:**
    a.  If `height` is equal to `width`, modify the output grid by setting the value of all cells in the first row (row index 0) to 3.
    b.  If `height` is less than `width`:
        i.  If `col_min` is equal to 0, modify the output grid by setting the value of all cells in the first row (row index 0) to 3.
        ii. If `col_min` is greater than 0, modify the output grid by setting the value of all cells in the last column (column index 9) to 3.
8.  Return the modified output grid.
