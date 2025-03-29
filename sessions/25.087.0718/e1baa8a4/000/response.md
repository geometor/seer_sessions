*   **Perception:** The input grids are composed of large, rectangular blocks of solid colors. These blocks are arranged adjacent to each other, forming a larger grid structure within the input. The output grid is a significantly smaller grid where each cell corresponds to one of the color blocks in the input. The color of each cell in the output matches the color of the corresponding block in the input, and the relative spatial arrangement of the blocks is preserved.

*   **YAML Facts:**
    
```yaml
    task_description: Downsample a grid composed of solid color blocks into a smaller grid representing the blocks.
    
    elements:
      - element: input_grid
        description: A 2D grid composed of adjacent, solid-colored rectangular blocks.
        properties:
          - shape: variable (height x width)
          - content: integers 0-9 representing colors
          - structure: divided into distinct rectangular regions of uniform color
    
      - element: output_grid
        description: A smaller 2D grid representing the blocks found in the input grid.
        properties:
          - shape: determined by the number of unique block rows and columns in the input
          - content: integers 0-9 representing the colors of the corresponding blocks
          - structure: each cell corresponds to a unique block in the input grid
    
    relationships:
      - type: correspondence
        description: Each cell in the output grid corresponds to a distinct, contiguous block of color in the input grid.
      - type: spatial_preservation
        description: The relative position (top-left, top-right, bottom-left, etc.) of the color blocks in the input grid is maintained in the output grid.
      - type: color_mapping
        description: The color of a cell in the output grid is the same as the color of the corresponding block in the input grid.
    
    actions:
      - action: identify_blocks
        description: Segment the input grid into its constituent contiguous blocks of uniform color.
      - action: determine_representative_points
        description: Find a unique point (e.g., the top-left corner) for each identified block.
      - action: determine_output_dimensions
        description: Calculate the number of rows and columns for the output grid based on the unique row and column indices of the representative points.
      - action: construct_output
        description: Create the output grid by placing the color of each input block into the corresponding cell based on the relative positions of their representative points.
    ```


*   **Natural Language Program:**
    1.  Identify all distinct, contiguous blocks (regions) of uniform color within the input grid.
    2.  For each identified block, determine its color and find its top-leftmost pixel coordinate.
    3.  Collect all unique top-leftmost row indices and sort them.
    4.  Collect all unique top-leftmost column indices and sort them.
    5.  Create a new output grid with dimensions equal to (number of unique row indices) x (number of unique column indices).
    6.  Iterate through the identified blocks. For each block with top-left coordinate (r, c) and color V:
        a.  Find the index `out_r` corresponding to `r` in the sorted unique row indices.
        b.  Find the index `out_c` corresponding to `c` in the sorted unique column indices.
        c.  Set the pixel at `output_grid[out_r][out_c]` to the block's color V.
    7.  Return the constructed output grid.