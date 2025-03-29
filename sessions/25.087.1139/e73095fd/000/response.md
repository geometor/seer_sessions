*   **Perception:**
    *   The input grids contain a background of white (0) pixels and various shapes constructed from gray (5) pixels.
    *   These gray shapes often form closed boundaries or walls.
    *   The output grids are largely identical to the input grids, except that certain areas of white (0) pixels within the input have been changed to yellow (4) pixels in the output.
    *   The gray shapes (5) themselves remain unchanged between input and output.
    *   The transformation specifically targets white (0) pixels that are fully enclosed or surrounded by gray (5) pixels. White pixels that have a path to the grid's edge without crossing a gray pixel remain white.

*   **Facts:**
    
```yaml
    task_description: Fill enclosed white regions with yellow.
    elements:
      - object: background
        color: white (0)
        role: Canvas, potential fill area.
      - object: boundaries
        color: gray (5)
        shape: Variable, often forming closed loops or walls.
        role: Define enclosed regions.
        persistence: Unchanged between input and output.
      - object: fill_color
        color: yellow (4)
        role: Used to fill enclosed regions in the output.
    actions:
      - action: identify_enclosed_regions
        input: grid
        target: white (0) pixels
        condition: Pixels must be completely surrounded by gray (5) pixels, meaning they cannot reach the grid boundary without crossing a gray pixel.
      - action: fill_regions
        input: identified enclosed white regions
        output: Regions changed to yellow (4) pixels.
        color_change: white (0) -> yellow (4)
    relationships:
      - The gray (5) pixels define the boundaries for the fill action.
      - Only white (0) pixels inside these boundaries are affected.
      - White (0) pixels outside these boundaries or connected to the grid edge remain unchanged.
    ```


*   **Natural Language Program:**
    1.  Identify all contiguous regions of white (0) pixels in the input grid.
    2.  For each white region, determine if it is fully enclosed by gray (5) pixels. A region is considered enclosed if none of its pixels can reach any edge of the grid by moving only through adjacent (up, down, left, right) white pixels without crossing a gray pixel.
    3.  Create the output grid by copying the input grid.
    4.  For every identified enclosed white region, change the color of all pixels within that region from white (0) to yellow (4) in the output grid.
    5.  Leave all other pixels (gray pixels and non-enclosed white pixels) unchanged.