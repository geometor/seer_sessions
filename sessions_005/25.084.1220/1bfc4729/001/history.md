
## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 1 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 4 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
1 1 1 1 1 1 1 1 1 1
1 0 0 0 0 0 0 0 0 1
1 1 1 1 1 1 1 1 1 1
1 0 0 0 0 0 0 0 0 1
1 0 0 0 0 0 0 0 0 1
4 0 0 0 0 0 0 0 0 4
4 0 0 0 0 0 0 0 0 4
4 4 4 4 4 4 4 4 4 4
4 0 0 0 0 0 0 0 0 4
4 4 4 4 4 4 4 4 4 4
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 6 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 7 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
6 6 6 6 6 6 6 6 6 6
6 0 0 0 0 0 0 0 0 6
6 6 6 6 6 6 6 6 6 6
6 0 0 0 0 0 0 0 0 6
6 0 0 0 0 0 0 0 0 6
7 0 0 0 0 0 0 0 0 7
7 0 0 0 0 0 0 0 0 7
7 7 7 7 7 7 7 7 7 7
7 0 0 0 0 0 0 0 0 7
7 7 7 7 7 7 7 7 7 7
```

*   **Perception**
    *   The input grids are sparse, containing predominantly white pixels (0) and exactly two non-white pixels.
    *   The two non-white pixels in the input have distinct colors and locations.
    *   The output grids have the same dimensions as the input grids.
    *   The output grids contain horizontal and vertical lines drawn in the colors of the two input pixels.
    *   Specifically, for each non-white input pixel with color C at position (row, col), a horizontal line of color C is drawn across the output grid at that `row`, and a vertical line of color C is drawn down the output grid at that `col`.
    *   At the intersection points of the lines, the color is determined by the horizontal line's color. That is, the pixel at (row1, col2) takes color C1, and the pixel at (row2, col1) takes color C2, where C1 is the color of the pixel at (row1, col1) and C2 is the color of the pixel at (row2, col2) in the input.

*   **Facts**
    
```yaml
    task_description: "Draw horizontal and vertical lines based on the position and color of two specific input pixels."
    elements:
      - element: "grid"
        properties:
          - property: "size"
            value: "Consistent between input and output (e.g., 10x10)"
          - property: "background_color"
            value: "white (0)"
      - element: "input_pixel"
        properties:
          - property: "quantity"
            value: "Exactly two non-white pixels per input grid."
          - property: "attributes"
            value: "[color (C), row (R), column (C)]"
      - element: "output_lines"
        properties:
          - property: "type"
            value: "Horizontal and Vertical"
          - property: "quantity"
            value: "Two horizontal lines and two vertical lines."
          - property: "derivation"
            value: "Each non-white input pixel (C, R, Col) generates one horizontal line at R with color C, and one vertical line at Col with color C."
          - property: "intersection_rule"
            value: "At intersections, the color of the horizontal line takes precedence."
    relationships:
      - relationship: "Input pixel to Output lines"
        details: "The position (row, col) and color (C) of each non-white input pixel determine the position and color of one horizontal line (at row, color C) and one vertical line (at col, color C) in the output."
    actions:
      - action: "Identify non-white pixels"
        actor: "System"
        input: "Input grid"
        output: "Coordinates (row1, col1), (row2, col2) and colors (C1, C2) of the two non-white pixels."
      - action: "Initialize output grid"
        actor: "System"
        input: "Input grid dimensions"
        output: "An output grid of the same size, filled with white (0)."
      - action: "Draw vertical lines"
        actor: "System"
        input: "(col1, C1), (col2, C2), output grid"
        output: "Output grid with vertical line at col1 in color C1 and vertical line at col2 in color C2."
      - action: "Draw horizontal lines"
        actor: "System"
        input: "(row1, C1), (row2, C2), output grid"
        output: "Output grid with horizontal line at row1 in color C1 and horizontal line at row2 in color C2. These lines overwrite any existing colors at their positions, including intersections."
    ```


*   **Natural Language Program**
    1.  Identify the two non-white pixels in the input grid. Record their colors (C1, C2) and their row and column coordinates (row1, col1) and (row2, col2).
    2.  Create a new output grid with the same dimensions as the input grid, filled entirely with the background color white (0).
    3.  Draw a vertical line down the entire height of the output grid at column `col1` using color `C1`.
    4.  Draw a vertical line down the entire height of the output grid at column `col2` using color `C2`.
    5.  Draw a horizontal line across the entire width of the output grid at row `row1` using color `C1`. This line will overwrite any pixels already colored in that row, including intersections with vertical lines.
    6.  Draw a horizontal line across the entire width of the output grid at row `row2` using color `C2`. This line will overwrite any pixels already colored in that row, including intersections with vertical lines.
    7.  The resulting grid is the final output.
