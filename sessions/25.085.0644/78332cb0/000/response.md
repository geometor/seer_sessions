*   **Perception:** The task involves rearranging blocks of pixels within a grid. The input grids contain distinct rectangular blocks separated by lines of a specific color (magenta, 6). The arrangement and orientation of these blocks change between the input and output.
*   **Segmentation:** Magenta (6) lines, either horizontal rows or vertical columns that span the grid, act as separators, dividing the input grid into smaller rectangular subgrids (blocks).
*   **Transformation:** The core operation is to extract these blocks and reassemble them in a new configuration.
*   **Orientation Change:** The orientation of the separators in the input determines the orientation of the assembly in the output.
    *   If the input has only horizontal magenta separators, the blocks are arranged horizontally in the output, separated by vertical magenta lines.
    *   If the input has only vertical magenta separators, the blocks are stacked vertically in the output, separated by horizontal magenta lines.
    *   If the input has both horizontal and vertical magenta separators (forming a grid of blocks), the blocks are stacked vertically in the output, separated by horizontal magenta lines.
*   **Ordering:** The order in which blocks are reassembled depends on the initial segmentation:
    *   Input with only horizontal separators: Blocks are ordered from bottom to top (reverse order of appearance).
    *   Input with only vertical separators: Blocks are ordered from left to right (normal order of appearance).
    *   Input with both horizontal and vertical separators (a 2x2 arrangement): Blocks are ordered specifically as Top-Left, Bottom-Right, Top-Right, Bottom-Left.
*   **Separators:** The magenta lines used for separation in the input are reused in the output, but their orientation changes (horizontal becomes vertical, vertical becomes horizontal). A single row or column of magenta is used between blocks in the output.


```yaml
facts:
  - item: grid
    attributes:
      - contains_pixels: yes
      - pixels_have_colors: yes, 0-9
      - background_color: orange (7) is common but not universal
      - foreground_objects: contiguous blocks of non-background color
  - item: separator
    attributes:
      - color: magenta (6)
      - shape: horizontal row or vertical column spanning the grid
      - function: divides the grid into distinct rectangular subgrids (blocks)
  - item: block
    attributes:
      - shape: rectangular subgrid
      - location: defined by separator lines
      - content: pixels forming patterns, typically surrounded by a background color (like orange 7)
  - process: transformation
    actions:
      - identify_separators: find all full rows and columns of magenta (6) pixels.
      - determine_segmentation_type: check if separators are horizontal, vertical, or both.
      - extract_blocks: isolate the rectangular subgrids defined by the separators, excluding the separators themselves. Keep track of original position (e.g., row/column index or TL/TR/BL/BR label for 2x2 case).
      - determine_output_orientation:
        - if input separators are horizontal only, output orientation is horizontal.
        - if input separators are vertical only, output orientation is vertical.
        - if input separators are both, output orientation is vertical.
      - determine_block_order:
        - if output is horizontal (input was horizontal): order blocks by decreasing original row index (bottom-up).
        - if output is vertical (input was vertical): order blocks by increasing original column index (left-to-right).
        - if output is vertical (input was both): order blocks by sequence TL, BR, TR, BL based on original position.
      - assemble_output:
        - create a new grid.
        - place the blocks in the determined order and orientation.
        - insert separators between blocks:
          - if output is vertical, insert a single horizontal row of magenta (6) pixels between blocks.
          - if output is horizontal, insert a single vertical column of magenta (6) pixels between blocks.
```



```plaintext
natural_language_program:
1.  Identify the separator color, which is magenta (6).
2.  Scan the input grid to find all full horizontal rows and full vertical columns composed entirely of the separator color.
3.  Determine the type of segmentation based on the separators found: "horizontal", "vertical", or "both".
4.  Extract the rectangular subgrids (blocks) located between the separators. Record the original position of each block (e.g., its row and column index in the grid of blocks).
5.  Determine the orientation for arranging blocks in the output grid:
    a. If the segmentation type is "horizontal", the output orientation is horizontal.
    b. If the segmentation type is "vertical" or "both", the output orientation is vertical.
6.  Determine the order of the extracted blocks for assembly:
    a. If the output orientation is horizontal (input segmentation was "horizontal"), order the blocks by their original row index in descending order (bottom-most block first).
    b. If the output orientation is vertical and the input segmentation was "vertical", order the blocks by their original column index in ascending order (left-most block first).
    c. If the output orientation is vertical and the input segmentation was "both" (forming a 2x2 grid of blocks: Top-Left, Top-Right, Bottom-Left, Bottom-Right), order the blocks in the specific sequence: Top-Left, Bottom-Right, Top-Right, Bottom-Left.
7.  Construct the output grid:
    a. If the output orientation is vertical, stack the ordered blocks vertically, placing a single horizontal row of the separator color (magenta 6) between each adjacent pair of blocks.
    b. If the output orientation is horizontal, arrange the ordered blocks horizontally, placing a single vertical column of the separator color (magenta 6) between each adjacent pair of blocks.
```