
## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 8 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 8 8 8 0 0 0 0 0 0 0
0 0 0 0 0 8 0 0 0 0 0 8 0 0 0 0 0
0 0 0 0 8 8 8 0 0 0 8 8 8 0 0 0 0
0 0 8 0 0 0 0 1 1 1 0 0 0 0 8 0 0
0 8 8 8 0 0 0 0 1 0 0 0 0 8 8 8 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 1 1 1 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0
0 0 0 0 1 1 1 0 0 0 1 1 1 0 0 0 0
0 0 0 0 0 1 0 0 0 0 0 1 0 0 0 0 0
0 1 1 1 0 0 0 0 8 0 0 0 0 1 1 1 0
0 0 1 0 0 0 0 8 8 8 0 0 0 0 1 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0
0 2 2 0 2 2 0 2 2 0 0 0
0 2 0 0 2 0 0 2 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 2 2 0 0 3 0 0 0
0 0 0 0 2 0 0 3 3 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0
0 0 3 0 0 3 0 0 3 0 0 0
0 3 3 0 3 3 0 3 3 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 3 0 2 2 0 0 0
0 0 0 0 3 3 0 2 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```


## train_3

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 3 0 3 0 3 0 3 0 0
0 0 3 0 0 0 3 0 0 0
0 0 3 0 0 0 3 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 8 0 0 0 0 0 0 0
0 8 8 8 0 0 0 0 0 0
0 0 8 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0
0 0 8 0 0 0 8 0 0 0
0 8 8 8 0 8 8 8 0 0
0 0 8 0 0 0 8 0 0 0
0 0 0 0 0 0 0 0 0 0
0 3 0 3 0 0 0 0 0 0
0 0 3 0 0 0 0 0 0 0
0 0 3 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


## train_4

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 1 0 0 1 0 0 0 7 0
0 0 1 0 0 1 0 7 0 0
0 0 0 0 0 0 0 0 0 0
0 1 0 0 0 0 0 0 0 0
0 0 1 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 1 0 0 0 0 0 0 0 0
0 0 1 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0
0 0 7 0 0 7 0 1 0 0
0 7 0 0 7 0 0 0 1 0
0 0 0 0 0 0 0 0 0 0
0 0 7 0 0 0 0 0 0 0
0 7 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 7 0 0 0 0 0 0 0
0 7 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

*   **Perception:**
    *   Each input grid contains pixels of three colors: white (0) and two other distinct non-white colors.
    *   The specific pair of non-white colors varies between examples (azure/blue, red/green, green/azure, blue/orange).
    *   The non-white pixels form distinct shapes or patterns (objects) on the white background.
    *   Comparing input and output grids, the overall structure and shapes formed by the non-white pixels remain identical in terms of position and form.
    *   The core transformation is a swap of the two non-white colors. Where one non-white color appeared in the input, the other non-white color appears in the output, and vice-versa.
    *   White background pixels remain unchanged.

*   **Facts:**
    
```yaml
    Input Grid:
      Properties:
        - Contains a background color: white (0).
        - Contains exactly two unique non-background colors, call them ColorA and ColorB.
      Objects:
        - Composed of contiguous pixels of ColorA.
        - Composed of contiguous pixels of ColorB.
        - Shapes and positions of these objects vary per example.
    Output Grid:
      Properties:
        - Same dimensions as the input grid.
        - Preserves the locations of all white (0) pixels from the input.
      Transformation Rule:
        - Every pixel location that held ColorA in the input grid now holds ColorB in the output grid.
        - Every pixel location that held ColorB in the input grid now holds ColorA in the output grid.
    Relationship:
      - The transformation performs a direct color swap between the two non-white colors present in the input grid, while leaving the background untouched.
    ```


*   **Natural Language Program:**
    1.  Identify the two distinct non-white colors present in the input grid. Let these colors be designated as Color1 and Color2.
    2.  Create a new output grid with the same dimensions as the input grid.
    3.  Iterate through each cell (row, column) of the input grid.
    4.  Read the color value of the current input cell.
    5.  If the input cell color is Color1, set the color of the corresponding cell in the output grid to Color2.
    6.  If the input cell color is Color2, set the color of the corresponding cell in the output grid to Color1.
    7.  If the input cell color is white (0), set the color of the corresponding cell in the output grid to white (0).
    8.  After iterating through all cells, the new grid represents the final output.
