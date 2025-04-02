Okay, let's break down the task based on the provided examples.

**Perception of Elements:**

1.  **Input Grid Structure:** Both input grids consist of a white background (color 0) with several distinct, solid, horizontal rectangular blocks of different colors stacked vertically. The blocks may have different heights and widths and might not be perfectly aligned horizontally.
2.  **Output Grid Structure:** The output grids are the same size as the corresponding input grids and also contain a white background with the same set of colored rectangular blocks.
3.  **Key Change:** The primary change between input and output is the vertical arrangement of these colored blocks.
4.  **Pattern Observation (Example 1):**
    *   Input Order (Top to Bottom): Green (rows 1-2), Red (3-4), Yellow (5-6), Blue (7-8).
    *   Output Order (Top to Bottom): Blue (1-2), Red (3-4), Yellow (5-6), Green (7-8).
    *   Observation: The top block (Green) and the bottom block (Blue) have swapped vertical positions. The middle blocks (Red, Yellow) retain their positions relative to each other and the overall structure.
5.  **Pattern Observation (Example 2):**
    *   Input Order (Top to Bottom): Orange (rows 0-1), Red (2-3), Magenta (4-7), Green (8-11).
    *   Output Order (Top to Bottom): Green (0-3), Red (4-5), Magenta (6-9), Orange (10-11).
    *   Observation: Again, the top block (Orange) and the bottom block (Green) have swapped their positions in the vertical sequence. The intermediate blocks (Red, Magenta) maintain their relative order but shift vertically to accommodate the swapped blocks. The entire stack seems to be reconstructed based on the new top/bottom swap.

**YAML Facts:**


```yaml
task_description: Swaps the vertical positions of the top-most and bottom-most colored rectangular blocks within their vertical stack, reconstructing the stack accordingly.

definitions:
  background_color: 0 (white)
  object: A maximal, contiguous, horizontal rectangle of a single non-background color.

analysis:
  example_1:
    input_objects:
      - color: 3 (green)
        shape: {height: 2, width: 3}
        position: {top_row: 1, left_col: 3}
      - color: 2 (red)
        shape: {height: 2, width: 3}
        position: {top_row: 3, left_col: 3}
      - color: 4 (yellow)
        shape: {height: 2, width: 3}
        position: {top_row: 5, left_col: 3}
      - color: 1 (blue)
        shape: {height: 2, width: 3}
        position: {top_row: 7, left_col: 3}
    vertical_stack:
      order: [green, red, yellow, blue]
      top_row: 1
      bottom_row: 8
    output_stack:
      order: [blue, red, yellow, green] # Swap first and last
      reconstruction: blue(1-2), red(3-4), yellow(5-6), green(7-8) # Based on original heights

  example_2:
    input_objects:
      - color: 7 (orange)
        shape: {height: 2, width: 2}
        position: {top_row: 0, left_col: 4}
      - color: 2 (red)
        shape: {height: 2, width: 4}
        position: {top_row: 2, left_col: 3}
      - color: 6 (magenta)
        shape: {height: 4, width: 6}
        position: {top_row: 4, left_col: 2}
      - color: 3 (green)
        shape: {height: 4, width: 8}
        position: {top_row: 8, left_col: 1}
    vertical_stack:
      order: [orange, red, magenta, green]
      top_row: 0
      bottom_row: 11
    output_stack:
      order: [green, red, magenta, orange] # Swap first and last
      reconstruction: green(0-3), red(4-5), magenta(6-9), orange(10-11) # Based on original heights

transformation:
  - Identify all distinct colored rectangular blocks.
  - Determine their vertical order based on top row index.
  - Identify the overall vertical extent (top-most row to bottom-most row) of the stack of blocks.
  - Identify the top block (first in the vertical order) and the bottom block (last in the vertical order).
  - Swap these two blocks in the order sequence.
  - Reconstruct the stack vertically in the output grid:
    - Start at the original top row of the stack.
    - Place each block from the (potentially modified) sequence one below the other, using its original shape (height, width), color, and horizontal position (left column).
    - Ensure the background color fills the rest of the grid.
```


**Natural Language Program:**

1.  Identify all maximal rectangular blocks of non-white color in the input grid. For each block, record its color, height, width, top row index, and leftmost column index.
2.  Sort these identified blocks based on their top row index to get the vertical sequence of blocks.
3.  Determine the top row index of the first block in the sequence (`stack_top_row`).
4.  If there are two or more blocks in the sequence, swap the first block and the last block in the sequence.
5.  Create a new grid of the same dimensions as the input, filled entirely with the white background color.
6.  Initialize a variable `current_row` to `stack_top_row`.
7.  Iterate through the sequence of blocks (which may have had its first and last elements swapped in step 4):
    a.  For the current block, retrieve its recorded color, height, width, and leftmost column index.
    b.  Draw this block onto the new grid starting at `current_row` and its original leftmost column index, extending for its width and height.
    c.  Increment `current_row` by the height of the block just drawn.
8.  The new grid with the reconstructed stack of blocks is the output.