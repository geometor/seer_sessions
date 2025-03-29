
## train_1

**input:**
```
0 4 0 3 0 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 4 0 3 0 2 0 0 8 8 8 8 0 0 0 8 8 8 8 0
0 4 0 3 0 2 0 0 8 8 8 8 0 0 0 8 8 8 8 0
0 4 0 3 0 2 0 0 8 8 8 8 8 8 0 8 8 8 8 0
0 4 0 3 0 2 0 0 8 8 8 8 8 8 0 8 8 8 8 0
0 4 0 3 0 2 0 0 0 0 0 0 8 8 0 0 0 0 0 0
0 4 0 3 0 2 0 0 0 0 0 0 8 8 0 0 0 0 0 0
0 4 0 3 0 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 4 4 4 4 0 0 0 2 2 2 2 0
0 0 0 0 0 0 0 0 4 4 4 4 0 0 0 2 2 2 2 0
0 0 0 0 0 0 0 0 4 4 4 4 3 3 0 2 2 2 2 0
0 0 0 0 0 0 0 0 4 4 4 4 3 3 0 2 2 2 2 0
0 0 0 0 0 0 0 0 0 0 0 0 3 3 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 3 3 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 1 0 6 0 7 0 8 8 8 0 0 8 8 8
0 1 0 6 0 7 0 8 8 8 0 0 8 8 8
0 1 0 6 0 7 0 0 0 0 8 8 8 8 8
0 1 0 6 0 7 0 0 0 0 8 8 0 0 0
0 1 0 6 0 7 0 0 0 0 8 8 0 0 0
0 1 0 6 0 7 0 0 0 0 8 8 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 1 1 1 0 0 7 7 7
0 0 0 0 0 0 0 1 1 1 0 0 7 7 7
0 0 0 0 0 0 0 0 0 0 6 6 7 7 7
0 0 0 0 0 0 0 0 0 0 6 6 0 0 0
0 0 0 0 0 0 0 0 0 0 6 6 0 0 0
0 0 0 0 0 0 0 0 0 0 6 6 0 0 0
```


## train_3

**input:**
```
0 3 0 2 0 4 0 7 0 8 8 0 0 0 8 8 0 0
0 3 0 2 0 4 0 7 0 8 8 8 8 0 8 8 0 0
0 3 0 2 0 4 0 7 0 0 0 8 8 0 8 8 0 0
0 3 0 2 0 4 0 7 0 0 0 8 8 0 8 8 8 8
0 3 0 2 0 4 0 7 0 0 0 0 0 0 8 8 8 8
0 3 0 2 0 4 0 7 0 0 0 0 0 0 0 0 8 8
0 3 0 2 0 4 0 7 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 3 3 0 0 0 4 4 0 0
0 0 0 0 0 0 0 0 0 3 3 2 2 0 4 4 0 0
0 0 0 0 0 0 0 0 0 0 0 2 2 0 4 4 0 0
0 0 0 0 0 0 0 0 0 0 0 2 2 0 4 4 7 7
0 0 0 0 0 0 0 0 0 0 0 0 0 0 4 4 7 7
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 7 7
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

*   **Perception of Task Elements:**
    *   The input grids consist of two main sections:
        *   A left section containing thin, vertical lines of distinct non-white colors (yellow, green, red, blue, magenta, orange) placed in odd-numbered columns, separated by white columns.
        *   A right section containing one or more distinct shapes made of azure pixels (color 8) against a white background.
    *   The output grids retain the dimensions of the input but modify the content:
        *   The left section (where the colored lines were) becomes entirely white.
        *   The right section (where the azure shapes were) now shows shapes in the same positions as the input azure shapes, but colored according to the vertical lines from the input's left section. The azure pixels are replaced; the white background remains.
    *   The core transformation involves using the colors from the vertical lines on the left to "paint" the azure shapes on the right.
    *   The key challenge is determining the mapping rule: which line color corresponds to which azure shape. Observing the examples reveals a consistent pattern: the Nth vertical line (reading from left to right) provides the color for the Nth azure shape (reading from left to right).

*   **YAML Facts:**
    
```yaml
    task_elements:
      - type: vertical_lines
        location: left side, odd-numbered columns
        properties:
          - colors: vary per example (yellow, green, red, blue, magenta, orange)
          - function: color source
      - type: shapes
        location: right side
        properties:
          - color: azure (8) in input
          - function: target areas to be colored
      - type: background
        location: everywhere else
        properties:
          - color: white (0)
          - function: remains unchanged, except where lines/shapes were

    transformation:
      - action: identify_color_sources
        input: vertical lines on the left
        output: ordered list of colors (left-to-right)
      - action: identify_target_shapes
        input: azure shapes on the right
        output: ordered list of shapes (left-to-right based on position)
      - action: map_colors_to_shapes
        rule: The color from the Nth vertical line is assigned to the Nth azure shape.
      - action: generate_output
        steps:
          - Create a white grid of the same dimensions as the input.
          - For each target shape identified:
            - Determine its corresponding color based on the mapping rule.
            - Color the pixels corresponding to the shape's location in the output grid with the assigned color.

    relationships:
      - type: spatial ordering
        applies_to:
          - vertical_lines (left-to-right)
          - azure_shapes (left-to-right)
        relevance: Determines the color-to-shape mapping. Nth line maps to Nth shape.
    ```


*   **Natural Language Program:**
    1.  Create a new output grid with the same dimensions as the input grid, initially filled entirely with white (0).
    2.  Scan the input grid's odd-numbered columns (1, 3, 5, ...) from left to right. Identify the non-white color present in each of these columns and store these colors in an ordered list (e.g., `color_palette`). The first color found corresponds to the first element, the second color to the second, and so on.
    3.  Identify all distinct contiguous regions (shapes) composed of azure pixels (8) in the input grid.
    4.  Determine the spatial order of these azure shapes from left to right. This can be done by finding the minimum column index (leftmost point) for each shape and sorting the shapes based on this index. Store the shapes (represented by their pixel coordinates) in an ordered list (`target_shapes`).
    5.  Iterate through the `target_shapes` list using an index `i` (starting from 0). For each shape `target_shapes[i]`:
        a.  Retrieve the corresponding color from the `color_palette` list using the same index: `paint_color = color_palette[i]`.
        b.  For every pixel coordinate `(row, col)` belonging to `target_shapes[i]`, set the pixel at `(row, col)` in the output grid to `paint_color`.
    6.  The final output grid is the result of these painting operations.
