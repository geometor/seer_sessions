*   **Perception:**
    The task involves duplicating the input grid and placing the two copies adjacent to each other, separated by a single line of white pixels. The orientation of the duplication (vertical or horizontal) depends on the aspect ratio of the input grid. If the input grid is wider than it is tall, the duplication is vertical, with a horizontal white line separating the copies. If the input grid is taller than it is wide, the duplication is horizontal, with a vertical white line separating the copies.

*   **YAML Facts:**
    
```yaml
    task_description: Duplicate the input grid and place the copies adjacent, separated by a line of white pixels. The orientation depends on the input grid's aspect ratio.
    
    elements:
      - element: input_grid
        description: The source 2D array of pixels.
        properties:
          height: H
          width: W
      - element: output_grid
        description: The target 2D array of pixels.
        properties:
          height: H_out
          width: W_out
      - element: separator
        description: A line (row or column) of white (0) pixels used to separate the duplicated input grids.
    
    relationships:
      - relationship: aspect_ratio_determines_orientation
        description: The relationship between the input grid's height (H) and width (W) determines how the duplication and separation occur.
        conditions:
          - condition: W > H (Wider than tall)
            action: Duplicate vertically, separate with a horizontal white row.
            output_dimensions: H_out = 2*H + 1, W_out = W
          - condition: H > W (Taller than wide)
            action: Duplicate horizontally, separate with a vertical white column.
            output_dimensions: H_out = H, W_out = 2*W + 1
          - condition: H == W (Square)
            action: (Assumed based on wider-than-tall case logic) Duplicate vertically, separate with a horizontal white row.
            output_dimensions: H_out = 2*H + 1, W_out = W
    
    actions:
      - action: determine_dimensions
        actor: system
        inputs: [input_grid]
        outputs: [H, W]
      - action: compare_dimensions
        actor: system
        inputs: [H, W]
        outputs: [orientation_rule] # e.g., 'vertical_duplication' or 'horizontal_duplication'
      - action: construct_output_grid
        actor: system
        inputs: [input_grid, orientation_rule]
        outputs: [output_grid]
        steps:
          - based on orientation_rule:
            - if vertical_duplication:
                - Create new grid of size (2*H + 1) x W.
                - Copy input_grid to top H rows.
                - Fill row H with white (0).
                - Copy input_grid to bottom H rows (starting from row H+1).
            - if horizontal_duplication:
                - Create new grid of size H x (2*W + 1).
                - Copy input_grid to left W columns.
                - Fill column W with white (0).
                - Copy input_grid to right W columns (starting from column W+1).
    ```


*   **Natural Language Program:**
    1.  Determine the height (H) and width (W) of the input grid.
    2.  Compare H and W.
    3.  If the width W is greater than or equal to the height H:
        a.  Create a new output grid with height (2 * H + 1) and width W.
        b.  Copy the input grid into the top H rows of the output grid (rows 0 to H-1).
        c.  Fill the middle row (row H) of the output grid with white pixels (value 0).
        d.  Copy the input grid into the bottom H rows of the output grid (rows H+1 to 2*H).
    4.  Else (if the height H is greater than the width W):
        a.  Create a new output grid with height H and width (2 * W + 1).
        b.  Copy the input grid into the left W columns of the output grid (columns 0 to W-1).
        c.  Fill the middle column (column W) of the output grid with white pixels (value 0).
        d.  Copy the input grid into the right W columns of the output grid (columns W+1 to 2*W).
    5.  Return the constructed output grid.