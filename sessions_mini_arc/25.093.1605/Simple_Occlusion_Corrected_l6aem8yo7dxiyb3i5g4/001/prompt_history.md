
## train_1

**input:**
```
0 0 8 0 0
0 8 0 8 0
6 6 6 0 0
6 0 6 0 0
6 6 6 0 0
```


**output:**
```
0 0 8 0 0
0 8 0 8 0
0 0 8 0 0
0 0 0 0 0
0 0 0 0 0
```


## train_2

**input:**
```
0 6 0 0 0
6 0 6 0 0
0 6 5 5 5
0 0 5 0 5
0 0 5 5 5
```


**output:**
```
0 6 0 0 0
6 0 6 0 0
0 6 0 0 0
0 0 0 0 0
0 0 0 0 0
```


## train_3

**input:**
```
0 0 9 0 0
0 9 0 9 0
0 5 5 5 0
0 5 0 5 0
0 5 5 5 0
```


**output:**
```
0 0 9 0 0
0 9 0 9 0
0 0 9 0 0
0 0 0 0 0
0 0 0 0 0
```

*   **Perception:**
    *   The input is a 5x5 grid containing numerical values. 0 represents the background color.
    *   Each input grid contains exactly two distinct connected components (objects) made of non-zero values.
    *   The two objects are always vertically separated by at least one row of zeros. One object is positioned higher ("upper object") in the grid than the other ("lower object").
    *   The output grid is also a 5x5 grid.
    *   The transformation retains the upper object completely in its original position and color.
    *   The lower object from the input is entirely removed in the output.
    *   A single pixel is added to the output grid. This pixel has the color of the upper object. Its position is determined as follows:
        *   Its row index is the same as the topmost row index of the *original* lower object in the input grid.
        *   Its column index is the same as the column index of the top-most, left-most pixel of the *upper* object in the input grid.
    *   All other cells in the output grid, specifically those below the upper object and not part of the single added pixel, are set to 0 (background).

*   **YAML Facts:**
    
```yaml
    task_description: Retain the upper of two vertically separated objects and place a single pixel representing the upper object's anchor at the starting row of the lower object.

    elements:
      - element: grid
        properties:
          - type: 2D array of integers
          - size: 5x5
          - background_color: 0
      - element: object
        description: A connected component of non-zero cells.
        properties:
          - color: The non-zero integer value of the cells.
          - pixels: List of (row, column) coordinates belonging to the object.
          - topmost_row: The minimum row index among the object's pixels.
          - anchor_point: The pixel with the minimum row index, and among those, the minimum column index. (e.g., top-left-most point).
        relationships:
          - relationship: vertical_separation
            description: Two objects are separated if there is at least one row containing only background pixels between the lowest row of the upper object and the highest row of the lower object.
          - relationship: relative_position
            values: [upper, lower]
            determination: Based on the minimum row index (topmost_row). The object with the smaller topmost_row is 'upper'.

    actions:
      - action: identify_objects
        inputs: [input_grid]
        outputs: [list_of_objects]
        description: Find all connected components of non-zero cells.
      - action: determine_relative_positions
        inputs: [list_of_objects]
        outputs: [upper_object, lower_object]
        description: Identify which object is upper and which is lower based on topmost_row. Assumes exactly two objects.
      - action: find_properties
        inputs: [object]
        outputs: [color, pixels, anchor_point, topmost_row]
        description: Extract key properties of an object.
      - action: create_output_grid
        inputs: [grid_size, background_color]
        outputs: [output_grid]
        description: Initialize an empty grid of the correct size filled with the background color.
      - action: copy_object
        inputs: [object_to_copy, target_grid]
        outputs: [modified_target_grid]
        description: Place the pixels of the object_to_copy onto the target_grid using the object's color.
      - action: place_anchor_pixel
        inputs: [upper_object_color, upper_object_anchor_col, lower_object_topmost_row, target_grid]
        outputs: [modified_target_grid]
        description: Set the pixel at (lower_object_topmost_row, upper_object_anchor_col) in the target_grid to the upper_object_color.

    transformation_rule:
      - step: Identify the two non-zero objects in the input grid.
      - step: Determine which object is the upper object and which is the lower object based on their topmost rows.
      - step: Find the color and anchor point (top-most, left-most pixel) of the upper object.
      - step: Find the topmost row index of the lower object.
      - step: Initialize the output grid with the background color (0).
      - step: Copy the upper object (all its pixels and its color) to the output grid at its original position.
      - step: Place a single pixel in the output grid. The pixel's color is the upper object's color. Its row is the lower object's topmost row. Its column is the upper object's anchor point column.
    ```


*   **Natural Language Program:**
    1.  Initialize the output grid as a 5x5 grid filled with zeros.
    2.  Identify all connected components of non-zero cells in the input grid. Assume there are exactly two such components (objects).
    3.  Determine the "upper object" as the one whose highest pixel (minimum row index) is smaller than the other object's highest pixel. Determine the "lower object" correspondingly.
    4.  Find the set of coordinates `{(r, c)}` for all pixels belonging to the upper object.
    5.  Find the color (`upper_color`) of the upper object.
    6.  Find the anchor point (`upper_anchor_row`, `upper_anchor_col`) of the upper object, defined as the pixel within the upper object with the minimum row index, breaking ties by choosing the minimum column index.
    7.  Find the topmost row index (`lower_topmost_row`) of the lower object.
    8.  For each coordinate `(r, c)` belonging to the upper object, set the cell `output[r][c]` to `upper_color`.
    9.  Set the cell `output[lower_topmost_row][upper_anchor_col]` to `upper_color`.
