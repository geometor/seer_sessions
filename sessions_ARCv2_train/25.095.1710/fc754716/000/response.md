Okay, analyzing the provided examples to understand the transformation rule.

**Perception of Elements:**

1.  **Input:** Each input is a 2D grid (matrix) of numbers. The grid predominantly contains the number 0. There is exactly one non-zero number present in each input grid. The position of this non-zero number varies across examples. The size of the grid also varies.
2.  **Output:** Each output is also a 2D grid of the same dimensions as its corresponding input. The output grid consists of a frame (the outermost border rows and columns) filled with the non-zero number found in the input. The interior cells (those not part of the frame) are all filled with 0.

**YAML Facts:**


```yaml
Task: Frame Generation

Objects:
  - Input_Grid:
      Type: 2D Array (Matrix)
      Properties:
        - Dimensions (Height, Width)
        - Contains numerical values
        - Predominantly filled with 0
        - Contains exactly one non-zero value (let's call this 'Frame_Color')
        - Position of the Frame_Color value
  - Output_Grid:
      Type: 2D Array (Matrix)
      Properties:
        - Dimensions (same as Input_Grid Height, Width)
        - Contains numerical values
        - Has a border frame
        - Frame color matches the Frame_Color from Input_Grid
        - Interior cells (non-frame) are all 0

Relationships:
  - Output_Grid dimensions are identical to Input_Grid dimensions.
  - The value used to construct the frame in Output_Grid is the single non-zero value (Frame_Color) found anywhere within the Input_Grid.
  - The original position of the Frame_Color in the Input_Grid becomes 0 in the Output_Grid (along with all other interior positions).

Actions:
  - Identify the dimensions (Height H, Width W) of the Input_Grid.
  - Scan the Input_Grid to find the single non-zero value (Frame_Color).
  - Create a new Output_Grid of size H x W, initialized with 0s.
  - Set all cells in the first row (index 0) of Output_Grid to Frame_Color.
  - Set all cells in the last row (index H-1) of Output_Grid to Frame_Color.
  - Set all cells in the first column (index 0) of Output_Grid to Frame_Color.
  - Set all cells in the last column (index W-1) of Output_Grid to Frame_Color.
```


**Natural Language Program:**

1.  Read the input grid and determine its height (H) and width (W).
2.  Iterate through the input grid to find the single non-zero value; store this value as `C`.
3.  Create a new output grid with the same dimensions (H x W) and initialize all its cells to 0.
4.  Fill the top border: For each column index `j` from 0 to W-1, set the cell at row 0, column `j` of the output grid to `C`.
5.  Fill the bottom border: For each column index `j` from 0 to W-1, set the cell at row H-1, column `j` of the output grid to `C`.
6.  Fill the left border: For each row index `i` from 1 to H-2 (exclusive of top/bottom rows already filled), set the cell at row `i`, column 0 of the output grid to `C`.
7.  Fill the right border: For each row index `i` from 1 to H-2 (exclusive of top/bottom rows already filled), set the cell at row `i`, column W-1 of the output grid to `C`.
8.  Return the completed output grid.