
## train_1

**input:**
```
0 0 0 0 3 0 0 0 0 0 0 0
0 0 0 0 3 0 0 0 0 0 0 0
4 4 4 4 4 4 4 4 4 4 4 4
0 0 0 0 3 3 3 0 0 0 0 0
0 0 0 0 0 0 3 0 0 0 0 0
0 0 0 0 0 0 3 0 0 0 0 0
0 0 3 0 0 3 3 0 0 0 0 0
0 0 3 0 0 3 0 0 0 0 0 0
0 0 3 3 3 3 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 3 0 0 0 0 0 0 0
0 0 0 0 3 0 0 0 0 0 0 0
4 4 4 4 4 4 4 4 4 4 4 4
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 0 0 7 7 7 7 7 7 0 0 0 0 0
0 0 7 7 7 0 0 0 0 0 0 0 0 0 0
0 0 7 0 0 0 0 0 0 0 0 0 0 0 0
0 0 7 0 0 0 0 0 0 0 0 0 0 0 0
0 0 7 7 7 7 0 0 0 0 0 0 0 0 0
0 0 0 0 0 7 0 0 0 0 0 0 0 0 0
4 4 4 4 4 4 4 4 4 4 4 4 4 4 4
0 0 0 7 7 7 0 0 0 0 0 0 0 0 0
0 0 0 7 0 0 0 0 0 0 0 0 0 0 0
0 0 0 7 0 0 0 0 0 0 0 0 0 0 0
0 0 0 7 7 7 7 7 7 7 0 0 0 0 0
0 0 0 0 0 0 0 0 0 7 0 0 0 0 0
0 0 0 0 0 0 7 7 7 7 0 0 0 0 0
```


**output:**
```
0 0 0 0 7 7 7 7 7 7 0 0 0 0 0
0 0 7 7 7 0 0 0 0 0 0 0 0 0 0
0 0 7 0 0 0 0 0 0 0 0 0 0 0 0
0 0 7 0 0 0 0 0 0 0 0 0 0 0 0
0 0 7 7 7 7 0 0 0 0 0 0 0 0 0
0 0 0 0 0 7 0 0 0 0 0 0 0 0 0
4 4 4 4 4 4 4 4 4 4 4 4 4 4 4
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

*   **Perception**:
    *   Each input grid contains a background of white pixels (0).
    *   A single, solid horizontal line of yellow pixels (4) exists in each input grid. This line spans the entire width of the grid.
    *   There are various objects composed of a single color (green=3 in the first example, orange=7 in the second) located both above and below the yellow line.
    *   The output grid retains the white background, the yellow horizontal line, and all objects located *above* the yellow line.
    *   All pixels (including parts of objects) located *below* the yellow line in the input grid are replaced with the white background color (0) in the output grid. The yellow line itself remains intact.

*   **Facts**:
    
```yaml
    elements:
      - object: grid
        properties:
          - background_color: white (0)
          - contains: horizontal_line
          - contains: colored_objects
      - object: horizontal_line
        properties:
          - color: yellow (4)
          - orientation: horizontal
          - spans: full_width
          - location: fixed_row_index (varies per example)
          - role: divider
      - object: colored_objects
        properties:
          - color: varies (green=3 or orange=7 in examples)
          - location: above_divider or below_divider
          - shape: varied, irregular
    actions:
      - name: identify_divider
        inputs: grid
        outputs: divider_row_index
      - name: preserve_above
        inputs: grid, divider_row_index
        description: Pixels at rows less than or equal to divider_row_index are copied from input to output.
      - name: remove_below
        inputs: grid, divider_row_index
        description: Pixels at rows greater than divider_row_index are replaced with the background color (white 0) in the output.
    relationships:
      - type: spatial
        subject: colored_objects
        predicate: relative_to
        object: horizontal_line (divider)
        value: above or below
      - type: transformation
        subject: colored_objects below divider
        predicate: are_replaced_by
        object: background_color (white 0)
      - type: transformation
        subject: colored_objects above divider
        predicate: are_preserved
        object: none
      - type: transformation
        subject: horizontal_line
        predicate: is_preserved
        object: none
    ```


*   **Natural Language Program**:
    1.  Identify the row index containing the solid horizontal line of yellow pixels (color 4). Let this be `divider_row`.
    2.  Create a new grid with the same dimensions as the input grid, initially filled with the background color (white 0).
    3.  Iterate through each row of the input grid from the top (row 0) down to and including `divider_row`.
    4.  For each row in this range, copy all pixels from the input grid's row to the corresponding row in the new output grid.
    5.  All rows below `divider_row` in the output grid remain filled with the background color (white 0).
    6.  Return the new grid.
