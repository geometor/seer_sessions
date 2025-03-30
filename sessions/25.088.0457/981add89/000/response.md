Okay, let's analyze the provided examples.

**Perception**

1.  **Grid Size:** The input and output grids have the same dimensions in both examples (20x20 for the first, 30x30 for the second).
2.  **Background Color:** There's a dominant background color in each example (azure/8 in the first, orange/7 in the second). This color seems mostly preserved in the output, except in specific locations.
3.  **Seed Pixels:** In both examples, the first row contains a few pixels that are *not* the background color. Let's call these "seed pixels".
4.  **Vertical Lines:** The primary transformation appears to involve drawing vertical lines downwards from each seed pixel. The color of the line corresponds to the color of the seed pixel.
5.  **Interaction/Overwriting:** These vertical lines interact with the existing pixels in the input grid column below the seed. The rules for this interaction seem consistent:
    *   If the line encounters a background pixel, the output pixel takes the line's color.
    *   If the line encounters a pixel of the *same* color as the line itself (the seed color), the output pixel changes to the background color.
    *   If the line encounters a pixel of a *different* non-background color, the output pixel takes the line's color (overwriting the original color).
6.  **Seed Row Preservation:** The seed pixels themselves (in the first row) seem to retain their original color in the output grid. The transformation rules apply only to the rows *below* the first row.

**Facts**


```yaml
task_context:
  grid_properties:
    - input_output_size_identical: True
    - background_color_exists: True
      # Example 1: Azure (8)
      # Example 2: Orange (7)
  object_identification:
    - type: background
      description: The most frequent color in the input grid. Persists in the output except where modified by transformation rules.
    - type: seed_pixels
      description: Pixels located in the first row (row 0) whose color is different from the background color.
      properties: [color, column_index]
    - type: target_columns
      description: The columns corresponding to the column indices of the seed_pixels.
    - type: existing_pixels
      description: Pixels in the target_columns below the first row in the input grid.

transformation_logic:
  actions:
    - action: identify_background_color
      inputs: [input_grid]
      outputs: [background_color]
    - action: identify_seed_pixels
      inputs: [input_grid, background_color]
      outputs: [list_of_seed_pixels] # Each element is {color: C, column: c}
    - action: initialize_output
      inputs: [input_grid]
      outputs: [output_grid] # Starts as a copy of input_grid
    - action: process_columns
      inputs: [list_of_seed_pixels, input_grid, output_grid, background_color]
      outputs: [modified_output_grid]
      sub_steps:
        - For each seed {color: C, column: c}:
        - For each row `r` from 1 to grid_height - 1:
            - Get input_pixel_color = input_grid[r, c]
            - Apply transformation rules:
                - IF input_pixel_color == background_color THEN set output_grid[r, c] = C
                - ELSE IF input_pixel_color == C THEN set output_grid[r, c] = background_color
                - ELSE set output_grid[r, c] = C # Overwrite other colors
  rule_summary: For each column containing a non-background seed pixel in the first row, transform the pixels below the first row based on the seed color (C) and the background color (BKG). Pixels matching BKG become C, pixels matching C become BKG, and all other pixels become C. The first row remains unchanged from the input.
```


**Natural Language Program**

1.  Identify the background color (BKG) of the input grid, which is the most common color.
2.  Create the output grid by making an identical copy of the input grid.
3.  Find all "seed pixels" in the first row (row 0) of the input grid. A seed pixel is any pixel whose color is not BKG. For each seed pixel, note its color (C) and its column index (c).
4.  For each identified seed pixel with color C and column c:
    a.  Iterate through all rows `r` starting from row 1 down to the bottom of the grid.
    b.  Examine the color of the pixel in the **input** grid at position `(r, c)`. Let this color be `input_color`.
    c.  Determine the color for the pixel in the **output** grid at position `(r, c)` using these rules:
        i.  If `input_color` is the background color (BKG), set the output pixel `output[r, c]` to the seed color C.
        ii. If `input_color` is the same as the seed color (C), set the output pixel `output[r, c]` to the background color BKG.
        iii.If `input_color` is any other color (neither BKG nor C), set the output pixel `output[r, c]` to the seed color C.
5.  After processing all columns corresponding to seed pixels, the resulting output grid is the final answer.