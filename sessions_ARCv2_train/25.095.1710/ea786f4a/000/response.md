**Perception of Task Elements:**

1.  **Input/Output Structure:** Both input and output are 2D grids (matrices) of integers.
2.  **Input Content:** Each input grid contains a single cell with the value '0'. All other cells contain a uniform positive integer (e.g., 2, 1, or 3), which acts as a "background" value.
3.  **Output Content:** The output grid has the same dimensions as the input grid. It contains cells with the value '0' and cells with the original background value. The '0' from the input grid always corresponds to a '0' in the same position in the output grid. Additional cells in the output grid are also changed to '0'.
4.  **Transformation Pattern:** The transformation seems to depend on the position of the '0' in the input grid. The cells that become '0' in the output form a pattern related to their distance from the original '0'. Specifically, the pattern resembles cells whose Manhattan distance (sum of absolute differences in row and column coordinates) from the original '0' is an even number.

**YAML Facts:**


```yaml
Task: Grid Transformation based on Manhattan Distance Parity

Objects:
  - InputGrid:
      Type: 2D List/Array of Integers
      Properties:
        - rows: Integer (number of rows)
        - columns: Integer (number of columns)
        - cells: List of Lists of Integers
        - background_value: Integer (the non-zero value filling most of the grid)
        - zero_position: Tuple (row_index, column_index) of the '0' cell
  - OutputGrid:
      Type: 2D List/Array of Integers
      Properties:
        - rows: Integer (same as InputGrid)
        - columns: Integer (same as InputGrid)
        - cells: List of Lists of Integers
  - Cell:
      Type: Element within a Grid
      Properties:
        - value: Integer
        - position: Tuple (row_index, column_index)

Relationships:
  - OutputGrid dimensions are identical to InputGrid dimensions.
  - A Cell's value in the OutputGrid depends on its position relative to the InputGrid's zero_position.

Actions:
  - Identify the background_value in the InputGrid.
  - Locate the zero_position in the InputGrid.
  - For each Cell position (r, c) in the target OutputGrid dimensions:
      - Calculate the Manhattan distance between (r, c) and the zero_position.
      - Determine if the Manhattan distance is even or odd.
      - Set the OutputGrid Cell value at (r, c):
          - to '0' if the Manhattan distance is even.
          - to the background_value if the Manhattan distance is odd.

Derived Properties:
  - Manhattan Distance:
      Definition: For two positions (r1, c1) and (r2, c2), the distance is |r1 - r2| + |c1 - c2|.
      Usage: Calculated between each potential output cell position and the input zero_position.
  - Parity:
      Definition: Whether an integer is even or odd.
      Usage: Applied to the calculated Manhattan distance.
```


**Natural Language Program:**

1.  Initialize the output grid with the same dimensions as the input grid.
2.  Identify the unique non-zero integer value in the input grid; this is the `background_value`.
3.  Find the row and column index (`zero_row`, `zero_col`) of the cell containing '0' in the input grid.
4.  Iterate through each cell position (`r`, `c`) of the grid (from row 0 to max_row, and column 0 to max_col).
5.  For the current cell position (`r`, `c`), calculate the Manhattan distance to the zero cell: `distance = abs(r - zero_row) + abs(c - zero_col)`.
6.  Check if the calculated `distance` is even (i.e., `distance % 2 == 0`).
7.  If the `distance` is even, set the value of the cell at position (`r`, `c`) in the output grid to '0'.
8.  If the `distance` is odd, set the value of the cell at position (`r`, `c`) in the output grid to the `background_value`.
9.  Return the completed output grid.