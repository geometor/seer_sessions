
## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 8 0 0
0 0 0 0 0 0 0 0 0 0
0 0 8 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 8 0 0 0 8
0 0 0 0 0 0 0 0 0 0
0 0 8 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 8 0 0
0 0 0 0 0 0 0 0 0 0
0 0 8 0 0 0 0 0 0 0
0 0 8 0 0 0 0 0 0 0
0 0 8 0 0 0 0 0 0 0
0 0 8 0 0 8 8 8 8 8
0 0 8 0 0 0 0 0 0 0
0 0 8 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 8 0 0 0 0 8 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 8 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 8 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 8 8 8 8 8 8 0 0 0
0 0 0 0 0 0 8 0 0 0
0 0 0 0 0 0 8 0 0 0
0 0 0 0 0 0 8 0 0 0
0 0 0 0 8 0 8 0 0 0
0 0 0 0 0 0 8 0 0 0
0 0 0 0 0 0 8 0 0 0
```


## train_3

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 8 0 0 0 8 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 8 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 8 0 0 0 8
0 0 0 0 0 0 0 0 0 0
0 0 8 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0
0 8 8 8 8 8 0 0 0 0
0 8 0 0 0 8 0 0 0 0
0 8 0 0 0 8 0 0 0 0
0 8 0 0 0 8 0 0 0 0
0 0 0 0 0 8 0 0 0 0
0 0 0 0 0 8 0 0 0 0
0 0 0 0 0 8 8 8 8 8
0 0 0 0 0 0 0 0 0 0
0 0 8 0 0 0 0 0 0 0
```

*   **Perception of the elements:**
    *   The input grids contain a white background (0) and several isolated azure pixels (8).
    *   The output grids retain the original azure pixels.
    *   Additional azure pixels appear in the output grids, forming straight horizontal or vertical lines.
    *   These lines connect pairs of original azure pixels that share the same row or column.
    *   If two azure pixels are in the same row, a horizontal azure line is drawn between them (inclusive of the endpoints).
    *   If two azure pixels are in the same column, a vertical azure line is drawn between them (inclusive of the endpoints).
    *   The process seems independent for rows and columns; lines are drawn for all aligned pairs.

*   **Facts:**
    
```yaml
    task_type: drawing
    grid_properties:
      - dimensions: variable (observed 10x10)
      - background_color: white (0)
    objects:
      - type: pixel
        color: azure (8)
        role: starting_points
        properties:
          - location: (row, column)
    actions:
      - type: identify_pairs
        description: Find all pairs of azure pixels that share the same row index.
      - type: identify_pairs
        description: Find all pairs of azure pixels that share the same column index.
      - type: draw_line
        color: azure (8)
        orientation: horizontal
        condition: Connects pairs of azure pixels sharing the same row index.
        extent: Between the column indices of the paired pixels (inclusive).
      - type: draw_line
        color: azure (8)
        orientation: vertical
        condition: Connects pairs of azure pixels sharing the same column index.
        extent: Between the row indices of the paired pixels (inclusive).
    output_composition:
      - The output grid is the input grid overlaid with the newly drawn horizontal and vertical lines.
    ```


*   **Natural Language Program:**
    1.  Create a copy of the input grid to serve as the output grid.
    2.  Identify the locations (row, column) of all azure (8) pixels in the input grid.
    3.  Iterate through all unique pairs of identified azure pixel locations.
    4.  For each pair:
        a.  If the two pixels have the same row index:
            i.  Determine the minimum and maximum column indices of the pair.
            ii. Fill all pixels in the output grid at that row index, between the minimum and maximum column indices (inclusive), with the azure color (8).
        b.  If the two pixels have the same column index:
            i.  Determine the minimum and maximum row indices of the pair.
            ii. Fill all pixels in the output grid at that column index, between the minimum and maximum row indices (inclusive), with the azure color (8).
    5.  Return the modified output grid.
