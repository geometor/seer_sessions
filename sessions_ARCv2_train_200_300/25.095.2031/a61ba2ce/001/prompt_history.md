
## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 8 8 0 0 0
0 0 0 0 0 0 0 0 0 8 0 0 0
0 0 1 1 0 0 0 0 0 0 0 0 0
0 0 1 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 2 0 0 0 0
0 0 0 0 0 0 0 2 2 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 4 0 0 0 0 0 0 0 0
0 0 0 0 4 4 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
1 1 8 8
1 0 0 8
4 0 0 2
4 4 2 2
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 8 8 0 0 0 0 0
0 0 0 0 0 0 8 0 0 0 0 0 0
0 2 2 0 0 0 0 0 0 0 0 0 0
0 0 2 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 1 0 0 0 0
0 0 0 0 0 0 0 1 1 0 0 0 0
0 0 0 3 0 0 0 0 0 0 0 0 0
0 0 0 3 3 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
8 8 2 2
8 0 0 2
3 0 0 1
3 3 1 1
```

*   **Perception of Task Elements:**
    *   The input is a 13x13 grid containing integers. Most cells are 0 (background).
    *   There are four distinct non-zero integers (colors) present in the input grid.
    *   Each non-zero integer forms a small connected shape composed of exactly three cells.
    *   These shapes resemble "L" shapes, fitting within a 2x2 bounding box. There are four possible orientations for these L-shapes (top-left corner missing, top-right missing, bottom-left missing, bottom-right missing).
    *   The output is a 4x4 grid.
    *   The output grid is composed of four 2x2 subgrids, arranged in a 2x2 layout.
    *   Each 2x2 subgrid in the output corresponds to one of the L-shapes found in the input.
    *   The specific 2x2 pattern placed in the output subgrid matches the 2x2 bounding box pattern of the corresponding input L-shape (including the single 0 cell).
    *   The position of each 2x2 pattern within the 4x4 output grid (top-left, top-right, bottom-left, bottom-right quadrant) is determined solely by the *orientation* of the L-shape it represents, not its color or its location in the input grid.

*   **YAML Fact Document:**
    
```yaml
    task_description: "Extract four L-shaped patterns from the input grid and arrange their 2x2 representations into a 4x4 output grid based on the orientation of each L-shape."

    elements:
      - object: input_grid
        properties:
          - type: 2D grid
          - dimensions: 13x13
          - content: integers (0 for background, non-zero for shapes)
          - contains: four distinct non-zero shapes

      - object: shape
        properties:
          - type: connected component of non-zero cells
          - color: a specific non-zero integer value
          - size: 3 cells
          - form: L-shape (fits within a 2x2 bounding box)
          - has: an orientation (one of four types based on the position of the missing cell within the 2x2 box)
            - TL_shape: [[X, X], [X, 0]]
            - TR_shape: [[X, X], [0, X]]
            - BL_shape: [[X, 0], [X, X]]
            - BR_shape: [[0, X], [X, X]]
          - has: a 2x2_representation (the minimal 2x2 grid containing the shape)

      - object: output_grid
        properties:
          - type: 2D grid
          - dimensions: 4x4
          - content: integers (derived from input shapes)
          - composed_of: four 2x2 subgrids (quadrants)

    actions:
      - action: identify_shapes
        description: "Find all distinct connected components of non-zero cells in the input grid."
        inputs: [input_grid]
        outputs: [list_of_shapes]

      - action: determine_2x2_representation
        description: "For each identified shape, determine its color and its 2x2 pattern (the minimal 2x2 bounding box containing the 3 shape cells and 1 background cell)."
        inputs: [shape]
        outputs: [color, 2x2_pattern]

      - action: determine_orientation
        description: "Classify the 2x2 pattern of a shape into one of four orientations (TL_shape, TR_shape, BL_shape, BR_shape)."
        inputs: [2x2_pattern]
        outputs: [orientation_type]

      - action: construct_output
        description: "Create an empty 4x4 grid. For each identified shape, place its 2x2_pattern into the quadrant of the output grid corresponding to its orientation_type."
        inputs: [list_of_shapes_with_representations_and_orientations]
        outputs: [output_grid]
        placement_rules:
          - if orientation is TL_shape, place 2x2_pattern in output[0:2, 0:2]
          - if orientation is TR_shape, place 2x2_pattern in output[0:2, 2:4]
          - if orientation is BL_shape, place 2x2_pattern in output[2:4, 0:2]
          - if orientation is BR_shape, place 2x2_pattern in output[2:4, 2:4]

    relationships:
      - relation: mapping
        from: input_shape_orientation
        to: output_quadrant_position
        description: "The orientation of an L-shape in the input determines which 2x2 quadrant its representation occupies in the output grid."
    ```


*   **Natural Language Program:**
    1.  Initialize an empty 4x4 grid for the output.
    2.  Identify all distinct connected components (shapes) of non-zero cells in the input 13x13 grid. There will be exactly four such shapes.
    3.  For each identified shape:
        a.  Determine its color (the non-zero integer value).
        b.  Find the minimal 2x2 bounding box that contains the three cells of the shape. This 2x2 grid, including the one background (0) cell, is the shape's `2x2_representation`.
        c.  Analyze the `2x2_representation` to determine the shape's orientation based on the position of the '0' cell:
            i.  If the '0' is at the bottom-right (`[[X, X], [X, 0]]`), the orientation is Top-Left (TL).
            ii. If the '0' is at the bottom-left (`[[X, X], [0, X]]`), the orientation is Top-Right (TR).
            iii.If the '0' is at the top-right (`[[X, 0], [X, X]]`), the orientation is Bottom-Left (BL).
            iv. If the '0' is at the top-left (`[[0, X], [X, X]]`), the orientation is Bottom-Right (BR).
        d.  Place the shape's `2x2_representation` into the corresponding quadrant of the 4x4 output grid:
            i.  If the orientation is TL, place it in the top-left quadrant (rows 0-1, columns 0-1).
            ii. If the orientation is TR, place it in the top-right quadrant (rows 0-1, columns 2-3).
            iii.If the orientation is BL, place it in the bottom-left quadrant (rows 2-3, columns 0-1).
            iv. If the orientation is BR, place it in the bottom-right quadrant (rows 2-3, columns 2-3).
    4.  Return the completed 4x4 output grid.
