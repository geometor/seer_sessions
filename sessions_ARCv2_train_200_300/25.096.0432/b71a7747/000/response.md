Okay, let's analyze the provided examples to understand the transformation.

## Perception

1.  **Input/Output Structure:** Both inputs and outputs are grids (2D arrays) of single-digit integers.
2.  **Content vs. Background:** The input grids seem to contain two types of numbers:
    *   "Content" numbers: These form distinct shapes or blocks (8, 9 in `train_1`; 3, 8 in `train_2`). These are also the only numbers present in the corresponding output grids.
    *   "Background/Separator" numbers: These appear to frame or separate the blocks of content numbers (1, 4, 6 in `train_1`; 1, 2 in `train_2`). These numbers are *not* present in the output grids.
3.  **Transformation:** The transformation appears to be a filtering and extraction process. The output grid is formed by:
    *   Identifying the rows and columns in the input that contain any "content" numbers.
    *   Selecting only the cells from the input grid that lie at the intersection of these identified rows and columns.
    *   Arranging these selected cells into a new, smaller grid, maintaining their original relative order.
4.  **Identifying Content Numbers:** The set of "content" numbers for a given input seems to be exactly the set of unique numbers present in the corresponding output grid.

## Facts


```yaml
Task: Grid Sub-selection based on Content

Objects:
  - Input_Grid: A 2D array of integers.
  - Output_Grid: A 2D array of integers, derived from the Input_Grid.
  - Content_Numbers: A set of integers considered significant for the transformation. These are the numbers that appear in the Output_Grid.
  - Background_Numbers: A set of integers present in the Input_Grid but not in the Output_Grid. They act as separators or padding.
  - Content_Rows: A list of row indices from the Input_Grid that contain at least one Content_Number.
  - Content_Columns: A list of column indices from the Input_Grid that contain at least one Content_Number.

Properties:
  - Input_Grid: Has dimensions (height_in, width_in). Contains both Content_Numbers and Background_Numbers.
  - Output_Grid: Has dimensions (height_out, width_out), where height_out <= height_in and width_out <= width_in. Contains only Content_Numbers. height_out is the count of Content_Rows. width_out is the count of Content_Columns.
  - Content_Numbers: Determined by the unique values present in the Output_Grid example.

Relationships:
  - The Output_Grid is composed of elements Input_Grid[r][c] where 'r' is an index in Content_Rows and 'c' is an index in Content_Columns.
  - The relative order of rows and columns from the Input_Grid is preserved in the Output_Grid.

Actions:
  1. Identify the set of Content_Numbers (e.g., by observing the unique numbers in the provided Output_Grid example).
  2. Scan the Input_Grid to determine the Content_Rows (rows containing any Content_Number).
  3. Scan the Input_Grid to determine the Content_Columns (columns containing any Content_Number).
  4. Construct the Output_Grid by extracting elements from the Input_Grid located at the intersections of Content_Rows and Content_Columns.
```


## Natural Language Program

1.  **Determine Content Numbers:** Identify the set of unique integer values present in the example output grid. Let this set be `Content_Numbers`.
2.  **Find Content Rows:** Iterate through each row index `r` of the input grid. If any cell in row `r` contains a number that is in the `Content_Numbers` set, add `r` to a list called `Content_Rows`.
3.  **Find Content Columns:** Iterate through each column index `c` of the input grid. If any cell in column `c` contains a number that is in the `Content_Numbers` set, add `c` to a list called `Content_Columns`.
4.  **Construct Output Grid:** Create a new grid (the output grid). For each row index `r` in `Content_Rows` (in order) and for each column index `c` in `Content_Columns` (in order), copy the value from the input grid at `input_grid[r][c]` to the next available cell in the output grid, filling the output grid row by row.