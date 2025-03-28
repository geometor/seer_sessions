*   **Perception of task elements:**
    *   The input grids are 11x11.
    *   The input grids contain mostly white (0) pixels.
    *   Each input grid contains exactly one green (3) pixel.
    *   Some input grids (Examples 2 and 3) also contain scattered red (2) pixels. Example 1 does not contain any red pixels.
    *   The output grid generally preserves the structure and non-green pixels of the input grid, except where modification occurs.
    *   The core transformation involves replacing the single green pixel with a larger, fixed 9x9 pattern representing the digit "3", drawn using green pixels.
    *   This green "3" pattern is centered exactly where the original green pixel was located in the input grid.
    *   The pixel at the center of the pattern (where the original green pixel was) becomes white (0) in the output.
    *   The drawn green "3" pattern overwrites any existing pixels (including red pixels) that fall within its 9x9 bounding box.
    *   There's a conditional modification: In Example 1, where the input grid *only* contained the single green pixel (and white pixels), the entire bottom row (row 10) of the output grid is filled with green (3). In Examples 2 and 3, where other non-white (red) pixels were present in the input, the bottom row remains unchanged from the input (except if the pattern itself were to overlap it, which it doesn't in these examples).

*   **YAML Facts:**
    
```yaml
    GridProperties:
      - Size: 11x11 (in examples)
      - BackgroundColor: White (0)

    Objects:
      - Name: TriggerPixel
        Color: Green (3)
        Count: 1 per input grid
        Location: Variable (e.g., (4,5), (5,5), (4,4))
      - Name: ObstaclePixel
        Color: Red (2)
        Count: Variable (0 or more)
        Location: Scattered, preserved unless overwritten
      - Name: StampPattern
        Shape: Digit "3"
        Size: 9x9 pixels
        Color: Green (3) on White (0) background
        CenterValue: White (0) # The location of the original TriggerPixel becomes White

    Actions:
      - Find: Locate the coordinates (row, col) of the TriggerPixel (Green 3).
      - Define: Specify the fixed 9x9 StampPattern relative to its center.
      - Copy: Initialize the output grid as a copy of the input grid.
      - Place: Draw the StampPattern onto the output grid, centered at the TriggerPixel's location.
      - Overwrite: Pixels within the StampPattern's 9x9 area in the output grid are replaced by the pattern's pixels.
      - ConditionCheck: Determine if the TriggerPixel was the *only* non-white pixel in the *input* grid.
      - ConditionalFill: If the ConditionCheck is true, fill the last row of the output grid with Green (3).

    Relationships:
      - Centering: The StampPattern is placed centered on the TriggerPixel's original location.
      - OverwritingRule: The StampPattern takes precedence over any pixels (ObstaclePixels or BackgroundColor) within its placement area.
      - ConditionalRule: The filling of the last row depends entirely on whether non-white pixels other than the single TriggerPixel existed in the input grid.
    ```


*   **Natural Language Program:**
    1.  Identify the location (row `r`, column `c`) of the single green pixel (color 3) in the input grid.
    2.  Define a fixed 9x9 pixel pattern representing the digit "3". This pattern consists of green pixels (3) and white pixels (0). Crucially, the pixel at the center of this 9x9 pattern (relative coordinates (4, 4)) should be white (0).
    3.  Create a new grid for the output, initially making it an exact copy of the input grid.
    4.  Determine the 9x9 area on the output grid centered at (`r`, `c`). This area spans from row `r-4` to `r+4` and column `c-4` to `c+4`.
    5.  For each position within this 9x9 area on the output grid, replace the current pixel with the corresponding pixel from the defined 9x9 "3" pattern (making sure to align the pattern's center with (`r`, `c`)). This effectively draws the "3" pattern and sets the pixel at (`r`, `c`) to white (0), overwriting any previous content.
    6.  Examine the original input grid. Count the number of non-white pixels.
    7.  If the count of non-white pixels in the input grid is exactly 1 (meaning only the single green trigger pixel was present), modify the output grid by setting all pixels in the last row to green (3).
    8.  If the count of non-white pixels in the input grid was greater than 1, make no further changes to the last row (it remains as set by steps 3 and 5).
    9.  Return the modified output grid.