
## train_1

**input:**
```
2 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
4 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
2 0 2 0 2 0 2 0 2 0 2 0 2
0 0 2 0 2 0 2 0 2 0 2 0 2
2 2 2 0 2 0 2 0 2 0 2 0 2
0 0 0 0 2 0 2 0 2 0 2 0 2
2 2 2 2 2 0 2 0 2 0 2 0 2
0 0 0 0 0 0 2 0 2 0 2 0 2
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 4 0 4 0 4 0 4
4 4 4 4 4 0 4 0 4 0 4 0 4
0 0 0 0 4 0 4 0 4 0 4 0 4
4 4 4 0 4 0 4 0 4 0 4 0 4
0 0 4 0 4 0 4 0 4 0 4 0 4
4 0 4 0 4 0 4 0 4 0 4 0 4
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 3
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
8 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 3 0 3 0 3 0 3 0 3 0 3
8 0 0 3 0 3 0 3 0 3 0 0
0 0 0 3 0 3 0 3 0 3 3 3
8 8 8 0 0 3 0 3 0 0 0 0
0 0 0 0 0 3 0 3 3 3 3 3
8 8 8 8 8 0 0 0 0 0 0 0
0 0 0 0 0 0 0 3 3 3 3 3
8 8 8 8 8 0 8 0 0 0 0 0
0 0 0 0 8 0 8 0 0 3 3 3
8 8 8 0 8 0 8 0 8 0 0 0
0 0 8 0 8 0 8 0 8 0 0 3
8 0 8 0 8 0 8 0 8 0 8 0
```


## train_3

**input:**
```
1 0 0 0 0 0 2
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
8 0 0 0 0 0 0
```


**output:**
```
1 0 1 0 2 0 2
0 0 1 0 2 0 0
1 1 1 0 2 2 2
0 0 0 0 0 0 0
8 8 8 0 0 2 2
0 0 8 0 8 0 0
8 0 8 0 8 0 0
```


## train_4

**input:**
```
1 0 0 0 0 0 0 0 0 2
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
1 0 1 0 1 2 0 2 0 2
0 0 1 0 1 2 0 2 0 0
1 1 1 0 1 2 0 2 2 2
0 0 0 0 1 2 0 0 0 0
1 1 1 1 1 2 2 2 2 2
0 0 0 0 0 0 0 0 0 0
1 1 1 1 1 2 2 2 2 2
0 0 0 0 0 0 0 0 0 0
1 1 1 1 1 2 2 2 2 2
0 0 0 0 0 0 0 0 0 0
```

*   **Perception:** The input grids contain a small number of non-white pixels (seeds), typically located near the corners or edges. The output grids are filled with patterns corresponding to these seed colors. The patterns seem to expand outwards from the seed locations, filling the grid based on proximity. Where regions associated with different seeds meet, there appears to be a boundary condition. Pixels equidistant from two or more different colored seeds remain white. The transformation involves calculating distances from each grid cell to the initial seeds and assigning the color of the uniquely closest seed.

*   **Facts:**
    
```yaml
    task_type: pattern_expansion
    input_features:
      - description: Grid containing a background color (white, 0) and one or more 'seed' pixels of other colors.
      - properties:
          seed_pixels:
            - description: Non-white pixels in the input.
            - count: Varies (1 to 3 in examples).
            - location: Typically near corners or edges, but can be anywhere.
            - color: Any color from 1-9.
      - background_pixels:
          - description: White pixels (0).
    output_features:
      - description: Grid filled with patterns based on the input seed pixels.
      - properties:
          patterns:
            - description: Regions colored according to the nearest seed pixel from the input.
            - shape: Determined by proximity (Voronoi regions based on Manhattan distance).
            - color: Matches the color of the corresponding input seed pixel.
          boundaries:
            - description: Pixels that remain white (0).
            - location: Occur where a pixel is equidistant from two or more different seed pixels.
    transformation:
      - type: Distance-based coloring
      - distance_metric: Manhattan distance (|row1 - row2| + |col1 - col2|)
      - rule: Each pixel in the output grid takes the color of the uniquely closest seed pixel from the input grid. If a pixel is equidistant to two or more seeds, it becomes white (0).
      - relationship: Input seed locations and colors directly determine the output patterns.
    ```


*   **Natural Language Program:**
    1.  Identify all non-white pixels in the input grid. Record their row index, column index, and color. These are the "seeds".
    2.  Create an output grid of the same dimensions as the input grid, initially filled with white (0).
    3.  For each pixel location (target\_row, target\_col) in the grid:
        a.  Calculate the Manhattan distance from this target pixel to every identified seed pixel. The Manhattan distance between (r1, c1) and (r2, c2) is `abs(r1 - r2) + abs(c1 - c2)`.
        b.  Find the minimum distance calculated in the previous step.
        c.  Identify all seeds that are located at this minimum distance from the target pixel.
        d.  If exactly one seed is at the minimum distance, set the color of the pixel at (target\_row, target\_col) in the output grid to the color of that single closest seed.
        e.  If two or more seeds are tied for the minimum distance, set the color of the pixel at (target\_row, target\_col) in the output grid to white (0).
    4.  Return the completed output grid.
