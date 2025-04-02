*   **Perception:**
    *   The task involves transforming grids based on vertical column interactions.
    *   Each example features columns containing pixels of a certain "primary" color (blue in example 1, yellow in example 2) mixed with white background pixels.
    *   Within some of these columns, there's a single pixel of a specific "trigger" color (green in example 1, orange in example 2).
    *   The transformation rule seems to operate independently on each column.
    *   If a column contains both a primary color and its corresponding trigger color, the primary color pixels located at or above the topmost trigger pixel in that column are changed to the trigger color.
    *   Primary color pixels below the topmost trigger pixel remain unchanged.
    *   If a column contains only the primary color (and background) but no trigger color, the primary color pixels remain unchanged.
    *   The background (white) pixels and the original trigger pixels remain unchanged.
    *   There appears to be a specific mapping between primary and trigger colors: blue (1) maps to green (3), and yellow (4) maps to orange (7).

*   **Facts:**
    
```yaml
    task_type: grid_transformation
    grid_properties:
      size: ثابت (input and output grids have the same dimensions)
      background_color: white (0)
    objects:
      - type: pixel
        properties:
          - color: (0-9, representing specific colors)
          - position: (row, column)
      - type: column
        properties:
          - pixels: a vertical sequence of pixels sharing the same column index
          - contains_primary_color: boolean (e.g., contains blue=1 or yellow=4)
          - contains_trigger_color: boolean (e.g., contains green=3 or orange=7)
          - topmost_trigger_row: integer (row index of the highest trigger pixel, if any)
    color_relationships:
      - primary: blue (1)
        trigger: green (3)
      - primary: yellow (4)
        trigger: orange (7)
    transformation:
      scope: operates independently on each column
      action: color_change
      condition: A column contains both a primary color and its corresponding trigger color.
      rule:
        if condition is true:
          for each pixel in the column:
            if pixel.color == primary_color and pixel.row <= topmost_trigger_row:
              change pixel.color to trigger_color
            else:
              pixel.color remains unchanged
        else: # condition is false (no trigger color in the column)
          all pixels in the column remain unchanged
    ```


*   **Natural Language Program:**
    1.  Iterate through each column of the input grid independently.
    2.  For the current column, determine if it contains any blue (1) pixels. If yes, check if it also contains any green (3) pixels.
    3.  If the column contains both blue and green pixels:
        a.  Find the row index of the topmost green pixel in that column.
        b.  For every pixel in that column: if its color is blue and its row index is less than or equal to the topmost green pixel's row index, change its color to green. Otherwise, leave its color unchanged.
    4.  For the current column, determine if it contains any yellow (4) pixels. If yes, check if it also contains any orange (7) pixels.
    5.  If the column contains both yellow and orange pixels:
        a.  Find the row index of the topmost orange pixel in that column.
        b.  For every pixel in that column: if its color is yellow and its row index is less than or equal to the topmost orange pixel's row index, change its color to orange. Otherwise, leave its color unchanged.
    6.  If a column contains blue pixels but no green pixels, or yellow pixels but no orange pixels, or only background/other colors, leave all pixels in that column unchanged.
    7.  Construct the output grid using the potentially modified pixels.