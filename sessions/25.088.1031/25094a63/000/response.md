**Perception of the Elements:**

1.  **Input/Output Grids:** Both input and output are 30x30 grids containing pixels of various colors (integers 0-9).
2.  **Transformation:** The output grid is largely identical to the input grid, except that specific rectangular regions within the input have their color changed to yellow (4) in the output.
3.  **Changed Regions:** The regions that change appear to be contiguous rectangular blocks composed of a single, non-white color in the input.
4.  **Selection Criteria:** Not *all* single-color rectangular blocks are changed. Comparing the changed blocks across examples suggests a selection criterion based on size. Specifically, for each color present in the input (excluding white - 0), the *largest* contiguous rectangular block of that color (by area) seems to be the one targeted for transformation.
5.  **Modification:** The selected largest rectangular block for each relevant color is entirely filled with yellow (4) in the output grid, replacing its original color. All other pixels remain unchanged.

**Facts (YAML):**


```yaml
elements:
  - element: grid
    properties:
      - height: 30
      - width: 30
      - pixels: variety of colors (0-9)
  - element: rectangular_block
    description: A contiguous rectangular area within the grid composed of a single color.
    properties:
      - color: The single color filling the block (value 1-9).
      - location: Defined by top-left corner (row, column).
      - dimensions: height and width.
      - area: height * width.
      - maximality: The block cannot be extended further in any direction while maintaining the single color and rectangular shape.
objects:
  - object: target_block
    definition: For each distinct color C (1-9) present in the input grid, the maximal rectangular_block of color C that has the largest area compared to all other maximal rectangular_blocks of the same color C.
actions:
  - action: identify_colors
    description: Find all unique colors (1-9) present in the input grid.
  - action: find_maximal_rectangles
    description: For a given color, find all maximal contiguous rectangular blocks of that color in the input grid.
  - action: calculate_area
    description: Compute the area (height * width) for each identified rectangular block.
  - action: find_largest_rectangle_per_color
    description: For each color identified, determine which of its maximal rectangular blocks has the largest area. Select this block as the target_block for that color.
  - action: recolor_block
    description: Change the color of all pixels within a specified rectangular block to a target color.
    parameters:
      - block: The rectangular block to modify (defined by location and dimensions).
      - target_color: The new color to fill the block with (yellow - 4).
relationships:
  - relationship: input_output_correspondence
    description: The output grid is initially identical to the input grid.
  - relationship: modification_trigger
    description: A rectangular block in the input grid is modified in the output grid only if it is the target_block (largest area rectangle) for its specific color.
transformation:
  - step: Copy the input grid to create the initial output grid.
  - step: Identify the set of unique non-white colors present in the input grid.
  - step: For each unique color found:
      - Find all maximal contiguous rectangular blocks of that color.
      - Calculate the area of each block.
      - Select the block with the maximum area for this color.
  - step: For each selected largest block (one per color):
      - Recolor the corresponding region in the output grid to yellow (4).
```


**Natural Language Program:**

1.  Initialize the `output_grid` as an identical copy of the `input_grid`.
2.  Find all unique colors present in the `input_grid`, excluding white (0). Let this set be `unique_colors`.
3.  Create an empty list called `largest_blocks` to store information about the largest rectangle found for each color.
4.  For each `color` in `unique_colors`:
    a.  Scan the `input_grid` to find all maximal contiguous rectangular blocks composed entirely of this `color`.
    b.  If no blocks are found for this `color`, continue to the next color.
    c.  Calculate the area (height * width) for each block found.
    d.  Determine the maximum area among these blocks.
    e.  Identify the block (or one of the blocks, if there's a tie in area) that has this maximum area. Record its top-left corner coordinates (`row`, `col`), `height`, and `width`.
    f.  Add this information (`color`, `row`, `col`, `height`, `width`) to the `largest_blocks` list.
5.  Iterate through each entry (`color`, `row`, `col`, `height`, `width`) in the `largest_blocks` list.
6.  For the current entry, modify the `output_grid`: For all pixels from row `r` = `row` to `r` = `row + height - 1`, and column `c` = `col` to `c` = `col + width - 1`, set the pixel value to yellow (4).
7.  Return the final `output_grid`.