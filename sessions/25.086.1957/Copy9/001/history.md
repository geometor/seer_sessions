
## train_1

**input:**
```
0 0 0 0 0 0 0 0 0
0 1 1 1 0 0 0 0 0
0 1 1 1 0 0 0 0 0
0 1 1 1 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 1 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0
0 1 1 1 0 0 0 0 0
0 1 1 1 0 0 0 0 0
0 1 1 1 0 0 0 0 0
0 0 0 0 0 1 1 1 0
0 0 0 0 0 1 1 1 0
0 0 0 0 0 1 1 1 0
0 0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0 0
0 0 0 2 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 3 0 3
2 2 2 0 0 0 0 3 0
0 2 0 0 0 0 3 0 3
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 3 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 2 0 0 0 0 0
0 0 2 2 2 0 0 0 0
0 0 0 2 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 3 0 3
2 2 2 0 0 0 0 3 0
0 2 0 0 0 0 3 0 3
0 0 0 0 0 0 0 0 0
0 0 0 0 3 0 3 0 0
0 0 0 0 0 3 0 0 0
0 0 0 0 3 0 3 0 0
0 0 0 0 0 0 0 0 0
```


## train_3

**input:**
```
0 0 0 0 0 0 0 0 0 0 0
0 8 8 8 0 0 0 0 0 6 0
0 8 0 8 0 0 0 0 0 0 0
0 8 8 8 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 8 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 6 6 6 0 0 0
0 0 0 0 0 0 6 0 0 0 0
0 0 0 0 0 6 6 6 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 6 6 6
0 8 8 8 0 0 0 0 0 6 0
0 8 0 8 0 0 0 0 6 6 6
0 8 8 8 0 0 0 0 0 0 0
0 0 0 0 0 8 8 8 0 0 0
0 0 0 0 0 8 0 8 0 0 0
0 0 0 0 0 8 8 8 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 6 6 6 0 0 0
0 0 0 0 0 0 6 0 0 0 0
0 0 0 0 0 6 6 6 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

*   **Perception**
    *   The task involves identifying specific pixels in the input grid and replacing them with larger shapes in the output grid.
    *   The core operation seems to be centered around pixels that are "isolated" - meaning they don't have any adjacent neighbors (including diagonals) of the same color.
    *   These isolated pixels are replaced by a 3x3 square of the same color, centered on the original pixel's location.
    *   Pixels that are part of larger contiguous shapes (connected horizontally, vertically, or diagonally to pixels of the same color) remain unchanged in the output.
    *   The background color (white, 0) remains unchanged unless overwritten by an expanding 3x3 square.
    *   The transformation applies independently to isolated pixels of any non-background color.
    *   If the 3x3 expansion goes beyond the grid boundaries, only the portion within the grid is drawn.
    *   Expanded squares can overlap.

*   **Facts**
    
```yaml
    elements:
      - type: grid
        properties:
          - height: variable (1-30)
          - width: variable (1-30)
          - pixels: colored cells (0-9)
      - type: pixel
        properties:
          - color: integer (0-9)
          - position: (row, column)
          - neighbors: 8 adjacent cells (including diagonals)
      - type: object/shape
        properties:
          - consists_of: contiguous pixels of the same non-background color
          - size: number of pixels
    relationships:
      - type: adjacency
        between: pixels
        definition: Sharing an edge or corner (8 neighbors).
      - type: isolation
        applies_to: non-background pixel
        definition: A pixel is isolated if none of its 8 neighbors have the same color.
    actions:
      - name: identify_isolated_pixels
        input: input_grid
        output: list of coordinates of isolated pixels
        steps:
          - Iterate through each pixel in the grid.
          - If pixel color is not background (0).
          - Check its 8 neighbors.
          - If no neighbor has the same color, mark the pixel as isolated.
      - name: expand_pixel
        input: isolated_pixel_coordinate, pixel_color, grid_dimensions
        output: coordinates and color for a 3x3 square
        steps:
          - Define a 3x3 area centered at the isolated pixel's coordinate.
          - Assign the original pixel's color to all cells within this 3x3 area.
          - Clip the 3x3 area to fit within the grid boundaries.
      - name: construct_output_grid
        input: input_grid, expansions
        output: output_grid
        steps:
          - Initialize output grid as a copy of the input grid.
          - For each expansion (3x3 area and color):
          - Overwrite the corresponding pixels in the output grid with the expansion color.
    ```


*   **Natural Language Program**
    1.  Create a copy of the input grid, which will serve as the basis for the output grid.
    2.  Iterate through each pixel of the input grid using its row and column index.
    3.  For the current pixel, check if its color is non-background (not white, i.e., color > 0).
    4.  If the pixel is non-background, examine its 8 neighboring pixels (up, down, left, right, and the four diagonals).
    5.  Count how many of these neighbors have the *same* color as the current pixel. Be careful to handle neighbors outside the grid boundaries (treat them as not having the same color).
    6.  If the count of same-colored neighbors is zero, the current pixel is considered "isolated".
    7.  If the pixel is isolated:
        a.  Determine the 3x3 region centered at the isolated pixel's coordinates.
        b.  For each cell within this 3x3 region:
            i.  Check if the cell's coordinates are within the bounds of the grid.
            ii. If within bounds, update the corresponding pixel in the *output grid* (created in step 1) to the color of the original isolated pixel.
    8.  After iterating through all pixels in the input grid and applying expansions for all isolated pixels found, the modified grid is the final output.
