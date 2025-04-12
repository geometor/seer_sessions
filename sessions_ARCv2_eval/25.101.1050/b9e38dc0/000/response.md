*   **Perception**: The task involves identifying specific regions within a grid and performing a "fill" operation based on the colors present. There seem to be three key color roles: a 'background' color that gets overwritten, a 'fill' color that serves as the starting point (seed) and the replacement color, and 'boundary' colors that limit the extent of the fill. The exact nature of the fill (e.g., standard flood fill vs. directional fill) can vary between examples.

*   **YAML Facts**:
    
```yaml
    task_type: grid_transformation
    transformation_type: conditional_fill
    components:
      - role: background_color
        description: The color of pixels eligible to be filled. Changes between input and output within specific regions.
        examples:
          - train_1: blue (1)
          - train_2: white (0)
          - train_3: orange (7)
      - role: fill_color
        description: The color used to fill the background pixels. Also serves as the starting seed(s) for the fill. Present in small amounts in the input, expands in the output.
        examples:
          - train_1: maroon (9)
          - train_2: yellow (4)
          - train_3: green (3)
      - role: boundary_colors
        description: Colors that block the fill operation. They remain unchanged between input and output and define the limits of the filled area.
        examples:
          - train_1: [green (3), gray (5)]
          - train_2: [gray (5)]
          - train_3: [maroon (9), magenta (6), azure (8)] # All non-background, non-fill colors act as boundaries
      - role: fill_mechanism
        description: The method by which the fill propagates from the seed(s).
        types:
          - flood_fill_4_way: Propagates up, down, left, right to adjacent background pixels. Stops at boundaries or grid edges. (e.g., train_1, train_3)
          - directional_fill_left: Propagates only leftwards to adjacent background pixels. Stops at boundaries or grid edges. (e.g., train_2)
    process_overview:
      - Identify background, fill, and boundary colors by comparing input and output.
      - Locate initial seed pixels (fill color) in the input.
      - Determine the appropriate fill mechanism (flood fill or directional).
      - Execute the fill starting from seeds, replacing background pixels with the fill color, respecting boundaries.
    ```


*   **Natural Language Program**:
    1.  Compare the input and output grids to identify the background color (changes), the fill color (replaces background, starts small), and boundary colors (unchanged, contain the fill).
    2.  Create a copy of the input grid to serve as the working output grid.
    3.  Find the coordinates of all pixels in the input grid that have the fill color (these are the initial seeds).
    4.  Determine the fill type:
        *   If the fill expands outwards in multiple directions (like train_1 and train_3), use a 4-directional flood fill. Initialize a queue with the seed coordinates.
        *   If the fill expands primarily leftwards (like train_2), use a directional left-fill mechanism.
    5.  Execute the fill:
        *   **For Flood Fill:** While the queue is not empty, remove a coordinate `(r, c)`. For each neighbor `(nr, nc)` (up, down, left, right): if the neighbor is within bounds and its color in the working output grid is the background color, change its color to the fill color and add `(nr, nc)` to the queue.
        *   **For Directional Left-Fill:** Repeatedly scan the grid. In each scan, if a pixel `(r, c)` has the fill color and the pixel to its left `(r, c-1)` exists and has the background color, change `(r, c-1)` to the fill color. Continue scanning until a full scan makes no changes.
    6.  Return the final working output grid.