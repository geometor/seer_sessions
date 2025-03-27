
## train_1

**input:**
```
2 2 2 2 2
8 8 8 8 8
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
```


**output:**
```
2 2 2 2 2
8 8 8 8 8
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
8 8 8 8 8
2 2 2 2 2
```


## train_2

**input:**
```
2 2 2
2 2 2
3 3 3
0 0 0
0 0 0
0 0 0
0 0 0
0 0 0
0 0 0
0 0 0
```


**output:**
```
2 2 2
2 2 2
3 3 3
0 0 0
0 0 0
0 0 0
0 0 0
3 3 3
2 2 2
2 2 2
```

Okay, I will analyze the provided examples and generate the requested deliverables.

## Perception

The input grids consist of a few rows of solid colors (red, azure, green) at the top, followed by rows of white pixels below. The output grids retain the original colored rows at the top and the white rows immediately following them. However, at the very bottom of the output grid, there's a vertically mirrored copy of the initial block of colored rows from the top of the input. The mirroring seems to happen across the horizontal centerline of the grid. For example, the color pattern in row 1 appears in the last row, the pattern in row 2 appears in the second-to-last row, and so on, only for the initial non-white rows.

## Facts


```yaml
Task: Reflect top colored rows to the bottom

Examples:
  - Input:
      Grid Dimensions: 10x5
      Objects:
        - Type: Horizontal Line
          Color: Red (2)
          Location: Row 0
        - Type: Horizontal Line
          Color: Azure (8)
          Location: Row 1
        - Type: Background
          Color: White (0)
          Location: Rows 2-9
    Output:
      Grid Dimensions: 10x5
      Objects:
        - Type: Horizontal Line
          Color: Red (2)
          Location: Row 0
        - Type: Horizontal Line
          Color: Azure (8)
          Location: Row 1
        - Type: Background
          Color: White (0)
          Location: Rows 2-7
        - Type: Horizontal Line (Reflected)
          Color: Azure (8)
          Location: Row 8 (from input Row 1)
        - Type: Horizontal Line (Reflected)
          Color: Red (2)
          Location: Row 9 (from input Row 0)
      Relationship: Rows 0 and 1 from the input are reflected vertically to Rows 9 and 8 respectively in the output. The reflection preserves the horizontal structure of the rows.

  - Input:
      Grid Dimensions: 10x3
      Objects:
        - Type: Horizontal Line
          Color: Red (2)
          Location: Rows 0, 1
        - Type: Horizontal Line
          Color: Green (3)
          Location: Row 2
        - Type: Background
          Color: White (0)
          Location: Rows 3-9
    Output:
      Grid Dimensions: 10x3
      Objects:
        - Type: Horizontal Line
          Color: Red (2)
          Location: Rows 0, 1
        - Type: Horizontal Line
          Color: Green (3)
          Location: Row 2
        - Type: Background
          Color: White (0)
          Location: Rows 3-6
        - Type: Horizontal Line (Reflected)
          Color: Green (3)
          Location: Row 7 (from input Row 2)
        - Type: Horizontal Line (Reflected)
          Color: Red (2)
          Location: Rows 8, 9 (from input Rows 1, 0 respectively)
      Relationship: Rows 0, 1, and 2 from the input are reflected vertically to Rows 9, 8, and 7 respectively in the output.

Transformation:
  Action: Identify the block of non-white rows starting from the top row of the input grid.
  Action: Determine the height (H) of the grid.
  Action: For each row `i` (0-based index) within this top non-white block:
    Copy the contents of input row `i` to the output row `H - 1 - i`.
  Action: Ensure the original top non-white rows and any intermediate white rows remain unchanged in the output grid.
```


## Natural Language Program

1.  Start with the input grid. The output grid will have the same dimensions.
2.  Initialize the output grid as a copy of the input grid.
3.  Identify all rows starting from the top (row 0) that contain at least one non-white pixel. Stop when the first fully white row is encountered or the bottom of the grid is reached. Let these identified rows be the "source rows".
4.  Determine the total number of rows (height `H`) in the grid.
5.  For each source row at index `i` (where `i` starts from 0):
    a.  Calculate the target row index `j = H - 1 - i`.
    b.  Copy the entire content of the source row `i` from the input grid to the target row `j` in the output grid.
6.  Return the modified output grid.
