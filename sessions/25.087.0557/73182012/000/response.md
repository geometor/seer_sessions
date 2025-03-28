*   **Perception:**
    *   Each task involves an input grid and a smaller output grid.
    *   The input grids contain various shapes composed of different colored pixels (values 1-9) on a white (value 0) background.
    *   The output grids are consistently 4x4 in size across all examples.
    *   The content of the output grid appears to be a direct copy of a specific region from the input grid.
    *   Comparing the input and output grids, the output seems to be the top-left 4x4 corner of the smallest rectangular area (bounding box) that encloses all the non-white pixels in the input grid.

*   **YAML Facts:**
    
```yaml
    task_description: Extract a specific 4x4 subgrid from the input grid based on the location of non-white pixels.
    
    elements:
      - element: input_grid
        description: A 2D array of pixels with integer values 0-9. Contains a background (white, 0) and one or more foreground objects (non-white pixels).
      - element: output_grid
        description: A 4x4 2D array of pixels, derived from the input grid.
      - element: non_white_pixels
        description: Pixels in the input grid with values from 1 to 9.
      - element: bounding_box
        description: The smallest rectangle enclosing all non_white_pixels in the input grid. Defined by its top-left corner coordinates (min_row, min_col).
    
    transformation:
      - step: 1
        action: identify_non_white_pixels
        input: input_grid
        output: coordinates of all pixels with value > 0.
      - step: 2
        action: calculate_bounding_box
        input: coordinates of non_white_pixels
        output: top_left_corner (min_row, min_col) of the bounding box.
      - step: 3
        action: extract_subgrid
        input: 
          - input_grid
          - top_left_corner (min_row, min_col)
        parameters:
          - height: 4
          - width: 4
        output: output_grid (the 4x4 subgrid from input_grid starting at [min_row, min_col]).
    
    relationships:
      - The output_grid's content is identical to a 4x4 subgrid within the input_grid.
      - The location of this 4x4 subgrid is determined by the top-left corner of the bounding_box of non_white_pixels.
      - The size of the output_grid is fixed at 4x4, regardless of the bounding_box size.
    ```


*   **Natural Language Program:**
    1.  Scan the input grid to find all pixels that are not white (value is not 0).
    2.  Determine the coordinates (row and column) of the top-most, bottom-most, left-most, and right-most non-white pixels. These define the minimum bounding box containing all non-white content.
    3.  Identify the row and column index of the top-left corner of this bounding box (minimum row, minimum column).
    4.  Extract a 4x4 subgrid from the input grid, starting at this identified top-left corner. This 4x4 subgrid is the output grid.