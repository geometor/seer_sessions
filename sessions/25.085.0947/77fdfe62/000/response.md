## Perception

1.  **Input Structure:** The input grids have a distinct structure. They feature a rectangular frame made of blue (1) pixels. This frame encloses an inner area. The four corner pixels of the input grid have specific colors that differ in each example.
2.  **Inner Content:** The area strictly inside the blue frame contains a pattern composed of white (0) and azure (8) pixels. The size of this inner area varies (2x2 in the first example, 4x4 in the others).
3.  **Output Structure:** The output grid's dimensions match the dimensions of the inner area extracted from the input grid.
4.  **Color Transformation:** The output grid's colors are derived from the input grid's corner colors and the pattern within the inner area. Specifically, white pixels (0) in the inner area remain white (0) in the output. Azure pixels (8) in the inner area are replaced by one of the four corner colors from the input grid.
5.  **Mapping Rule:** The choice of which corner color replaces an azure (8) pixel depends on the pixel's position within the inner grid. The inner grid is conceptually divided into four equal quadrants (top-left, top-right, bottom-left, bottom-right). An azure pixel's color in the output is determined by the corner color corresponding to the quadrant it falls into (e.g., an azure pixel in the top-left quadrant of the inner grid becomes the top-left corner color of the input grid).

## Facts


```yaml
task_elements:
  - item: input_grid
    properties:
      - type: 2D grid of pixels (colors 0-9)
      - contains a rectangular frame object
      - contains four distinct corner pixels
      - contains an inner area enclosed by the frame
  - item: output_grid
    properties:
      - type: 2D grid of pixels
      - dimensions match the inner area of the input grid
      - colors are derived from input corner colors and the inner area pattern

objects:
  - object: frame
    description: A rectangle composed of contiguous blue (1) pixels in the input grid.
    properties:
      - color: blue (1)
      - shape: rectangle
      - function: encloses the inner_area
  - object: corners
    description: The four pixels at the absolute corners of the input grid.
    properties:
      - count: 4
      - position: top-left (TL), top-right (TR), bottom-left (BL), bottom-right (BR)
      - color: variable (e.g., maroon, yellow, red, green in example 1)
      - role: source colors for the output grid transformation
  - object: inner_area
    description: The subgrid strictly inside the blue frame.
    properties:
      - content: pixels are either white (0) or azure (8)
      - dimensions: variable (e.g., 2x2, 4x4)
      - role: pattern template for the output grid
      - structure: conceptually divisible into four equal quadrants (TL, TR, BL, BR)

actions:
  - action: identify_frame
    description: Locate the boundaries of the blue (1) rectangle.
    inputs: input_grid
    outputs: frame_boundaries
  - action: extract_inner_area
    description: Get the subgrid located inside the frame_boundaries.
    inputs: input_grid, frame_boundaries
    outputs: inner_area_grid
  - action: identify_corner_colors
    description: Get the colors of the four corner pixels of the input_grid.
    inputs: input_grid
    outputs: corner_colors (TL_color, TR_color, BL_color, BR_color)
  - action: generate_output_grid
    description: Create a new grid with the same dimensions as inner_area_grid.
    inputs: inner_area_grid dimensions
    outputs: empty_output_grid
  - action: map_pixels
    description: >
      Populate the output grid based on the inner_area_grid pixels and input corner colors.
      For each pixel (r, c) in the inner_area_grid:
      If inner_area_grid[r, c] is white (0), output_grid[r, c] becomes white (0).
      If inner_area_grid[r, c] is azure (8), determine its quadrant (TL, TR, BL, BR) within inner_area_grid.
      Set output_grid[r, c] to the corresponding input corner color (TL_color, TR_color, BL_color, BR_color).
    inputs: inner_area_grid, corner_colors, output_grid
    outputs: populated_output_grid (final result)

relationships:
  - relationship: output_size_determination
    description: The height and width of the output_grid are identical to the height and width of the inner_area.
  - relationship: pixel_color_mapping
    description: >
      The color of a pixel in the output_grid depends on the color of the corresponding pixel in the inner_area
      and, if that color is azure (8), its quadrant position within the inner_area and the input grid's corner colors.
```


## Natural Language Program

1.  **Identify the boundaries** of the rectangular frame composed entirely of blue (1) pixels within the input grid.
2.  **Extract the subgrid** (the `inner_area`) located strictly inside these frame boundaries. Note its dimensions (Height x Width).
3.  **Identify the four corner colors** from the original input grid: `top_left_color`, `top_right_color`, `bottom_left_color`, `bottom_right_color`.
4.  **Create a new output grid** with the same dimensions (Height x Width) as the `inner_area`.
5.  **Iterate** through each pixel at position `(row, col)` in the `inner_area`:
    *   a. If the `inner_area` pixel at `(row, col)` is white (0), set the output grid pixel at `(row, col)` to white (0).
    *   b. If the `inner_area` pixel at `(row, col)` is azure (8), determine which quadrant it belongs to based on its position relative to the center of the `inner_area` (Height/2, Width/2):
        *   If `row < Height / 2` and `col < Width / 2` (Top-Left Quadrant), set the output grid pixel at `(row, col)` to `top_left_color`.
        *   If `row < Height / 2` and `col >= Width / 2` (Top-Right Quadrant), set the output grid pixel at `(row, col)` to `top_right_color`.
        *   If `row >= Height / 2` and `col < Width / 2` (Bottom-Left Quadrant), set the output grid pixel at `(row, col)` to `bottom_left_color`.
        *   If `row >= Height / 2` and `col >= Width / 2` (Bottom-Right Quadrant), set the output grid pixel at `(row, col)` to `bottom_right_color`.
6.  **Return** the populated output grid.