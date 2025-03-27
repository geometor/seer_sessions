*   **Perception**
    *   The input is a 9x9 grid containing white (0), azure (8), and blue (1) pixels.
    *   The output is a smaller 3x3 grid containing only azure (8) and blue (1) pixels.
    *   The task involves identifying and extracting a specific 3x3 subgrid from the input grid based on its content.
    *   The relevant pixels for the transformation appear to be only azure (8) and blue (1). White (0) pixels seem to act as background or separators and are not part of the extracted output pattern.
    *   The input grid contains multiple potential 3x3 subgrids composed solely of azure and blue pixels.
    *   A selection criterion must exist to choose exactly one of these 3x3 subgrids to become the output.
    *   Comparing the number of blue (1) pixels within the valid 3x3 candidate subgrids appears to be the key selection criterion. The subgrid with the highest count of blue pixels is chosen.
    *   In case of a tie in the count of blue pixels, a positional tie-breaking rule (topmost, then leftmost) seems to be applied.

*   **Facts**
    
```yaml
    elements:
      - item: grid
        properties:
          - type: input
          - size: 9x9
          - colors: [white, azure, blue] # 0, 8, 1
      - item: grid
        properties:
          - type: output
          - size: 3x3
          - colors: [azure, blue] # 8, 1
      - item: subgrid
        properties:
          - definition: a 3x3 contiguous block of pixels within the input grid
          - category: candidate
            condition: contains only azure (8) and blue (1) pixels
          - attribute: blue_pixel_count
            definition: the number of blue (1) pixels within the subgrid
          - attribute: position
            definition: the row and column index of the top-left pixel of the subgrid
      - item: selection_criterion
        properties:
          - primary: maximize the blue_pixel_count among all candidate subgrids
          - tie_breaker_1: choose the subgrid with the minimum top-left row index
          - tie_breaker_2: choose the subgrid with the minimum top-left column index (if row indices are also tied)
    actions:
      - action: scan
        actor: system
        target: input grid
        details: Iterate through all possible 3x3 subgrids.
      - action: filter
        actor: system
        target: all 3x3 subgrids
        details: Keep only subgrids containing exclusively azure (8) and blue (1) pixels. These are the 'candidate' subgrids.
      - action: evaluate
        actor: system
        target: candidate subgrids
        details: For each candidate subgrid, count the number of blue (1) pixels and record its top-left position.
      - action: select
        actor: system
        target: candidate subgrids
        details: Choose the single candidate subgrid based on the selection_criterion (maximize blue count, then use positional tie-breakers).
      - action: extract
        actor: system
        target: selected subgrid
        details: Copy the selected 3x3 subgrid to form the output grid.
    ```


*   **Natural Language Program**
    1.  Initialize variables to keep track of the best candidate subgrid found so far: maximum blue pixel count (`max_blue_count` = -1), position of the best subgrid (`best_subgrid_pos` = None), and the content of the best subgrid (`best_subgrid` = None).
    2.  Iterate through all possible top-left starting positions (row `r`, column `c`) for a 3x3 subgrid within the input grid. The valid range for `r` is from 0 to `input_height - 3`, and for `c` is from 0 to `input_width - 3`.
    3.  For each position (`r`, `c`), extract the corresponding 3x3 subgrid.
    4.  Check if this 3x3 subgrid contains *only* azure (8) and blue (1) pixels. If it contains any other color (like white, 0), discard it and proceed to the next position.
    5.  If the subgrid contains only azure and blue pixels, count the number of blue (1) pixels within it (`current_blue_count`).
    6.  Compare `current_blue_count` with `max_blue_count`:
        *   If `current_blue_count` > `max_blue_count`, then this subgrid is the new best candidate. Update `max_blue_count` to `current_blue_count`, update `best_subgrid_pos` to (`r`, `c`), and store the content of this subgrid in `best_subgrid`.
        *   If `current_blue_count` == `max_blue_count`, apply the tie-breaking rule: Compare the current position (`r`, `c`) with `best_subgrid_pos`. If the current subgrid's position is "smaller" (first by row `r`, then by column `c`) than `best_subgrid_pos`, update `best_subgrid_pos` to (`r`, `c`) and update `best_subgrid` to the content of the current subgrid.
    7.  After iterating through all possible positions, the `best_subgrid` variable will hold the content of the 3x3 subgrid that satisfies the criteria.
    8.  Return `best_subgrid` as the output grid.