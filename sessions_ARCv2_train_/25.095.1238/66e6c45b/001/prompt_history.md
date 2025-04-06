
## train_1

**input:**
```
0 0 0 0
0 5 6 0
0 8 3 0
0 0 0 0
```


**output:**
```
5 0 0 6
0 0 0 0
0 0 0 0
8 0 0 3
```


## train_2

**input:**
```
0 0 0 0
0 3 4 0
0 7 6 0
0 0 0 0
```


**output:**
```
3 0 0 4
0 0 0 0
0 0 0 0
7 0 0 6
```

## Perception of the Elements

The input and output are both 4x4 grids containing single-digit integers.
The input grid has non-zero numbers clustered in the central 2x2 area (rows 1 and 2, columns 1 and 2, using 0-based indexing). The border cells (row 0, row 3, column 0, column 3) are all zeros.
The output grid contains the same non-zero numbers as the input, but they have been repositioned to the four corners of the grid (positions [0,0], [0,3], [3,0], [3,3]). All other cells in the output grid, including the central 2x2 area where the numbers originated, are filled with zeros.

Specifically, the element at:
- Input[1][1] moves to Output[0][0]
- Input[1][2] moves to Output[0][3]
- Input[2][1] moves to Output[3][0]
- Input[2][2] moves to Output[3][3]

## YAML Facts Documentation


```yaml
Grid:
  Type: 2D Array
  Dimensions: 4x4
  Cell_Content: Integer

Objects:
  - Input_Grid:
      Properties:
        - Size: 4x4
        - Central_Subgrid: Contains non-zero integers at indices [1,1], [1,2], [2,1], [2,2].
        - Border: Contains zeros.
  - Output_Grid:
      Properties:
        - Size: 4x4
        - Corners: Contain the non-zero integers from the Input_Grid's central subgrid.
          - Top_Left_Corner (0,0): Value from Input_Grid[1][1]
          - Top_Right_Corner (0,3): Value from Input_Grid[1][2]
          - Bottom_Left_Corner (3,0): Value from Input_Grid[2][1]
          - Bottom_Right_Corner (3,3): Value from Input_Grid[2][2]
        - Other_Cells: Contain zeros.

Action:
  - Name: Relocate_Central_Elements_To_Corners
  - Input: Input_Grid
  - Output: Output_Grid
  - Steps:
      1. Initialize Output_Grid as a 4x4 grid filled with zeros.
      2. Copy the value from Input_Grid[1][1] to Output_Grid[0][0].
      3. Copy the value from Input_Grid[1][2] to Output_Grid[0][3].
      4. Copy the value from Input_Grid[2][1] to Output_Grid[3][0].
      5. Copy the value from Input_Grid[2][2] to Output_Grid[3][3].

Relationships:
  - The four non-zero values in the Input_Grid's central 2x2 subgrid correspond directly to the four values at the corners of the Output_Grid.
  - The positions of the non-zero elements change from the center in the input to the corners in the output.
```


## Natural Language Program

1.  Create a new 4x4 grid, initialized entirely with zeros. This will be the output grid.
2.  Take the value from the cell at row 1, column 1 of the input grid and place it into the cell at row 0, column 0 of the output grid.
3.  Take the value from the cell at row 1, column 2 of the input grid and place it into the cell at row 0, column 3 of the output grid.
4.  Take the value from the cell at row 2, column 1 of the input grid and place it into the cell at row 3, column 0 of the output grid.
5.  Take the value from the cell at row 2, column 2 of the input grid and place it into the cell at row 3, column 3 of the output grid.
6.  Return the modified output grid.
