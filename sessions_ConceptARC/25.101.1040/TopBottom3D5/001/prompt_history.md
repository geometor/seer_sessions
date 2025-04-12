
## train_1

**input:**
```
0 0 1 1 1 1 1 1 0 0 0 0
0 0 1 1 1 1 1 1 0 0 0 0
0 0 1 1 2 2 2 1 7 7 7 0
0 3 3 3 2 2 2 1 7 7 7 0
0 3 3 3 2 2 2 1 7 7 7 0
0 3 3 3 3 3 1 1 7 7 7 0
0 3 3 3 3 3 1 1 0 0 0 0
0 3 3 3 3 3 0 0 0 0 0 0
0 3 3 3 0 0 0 0 0 0 0 0
```


**output:**
```
2 2 2
2 2 2
2 2 2
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 3 3 0
0 9 9 9 9 0 3 3 0
4 9 9 9 9 4 4 4 4
4 9 9 9 9 4 4 4 4
4 9 9 9 9 4 4 4 4
0 9 9 9 9 0 0 0 0
0 9 7 7 7 7 0 0 0
0 0 7 7 7 7 0 0 0
0 0 7 7 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```


**output:**
```
7 7 7 7
7 7 7 7
7 7 0 0
```


## train_3

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 4 4 4 0 0
0 0 0 0 3 3 3 4 0 0
0 0 0 2 2 2 3 4 0 0
0 0 5 5 5 2 3 0 0 0
0 0 0 5 5 2 0 0 0 0
0 0 0 0 5 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
5 5 5
0 5 5
0 0 5
```

*   **Perception:** The task involves identifying a specific "target" object within a larger input grid based on its color and then extracting a 3x3 representation of that object. The input grids contain multiple objects of different colors and shapes, set against a white background. The output grid is always 3x3 and contains the pixels corresponding to the top-left 3x3 portion of the identified target object's bounding box. If the target object doesn't completely fill this 3x3 area within its bounding box, the remaining cells are white.

*   **Facts:**
    
```yaml
    task_type: object_extraction
    input_grid_properties:
      - contains_multiple_objects: true
      - background_color: white (0)
      - object_colors_present: [blue, red, green, yellow, gray, orange, maroon] # Across examples
    output_grid_properties:
      - size: 3x3
      - content: derived_from_single_input_object
    transformation_logic:
      - step: identify_target_object
        criteria:
          - property: color
          - rule: color is one of [red (2), orange (7), gray (5)] # Based on observed examples
          - assumption: only one such object exists per input grid
      - step: determine_bounding_box
        target: identified_target_object
      - step: extract_subgrid
        source: bounding_box_of_target_object
        subgrid_definition: top_left_3x3_area
      - step: handle_incomplete_fill
        rule: if a cell within the 3x3 subgrid does not correspond to a pixel of the target object (e.g., outside the object but inside its bounding box, or if the bounding box is smaller than 3x3), the output cell value is white (0).
      - step: generate_output
        content: extracted_3x3_subgrid
    ```


*   **Natural Language Program:**
    1.  Scan the input grid to find the object whose color is red (2), orange (7), or gray (5). Assume exactly one such object exists.
    2.  Determine the minimum bounding box containing this target object.
    3.  Create a new 3x3 grid initialized with white (0) pixels.
    4.  Iterate through the cells from row 0 to 2 and column 0 to 2 of the output grid.
    5.  For each output cell at `(row, col)`, find the corresponding cell in the input grid at `(bounding_box_top_row + row, bounding_box_left_col + col)`.
    6.  If this corresponding input cell exists within the bounds of the input grid *and* contains the color of the target object, copy the target object's color to the output cell at `(row, col)`. Otherwise, leave the output cell as white (0).
    7.  Return the generated 3x3 grid.
