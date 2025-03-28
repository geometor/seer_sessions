
## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 5 5 0 5 0 0 0 0
0 0 5 0 0 5 0 0 0 0
0 0 5 0 0 5 0 0 0 0
0 0 5 5 5 5 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
2 2 2 2 2 0 0 0 0 0
0 0 5 5 2 5 0 0 0 0
0 0 5 2 2 5 0 0 0 0
0 0 5 2 2 5 0 0 0 0
0 0 5 5 5 5 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 5 0 5 5 0 0 0
0 0 0 5 0 0 5 0 0 0
0 0 0 5 0 0 5 0 0 0
0 0 0 5 0 0 5 0 0 0
0 0 0 5 5 5 5 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 2 2 2 2 2 2
0 0 0 5 2 5 5 0 0 0
0 0 0 5 2 2 5 0 0 0
0 0 0 5 2 2 5 0 0 0
0 0 0 5 2 2 5 0 0 0
0 0 0 5 5 5 5 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


## train_3

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 5 0 5 5 0 0 0 0 0
0 5 0 0 5 0 0 0 0 0
0 5 0 0 5 0 0 0 0 0
0 5 5 5 5 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 5 5 0 5 0
0 0 0 0 0 5 0 0 5 0
0 0 0 0 0 5 5 5 5 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0
0 0 2 2 2 2 2 2 2 2
0 5 2 5 5 0 0 0 0 0
0 5 2 2 5 0 0 0 0 0
0 5 2 2 5 0 0 0 0 0
0 5 5 5 5 0 0 0 0 0
2 2 2 2 2 2 2 2 0 0
0 0 0 0 0 5 5 2 5 0
0 0 0 0 0 5 2 2 5 0
0 0 0 0 0 5 5 5 5 0
```

*   **Perception:** The input grids contain one or more shapes constructed from gray pixels (5) on a white background (0). These shapes appear to be hollow, forming boundaries around regions of white pixels. The output grids retain the original gray shapes but modify the white pixels both inside and directly above these shapes. Specifically, the white area enclosed by each gray shape is filled with red pixels (2). Additionally, a horizontal red line (2) is drawn one row above the top extent of each gray shape, spanning the width defined by the shape's leftmost and rightmost points.

*   **YAML Facts:**
    
```yaml
    task_elements:
      - element: grid
        description: A 2D array of pixels with values 0-9 representing colors. Background is white (0).
      - element: object
        description: Contiguous blocks of gray pixels (5).
        properties:
          - shape: Forms a boundary, often U-shaped, enclosing white pixels.
          - location: Can appear anywhere on the grid.
          - count: One or more per grid.
    transformation:
      - action: identify_objects
        input: input grid
        output: coordinates of all gray (5) objects.
      - action: process_each_object
        for_each: gray object identified
        steps:
          - step: find_bounding_box
            input: gray object coordinates
            output: min_row, max_row, min_col, max_col
          - step: identify_interior
            input: input grid, gray object coordinates, bounding_box
            description: Find all white (0) pixels enclosed by the gray object boundary. This can be done by performing a flood fill from the outside (e.g., grid corners or bounding box edges) marking reachable white pixels, and considering the unmarked white pixels within the bounding box as interior.
            output: coordinates of interior white pixels.
          - step: fill_interior
            input: output grid (initially copy of input), interior coordinates
            description: Change the color of the identified interior pixels to red (2).
            output: modified output grid.
          - step: draw_top_line
            input: output grid, bounding_box
            condition: min_row > 0
            description: Change the color of pixels in row (min_row - 1) from column min_col to max_col (inclusive) to red (2).
            output: modified output grid.
    relationships:
      - type: spatial
        description: The transformation depends on the spatial structure of the gray objects (enclosure) and their position (bounding box).
      - type: procedural
        description: Each gray object is processed independently using the same set of steps.
    output_grid:
      description: The final grid after applying the fill_interior and draw_top_line steps for all identified gray objects.
    ```


*   **Natural Language Program:**
    1.  Initialize the output grid as a copy of the input grid.
    2.  Identify all distinct contiguous objects composed of gray pixels (5) in the input grid.
    3.  For each identified gray object:
        a.  Determine the bounding box of the object (the minimum and maximum row and column indices it occupies).
        b.  Identify the set of white pixels (0) that are enclosed within the boundary formed by the gray object. These are the "interior" pixels. (One way to find these is to flood-fill white pixels reachable from the grid's border and consider any remaining white pixels within the object's bounding box as interior).
        c.  Change the color of all identified interior pixels in the output grid to red (2).
        d.  Let `min_row` be the topmost row index and `min_col`, `max_col` be the leftmost and rightmost column indices of the object's bounding box. If `min_row` is greater than 0, change the color of all pixels in the output grid at row `min_row - 1`, from column `min_col` to `max_col` (inclusive), to red (2).
    4.  Return the final modified output grid.
