*   **Perception of Task Elements:**
    1.  The input and output grids are the same size (10x10).
    2.  The transformation primarily affects specific 3x3 patterns within the grid. Other areas remain unchanged.
    3.  The key pattern is a 3x3 square where the 8 surrounding 'frame' pixels are all of one color (let's call it Frame Color, F) and the central pixel is of a different color (Center Color, C). White (0) pixels are ignored when determining the frame color; the frame pixels must all be the *same* non-white color F.
    4.  Based on the specific pair of (Center Color C, Frame Color F), one of two actions occurs:
        *   **Removal:** The entire 3x3 area (center and frame) is replaced with white (0) pixels.
        *   **Center Color Change:** Only the center pixel's color is changed to a new color (N). The frame pixels remain untouched.
    5.  The transformation rules seem consistent across all examples, defined by a specific mapping for (C, F) pairs.
    6.  Objects or patterns not matching this 3x3 frame/center structure are preserved (e.g., the gray L-shape in example 1, the gray structure in example 2, the gray 'plus' signs in example 3).

*   **Facts:**
    
```yaml
    objects:
      - type: grid
        description: A 2D array of pixels with colors 0-9.
      - type: pattern
        description: A 3x3 area within the grid.
        properties:
          - center_pixel: The pixel at the geometric center of the 3x3 area.
          - frame_pixels: The 8 pixels surrounding the center pixel.
          - center_color: The color (C) of the center_pixel (must be non-white).
          - frame_color: The color (F) of all frame_pixels (must be non-white, the same for all 8, and different from C).
      - type: background
        description: white pixels (color 0) or pixels not part of identified patterns.

    actions:
      - name: identify_patterns
        description: Scan the input grid to find all instances of the 3x3 pattern described above.
      - name: remove_pattern
        description: Replace all 9 pixels of an identified 3x3 pattern with white (0).
        condition: Triggered by specific (Center Color, Frame Color) pairs.
      - name: change_center_color
        description: Change the color of the center pixel of an identified 3x3 pattern to a new color (N).
        condition: Triggered by specific (Center Color, Frame Color) pairs, resulting in a specific new color N.
      - name: preserve
        description: Pixels not part of a modified pattern remain unchanged.

    relationships:
      - type: mapping
        description: Defines the action based on the (Center Color C, Frame Color F) pair of an identified pattern.
        rule_set_remove: # Pairs (C, F) that trigger removal
          - [6, 2] # Magenta center, Red frame
          - [2, 3] # Red center, Green frame
          - [8, 4] # Azure center, Yellow frame
          - [2, 4] # Red center, Yellow frame
          - [3, 1] # Green center, Blue frame
          - [3, 4] # Green center, Yellow frame
          - [6, 3] # Magenta center, Green frame
          - [9, 2] # Maroon center, Red frame
        rule_set_change: # Pairs (C, F) that trigger center change to N
          - C: 4 # Yellow
            F: 1 # Blue
            N: 8 # Azure
          - C: 3 # Green
            F: 8 # Azure
            N: 2 # Red
          - C: 4 # Yellow
            F: 3 # Green
            N: 2 # Red
          - C: 1 # Blue
            F: 6 # Magenta
            N: 3 # Green
          - C: 2 # Red
            F: 1 # Blue
            N: 9 # Maroon
          - C: 4 # Yellow
            F: 7 # Orange
            N: 3 # Green

    ```


*   **Natural Language Program:**
    1.  Initialize the output grid as a copy of the input grid.
    2.  Iterate through each possible center pixel location (r, c) in the input grid, excluding the borders (i.e., where 0 < r < height-1 and 0 < c < width-1).
    3.  For each potential center (r, c), get its color C. If C is white (0), continue to the next center.
    4.  Check the 8 neighboring pixels (the frame) around (r, c).
    5.  Determine if all 8 neighbors have the *exact same* non-white color F, and ensure that F is different from the center color C (F != C).
    6.  If such a pattern is found (a non-white center C surrounded by a uniform, non-white frame F, where C != F):
        a.  Consult the predefined mapping rules for the pair (C, F).
        b.  If the pair (C, F) exists in the `rule_set_remove` mapping: Mark the 3x3 area centered at (r, c) in the output grid to be changed to white (0).
        c.  If the pair (C, F) exists in the `rule_set_change` mapping: Find the corresponding new center color N. Mark the center pixel (r, c) in the output grid to be changed to color N.
    7.  After checking all potential centers, apply the marked changes to the output grid. (This avoids issues if patterns overlap, although they don't appear to in the examples). Specifically, first apply all color changes to center pixels, then apply all removals (setting 3x3 areas to white). If a center pixel was marked for change and also part of an area marked for removal, the removal takes precedence for that pixel.
    8.  Return the modified output grid.