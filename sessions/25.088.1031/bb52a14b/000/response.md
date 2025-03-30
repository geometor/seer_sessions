**Perception**

1.  **Grid Structure:** The input and output are grids of the same size (22x22 in the examples).
2.  **Color Palette:** The grids primarily use white (0), blue (1), and azure (8). Yellow (4) appears distinctively within specific 3x3 patterns.
3.  **Core Transformation:** The transformation involves identifying a specific 3x3 pattern (the "source") in the input and copying it to a different location (the "destination") in the output grid. The original pixels at the destination are overwritten.
4.  **Source Pattern Identification:** In each example, there is exactly one 3x3 block that contains the color yellow (4). This unique block serves as the source pattern to be copied. The specific arrangement of colors within this source pattern varies between examples.
5.  **Destination Pattern Identification:** The destination location is identified by finding a 3x3 block that matches one of two specific predefined patterns.
    *   Pattern A: `[[1, 0, 1], [0, 8, 0], [0, 0, 1]]` (Seen in `train_1` and `train_2`)
    *   Pattern B: `[[8, 0, 0], [8, 0, 1], [0, 0, 0]]` (Seen in `train_3`)
    It appears that in any given input grid, exactly one instance of either Pattern A or Pattern B will exist, marking the destination.
6.  **Consistency:** Apart from the copy-paste operation, the rest of the grid remains unchanged between input and output.

**Facts**


```yaml
objects:
  - type: grid
    description: A 2D array of pixels with integer values 0-9 representing colors. Input and output grids have the same dimensions.
  - type: pattern
    subtype: 3x3_block
    description: A contiguous 3x3 region of pixels within the grid.
    attributes:
      - location: top-left coordinate (row, column).
      - content: 2D array of 9 pixel values.
properties:
  - property: contains_yellow
    applies_to: 3x3_block
    definition: The block contains at least one pixel with the value 4 (yellow).
  - property: matches_target_pattern_A
    applies_to: 3x3_block
    definition: The block's content exactly matches [[1, 0, 1], [0, 8, 0], [0, 0, 1]].
  - property: matches_target_pattern_B
    applies_to: 3x3_block
    definition: The block's content exactly matches [[8, 0, 0], [8, 0, 1], [0, 0, 0]].
relationships:
  - relationship: uniqueness
    applies_to: 3x3_block
    conditions:
      - In each input grid, there is exactly one 3x3 block that `contains_yellow`. This is the "source_block".
      - In each input grid, there is exactly one 3x3 block that either `matches_target_pattern_A` or `matches_target_pattern_B`. This is the "destination_block".
actions:
  - action: find_source_block
    input: input_grid
    output: source_block (content and location)
    description: Iterate through all possible 3x3 blocks in the input grid and identify the unique block that `contains_yellow`.
  - action: find_destination_block
    input: input_grid
    output: destination_block (location)
    description: Iterate through all possible 3x3 blocks in the input grid and identify the unique block that `matches_target_pattern_A` or `matches_target_pattern_B`.
  - action: copy_paste_block
    input:
      - source_block_content
      - destination_block_location
      - input_grid
    output: output_grid
    description: Create a copy of the input grid. Overwrite the 3x3 area starting at the `destination_block_location` with the `source_block_content`.
```


**Natural Language Program**

1.  **Define Target Patterns:** Define two constant 3x3 patterns:
    *   Target Pattern A: `[[1, 0, 1], [0, 8, 0], [0, 0, 1]]`
    *   Target Pattern B: `[[8, 0, 0], [8, 0, 1], [0, 0, 0]]`
2.  **Find Source Block:** Iterate through all possible top-left coordinates (row `r`, column `c`) for a 3x3 block within the input grid's boundaries. For each 3x3 block starting at `(r, c)`:
    *   Check if any pixel within the block has the value 4 (yellow).
    *   If it contains yellow, store this block's content (as a 3x3 array) as the `source_pattern` and its top-left coordinate `(r, c)` as the `source_location`. Assume there will be only one such block.
3.  **Find Destination Block:** Iterate through all possible top-left coordinates (row `r`, column `c`) for a 3x3 block within the input grid's boundaries. For each 3x3 block starting at `(r, c)`:
    *   Compare the block's content to Target Pattern A. If it matches, store its top-left coordinate `(r, c)` as the `destination_location`.
    *   Compare the block's content to Target Pattern B. If it matches, store its top-left coordinate `(r, c)` as the `destination_location`.
    *   Assume exactly one match (either A or B) will be found across the entire grid.
4.  **Create Output Grid:** Initialize the output grid as an identical copy of the input grid.
5.  **Perform Copy:** Using the `destination_location` found in Step 3 and the `source_pattern` found in Step 2, overwrite the 3x3 region in the output grid starting at `destination_location` with the pixels from the `source_pattern`.
6.  **Return Output:** The modified grid is the final output.