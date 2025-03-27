*   **Perception:** The task involves identifying a target subgrid within a larger input grid based on the locations of special marker pixels: white (0) and red (2). The output grid is a copy of this target subgrid.
    *   White pixels (0) form a rectangular block (possibly 1x1) which acts as a primary reference point and determines the size of the output grid.
    *   A single red pixel (2), if present, acts as a secondary marker, modifying the location calculation for the target subgrid relative to the white block.
    *   The location of the target subgrid is calculated based on the position of the white block and, if present, the position of the red pixel. The rules for calculating the target location depend on whether the red pixel exists and its column position relative to the white block.
    *   The output grid has the same dimensions as the white block.

*   **Facts:**
    
```yaml
    task_elements:
      - input_grid: 2D array of integers (colors)
      - output_grid: 2D array of integers (colors), a subgrid of the input
      - markers:
          - white_block:
              color: 0 (white)
              shape: contiguous rectangle (can be 1x1)
              function: Primary reference point, defines output size.
              properties: top_left_coord (wr, wc), dimensions (wh, ww)
          - red_pixel:
              color: 2 (red)
              shape: single pixel
              function: Secondary marker, modifies target location calculation.
              properties: location (rr, rc)
              presence: Optional (may not exist in all inputs)
      - target_subgrid:
          location: Calculated based on white_block and red_pixel positions.
          properties: top_left_coord (otr, otc), dimensions (wh, ww) determined by white_block.
          content: Copied directly from the input_grid at the calculated location.
    relationships_and_rules:
      - output_dimensions: Equal to the dimensions of the white_block (wh, ww).
      - target_location_calculation (otr, otc):
          - if red_pixel does not exist:
              otr = wr + 2
              otc = wc
          - if red_pixel exists at (rr, rc):
              otr = wr
              if rc < wc: # Red pixel is to the left of the white block
                otc = wc + 2 * (rc - wc)
              else: # Red pixel is in the same columns or to the right (rc >= wc)
                otc = rc
    ```


*   **Natural Language Program:**
    1.  Identify all white pixels (color 0) in the input grid. Determine the bounding box of these pixels, finding the top-left coordinate `(wr, wc)` and the dimensions `(wh, ww)` of this white block.
    2.  Search the input grid for a single red pixel (color 2). Record its coordinate `(rr, rc)` if found.
    3.  The dimensions of the output grid will be `wh x ww`.
    4.  Calculate the top-left coordinate `(otr, otc)` of the target subgrid within the input grid using the following rules:
        a.  If no red pixel was found: Set `otr = wr + 2` and `otc = wc`.
        b.  If a red pixel was found at `(rr, rc)`:
            i.  Set `otr = wr`.
            ii. If the red pixel's column `rc` is less than the white block's starting column `wc`, set `otc = wc + 2 * (rc - wc)`.
            iii. Otherwise (if `rc` is greater than or equal to `wc`), set `otc = rc`.
    5.  Extract the subgrid of size `wh x ww` starting from the calculated coordinate `(otr, otc)` in the input grid.
    6.  Return this extracted subgrid as the output.