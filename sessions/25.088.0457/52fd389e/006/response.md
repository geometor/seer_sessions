## General Assessment

The previous code failed because it incorrectly assumed that the triggering object must be a *solid* yellow rectangle. The examples show that the object is a contiguous group of yellow pixels which may contain "holes" filled with other colors. The transformation rule applies if these "holes" (internal pixels that are not yellow and not white) within the bounding box of the yellow component *all share the same color*. The number of these internal pixels determines the thickness of the border, and their shared color determines the border color.

The strategy is to:
1.  Correctly identify contiguous components of yellow pixels.
2.  Determine the bounding box for each yellow component.
3.  Identify all non-yellow, non-white pixels strictly *within* that bounding box.
4.  Verify if these internal pixels exist and all share a single color.
5.  If the condition is met, calculate the border thickness (count of internal pixels) and color (shared color of internal pixels).
6.  Draw the border by expanding the bounding box outwards by the calculated thickness, filling the new area with the border color.
7.  Ensure the original yellow pixels within the bounding box remain yellow in the final output.

## Metrics and Observations

**Example 1:**

*   **Input:** Contains two yellow components.
    *   Component 1 (Top): Bounding box (rows 2-4, cols 3-5). Contains 1 internal non-yellow/non-white pixel: Green (3) at (3,4).
    *   Component 2 (Bottom): Bounding box (rows 12-17, cols 11-17). Contains 4 internal non-yellow/non-white pixels: Red (2) at (13,13), (15,16), (16,12), (16,16).
*   **Expected Output:**
    *   Component 1: Gets a Green (3) border of thickness 1.
    *   Component 2: Gets a Red (2) border of thickness 4.
*   **Analysis:** The internal pixels for each component share a single color (Green for component 1, Red for component 2). The border thickness matches the count of internal pixels for each component.

**Example 2:**

*   **Input:** Contains two yellow components.
    *   Component 1 (Top): Bounding box (rows 2-7, cols 2-7). Contains 2 internal non-yellow/non-white pixels: Red (2) at (3,3) and (6,5).
    *   Component 2 (Bottom): Bounding box (rows 15-20, cols 13-20). Contains 3 internal non-yellow/non-white pixels: Blue (1) at (16,16), (18,14), (19,16).
*   **Expected Output:**
    *   Component 1: Gets a Red (2) border of thickness 2.
    *   Component 2: Gets a Blue (1) border of thickness 3.
*   **Analysis:** The internal pixels for each component share a single color (Red for component 1, Blue for component 2). The border thickness matches the count of internal pixels for each component.

**Example 3:**

*   **Input:** Contains two yellow components.
    *   Component 1 (Top): Bounding box (rows 2-5, cols 6-9). Contains 1 internal non-yellow/non-white pixel: Blue (1) at (3,7).
    *   Component 2 (Bottom): Bounding box (rows 12-19, cols 8-17). Contains 4 internal non-yellow/non-white pixels: Azure (8) at (13,10), (14,14), (16,11), (18,14).
*   **Expected Output:**
    *   Component 1: Gets a Blue (1) border of thickness 1.
    *   Component 2: Gets an Azure (8) border of thickness 4.
*   **Analysis:** The internal pixels for each component share a single color (Blue for component 1, Azure for component 2). The border thickness matches the count of internal pixels for each component.

## YAML Fact Sheet


