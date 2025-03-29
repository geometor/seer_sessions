**Perception**

1.  **Grid Structure:** Each input and output is a grid of pixels with different colors.
2.  **Background Color:** In each example, there's a predominant background color (blue in Ex1, azure in Ex2, yellow in Ex3).
3.  **Key Pixel:** Each input grid contains exactly one pixel that is neither the background color nor white (color 0). This pixel seems to be the "source" or "trigger" for the transformation. Its color varies between examples (green in Ex1, red in Ex2, azure in Ex3).
4.  **White Pixels:** There are also white pixels (color 0) present in the input grids, often forming simple shapes. These white pixels, along with the background, seem to remain unchanged in the output, *unless* overwritten by the transformation process. They don't appear to directly influence the core transformation logic.
5.  **Transformation:** The primary transformation involves adding a pattern of pixels to the grid. The color of the added pixels is the same as the color of the "source" pixel identified in step 3.
6.  **Pattern Characteristics:** The shape and relative position of the added pattern depend entirely on the *color* of the source pixel. Each source color (green, red, azure) corresponds to a unique, fixed pattern of relative coordinates.
7.  **Pattern Application:** The pattern (defined as a set of relative row/column offsets) is applied relative to the location of the source pixel. The source pixel itself is part of the pattern (offset (0,0)). Pixels in the input grid at the target locations are overwritten with the source pixel's color.
8.  **Boundary Conditions:** The pattern application respects the grid boundaries; only pixels within the grid dimensions are modified.

**Facts**


```yaml
task_elements:
  - element: grid
    attributes:
      - background_color: most frequent color in the input grid
      - dimensions: height and width
  - element: source_pixel
    description: A single pixel in the input grid whose color is neither the background color nor white (0).
    attributes:
      - color: identifies the type of transformation/pattern
      - location: (row, column) coordinates, serves as the anchor point for the pattern
  - element: pattern
    description: A set of relative (row, column) offsets specific to the source_pixel's color.
    attributes:
      - color_association: Each potential source_pixel color (e.g., green, red, azure) maps to a distinct pattern.
      - shape: The collection of offsets defines the shape of the pixels to be added/changed.
      - origin: Includes the offset (0,0), meaning the source_pixel location is part of the pattern.
  - element: white_pixels
    description: Pixels with color 0.
    attributes:
      - role: Appear to be distractors or fixed elements, preserved unless overwritten by the pattern application.

transformation:
  - action: identify_background_color
    inputs: input_grid
    outputs: background_color
  - action: identify_source_pixel
    inputs: input_grid, background_color
    outputs: source_pixel (color and location)
  - action: select_pattern
    inputs: source_pixel_color
    outputs: pattern (set of relative offsets)
    details: Uses a predefined mapping {source_color -> pattern}.
      - color_3_pattern: '{(0,0), (1,0), (1,1), (1,2), (2,-2), (2,0), (3,-3), (3,-2), (3,-1), (4,-4), (4,-2), (5,-4), (5,-3)}'
      - color_2_pattern: '{(0,0), (1,-1), (1,1), (2,0), (2,2), (3,1), (3,3), (4,2), (4,4), (5,3), (5,5), (6,4), (6,6)}'
      - color_8_pattern: '{(-4,0), (-4,1), (-4,3), (-4,4), (-3,0), (-3,1), (-3,3), (-3,4), (-2,2), (-1,0), (-1,1), (-1,3), (-1,4), (0,0), (0,1), (0,3), (0,4)}'
  - action: apply_pattern
    inputs: input_grid, source_pixel (color and location), selected_pattern
    outputs: output_grid
    details:
      - Create a copy of the input grid.
      - For each offset (dr, dc) in the pattern:
        - Calculate target coordinates (source_row + dr, source_col + dc).
        - If target coordinates are within grid bounds, set the pixel at that location in the copied grid to the source_pixel's color.

relationships:
  - The output pattern's color matches the source_pixel's color.
  - The output pattern's shape and position relative to the source_pixel depend only on the source_pixel's color.
  - The background color helps identify the source_pixel but doesn't directly influence the pattern shape or color.
  - White pixels are static elements unless overwritten.
```


**Natural Language Program**

1.  Initialize the output grid as a copy of the input grid.
2.  Determine the most frequent color in the input grid; this is the `background_color`.
3.  Find the coordinates (`source_row`, `source_col`) and color (`source_color`) of the unique pixel in the input grid that is neither the `background_color` nor white (color 0).
4.  Define the patterns associated with specific `source_color` values:
    *   `pattern_green` = `{(0,0), (1,0), (1,1), (1,2), (2,-2), (2,0), (3,-3), (3,-2), (3,-1), (4,-4), (4,-2), (5,-4), (5,-3)}`
    *   `pattern_red` = `{(0,0), (1,-1), (1,1), (2,0), (2,2), (3,1), (3,3), (4,2), (4,4), (5,3), (5,5), (6,4), (6,6)}`
    *   `pattern_azure` = `{(-4,0), (-4,1), (-4,3), (-4,4), (-3,0), (-3,1), (-3,3), (-3,4), (-2,2), (-1,0), (-1,1), (-1,3), (-1,4), (0,0), (0,1), (0,3), (0,4)}`
5.  Select the appropriate pattern based on the identified `source_color`:
    *   If `source_color` is green (3), select `pattern_green`.
    *   If `source_color` is red (2), select `pattern_red`.
    *   If `source_color` is azure (8), select `pattern_azure`.
    *   (Assume other colors, if encountered, might have their own patterns or default behavior, though only these three are shown).
6.  Iterate through each relative offset coordinate (`dr`, `dc`) in the selected pattern.
7.  For each offset, calculate the target grid coordinates: `target_row = source_row + dr`, `target_col = source_col + dc`.
8.  Check if the `target_row` and `target_col` are within the valid row and column ranges of the grid.
9.  If the target coordinates are within the grid boundaries, update the pixel at (`target_row`, `target_col`) in the output grid to be the `source_color`.
10. Return the modified output grid.