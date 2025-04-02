
## train_1

**input:**
```
0 0 0 0 0 0
0 3 0 3 0 0
0 3 3 0 0 0
0 0 3 3 3 0
0 3 3 0 3 0
0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0
0 3 3 3 3 0
0 3 3 3 3 0
0 3 3 3 3 0
0 3 3 3 3 0
0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 0 0 0 0
0 4 0 0 4 0
0 4 4 4 0 0
0 4 0 4 4 0
0 0 4 0 4 0
0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0
0 4 4 4 4 0
0 4 4 4 4 0
0 4 4 4 4 0
0 4 4 4 4 0
0 0 0 0 0 0
```

*   **Perception:** The task involves transforming a grid containing scattered pixels of a single non-background color (green in the first example, yellow in the second) into a solid rectangle of that same color. The background color is white (0). The rectangle in the output grid seems to occupy the area defined by the outermost extent of the colored pixels in the input grid.

*   **Facts:**
    
```yaml
    - task_type: fill_bounding_box
    - input_grid:
        properties:
          - contains background color (white, 0)
          - contains scattered pixels of a single foreground color (e.g., green, 3 or yellow, 4)
    - output_grid:
        properties:
          - same dimensions as input_grid
          - contains background color (white, 0)
          - contains a solid rectangle filled with the foreground color from the input_grid
    - relationship:
        - foreground_color: the non-white color is preserved from input to output.
        - rectangle_boundaries: defined by the minimum and maximum row and column indices of the foreground pixels in the input_grid.
        - transformation: fills the bounding box of the input foreground pixels with the foreground color in the output grid.
    ```


*   **Natural Language Program:**
    1.  Identify the single non-background color present in the input grid. Call this the `foreground_color`.
    2.  Find all grid cells containing the `foreground_color`.
    3.  Determine the minimum row index (`min_row`), maximum row index (`max_row`), minimum column index (`min_col`), and maximum column index (`max_col`) among these cells.
    4.  Create an output grid of the same dimensions as the input grid, initially filled entirely with the background color (white, 0).
    5.  Fill all cells within the rectangular region defined by `min_row`, `max_row`, `min_col`, and `max_col` (inclusive) in the output grid with the `foreground_color`.
    6.  Return the modified output grid.
