## Perception

1.  **Grid Structure:** Both examples involve rectangular grids of varying sizes.
2.  **Color Palette:** Each example uses primarily two colors: a background color (blue=1 in Ex1, white=0 in Ex2) and a foreground color (magenta=6 in Ex1, green=3 in Ex2). The background color is the most frequent color in the input grid.
3.  **Input Patterns:** The inputs contain scattered foreground pixels, as well as horizontal and vertical lines or small blocks made of the foreground color, all set against the background color.
4.  **Output Patterns:** The outputs are largely similar to the inputs, maintaining the grid size and the primary colors.
5.  **Key Transformations:** Two main types of changes are observed between input and output:
    *   **Pixel Removal:** In Example 1, a single magenta pixel (at row 3, col 19) that was surrounded horizontally and vertically by blue pixels is changed to blue in the output. This suggests a rule for removing "isolated" foreground pixels.
    *   **Gap Filling:** In both examples, horizontal gaps of background pixels that are situated directly between two foreground pixels *on the same row* are filled with the foreground color. This occurred in Example 1 (row 7 and row 9) and Example 2 (row 9). The size of the gap filled can be one or more pixels.
6.  **Consistency:** The transformation appears to happen in two stages: first, cleaning up isolated pixels, and second, filling horizontal gaps based on the cleaned-up state.

## Facts


```yaml
task_context:
  description: "The task involves modifying a grid by cleaning up isolated foreground pixels and filling horizontal gaps between foreground pixels."
  grid_properties:
    - dimensions_vary: True
    - background_color_varies: True # Example 1: Blue (1), Example 2: White (0)
    - foreground_color_varies: True # Example 1: Magenta (6), Example 2: Green (3)

elements:
  - object: background_pixel
    properties:
      - color: Most frequent color in the input grid (e.g., Blue=1 or White=0)
      - role: Fills most of the grid area initially. Can be part of gaps.
  - object: foreground_pixel
    properties:
      - color: The less frequent, non-background color (e.g., Magenta=6 or Green=3)
      - role: Forms patterns, lines, or scattered points. Can be isolated or connected.
  - object: isolated_foreground_pixel
    description: A foreground_pixel with no adjacent (horizontal or vertical) neighbors of the same foreground color.
    properties:
      - color: Foreground color
      - location: Specific row and column
      - condition: All four cardinal neighbors (up, down, left, right) have the background color.
  - object: horizontal_gap
    description: A sequence of one or more background pixels on a single row.
    properties:
      - content: Sequence of background_pixels
      - location: Specific row and column range
      - condition: Immediately preceded and followed by a foreground_pixel on the same row.

actions:
  - action: identify_colors
    description: Determine the background and foreground colors based on frequency in the input grid.
  - action: cleanup_isolated_pixels
    description: Iterate through all foreground pixels. If a pixel is identified as isolated, change its color to the background color.
    input: grid, background_color, foreground_color
    output: modified_grid
  - action: fill_horizontal_gaps
    description: Iterate through each row of the (potentially modified) grid. Find horizontal gaps flanked by foreground pixels and fill them with the foreground color.
    input: grid, background_color, foreground_color
    output: final_grid

relationships:
  - type: adjacency
    description: Pixels are considered adjacent if they share an edge (horizontally or vertically). Used to determine isolation.
  - type: horizontal_betweenness
    description: A background pixel (or sequence) is between two foreground pixels if they are on the same row, and the background pixel(s) are located at columns strictly between the columns of the foreground pixels, with no other foreground pixels intervening in that row segment. Used for gap filling.
```


## Natural Language Program

1.  **Identify Colors:** Determine the background color (the most common color in the input grid) and the foreground color (the other color present).
2.  **Create a Working Copy:** Start with a copy of the input grid.
3.  **Cleanup Isolated Pixels:** Examine every pixel in the working copy. If a pixel has the foreground color, check its four cardinal neighbors (up, down, left, right). If *none* of these neighbors have the foreground color, change the color of the current pixel to the background color. Perform this check for all foreground pixels based on the state *before* any changes in this step are made (or iterate until no more changes occur).
4.  **Fill Horizontal Gaps:** Iterate through each row of the grid modified in Step 3. Within each row, scan from left to right. If you encounter a sequence like `[Foreground Pixel] [Background Pixel] ... [Background Pixel] [Foreground Pixel]`, change all the background pixels within that sequence to the foreground color. Repeat this for all such sequences found in every row.
5.  **Output:** The final state of the working grid after completing Step 4 is the output grid.