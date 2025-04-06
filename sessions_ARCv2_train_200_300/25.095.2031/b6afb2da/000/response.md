**Perception of the Elements:**

The task involves transforming a 2D grid of integers. The input grid consists of the digits 0 and 5. The digit 5 appears in solid rectangular blocks, while 0 represents the background. The output grid replaces these blocks of 5s with new patterns using digits 1, 2, and 4, while preserving the locations of the 0s.

The transformation rule appears to operate locally on each rectangular block of 5s independently. Within each block, the transformation depends on the position of a cell relative to the block's boundaries:
- Cells at the corners of a block are transformed to 1.
- Cells along the edges of a block (but not corners) are transformed to 4.
- Cells in the interior of a block are transformed to 2.
- Background cells (0) remain 0.

**Facts:**


```yaml
grid_dimensions:
  rows: 10
  columns: 10
input_elements:
  - value: 0
    role: background
  - value: 5
    role: object_component
objects:
  - type: rectangle
    composed_of: input_element 5
    properties:
      - solid_fill
output_elements:
  - value: 0
    role: background
  - value: 1
    role: object_corner
  - value: 2
    role: object_interior
  - value: 4
    role: object_edge (non-corner)
transformation:
  - scope: grid
  - preserves_zeros: True
  - identifies_objects: Finds connected rectangular blocks of '5's.
  - maps_objects: Replaces each '5' within a block based on its relative position.
    position_mapping:
      - relative_position: corner
        output_value: 1
      - relative_position: edge (excluding corners)
        output_value: 4
      - relative_position: interior
        output_value: 2
```


**Natural Language Program:**

1.  **Initialize Output Grid:** Create an output grid of the same dimensions as the input grid, initially filled with zeros.
2.  **Identify Blocks:** Scan the input grid to find all distinct rectangular blocks composed entirely of the digit 5. Determine the minimum and maximum row and column indices for each block.
3.  **Process Each Block:** For each identified rectangular block of 5s:
    a.  Iterate through every cell (row `r`, column `c`) within the block's boundaries (from min row to max row, and min col to max col).
    b.  **Check Position:** Determine the position of the cell (`r`, `c`) relative to the block's boundaries:
        i.  If the cell is one of the four corners of the block, set the corresponding cell in the output grid to 1.
        ii. Else if the cell is on one of the four edges of the block (but not a corner), set the corresponding cell in the output grid to 4.
        iii. Else (the cell is in the interior of the block), set the corresponding cell in the output grid to 2.
4.  **Return Output:** The final output grid contains the transformed blocks (with 1s, 2s, and 4s) and the original background 0s.