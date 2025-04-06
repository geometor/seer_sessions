
## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 5 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 5 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 5 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 2 0 0 2 0 0 2 0 0
```


**output:**
```
0 0 2 0 2 0 0 2 0 0
0 0 2 0 2 0 0 2 0 0
0 0 2 0 2 0 0 2 0 0
0 0 2 0 2 5 0 2 0 0
0 0 2 0 2 0 0 2 0 0
0 5 2 0 2 0 0 2 0 0
0 2 2 0 2 0 0 2 5 0
0 2 0 0 2 0 0 2 0 0
0 2 0 0 2 0 0 2 0 0
0 2 0 0 2 0 0 2 0 0
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 5 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 5 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 2 0 0 2 0 2 0 0 0
```


**output:**
```
0 2 0 0 2 0 0 2 0 0
0 2 0 0 2 0 0 2 0 0
0 2 0 0 2 0 0 2 0 0
0 2 0 0 2 0 5 2 0 0
0 2 0 0 2 0 2 2 0 0
0 2 5 0 2 0 2 0 0 0
0 2 0 0 2 0 2 0 0 0
0 2 0 0 2 0 2 0 0 0
0 2 0 0 2 0 2 0 0 0
0 2 0 0 2 0 2 0 0 0
```

*   **Perception:**
    *   The task operates on 2D grids (10x10) containing numerical values.
    *   The primary values present are 0, 2, and 5.
    *   The input grids have a sparse distribution of 5s and a few 2s located exclusively in the last row.
    *   The output grids are derived from the input grids. The key transformation involves identifying the columns where a '2' exists in the last row of the input. These columns are then filled entirely with '2's in the output grid.
    *   However, the original positions of the '5's from the input grid are preserved in the output grid. If a '5' was located in a column designated to be filled with '2's, the '5' takes precedence and appears in that cell in the output instead of a '2'.
    *   All other cells (those not containing an original '5' and not in a column marked by a '2' in the input's last row) remain '0'.

*   **Facts:**
    
```yaml
    Objects:
      - InputGrid: A 2D array of integers.
      - OutputGrid: A 2D array of integers, derived from InputGrid.
      - Cell: An element within a grid, defined by row and column index.
      - Value: An integer contained within a Cell (0, 2, or 5).
    
    Properties:
      - GridDimensions: rows, columns (e.g., 10x10).
      - CellCoordinates: row_index, column_index.
      - CellValue: The integer value (0, 2, or 5) at a specific coordinate.
      - LastRow: The row with the maximum row index in the InputGrid.
    
    KeyLocations:
      - TriggerColumns: Columns in the InputGrid where the Cell in the LastRow has a Value of 2.
      - PreservedValueLocations: Coordinates in the InputGrid where the CellValue is 5.
    
    Actions:
      - IdentifyTriggerColumns: Find all column indices where InputGrid[LastRow][column_index] == 2.
      - FillColumns: Populate specific columns of the OutputGrid with the Value 2.
      - PreserveValues: Copy Values of 5 from their original locations in InputGrid to the corresponding locations in OutputGrid, potentially overwriting other values.
    
    Relationships:
      - TransformationRule: The OutputGrid is generated based on TriggerColumns and PreservedValueLocations from the InputGrid.
      - ColumnFilling: TriggerColumns dictate which columns in the OutputGrid are initially filled with 2s.
      - ValuePrecedence: The Value 5 at PreservedValueLocations in the InputGrid overrides any Value (specifically 2) assigned during the FillColumns action at the same location in the OutputGrid.
    ```


*   **Natural Language Program:**
    1.  Initialize the output grid with the same dimensions as the input grid, filled entirely with zeros.
    2.  Identify the set of column indices where the value '2' appears in the last row of the input grid.
    3.  For each identified column index:
        a.  Fill the entire corresponding column in the output grid with the value '2'.
    4.  Iterate through each cell (row, column) of the input grid.
    5.  If the value of the cell in the input grid is '5':
        a.  Set the value of the corresponding cell (row, column) in the output grid to '5'.
