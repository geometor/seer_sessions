*   **Perception:** The input grids contain various colored pixels (non-white) scattered on a white background. In each example, there is one prominent, large, contiguous object composed of non-white pixels, along with some smaller, isolated non-white pixels or small groups. The output grid is always a cropped version of the input grid, containing only the largest contiguous object found in the input. The cropping dimensions precisely match the bounding box of this largest object.

*   **YAML Facts:**
    
```yaml
    task_type: object_extraction
    input_properties:
      - background_color: white (0)
      - contains_multiple_objects: true
      - objects_are_contiguous_non_white_pixels: true
      - objects_can_be_different_colors: true
      - objects_vary_in_size: true
    output_properties:
      - background_color: not guaranteed (depends on extracted object)
      - contains_single_object: true (the largest from the input)
      - grid_size: variable (matches bounding box of the extracted object)
    transformation:
      - identify_objects: Find all contiguous regions of non-white pixels in the input.
      - filter_objects: Select the object with the largest area (pixel count).
      - determine_bounds: Find the minimum and maximum row and column indices (bounding box) of the selected largest object.
      - crop_input: Extract the subgrid from the input corresponding to the calculated bounding box.
      - result: The extracted subgrid is the output.
    relationships:
      - The output grid is a subgrid of the input grid.
      - The content of the output grid corresponds exactly to the largest contiguous non-white object from the input, including any white pixels within its bounding box.
      - Smaller non-white objects or pixels outside the bounding box of the largest object are discarded.
    ```


*   **Natural Language Program:**
    1.  Scan the input grid to identify all distinct contiguous areas (objects) formed by connected non-white pixels (pixels with values 1 through 9). Consider pixels connected if they are adjacent horizontally or vertically.
    2.  Calculate the size (number of pixels) for each identified object.
    3.  Determine which object has the largest size. If there's a tie, any of the largest objects can be chosen (though the examples don't show ties).
    4.  Find the bounding box of this largest object: determine its minimum row index, maximum row index, minimum column index, and maximum column index.
    5.  Create a new grid whose dimensions are determined by the height (max_row - min_row + 1) and width (max_col - min_col + 1) of the bounding box.
    6.  Copy the pixels from the input grid within the range [min_row, max_row] and [min_col, max_col] into the new output grid, preserving their relative positions.