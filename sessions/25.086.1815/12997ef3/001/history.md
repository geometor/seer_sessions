
## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 6 0 0 0
0 0 0 1 0 0 0 0 0 0 0
0 0 1 1 0 0 0 2 0 0 0
0 0 0 0 1 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 6 0
6 6 0
0 0 6
0 2 0
2 2 0
0 0 2
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0 0
0 0 0 0 0 3 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 6 0 0 0
0 1 1 0 0 0 0 0 0
1 1 1 0 0 8 0 0 0
0 1 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```


**output:**
```
0 3 3
3 3 3
0 3 0
0 6 6
6 6 6
0 6 0
0 8 8
8 8 8
0 8 0
```


## train_3

**input:**
```
0 0 1 1 0 0 0 0 0 0
0 1 1 0 0 0 0 0 0 0
0 0 1 1 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 3 0 2 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 3 3 0 2 2
3 3 0 2 2 0
0 3 3 0 2 2
```


## train_4

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 1 0 1 0 0 0 0 0 0 0 0 0 0
0 0 1 0 0 0 0 0 0 0 0 0 0 0
0 1 1 1 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 2 0 3 0 4 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
2 0 2 3 0 3 4 0 4
0 2 0 0 3 0 0 4 0
2 2 2 3 3 3 4 4 4
```

*   **Perception:**
    *   Each input grid contains multiple distinct objects (contiguous blocks of non-white pixels).
    *   One object is always blue (color 1). Its shape varies across examples ('L', 'T', '+', 'S'/'Z').
    *   Other objects are single pixels of various colors (magenta, red, green, azure, yellow).
    *   The output grid consists of multiple objects, each being a 3x3 grid pattern.
    *   The *shape* of the output objects matches the shape of the blue object found in the corresponding input grid (scaled or represented within a 3x3 bounding box).
    *   The *colors* of the output objects correspond to the colors of the single non-blue pixels found in the input grid.
    *   The number of output objects equals the number of single non-blue pixels in the input.
    *   The blue object from the input does not appear directly in the output; it serves only as a shape template.
    *   The arrangement of the output objects (stacked vertically or horizontally) depends on the relative positions of the single-pixel color sources in the input. If they share the same column, they stack vertically (Examples 1, 2). If they share the same row, they stack horizontally (Examples 3, 4).
    *   When stacked horizontally, there is a single column of white pixels separating the output shapes. When stacked vertically, there is no separation.
    *   The order of the stacked shapes in the output matches the order (top-to-bottom or left-to-right) of the corresponding single-pixel color sources in the input.

*   **Facts:**
    
```yaml
    task_description: Replicate a template shape using colors derived from specific input pixels.

    elements:
      - element: input_grid
        description: A 2D grid containing pixels of different colors.
      - element: output_grid
        description: A 2D grid derived from the input grid.
      - element: blue_object
        description: A contiguous object of blue pixels (color 1) in the input grid. Acts as a shape template.
        properties:
          - shape: The relative arrangement of its pixels.
          - location: Its position within the input grid (appears irrelevant for output generation).
          - bounding_box: The minimal rectangle enclosing the shape (observed to be 3x3 or smaller in examples).
      - element: color_source_pixels
        description: Single non-blue, non-white pixels in the input grid.
        properties:
          - color: The color value of the pixel.
          - location: The row and column index of the pixel.
      - element: output_shapes
        description: Objects in the output grid.
        properties:
          - shape: Matches the shape of the input `blue_object`.
          - color: Matches the color of one of the input `color_source_pixels`.
          - size: Appears to be consistently 3x3, containing the replicated shape.

    relationships:
      - type: template_replication
        from: blue_object
        to: output_shapes
        detail: The shape of the `blue_object` determines the pattern of colored pixels within each `output_shape`.
      - type: color_mapping
        from: color_source_pixels
        to: output_shapes
        detail: Each `color_source_pixel` provides the color for one `output_shape`.
      - type: arrangement
        based_on: color_source_pixels
        applied_to: output_shapes
        detail: >
          The relative positions of `color_source_pixels` in the input dictate the stacking (vertical or horizontal)
          and order of the `output_shapes` in the output grid. Horizontal stacking includes a one-pixel white buffer column.

    actions:
      - action: identify_template
        actor: system
        input: input_grid
        output: blue_object_shape, blue_object_bounding_box
        description: Find the blue object and extract its shape pattern within its minimal bounding box.
      - action: identify_color_sources
        actor: system
        input: input_grid
        output: list_of_color_source_pixels (color, row, col)
        description: Find all single non-blue, non-white pixels and record their color and location.
      - action: generate_output_shapes
        actor: system
        input: blue_object_shape, list_of_color_source_pixels
        output: list_of_individual_output_shapes (3x3 grids)
        description: For each color source pixel, create a 3x3 grid replicating the blue object shape using the source pixel's color.
      - action: arrange_output
        actor: system
        input: list_of_individual_output_shapes, list_of_color_source_pixels (for relative positions)
        output: final_output_grid
        description: >
          Determine stacking direction (vertical if source pixels share a column, horizontal if they share a row).
          Assemble the individual output shapes into the final output grid according to the determined stacking direction,
          maintaining the original relative order, and adding a white buffer column for horizontal stacking.

    uncertainties:
      - What happens if the blue object isn't contained within a 3x3 bounding box? (Assumed 3x3 based on examples).
      - What happens if color source pixels are neither in the same row nor the same column? (Not covered by examples).
      - What happens if there is no blue object or no color source pixels? (Not covered by examples).
      - What happens if a non-blue object is larger than a single pixel? (Not covered by examples).
    ```


*   **Natural Language Program:**
    1.  Identify the contiguous object composed of blue pixels (color 1) in the input grid. Determine its shape pattern within its minimal 3x3 bounding box. This is the `template_shape`.
    2.  Identify all single pixels in the input grid that are not blue (color 1) and not white (color 0). Store these `color_source_pixels`, noting their color and original position (row, column).
    3.  Sort the `color_source_pixels` based on their position: primarily by row index, then by column index.
    4.  For each `color_source_pixel` in the sorted list:
        a.  Create a 3x3 grid initialized with white pixels (color 0).
        b.  Apply the `template_shape` to this 3x3 grid, coloring the corresponding pixels with the color of the current `color_source_pixel`. This creates an `individual_output_shape`.
    5.  Collect all generated `individual_output_shapes`.
    6.  Determine the arrangement of the `color_source_pixels`:
        a.  If all `color_source_pixels` share the same column index in the input grid, arrange the `individual_output_shapes` vertically, stacked top-to-bottom in their generated order.
        b.  If all `color_source_pixels` share the same row index in the input grid, arrange the `individual_output_shapes` horizontally, placed left-to-right in their generated order, separated by a single column of white pixels.
    7.  Construct the final output grid based on the determined arrangement.
