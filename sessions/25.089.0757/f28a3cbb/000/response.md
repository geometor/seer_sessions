*   **Perception:** The input grids contain distinct 3x3 square blocks of color in the top-left and bottom-right corners. The rest of the grid is primarily filled with a third, dominant "background" color, interspersed with scattered pixels matching the corner block colors or other colors. The transformation involves expanding the corner blocks and cleaning up the rest of the grid. The top-left block expands one column to the right. The bottom-right block expands one row upwards. All pixels in the output grid that are not part of these expanded corner blocks take on the background color. The background color appears to be the most frequent color in the input grid, excluding the colors of the two corner blocks.

*   **Facts:**
    
```yaml
    - task: Grid transformation
    - examples: 2
    - grid_size:
        input: 9x9
        output: 9x9
    - elements:
        - type: solid_block
          location: top-left corner (0,0)
          size: 3x3
          color: variable (Maroon in ex1, Red in ex2)
          property: represents top-left object (TL_object)
        - type: solid_block
          location: bottom-right corner (H-1, W-1)
          size: 3x3
          color: variable (Yellow in ex1, Gray in ex2)
          property: represents bottom-right object (BR_object)
        - type: background
          color: variable (Magenta in both examples)
          property: determined by frequency analysis (most frequent excluding corner block colors)
        - type: scattered_pixels
          color: same as TL_object or BR_object, or other colors
          location: distributed across the grid outside corner blocks
    - actions:
        - identify: TL_object color (TL_color) from input[0,0]
        - identify: BR_object color (BR_color) from input[H-1, W-1]
        - identify: background color (BG_color) by finding the most frequent color in the input grid, excluding TL_color and BR_color.
        - initialize: output grid with the same dimensions as input, filled with BG_color.
        - expand_and_fill: TL_object area in output grid to cover rows 0-2 and columns 0-3 with TL_color.
        - expand_and_fill: BR_object area in output grid to cover rows H-4 to H-1 and columns W-3 to W-1 with BR_color.
    - relationships:
        - TL_object expands rightwards by one column.
        - BR_object expands upwards by one row.
        - All other pixels become the background color.
    ```


*   **Natural Language Program:**
    1.  Determine the dimensions (Height H, Width W) of the input grid.
    2.  Identify the color of the top-left pixel (input[0,0]) as the Top-Left Color (TL_Color).
    3.  Identify the color of the bottom-right pixel (input[H-1, W-1]) as the Bottom-Right Color (BR_Color).
    4.  Count the frequency of each color in the input grid. Determine the Background Color (BG_Color) as the color with the highest frequency, excluding TL_Color and BR_Color.
    5.  Create a new output grid of the same dimensions (H x W) and fill it entirely with the BG_Color.
    6.  Fill the rectangular region from row 0 to row 2 and from column 0 to column 3 in the output grid with TL_Color.
    7.  Fill the rectangular region from row H-4 to row H-1 and from column W-3 to column W-1 in the output grid with BR_Color.
    8.  Return the modified output grid.