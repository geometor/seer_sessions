Okay, let's analyze the task examples.

## Perception

1.  **Grid Structure:** The input and output are grids of pixels represented by numbers 0-9 (colors). The grid sizes vary slightly but are generally around 10x10.
2.  **Background Color:** A consistent background color, orange (7), is present in all examples and remains largely unchanged in the output.
3.  **Foreground Objects:** The input grids contain distinct shapes or patterns made of colors other than the background (magenta 6, azure 8). These shapes vary between examples (e.g., 'C' shape, 'H' shape, rectangles).
4.  **Transformation:** The primary transformation involves adding new pixels of a specific color, red (2), to the grid. The original foreground shapes and the background pixels not affected by the change remain the same in the output.
5.  **Placement of Red Pixels:** The red (2) pixels appear in the output at specific locations relative to the original foreground shapes. Visually, they seem to be near the "corners" or points where the shape's outline changes direction.
6.  **Local Pattern:** Examining the relationship more closely, a background pixel (orange 7) seems to change to red (2) if it's part of a 2x2 square in the input that contains exactly one foreground pixel (magenta 6 or azure 8) and three background pixels (orange 7). Multiple such 2x2 squares can trigger the change for the same pixel.

## Facts


```yaml
task_context:
  grid_representation: 2D array of integers 0-9 representing colors.
  background_color: 7 (orange)
  foreground_colors:
    - 6 (magenta) in examples 1, 2
    - 8 (azure) in example 3
  output_color_added: 2 (red)
transformation_elements:
  - element_type: background_pixel
    color: 7 (orange)
    action: Conditional change to 2 (red).
    condition: The pixel is part of at least one 2x2 square in the input grid that contains exactly one non-background pixel (color != 7) and three background pixels (color == 7).
  - element_type: foreground_pixel
    color: Any color != 7
    action: No change. Retains original color in the output.
  - element_type: background_pixel
    color: 7 (orange)
    action: No change. Retains original color in the output.
    condition: The pixel does not meet the condition for changing to red (2).
relationships:
  - The placement of the new red (2) pixels depends on the local 2x2 neighborhood configuration around each background pixel in the input grid, specifically the count of foreground vs. background pixels within those 2x2 squares.
```


## Natural Language Program

1.  Initialize the output grid as a copy of the input grid.
2.  Iterate through each pixel `(r, c)` in the input grid, where `r` is the row index and `c` is the column index.
3.  For each pixel `(r, c)`, check if its color in the input grid is the background color (orange, 7).
4.  If the pixel `(r, c)` is a background pixel, examine the four possible 2x2 squares that include this pixel:
    *   Square 1 (Top-Left Origin): Pixels at `(r-1, c-1), (r-1, c), (r, c-1), (r, c)`
    *   Square 2 (Top-Right Origin): Pixels at `(r-1, c), (r-1, c+1), (r, c), (r, c+1)`
    *   Square 3 (Bottom-Left Origin): Pixels at `(r, c-1), (r, c), (r+1, c-1), (r+1, c)`
    *   Square 4 (Bottom-Right Origin): Pixels at `(r, c), (r, c+1), (r+1, c), (r+1, c+1)`
    *   Ensure that when checking these squares, you only consider pixels that are within the bounds of the input grid.
5.  For each valid 2x2 square found in step 4, count the number of foreground pixels (any color not equal to 7) within that square.
6.  If *any* of these valid 2x2 squares contains *exactly one* foreground pixel (and therefore three background pixels), change the color of the pixel at `(r, c)` in the *output* grid to red (2).
7.  If a pixel `(r, c)` was originally a foreground pixel in the input, or if it was a background pixel but did not meet the condition in step 6, its color in the output grid remains the same as in the input grid.
8.  Return the final output grid.