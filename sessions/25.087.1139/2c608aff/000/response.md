*   **Perception:**
    *   The input grids contain a background color, a large central object (usually rectangular), and one or more small "agent" pixels of different colors.
    *   The background color appears to be the most frequent color in the grid.
    *   The large object is typically the largest contiguous block of non-background color.
    *   The agent pixels seem to "drip" or extend towards the large object along cardinal axes (up, down, left, right).
    *   This dripping action changes the color of the background pixels along the path to the agent pixel's color.
    *   The dripping stops when the path reaches the boundary of the large object.
    *   Agent pixels only drip if they are aligned (share a row or column) with the bounding box of the large object and have a clear path of background pixels towards it. Agent pixels not aligned or whose path is blocked or leads away from the object do not drip.

*   **YAML Facts:**
    
```yaml
    background_color:
      property: Most frequent color in the input grid.
      role: Medium through which agents move; potentially modified.
    largest_contiguous_object (LCO):
      property: Largest connected component of pixels with the same non-background color.
      property: Often rectangular.
      role: Acts as a barrier or target for agent movement. Remains unchanged itself.
    agent_pixels:
      property: Pixels whose color is neither the background nor the LCO color.
      property: Often single pixels, but could potentially be small objects.
      role: Initiate the dripping/painting action.
      relationship: Position relative to the LCO determines drip direction.
      relationship: Must be aligned (share row or column) with the LCO's bounding box to activate.
    action:
      type: Dripping/Path Painting
      actor: Agent pixels
      target: Background pixels
      condition: Agent pixel is aligned with LCO bounding box (vertically or horizontally).
      direction: Towards the LCO along the axis of alignment (up, down, left, or right).
      effect: Changes background pixels along the path to the agent pixel's color.
      termination: Stops when the path reaches the pixel adjacent to the LCO.
    grid:
      property: Contains background, LCO, and agent pixels.
      transformation: Modified by changing background pixels along drip paths.
    ```


*   **Natural Language Program:**
    1.  Identify the background color by finding the most frequent pixel color in the input grid.
    2.  Find all contiguous objects (connected components) of non-background colors. Identify the largest one (by pixel count) as the Largest Contiguous Object (LCO). Determine the bounding box (minimum/maximum row/column) of the LCO.
    3.  Identify all pixels ("agent pixels") whose color is neither the background color nor the color of the LCO.
    4.  Create a copy of the input grid to serve as the output grid.
    5.  For each agent pixel at position (row `r`, column `c`) with color `agent_color`:
        a.  **Check Vertical Alignment:** If the agent pixel's column `c` is within the LCO's column range (`min_col_LCO <= c <= max_col_LCO`):
            i.  If the agent pixel is above the LCO (`r < min_row_LCO`): Check the path downwards from `(r + 1, c)` to `(min_row_LCO - 1, c)`. If all pixels in this path have the background color, change the color of these pixels in the output grid to `agent_color`.
            ii. If the agent pixel is below the LCO (`r > max_row_LCO`): Check the path upwards from `(r - 1, c)` to `(max_row_LCO + 1, c)`. If all pixels in this path have the background color, change the color of these pixels in the output grid to `agent_color`.
        b.  **Check Horizontal Alignment:** If the agent pixel's row `r` is within the LCO's row range (`min_row_LCO <= r <= max_row_LCO`):
            i.  If the agent pixel is to the left of the LCO (`c < min_col_LCO`): Check the path rightwards from `(r, c + 1)` to `(r, min_col_LCO - 1)`. If all pixels in this path have the background color, change the color of these pixels in the output grid to `agent_color`.
            ii. If the agent pixel is to the right of the LCO (`c > max_col_LCO`): Check the path leftwards from `(r, c - 1)` to `(r, max_col_LCO + 1)`. If all pixels in this path have the background color, change the color of these pixels in the output grid to `agent_color`.
    6.  Return the modified output grid.