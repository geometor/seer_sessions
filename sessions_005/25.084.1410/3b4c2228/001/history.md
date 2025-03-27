
## train_1

**input:**
```
0 3 3 0 0
0 3 3 0 0
0 0 0 0 0
2 2 0 0 2
2 2 0 0 0
0 0 0 2 2
0 0 0 2 2
```


**output:**
```
1 0 0
0 0 0
0 0 0
```


## train_2

**input:**
```
0 3 3 0 0 0 3
0 3 3 0 0 0 0
0 0 0 0 2 0 0
3 0 0 0 3 3 0
0 0 3 0 3 3 0
```


**output:**
```
1 0 0
0 1 0
0 0 0
```


## train_3

**input:**
```
0 0 0 2 2
3 3 0 2 2
3 3 0 0 0
0 0 2 2 0
3 0 2 2 0
```


**output:**
```
1 0 0
0 0 0
0 0 0
```


## train_4

**input:**
```
0 0 3 3 0 0 0
2 0 3 3 0 3 0
0 0 0 0 0 0 0
3 3 0 0 2 2 0
3 3 0 0 2 2 0
0 0 3 3 0 0 0
0 0 3 3 0 0 0
```


**output:**
```
1 0 0
0 1 0
0 0 1
```


## train_5

**input:**
```
2 2 0 3 0 0 3
2 2 0 2 2 0 0
0 0 0 2 2 0 0
2 3 3 0 0 2 2
0 3 3 0 0 2 2
0 0 0 0 3 3 0
3 0 2 0 3 3 0
```


**output:**
```
1 0 0
0 1 0
0 0 0
```

*   **Perception:**
    *   The input grids vary in size and contain pixels of white (0), green (3), and red (2).
    *   The output grids are consistently 3x3 and contain only white (0) and blue (1) pixels.
    *   The input grids feature distinct 2x2 square blocks made of green pixels and sometimes red pixels.
    *   There appears to be a direct relationship between the *number* of complete 2x2 green squares in the input and the number and placement of blue pixels in the output.
    *   The red squares and any incomplete green shapes seem to be ignored in the transformation.
    *   The blue pixels in the output grid are always placed along the main diagonal (top-left to bottom-right).
    *   The number of blue pixels placed corresponds to the count of 2x2 green squares found in the input, up to a maximum of 3 (filling the diagonal of the 3x3 output).

*   **Facts:**
    
```yaml
    Task: Count specific objects and represent the count diagonally in a fixed-size grid.
    
    Input:
      Type: Grid
      Pixels: white(0), green(3), red(2)
      Size: Variable (rows/columns <= 30)
      Objects:
        - Name: GreenSquare
          Shape: 2x2
          Color: green(3)
          Relevance: Key element for transformation.
        - Name: RedSquare
          Shape: 2x2
          Color: red(2)
          Relevance: Appears irrelevant.
        - Name: Background
          Color: white(0)
    
    Output:
      Type: Grid
      Pixels: white(0), blue(1)
      Size: Fixed 3x3
    
    Transformation:
      Action: Identify and count all distinct occurrences of GreenSquare objects in the Input grid.
      Mapping: The count of GreenSquare objects determines the number of blue(1) pixels placed in the Output grid.
      Placement: Blue(1) pixels are placed sequentially along the main diagonal (top-left to bottom-right) of the 3x3 Output grid, starting at (0,0).
      Limit: A maximum of 3 blue(1) pixels are placed (corresponding to the diagonal length of the 3x3 output).
      Default: All other positions in the Output grid are filled with white(0).
    
    Relationship:
      - The number of GreenSquare objects (N) in the Input grid dictates the number of blue(1) pixels (min(N, 3)) on the main diagonal of the Output grid.
    ```


*   **Natural Language Program:**
    1.  Initialize a 3x3 grid filled with white (0) pixels; this will be the output grid.
    2.  Initialize a counter variable, `green_square_count`, to 0.
    3.  Iterate through the input grid, checking every possible top-left position (row `r`, column `c`) for a 2x2 square. Stop iterating rows at `height - 2` and columns at `width - 2`.
    4.  For each position (`r`, `c`), check if the pixels at (`r`, `c`), (`r+1`, `c`), (`r`, `c+1`), and (`r+1`, `c+1`) are all green (3).
    5.  If all four pixels are green (3), increment the `green_square_count`.
    6.  After checking all possible positions, determine the number of blue pixels to place: `num_blue = min(green_square_count, 3)`.
    7.  Iterate from `i = 0` up to `num_blue - 1`.
    8.  In the output grid, set the pixel at position (`i`, `i`) to blue (1).
    9.  Return the completed 3x3 output grid.
