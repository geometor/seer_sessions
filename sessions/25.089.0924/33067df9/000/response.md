*   **Perception:** The task transforms a small input grid containing sparsely placed colored pixels into a much larger, fixed-size output grid (26x26). The input grid acts as a blueprint or map. Each non-white pixel in the input corresponds to a solid-colored rectangular block in the output. The relative positions of these blocks in the output grid mirror the relative positions of the source pixels in the input grid. The output grid has a consistent 2-pixel white border. The central 22x22 area of the output is divided into a grid of colored blocks separated by 2-pixel wide white gaps (both horizontally and vertically). The size of each colored block depends on the number of input rows and columns that contain non-white pixels. Specifically, the total height (or width) of the blocks plus the gaps sums to 22 pixels.

*   **Facts:**
    
```yaml
    task_type: grid_transformation
    input_features:
      - type: grid
      - dimensionality: 2D
      - element_type: color_pixels (integers 0-9)
      - content: sparse non-white pixels on a white background
    output_features:
      - type: grid
      - dimensionality: 2D
      - size: fixed (26x26)
      - element_type: color_pixels (integers 0-9)
      - content: solid rectangular blocks of color on a white background
      - structure:
          - border: 2-pixel white border
          - inner_area: 22x22 active region
          - layout: grid of colored blocks separated by 2-pixel white gaps
    transformation:
      - action: identify_active_elements
        target: input grid rows and columns containing non-white pixels
        result: sets of active row indices and active column indices
      - action: calculate_layout_parameters
        inputs: count of active rows (N_rows), count of active columns (N_cols)
        constants: active_area_dimension=22, gap_size=2
        outputs: block_height = (22 - (N_rows - 1) * 2) / N_rows, block_width = (22 - (N_cols - 1) * 2) / N_cols
      - action: map_pixels_to_blocks
        mapping: Each non-white pixel at input[r][c] maps to an output block.
        details:
          - The sequential index of 'r' within the sorted active rows determines the row position of the output block.
          - The sequential index of 'c' within the sorted active columns determines the column position of the output block.
      - action: render_output_grid
        steps:
          - Initialize a 26x26 white grid.
          - For each non-white input pixel:
            - Determine its color.
            - Determine its corresponding output block's top-left corner based on its active row/column index, block dimensions, and gap size (starting from offset (2,2)).
            - Fill the calculated rectangular area (block_height x block_width) in the output grid with the pixel's color.
    relationships:
      - Each non-white input pixel directly determines the color and location of one output block.
      - The number of active rows/columns in the input determines the size of all output blocks.
      - Relative positioning is preserved: a pixel to the right/below another in the input results in a block to the right/below the corresponding block in the output.
    ```


*   **Natural Language Program:**
    1.  Create a new output grid of size 26x26, filled entirely with the background color (white, 0).
    2.  Scan the input grid to find all row indices that contain at least one non-white pixel. Store these unique row indices in a sorted list called `active_rows`. Let `N_rows` be the number of elements in `active_rows`.
    3.  Scan the input grid to find all column indices that contain at least one non-white pixel. Store these unique column indices in a sorted list called `active_cols`. Let `N_cols` be the number of elements in `active_cols`.
    4.  Calculate the height of the output blocks: `block_height = (22 - (N_rows - 1) * 2) / N_rows`.
    5.  Calculate the width of the output blocks: `block_width = (22 - (N_cols - 1) * 2) / N_cols`.
    6.  Define the gap size between blocks: `gap_size = 2`.
    7.  Define the border offset: `offset = 2`.
    8.  Iterate through each pixel `(r, c)` in the input grid.
    9.  If the color `clr` of the input pixel `input[r, c]` is not white (0):
        a.  Find the index `i` such that `active_rows[i]` equals `r`.
        b.  Find the index `j` such that `active_cols[j]` equals `c`.
        c.  Calculate the starting row for the output block: `out_r_start = offset + i * (block_height + gap_size)`.
        d.  Calculate the starting column for the output block: `out_c_start = offset + j * (block_width + gap_size)`.
        e.  Fill the rectangular region in the output grid from row `out_r_start` to `out_r_start + block_height - 1` and from column `out_c_start` to `out_c_start + block_width - 1` with the color `clr`.
    10. Return the completed output grid.