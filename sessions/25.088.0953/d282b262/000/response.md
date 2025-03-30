*   **Perception:** The task involves manipulating distinct objects within a grid. The input grid contains several multi-colored objects scattered across a white background. The output grid shows these same objects, preserving their shapes and internal color patterns, but relocated. All objects in the output are positioned such that their rightmost edge aligns with the rightmost column of the grid. The relative vertical positions of the objects are maintained. Objects that might have overlapped horizontally in the input due to their relative positions are also shown overlapping in the output after being moved. The grid dimensions remain constant.

*   **YAML Facts:**
    
```yaml
    task_description: Move objects to the right edge of the grid while preserving their shape and relative vertical order.
    grid_properties:
      - size_input: [15, 15] # Examples 1, 2, 3
      - size_output: [15, 15] # Examples 1, 2, 3
      - background_color: 0 # white
    objects:
      - description: Contiguous blocks of non-background (non-white) pixels.
      - properties:
          - shape: Preserved during transformation.
          - internal_colors: Preserved during transformation.
          - relative_vertical_position: Preserved during transformation.
    transformation:
      - type: Spatial rearrangement (translation)
      - scope: Applied independently to each identified object.
      - rule:
          - Identify each distinct connected object (non-white pixels).
          - For each object, determine its rightmost column index (`object_max_col`).
          - Calculate the horizontal shift required for the object: `shift = grid_width - object_max_col - 1`.
          - Move all pixels of the object horizontally by the calculated `shift` amount.
      - output_construction: Create a new grid of the same dimensions, initialized with the background color. Place each moved object onto this new grid at its shifted coordinates.
    relationships:
      - Object integrity: Each object is treated as a single unit and moved without distortion.
      - Alignment: All objects in the output are aligned such that their rightmost extent is at the last column of the grid.
    ```


*   **Natural Language Program:**
    1.  Initialize an empty output grid with the same dimensions as the input grid, filled with the background color (white, 0).
    2.  Identify all distinct connected components (objects) of non-white pixels in the input grid.
    3.  For each identified object:
        a.  Find the set of coordinates `(row, col)` for all pixels belonging to this object.
        b.  Determine the maximum column index (`object_max_col`) among all pixels in this object.
        c.  Calculate the horizontal shift distance required for this specific object: `shift = input_grid_width - object_max_col - 1`.
        d.  For each pixel `(row, col)` belonging to this object with color `c`:
            i.  Calculate its new position in the output grid: `(new_row, new_col) = (row, col + shift)`.
            ii. Place the color `c` at the `(new_row, new_col)` position in the output grid.
    4.  Return the completed output grid.