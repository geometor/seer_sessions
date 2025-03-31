
## train_1

**input:**
```
2 1 1 1 2
0 1 0 1 0
0 1 0 1 0
0 1 0 1 0
0 0 0 0 0
```


**output:**
```
2 1 1 1 2
4 1 0 1 4
4 1 0 1 4
4 1 0 1 4
4 4 4 4 4
```


## train_2

**input:**
```
0 0 0 1 2
0 0 0 1 0
0 1 0 1 0
0 1 0 0 0
2 1 0 0 0
```


**output:**
```
0 0 0 1 2
4 4 4 1 4
4 1 4 1 4
4 1 4 4 4
2 1 0 0 0
```


## train_3

**input:**
```
2 0 0 0 0 0
1 1 1 1 0 0
0 0 0 0 0 0
0 0 0 1 1 1
0 0 0 0 0 2
0 0 0 0 0 0
```


**output:**
```
2 4 4 4 4 0
1 1 1 1 4 0
0 0 4 4 4 0
0 0 4 1 1 1
0 0 4 4 4 2
0 0 0 0 0 0
```


## train_4

**input:**
```
0 0 0 0 0 2
0 1 1 1 1 1
0 0 0 0 0 0
1 1 1 1 1 0
2 0 0 0 0 0
0 0 0 0 0 0
```


**output:**
```
4 4 4 4 4 2
4 1 1 1 1 1
4 4 4 4 4 4
1 1 1 1 1 4
2 4 4 4 4 4
0 0 0 0 0 0
```


## train_5

**input:**
```
0 0 0 1 1 0 0 0 1 2
0 0 0 1 1 0 0 0 1 0
0 0 0 1 1 0 0 0 1 0
0 0 0 1 1 0 0 0 1 0
0 1 0 1 1 0 1 0 1 0
0 1 0 0 0 0 1 0 0 0
0 1 0 0 0 0 1 0 0 0
0 1 0 0 0 0 1 0 0 0
0 1 0 0 0 0 1 0 0 0
2 1 0 0 0 0 1 0 0 0
```


**output:**
```
0 0 0 1 1 0 0 0 1 2
0 0 0 1 1 0 0 0 1 4
0 0 0 1 1 0 0 0 1 4
4 4 4 1 1 4 4 4 1 4
4 1 4 1 1 4 1 4 1 4
4 1 4 4 4 4 1 4 4 4
4 1 0 0 0 0 1 0 0 0
4 1 0 0 0 0 1 0 0 0
4 1 0 0 0 0 1 0 0 0
2 1 0 0 0 0 1 0 0 0
```

*   **Perception of Task Elements:**
    *   The task involves transforming an input grid into an output grid of the same dimensions.
    *   The input grids contain pixels of three colors: white (0), blue (1), and red (2).
    *   The output grids contain pixels of four colors: white (0), blue (1), red (2), and yellow (4).
    *   Blue (1) and red (2) pixels appear to be static; their positions and colors remain unchanged between the input and output grids.
    *   White (0) pixels are the primary focus of the transformation. Some white pixels change color, while others remain white.
    *   The change in white pixels seems dependent on their proximity to blue pixels. Specifically, white pixels that are cardinally adjacent (up, down, left, or right) to at least one blue pixel in the input grid are changed to yellow (4) in the output grid.
    *   White pixels that are not cardinally adjacent to any blue pixels remain white in the output grid.

*   **YAML Fact Document:**
    
```yaml
    Grid:
      Properties:
        - dimensions (height, width) remain constant between input and output.
    Pixels:
      Types:
        - White: value 0
        - Blue: value 1
        - Red: value 2
        - Yellow: value 4 (only in output)
      Relationships:
        - Adjacency: cardinal (up, down, left, right neighbors)
    Transformation:
      Input_State:
        - White pixels (0)
        - Blue pixels (1)
        - Red pixels (2)
      Output_State:
        - Some input White pixels (0) become Yellow pixels (4)
        - Other input White pixels (0) remain White pixels (0)
        - Input Blue pixels (1) remain Blue pixels (1)
        - Input Red pixels (2) remain Red pixels (2)
      Rule:
        - Action: Change color of a pixel.
        - Target: White pixels (0) in the input grid.
        - Condition: The target White pixel must have at least one Blue pixel (1) as a cardinal neighbor (up, down, left, or right) in the input grid.
        - Result: If the condition is met, the White pixel (0) becomes a Yellow pixel (4) in the output grid. Otherwise, it remains a White pixel (0).
        - Non-Target Handling: Blue (1) and Red (2) pixels are copied directly from input to output without modification.

    ```


*   **Natural Language Program:**
    1.  Create a new grid with the same dimensions as the input grid. Initialize it as a copy of the input grid.
    2.  Iterate through each pixel (cell) of the input grid using its row and column index.
    3.  For the current pixel at `(row, col)`:
        a.  Check if the pixel's value in the input grid is white (0).
        b.  If it is white (0), then examine its cardinal neighbors (pixels at `(row-1, col)`, `(row+1, col)`, `(row, col-1)`, `(row, col+1)`), ensuring neighbor coordinates are within the grid boundaries.
        c.  Check if any of these valid cardinal neighbors in the *input* grid has the value blue (1).
        d.  If at least one cardinal neighbor is blue (1), set the value of the pixel at `(row, col)` in the *new* grid to yellow (4).
        e.  If the pixel's value in the input grid is not white (0) (i.e., it's blue (1) or red (2)), its value in the new grid remains unchanged (as it was initialized by copying).
    4.  Return the new grid as the output.