```yaml
task_context:
  description: Draw a border around specific yellow structures based on internal pixels.
  input_grid: Represents a 2D space with colored pixels (0-9).
  output_grid: Input grid modified by adding colored borders around qualifying structures.

objects:
  - object: yellow_component
    description: A contiguous group of yellow (4) pixels (connected via 4-way adjacency). It may not form a solid rectangle.
    properties:
      - color: yellow (4)
      - coordinates: Set of (row, col) tuples for each yellow pixel in the component.
      - bounding_box: The minimum rectangle enclosing all pixels of the yellow component (min_row, min_col, max_row, max_col).
  - object: internal_pixel
    description: A pixel located within the bounding box of a yellow component that is NOT yellow (4) and NOT white (0).
    properties:
      - color: Any color except yellow (4) or white (0).
      - location: (row, col) coordinate within the yellow component's bounding box.
  - object: border
    description: A colored frame drawn around the bounding box of a qualifying yellow component.
    properties:
      - color: Determined by the shared color of the internal pixels of the associated yellow component.
      - thickness: Determined by the count of internal pixels of the associated yellow component.
      - location: The area between the original bounding box and an expanded bounding box.

actions:
  - action: identify_yellow_components
    description: Find all distinct contiguous groups of yellow pixels in the input grid.
    inputs: input_grid
    outputs: List of yellow_component objects (including their coordinates and bounding_box).
  - action: find_internal_pixels
    description: For a given yellow component's bounding box, find all pixels within that box that are neither yellow nor white.
    inputs: input_grid, bounding_box
    outputs: List of internal_pixel objects (including their color and location).
  - action: check_conditions_for_border
    description: Determine if a yellow component qualifies for a border.
    inputs: List of internal_pixels found for a yellow component.
    outputs: Boolean (True if internal pixels exist AND they all share the same color).
    conditions:
      - Must be at least one internal_pixel.
      - All internal_pixels must have the same color value.
  - action: calculate_border_properties
    description: Determine the color and thickness of the border.
    inputs: List of internal_pixels for a qualifying yellow component.
    outputs: border_color (the shared color), border_thickness (the count of internal pixels).
  - action: draw_border
    description: Modify the output grid to add the border.
    inputs: output_grid, bounding_box, border_color, border_thickness
    process:
      - Calculate the expanded bounding box by extending the original bounding box outwards by 'border_thickness'.
      - Fill pixels in the output_grid that are within the expanded bounding box but outside the original bounding box with the 'border_color'.
  - action: preserve_yellow_component
    description: Ensure the original yellow pixels of the component are retained in the output grid.
    inputs: output_grid, coordinates of the yellow_component
    process: Set the color of pixels at the yellow component's coordinates back to yellow (4). This handles cases where the border might overwrite parts of the component.

workflow:
  - Initialize output_grid as a copy of input_grid.
  - Identify all yellow_components in the input_grid.
  - Create a list to store components that qualify for a border and their border properties.
  - For each yellow_component:
    - Find its internal_pixels using its bounding_box.
    - Check if the component qualifies for a border based on its internal_pixels.
    - If it qualifies:
      - Calculate the border_color and border_thickness.
      - Store the component's bounding_box, original yellow coordinates, border_color, and border_thickness.
  - For each qualifying component (from the stored list):
    - draw_border onto the output_grid using its bounding_box, border_color, and border_thickness.
  - For each qualifying component (from the stored list):
    - preserve_yellow_component by setting its original yellow coordinates back to yellow (4) on the output_grid.
  - Return the final output_grid.

```


## Natural Language Program

1.  **Initialization**: Create an output grid as an exact copy of the input grid.
2.  **Identify Yellow Components**: Find all distinct, contiguous groups of yellow (4) pixels in the input grid using 4-way adjacency. For each component found:
    a.  Record the set of coordinates `(r, c)` for all yellow pixels belonging to this component.
    b.  Determine the minimal bounding box `(min_r, min_c, max_r, max_c)` that encloses all yellow pixels of this component.
3.  **Analyze Each Component**: For every identified yellow component and its bounding box:
    a.  **Find Internal Pixels**: Search within the component's bounding box `(min_r, min_c, max_r, max_c)` in the *input* grid. Identify all pixels whose color is *not* yellow (4) and *not* white (0). Record the color and coordinates of each such internal pixel found.
    b.  **Check Border Conditions**: Examine the list of internal pixels found for the component:
        i.  If no internal pixels were found, this component does not get a border. Proceed to the next component.
        ii. If internal pixels *were* found, check if they *all* share the exact same color.
        iii.If they do not all share the same color, this component does not get a border. Proceed to the next component.
    c.  **Qualify for Border**: If internal pixels exist and they all share the same single color (let's call this the `inner_color`), then this component qualifies for a border.
        i.  **Calculate Thickness**: The border thickness (`T`) is equal to the total *number* of internal pixels found for this component.
        ii. **Store Information**: Keep track of the component's original yellow pixel coordinates, its bounding box, the calculated `inner_color`, and the calculated thickness `T`.
4.  **Draw Borders**: After analyzing all yellow components, iterate through the list of *qualifying* components:
    a.  For each qualifying component, retrieve its bounding box `(min_r, min_c, max_r, max_c)`, `inner_color`, and thickness `T`.
    b.  **Calculate Expanded Box**: Determine the coordinates of an expanded bounding box by extending the original bounding box outwards by `T` pixels in all four directions (up, down, left, right). Ensure these coordinates stay within the grid boundaries (clamp at 0 and grid dimension minus 1). Let the expanded box be `(exp_min_r, exp_min_c, exp_max_r, exp_max_c)`.
    c.  **Fill Border Area**: Iterate through all coordinates `(r, c)` within the *expanded* bounding box. If a coordinate `(r, c)` falls *outside* the *original* bounding box (`r < min_r` or `r > max_r` or `c < min_c` or `c > max_c`), set the color of the pixel at `(r, c)` in the *output* grid to the `inner_color`.
5.  **Preserve Original Yellow**: After drawing all borders, iterate through the list of *qualifying* components again:
    a.  For each qualifying component, retrieve the set of its original yellow pixel coordinates.
    b.  For every coordinate `(r, c)` in this set, set the color of the pixel at `(r, c)` in the *output* grid back to yellow (4). This ensures the original yellow shape is preserved and corrects any pixels that might have been overwritten by a border.
6.  **Final Output**: Return the modified output grid.