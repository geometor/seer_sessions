
## train_1

**input:**
```
0 0 0 5 0 0 0 5 0 0 0
0 3 0 5 0 1 0 5 0 4 0
0 0 0 5 0 0 0 5 0 0 0
```


**output:**
```
8 8 8 5 6 6 6 5 9 9 9
8 8 8 5 6 6 6 5 9 9 9
8 8 8 5 6 6 6 5 9 9 9
```


## train_2

**input:**
```
0 0 0 5 0 0 0 5 0 0 0
0 2 0 5 0 3 0 5 0 1 0
0 0 0 5 0 0 0 5 0 0 0
```


**output:**
```
7 7 7 5 8 8 8 5 6 6 6
7 7 7 5 8 8 8 5 6 6 6
7 7 7 5 8 8 8 5 6 6 6
```


## train_3

**input:**
```
0 0 0 5 0 0 0 5 0 0 0
0 4 0 5 0 1 0 5 0 2 0
0 0 0 5 0 0 0 5 0 0 0
5 5 5 5 5 5 5 5 5 5 5
0 0 0 5 0 0 0 5 0 0 0
0 2 0 5 0 3 0 5 0 4 0
0 0 0 5 0 0 0 5 0 0 0
```


**output:**
```
9 9 9 5 6 6 6 5 7 7 7
9 9 9 5 6 6 6 5 7 7 7
9 9 9 5 6 6 6 5 7 7 7
5 5 5 5 5 5 5 5 5 5 5
7 7 7 5 8 8 8 5 9 9 9
7 7 7 5 8 8 8 5 9 9 9
7 7 7 5 8 8 8 5 9 9 9
```


## train_4

**input:**
```
0 0 0 5 0 0 0 5 0 0 0
0 1 0 5 0 2 0 5 0 1 0
0 0 0 5 0 0 0 5 0 0 0
```


**output:**
```
6 6 6 5 7 7 7 5 6 6 6
6 6 6 5 7 7 7 5 6 6 6
6 6 6 5 7 7 7 5 6 6 6
```

*   **Perception:**
    *   The input grids contain vertical gray lines (color 5) which act as separators, dividing the grid horizontally into sections.
    *   In some examples (like train\_3), there are also horizontal gray lines that divide the grid vertically into independent regions.
    *   Within each section defined by the vertical separators (and potentially bounded by horizontal separators or grid edges), there is exactly one non-white (color 0), non-gray pixel.
    *   The output grids preserve the gray lines from the input.
    *   The areas/sections between the gray lines (and within horizontal regions if present) are filled entirely with a new color in the output.
    *   The fill color for each section in the output is determined by the color of the single non-white, non-gray pixel found in the corresponding section of the input.
    *   There is a consistent mapping between the input pixel color and the output fill color across all examples.

*   **Color Mapping:**
    *   Blue (1) in input maps to Magenta (6) in output.
    *   Red (2) in input maps to Orange (7) in output.
    *   Green (3) in input maps to Azure (8) in output.
    *   Yellow (4) in input maps to Maroon (9) in output.
    *   This mapping follows the rule: `output_color = input_color + 5`.

*   **Transformation Process:**
    1.  Identify all gray pixels (color 5). These form horizontal and vertical separators.
    2.  Treat horizontal gray lines as complete dividers, creating independent horizontal regions.
    3.  Within each horizontal region (or the entire grid if no horizontal separators exist):
        *   Identify the vertical sections based on the vertical gray lines (and grid boundaries).
        *   For each vertical section:
            *   Find the single pixel that is not white (0) and not gray (5). Let its color be `C_in`.
            *   Calculate the target fill color `C_out = C_in + 5`.
            *   In the output grid, fill all cells within this vertical section (and the current horizontal region) that are not gray separators with the color `C_out`.
    4.  Copy all gray pixels from the input to the output in their original positions.

*   **Facts:**
    
```yaml
    observations:
      - object: grid
        description: Input and output are 2D grids of pixels.
      - object: separators
        description: Gray pixels (color 5) act as separators.
        properties:
          - type: vertical
            function: Divide the grid (or horizontal regions) into vertical sections.
          - type: horizontal
            function: Divide the grid into independent horizontal regions.
        persistence: Gray separators are preserved in the output grid.
      - object: sections
        description: Areas defined by vertical separators (and grid boundaries), potentially within horizontal regions.
        properties:
          - content_input: Each section contains exactly one non-white, non-gray pixel and potentially white pixels.
          - content_output: Each section is filled with a single color, excluding the separator pixels.
      - pattern: color_mapping
        description: The fill color of an output section depends on the color of the unique non-white, non-gray pixel in the corresponding input section.
        rule: output_color = input_color + 5
        examples:
          - input: 1 (blue)
            output: 6 (magenta)
          - input: 2 (red)
            output: 7 (orange)
          - input: 3 (green)
            output: 8 (azure)
          - input: 4 (yellow)
            output: 9 (maroon)
      - transformation: fill
        description: Areas corresponding to input sections are filled in the output.
        details:
          - Identify horizontal regions defined by horizontal gray lines.
          - Within each region, identify vertical sections defined by vertical gray lines.
          - Find the unique colored pixel (not 0 or 5) in each input section.
          - Calculate the output color using the color_mapping rule.
          - Fill the corresponding output section (excluding gray pixels) with the calculated output color.
          - Preserve all gray pixels.
    ```


*   **Natural Language Program:**
    1.  Create an output grid of the same dimensions as the input grid, initially empty or filled with a temporary value.
    2.  Copy all gray pixels (color 5) from the input grid to their corresponding positions in the output grid.
    3.  Identify the row indices of any horizontal gray lines (rows filled entirely with gray). These define boundaries of horizontal regions. Add the top (index -1) and bottom (index = grid height) boundaries.
    4.  Identify the column indices of any vertical gray lines. These define boundaries of vertical sections. Add the left (index -1) and right (index = grid width) boundaries.
    5.  Iterate through each horizontal region defined by consecutive horizontal boundary indices (row_start, row_end).
    6.  Within each horizontal region, iterate through each vertical section defined by consecutive vertical boundary indices (col_start, col_end).
    7.  Search within the current input grid block defined by `rows[row_start+1 : row_end]` and `columns[col_start+1 : col_end]` to find the single pixel whose color (`C_in`) is not white (0) and not gray (5).
    8.  If such a pixel is found, calculate the output color `C_out = C_in + 5`.
    9.  Fill the corresponding block in the output grid (`rows[row_start+1 : row_end]`, `columns[col_start+1 : col_end]`) with `C_out`, but only modifying cells that are not already marked as gray separators (from step 2).
