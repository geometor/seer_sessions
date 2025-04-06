## Perception

The input consists of rectangular grids filled entirely with the digit `0`. The dimensions of the grids vary across the examples. The output grids have the same dimensions as their corresponding input grids. The output grids feature the digit `8` forming a rectangular border, while the interior cells retain the digit `0`. The transformation essentially draws a frame or border using the digit `8` around the original grid content (which is uniformly `0`).

## Facts


```yaml
Objects:
  - InputGrid:
      Properties:
        - type: grid
        - elements: integers (always 0)
        - dimensions:
            - height: variable (e.g., 5, 4, 5, 3)
            - width: variable (e.g., 4, 3, 6, 3)
  - OutputGrid:
      Properties:
        - type: grid
        - elements: integers (0 or 8)
        - dimensions: same as InputGrid
  - Cell:
      Properties:
        - value: integer (0 or 8)
        - position:
            - row_index: integer
            - column_index: integer
Relationships:
  - OutputGrid is derived from InputGrid.
  - Cells belong to a Grid.
  - Cells on the perimeter of the OutputGrid have a value of 8.
  - Cells in the interior of the OutputGrid have a value of 0.
Actions:
  - Identify the dimensions (height, width) of the InputGrid.
  - Create an OutputGrid with the same dimensions.
  - For each Cell in the grid:
      - Determine if the Cell's position is on the border (first row, last row, first column, or last column).
      - If the Cell is on the border, set its value in the OutputGrid to 8.
      - If the Cell is not on the border (i.e., it's in the interior), set its value in the OutputGrid to the corresponding value from the InputGrid (which is 0).
```


## Natural Language Program

1.  Determine the height and width of the input grid.
2.  Create a new grid (the output grid) with the same height and width.
3.  Iterate through each cell of the grid using its row index (`r`) and column index (`c`).
4.  For each cell:
    *   If the cell is in the first row (`r == 0`), or the last row (`r == height - 1`), or the first column (`c == 0`), or the last column (`c == width - 1`), set the value of the corresponding cell in the output grid to `8`.
    *   Otherwise (if the cell is not on the border), set the value of the corresponding cell in the output grid to `0`.
5.  Return the completed output grid.