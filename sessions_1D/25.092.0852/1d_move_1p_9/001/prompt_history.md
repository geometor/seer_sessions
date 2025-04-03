
## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 4 4 4 4 4 4 4 4 4 4 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 4 4 4 4 4 4 4 4 4 4 0 0 0 0 0
```


## train_2

**input:**
```
0 0 0 0 0 0 0 7 7 7 7 7 7 7 7 7 7 7 7 7 7 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 7 7 7 7 7 7 7 7 7 7 7 7 7 7 0 0 0
```


## train_3

**input:**
```
0 0 0 5 5 5 5 5 5 5 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 5 5 5 5 5 5 5 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

*   **Perception:**
    *   The task operates on single-row grids (1D arrays).
    *   Each input grid contains a single contiguous block of a non-white color, surrounded by white pixels (color 0).
    *   The non-white color varies between examples (yellow, orange, gray).
    *   The length of the non-white block also varies.
    *   The position of the non-white block varies.
    *   The output grid is the same size as the input grid.
    *   The transformation consistently involves shifting the non-white block exactly one position to the right. The white pixels effectively fill the space vacated by the block on the left and are displaced by the block on the right.

*   **YAML Facts:**
    
```yaml
    task_type: grid_transformation
    grid_dimensionality: 1D (single row)
    background_color: 0 (white)
    objects:
      - type: contiguous_block
        color: non_white (variable, e.g., 4, 7, 5)
        count: 1 per grid
        properties:
          - surrounded_by_background
    action:
      type: shift
      direction: right
      distance: 1 pixel
      target: the non_white contiguous_block
    relationships:
      - The block maintains its color and length during the shift.
      - The shift increases the number of leading background pixels by one.
      - The shift decreases the number of trailing background pixels by one.
      - The overall grid size remains constant.
    ```


*   **Natural Language Program:**
    1.  Identify the input grid, which is a single row.
    2.  Locate the contiguous block of non-white pixels within the row. Determine its starting index, ending index, and color.
    3.  Create a new output grid of the same length as the input grid, filled entirely with the background color (white, 0).
    4.  Copy the identified block of non-white pixels from the input grid into the output grid, placing it one position further to the right (i.e., starting at `start_index + 1` and ending at `end_index + 1`).
