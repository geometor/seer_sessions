## Perception

1.  **Input/Output Structure:** The task takes an 11x11 grid as input and produces an 11x11 grid as output. The background color is predominantly orange (7).
2.  **Key Object:** The central feature in each input is a 3x3 area containing mostly green (3) pixels and a single red (2) pixel, typically near the center of the 3x3 area.
3.  **Variations:**
    *   **Magenta Border:** In Examples 1 and 2, the 3x3 green/red block is immediately surrounded by a border of magenta (6) pixels. In Example 3, this border is absent.
    *   **Maroon Pixels:** Maroon (9) pixels are present in all examples, sometimes scattered, sometimes clustered. Their presence and proximity to the central 3x3 block seem crucial.
4.  **Transformation Logic:** The core transformation modifies the colors within the 3x3 green/red block. The specific changes depend on two factors:
    *   The presence or absence of the magenta (6) border around the block.
    *   The proximity of any maroon (9) pixel to the block (or its border, if present).
5.  **Secondary Transformations:**
    *   In Example 3 (no border), isolated maroon (9) pixels (those with no maroon neighbors) are changed to orange (7).
    *   In Example 1 (border present, no adjacent maroon), a single magenta (6) pixel, seemingly outside the main border but adjacent to maroon pixels, changes to orange (7). This might be a separate sub-rule or related to the maroon adjacency check.

## YAML Facts


```yaml
task_context:
  grid_size: fixed 11x11 for both input and output.
  primary_colors:
    - orange (7): Background, generally static.
    - green (3): Forms a 3x3 block with red. Target of modification.
    - red (2): Single pixel within the green block. Target of modification.
    - magenta (6): Forms an optional border around the green/red block. Can change under specific conditions.
    - maroon (9): Appears scattered. Acts as a conditional trigger and can change under specific conditions.
objects:
  - object: central_block
    description: A 3x3 area composed primarily of green (3) pixels and a single red (2) pixel.
    properties:
      - location: [row, column] of the top-left corner.
      - red_pixel_location: [row, column] of the red (2) pixel within the block.
      - has_magenta_border: boolean, indicates if the block is immediately surrounded by magenta (6) pixels.
  - object: maroon_pixels
    description: Pixels with value 9.
    properties:
      - locations: list of [row, column] coordinates.
      - is_adjacent_to_block: boolean, indicates if any maroon pixel is adjacent (including diagonals) to the central_block or its magenta border (if present).
      - is_isolated: boolean, indicates if a maroon pixel has no neighbours (including diagonals) of the same color (maroon).
  - object: magenta_pixels
    description: Pixels with value 6.
    properties:
      - locations: list of [row, column] coordinates.
      - part_of_border: boolean, indicates if the pixel belongs to the immediate border around the central_block.
relationships:
  - type: adjacency
    description: Determines if pixels are next to each other horizontally, vertically, or diagonally. Used for checking maroon proximity and isolation, and defining the magenta border.
  - type: relative_position
    description: Used to identify pixels relative to the red pixel within the central_block (e.g., top-left, above, left).
actions:
  - action: identify_block_and_properties
    description: Locate the 3x3 green/red block, find the red pixel, and determine if a magenta border exists.
  - action: check_maroon_adjacency
    description: Determine if any maroon pixel is adjacent to the block or its border.
  - action: modify_block_case_border_present
    description: Change pixels within the block based on maroon adjacency.
      - if adjacent maroon: Change all green (3) and the red (2) to maroon (9).
      - if no adjacent maroon: Change specific green (3) pixels (relative to red pixel) to maroon (9).
  - action: modify_block_case_border_absent
    description: Change pixels within the block based on relative position to the original red pixel location. Change red (2) to green (3).
  - action: modify_isolated_maroons
    description: Change isolated maroon (9) pixels to orange (7) (only when no magenta border is present).
  - action: modify_stray_magentas (potential)
    description: Change magenta (6) pixels not part of the border but adjacent to maroon (9) to orange (7) (only when magenta border is present and no maroon is adjacent to the block).
```


## Natural Language Program

1.  **Identify** the 3x3 region containing predominantly green (3) pixels and exactly one red (2) pixel (the `central_block`). Record the location `[r, c]` of the red pixel.
2.  **Determine** if the `central_block` is immediately surrounded by a solid border of magenta (6) pixels (`has_magenta_border`).
3.  **Check** if any maroon (9) pixel in the input grid is adjacent (horizontally, vertically, or diagonally) to any pixel belonging to the `central_block` or its surrounding magenta border (if `has_magenta_border` is true). Record this as `is_maroon_adjacent`.
4.  **If `has_magenta_border` is true:**
    *   **If `is_maroon_adjacent` is true:** Change the color of all green (3) pixels and the single red (2) pixel within the `central_block` to maroon (9).
    *   **If `is_maroon_adjacent` is false:** Change the color of the two green (3) pixels located at grid coordinates `[r-1, c-1]` and `[r-1, c]` to maroon (9). Additionally, find any magenta (6) pixel that is *not* part of the immediate border defined in step 2 but *is* adjacent to any maroon (9) pixel, and change its color to orange (7).
5.  **If `has_magenta_border` is false:**
    *   Iterate through the green (3) pixels within the `central_block`:
        *   If a green pixel's row index is less than `r`, change its color to maroon (9).
        *   If a green pixel's row index is equal to `r` and its column index is less than `c`, change its color to maroon (9).
    *   Change the color of the pixel at `[r, c]` (originally red) to green (3).
    *   Identify all maroon (9) pixels in the input grid. For each maroon pixel, check if it has any adjacent (including diagonal) neighbours that are also maroon (9). If a maroon pixel has *no* maroon neighbours, change its color to orange (7).
6.  **Copy** all other pixels from the input grid to the output grid without changing their color.