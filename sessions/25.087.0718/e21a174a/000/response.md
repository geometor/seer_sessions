*   **Perception:** The input grids contain several distinct colored objects or patterns placed on a white background. The output grids contain the exact same objects and patterns, also on a white background. The key difference is the vertical positioning of these objects. It appears the entire content of the input grid, excluding the background, has been flipped vertically. The top rows of the input become the bottom rows of the output, and vice-versa, maintaining the horizontal positions of the pixels within each row.

*   **Facts:**
    
```yaml
    task_type: geometric_transformation
    transformation: vertical_flip
    background_color: white (0)
    objects:
      - type: contiguous_pixels
      - property: single_color_per_object
      - property: multiple_objects_per_grid
      - property: shapes_preserved_in_output
      - property: colors_preserved_in_output
    grid_properties:
      - dimension_preserved: true (input and output grids have the same height and width)
      - background_preserved: true (white pixels remain in the same relative positions if not overwritten by a flipped object)
    actions:
      - name: flip_grid
      - parameter: axis=vertical
    relationships:
      - input_row[i] corresponds to output_row[height - 1 - i]
    ```


*   **Natural Language Program:**
    1.  Determine the height (number of rows) of the input grid.
    2.  Create a new output grid with the same dimensions as the input grid, initialized with the background color (white, 0).
    3.  For each row `i` in the input grid (from top to bottom, starting at index 0):
        a.  Copy the content of input row `i`.
        b.  Place this copied row into the output grid at row `height - 1 - i`.
    4.  The resulting grid is the final output.