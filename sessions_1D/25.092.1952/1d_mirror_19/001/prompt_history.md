
## train_1

**input:**
```
0 0 0 0 0 1 1 1 1 1 1 1 1 0 9 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 9 0 1 1 1 1 1 1 1 1 0 0 0 0
```


## train_2

**input:**
```
0 0 2 2 2 2 2 2 2 0 0 0 9 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0 9 0 0 0 2 2 2 2 2 2 2 0 0 0 0 0
```


## train_3

**input:**
```
0 0 5 5 5 5 5 5 5 5 0 0 0 9 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 9 0 0 0 5 5 5 5 5 5 5 5 0 0 0
```

*   **Perception:** The task involves manipulating elements within a grid. The input and output are presented as 1D arrays, but analyzing them as 14x2 grids reveals the underlying structure and transformation. Each example contains three main components: a white background (0), a single maroon pixel (9), and a connected object of another color (blue, red, or gray). The transformation involves moving both the maroon pixel and the colored object based on the initial position of the maroon pixel.

*   **YAML Facts:**
    
```yaml
    grid_dimensions:
      rows: 14
      columns: 2
    background_color: 0 # white
    elements:
      - type: marker
        color: 9 # maroon
        count: 1
        properties:
          - initial_position: (row, column)
          - movement_rule: Moves one column to the right if initially in column 0, otherwise stays put.
      - type: object
        color: [1, 2, 5] # blue, red, or gray in examples
        count: 1
        properties:
          - shape: Connected component of a single color
          - initial_position: Defined by the set of pixel coordinates
          - movement_rule: Shifts vertically downwards.
    relationships:
      - The vertical shift distance of the 'object' depends on the initial column of the 'marker'.
      - The target vertical position of the 'object' is relative to the row of the 'marker'.
    transformation_logic:
      - The marker's final column is always 1.
      - The object is moved so its top-most row is positioned relative to the marker's row.
      - If the marker started in column 0, the object's top row moves to the row immediately below the marker's row.
      - If the marker started in column 1, the object's top row moves to the second row below the marker's row.
    ```


*   **Natural Language Program:**
    1.  Interpret the input array as a 14x2 grid of pixels.
    2.  Identify the coordinates (row `R`, column `C`) of the single maroon pixel (9).
    3.  Identify all pixels belonging to the connected object of a color other than white (0) or maroon (9). Determine the minimum row index (`min_row_obj`) occupied by this object.
    4.  Initialize the output grid as a 14x2 grid filled with white pixels (0).
    5.  Determine the final position of the maroon pixel in the output grid: Place it at coordinates (`R`, 1).
    6.  Determine the target minimum row (`target_min_row`) for the colored object in the output grid:
        *   If the initial column `C` of the maroon pixel was 0, set `target_min_row = R + 1`.
        *   If the initial column `C` of the maroon pixel was 1, set `target_min_row = R + 2`.
    7.  Calculate the required vertical shift for the object: `shift = target_min_row - min_row_obj`.
    8.  For each pixel `(r, c)` belonging to the original colored object, place a pixel of the same color at coordinates `(r + shift, c)` in the output grid.
