
## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 2 7 0 0 0 0 0
0 0 0 2 7 7 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
3 3 3 3 3 3 3 3 3 3
3 3 3 3 3 3 3 3 3 3
3 3 3 3 3 3 3 3 3 3
3 3 3 3 3 3 3 3 3 3
3 3 3 7 7 3 3 3 3 3
3 3 7 7 7 7 3 3 3 3
3 3 3 3 3 3 3 3 3 3
3 3 3 3 3 3 3 3 3 3
3 3 3 3 3 3 3 3 3 3
3 3 3 3 3 3 3 3 3 3
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 2 2 0 0 0 0 0
0 0 0 6 6 0 0 0 0 0
0 0 0 0 6 0 0 0 0 0
0 0 0 0 6 6 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
3 3 3 3 3 3 3 3 3 3
3 3 3 3 6 6 3 3 3 3
3 3 3 3 6 3 3 3 3 3
3 3 3 6 6 3 3 3 3 3
3 3 3 6 6 3 3 3 3 3
3 3 3 3 6 3 3 3 3 3
3 3 3 3 6 6 3 3 3 3
3 3 3 3 3 3 3 3 3 3
3 3 3 3 3 3 3 3 3 3
3 3 3 3 3 3 3 3 3 3
```


## train_3

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 8 8 8 0 0 0 0
0 0 0 0 0 8 0 0 0 0
0 0 0 0 0 2 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
3 3 3 3 3 3 3 3 3 3
3 3 3 3 3 3 3 3 3 3
3 3 3 3 3 3 3 3 3 3
3 3 3 3 3 3 3 3 3 3
3 3 3 8 8 8 3 3 3 3
3 3 3 3 3 8 3 3 3 3
3 3 3 3 3 8 3 3 3 3
3 3 3 8 8 8 3 3 3 3
3 3 3 3 3 3 3 3 3 3
3 3 3 3 3 3 3 3 3 3
```


## train_4

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 4 2 0 0 0 0
0 0 4 4 4 2 0 0 0 0
0 0 0 0 4 2 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
3 3 3 3 3 3 3 3 3 3
3 3 3 3 3 3 3 3 3 3
3 3 3 3 3 3 3 3 3 3
3 3 3 3 4 4 3 3 3 3
3 3 4 4 4 4 4 4 3 3
3 3 3 3 4 4 3 3 3 3
3 3 3 3 3 3 3 3 3 3
3 3 3 3 3 3 3 3 3 3
3 3 3 3 3 3 3 3 3 3
3 3 3 3 3 3 3 3 3 3
```

*   **Perception:**
    *   The task involves transforming an input grid into an output grid of the same dimensions (10x10 in the examples).
    *   The background color consistently changes from white (0) in the input to green (3) in the output.
    *   The input grids contain distinct shapes or "objects" composed of non-white pixels.
    *   These objects appear to consist of two primary colors: red (2) and one other color, which varies between examples (orange (7), magenta (6), azure (8), yellow (4)).
    *   In the output grid, the original position and shape of the object are generally preserved, but the colors change.
    *   Specifically, the red (2) pixels from the input object are replaced in the output by the *other* color present in the input object. The pixels that were originally the *other* color retain their color in the output.

*   **Facts:**
    
```yaml
    task_type: grid_transformation
    grid_properties:
      size_preservation: true
      dimensions: [10, 10] # Based on examples
    background_transformation:
      input_color: 0 # white
      output_color: 3 # green
    object_properties:
      input_composition:
        - color: 2 # red
        - color: C # Variable color (e.g., 7, 6, 8, 4)
      output_composition:
        - color: C # All pixels of the original object become color C
    actions:
      - action: identify_colors
        description: Find the two non-background colors present in the input grid. One is always red (2), identify the other (C).
      - action: create_output_grid
        description: Generate a new grid of the same dimensions as the input.
      - action: fill_background
        description: Set all cells in the output grid to green (3).
      - action: replace_pixels
        description: Iterate through the input grid. If a pixel is red (2) or color C, place color C at the corresponding position in the output grid.
    relationships:
      - type: color_replacement
        input_color: 2 # red
        output_color: C # The other non-background color found in the input object.
      - type: color_persistence
        input_color: C
        output_color: C
    ```


*   **Natural Language Program:**
    1.  Determine the height and width of the input grid.
    2.  Scan the input grid to find the unique non-white (0) colors present. Identify the color that is *not* red (2); let this be the `fill_color`.
    3.  Create a new output grid with the same height and width as the input grid.
    4.  Initialize all cells of the output grid with the color green (3).
    5.  Iterate through each cell of the input grid at `(row, column)`.
    6.  If the color of the input cell at `(row, column)` is red (2) or the identified `fill_color`, set the color of the output grid cell at `(row, column)` to the `fill_color`.
    7.  Return the completed output grid.
