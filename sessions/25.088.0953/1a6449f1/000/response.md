*   **Perception**: The task requires identifying a specific rectangular region within the input grid and extracting its contents. The key feature defining this region is a hollow rectangular frame made of a single, non-background color. The largest such frame in the input grid dictates the area to be extracted. The output is the content found strictly inside this frame.

*   **Facts YAML**:
    
```yaml
    task_type: extraction
    input_features:
      - grid: 2D array of pixels (integers 0-9)
      - objects:
          - type: hollow_rectangle_frame
            color: non-background (1-9)
            contiguity: horizontal/vertical adjacency
            properties:
              - boundary_color: single uniform color
              - largest_area: defined by bounding box (height * width)
              - location: coordinates of the bounding box (min_row, min_col, max_row, max_col)
              - interior_content: the pixels inside the frame
    output_features:
      - grid: 2D array of pixels extracted from the input
    transformation:
      - action: find_frames
        description: Identify all maximal hollow rectangular frames formed by a single contiguous non-background color.
        criteria:
          - Boundary must be at least 1 pixel thick.
          - Interior must contain at least one pixel different from the boundary color.
      - action: select_largest_frame
        description: Choose the frame with the maximum bounding box area (height * width). If multiple frames have the same maximal area, select the top-most, then left-most one.
        input: list of identified frames
        output: the single largest frame
      - action: extract_interior
        description: Extract the subgrid located strictly inside the boundary of the selected largest frame.
        input: input grid, location of the selected frame
        output: output grid
    relationships:
      - The output grid's content and dimensions are determined by the interior of the largest hollow rectangular frame found in the input grid.
      - The frame itself is composed of a single color found within the input grid.
    ```


*   **Natural Language Program**:
    1.  Scan the input grid to identify all distinct maximal hollow rectangular frames. A frame is defined as a rectangular boundary, at least one pixel thick, composed entirely of a single, contiguous non-background color (colors 1 through 9). The region inside the frame (the interior) must contain at least one pixel whose color differs from the frame's color.
    2.  Calculate the area (height * width) of the bounding box for each identified frame.
    3.  Select the frame that has the largest bounding box area. If there is a tie in area, select the frame whose top-left corner is located at the smallest row index; if there is still a tie, select the one with the smallest column index.
    4.  Determine the coordinates of the interior region of the selected frame. This region excludes the frame's boundary pixels. If the frame's bounding box spans rows `min_row` to `max_row` and columns `min_col` to `max_col`, the interior spans rows `min_row + 1` to `max_row - 1` and columns `min_col + 1` to `max_col - 1`.
    5.  Extract the subgrid corresponding to these interior coordinates from the input grid. This extracted subgrid is the output.