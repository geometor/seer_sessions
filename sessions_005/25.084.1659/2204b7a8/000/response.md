Okay, let's analyze the provided examples.

**Perception:**

1.  **Grid Structure:** All examples use 10x10 grids.
2.  **Key Colors:** The transformation seems to primarily involve green pixels (color 3) changing color. The grids also feature distinct border colors.
3.  **Border Patterns:**
    *   Example 1: The top row is entirely yellow (4), and the bottom row is entirely orange (7).
    *   Example 2: The leftmost column is entirely blue (1), and the rightmost column is entirely red (2).
    *   Example 3: The top row is entirely azure (8), and the bottom row is entirely maroon (9).
    *   It appears each grid has either uniform horizontal borders (top/bottom) or uniform vertical borders (left/right), but not both. These borders are non-white (color 0).
4.  **Transformation Focus:** Only the green (3) pixels located *between* the identified borders change color. The borders themselves and any other pixels remain unchanged.
5.  **Color Change Logic:** The new color assigned to a green pixel seems to depend on its proximity to the two borders.
    *   In Example 1 (horizontal borders), green pixels closer to the top yellow border become yellow, and those closer to the bottom orange border become orange.
    *   In Example 2 (vertical borders), green pixels closer to the left blue border become blue, and those closer to the right red border become red.
    *   In Example 3 (horizontal borders), green pixels closer to the top azure border become azure, and those closer to the bottom maroon border become maroon.
    *   The distance appears to be measured orthogonally (vertically for horizontal borders, horizontally for vertical borders).
6.  **Tie-Breaking:** In the provided examples, no green pixel is exactly equidistant from the two relevant borders. The rule seems to be based on which border is strictly closer. If a pixel were equidistant, a default rule might apply (e.g., defaulting to the top or left border), but this isn't explicitly demonstrated.

**Facts (YAML):**


```yaml
task_description: Modify the color of specific pixels based on their proximity to colored borders.

elements:
  - type: grid
    properties:
      - size: constant 10x10 in examples, but potentially variable.
      - background: primarily white (0).
  - type: border
    properties:
      - orientation: either "horizontal" (top and bottom rows) or "vertical" (left and right columns).
      - uniformity: each border line (row or column) consists of a single, non-white color.
      - colors: two distinct colors define the borders (e.g., top_color, bottom_color or left_color, right_color).
  - type: target_pixel
    properties:
      - color: green (3).
      - location: positioned within the grid, not on the borders themselves.

actions:
  - name: identify_borders
    inputs: input_grid
    outputs: border_type ("horizontal" or "vertical"), border_colors (pair of colors)
    description: Check if top/bottom rows or left/right columns are uniform non-white colors.
  - name: measure_distance
    inputs: pixel_coordinates (row, col), border_type
    outputs: distance_to_first_border, distance_to_second_border
    description: Calculate orthogonal distance from the pixel to the relevant borders.
  - name: change_color
    inputs: pixel_coordinates (row, col), distances, border_colors
    outputs: modified_pixel_color
    description: Change the green pixel's color to the color of the nearest border.

relationships:
  - The transformation rule depends on the type of border present (horizontal or vertical).
  - The final color of a target pixel is determined by its relative orthogonal distance to the two identified borders.
  - Pixels that are not green (3) or are part of the borders are unaffected.

assumptions:
  - Only one type of border (horizontal or vertical) will be present in a valid input.
  - If a green pixel is exactly equidistant between the two borders, it defaults to the color of the top border (for horizontal) or the left border (for vertical). (Note: This is an assumption as no equidistant examples were provided).

```


**Natural Language Program:**

1.  **Initialize:** Create a copy of the input grid to serve as the output grid.
2.  **Identify Borders:**
    a.  Check if the top row (row 0) consists of a single, non-white color (`color1`) AND the bottom row (last row) also consists of a single, non-white color (`color2`).
    b.  If yes, note that the borders are "horizontal", `border1_color` is `color1`, and `border2_color` is `color2`. Proceed to step 4.
    c.  If no, check if the left column (column 0) consists of a single, non-white color (`color1`) AND the right column (last column) also consists of a single, non-white color (`color2`).
    d.  If yes, note that the borders are "vertical", `border1_color` is `color1`, and `border2_color` is `color2`. Proceed to step 4.
    e.  If neither condition is met, return the unmodified input grid (or handle as an error case, though examples suggest borders are always present).
3.  **Iterate and Transform:** Go through each pixel `(r, c)` in the grid, *excluding* the border rows/columns identified in step 2.
4.  **Check Pixel Color:** If the color of the pixel `(r, c)` in the input grid is green (3):
    a.  **If Horizontal Borders:**
        i.  Calculate `distance1 = r` (distance to top row).
        ii. Calculate `distance2 = grid_height - 1 - r` (distance to bottom row).
        iii. If `distance1 <= distance2`, change the color of the pixel `(r, c)` in the *output* grid to `border1_color`.
        iv. Else (`distance1 > distance2`), change the color of the pixel `(r, c)` in the *output* grid to `border2_color`.
    b.  **If Vertical Borders:**
        i.  Calculate `distance1 = c` (distance to left column).
        ii. Calculate `distance2 = grid_width - 1 - c` (distance to right column).
        iii. If `distance1 <= distance2`, change the color of the pixel `(r, c)` in the *output* grid to `border1_color`.
        iv. Else (`distance1 > distance2`), change the color of the pixel `(r, c)` in the *output* grid to `border2_color`.
5.  **Return Output:** After checking all relevant pixels, return the modified output grid.