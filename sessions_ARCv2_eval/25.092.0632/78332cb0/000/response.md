**Perception**

1.  **Input Structure:** The input grids contain multiple distinct rectangular subgrids (segments). These segments appear to be consistently 5x5 pixels in size across the examples.
2.  **Separators:** The segments in the input are separated by lines (rows or columns) composed entirely of the magenta color (6). The background color within the segments is orange (7).
3.  **Content:** Each segment contains a shape made of a single color (other than magenta or orange) placed on the orange background.
4.  **Transformation Goal:** The task is to rearrange these segments from the input grid into a new configuration in the output grid, using the same magenta color as a separator between the rearranged segments.
5.  **Arrangement Rules:** The rearrangement logic depends on how the segments are arranged in the input:
    *   **Input 2x2 Grid (train_1):** If the input has segments arranged in a 2x2 grid (separated by one magenta row and one magenta column), the output stacks these segments vertically. The order of stacking is specific: top-left, bottom-right, top-right, bottom-left. Magenta rows are used as separators in the output.
    *   **Input Vertical Stack (train_2):** If the input segments are stacked vertically (separated by magenta rows), the output arranges them horizontally. The order is reversed compared to the input (bottom segment becomes leftmost, top segment becomes rightmost). Magenta columns are used as separators in the output.
    *   **Input Horizontal Row (train_3):** If the input segments are arranged horizontally (separated by magenta columns), the output stacks them vertically. The order is preserved (left segment becomes topmost, right segment becomes bottommost). Magenta rows are used as separators in the output.
6.  **Output Structure:** The output grid consists of the extracted segments rearranged according to the specific rule, with single magenta lines (rows or columns) separating them.

**Facts**


```yaml
elements:
  - role: separator
    color: magenta (6)
    form: lines (full rows or full columns)
  - role: background
    color: orange (7)
    location: within segments
  - role: segment
    description: Rectangular subgrids extracted from the input, defined by the magenta separators.
    properties:
      size: Consistently 5x5 in examples.
      content: Contains an orange background and a shape of a single distinct color.
  - role: shape
    description: Contiguous group of pixels of the same color (not magenta or orange) within a segment.

relationships:
  - type: separation
    entity1: segment
    entity2: segment
    via: separator (magenta lines)
  - type: containment
    container: segment
    contained:
      - background (orange)
      - shape

transformations:
  - action: identify_layout
    input: input grid
    criteria: arrangement of magenta separators (rows, columns, or both)
    output: layout type (2x2 grid, vertical stack, horizontal row)
  - action: extract_segments
    input: input grid, separator locations
    output: list of segments (subgrids)
  - action: reassemble_segments
    input: list of segments, layout type
    rules:
      - if layout == 2x2 grid:
          order: top-left, bottom-right, top-right, bottom-left
          arrangement: vertical stack
          separator: magenta row
      - if layout == vertical stack:
          order: reversed input order
          arrangement: horizontal row
          separator: magenta column
      - if layout == horizontal row:
          order: same as input order
          arrangement: vertical stack
          separator: magenta row
    output: output grid
```


**Natural Language Program**

1.  **Identify Separators:** Scan the input grid to find complete rows and columns consisting solely of the magenta color (6).
2.  **Determine Input Layout:**
    *   If both a magenta row and a magenta column are found, identify the layout as '2x2 grid'.
    *   If only magenta rows are found, identify the layout as 'vertical stack'.
    *   If only magenta columns are found, identify the layout as 'horizontal row'.
3.  **Extract Segments:** Based on the locations of the magenta separators, extract the rectangular subgrids (segments) located between them. Store these segments along with their original positions (e.g., top-left, top-right, bottom-left, bottom-right for 2x2; top, middle, bottom for vertical; left, middle, right for horizontal).
4.  **Rearrange Segments:**
    *   **If the input layout was '2x2 grid':** Create a new grid by stacking the segments vertically in the following order: top-left, bottom-right, top-right, bottom-left. Insert a single row of magenta pixels between each pair of stacked segments.
    *   **If the input layout was 'vertical stack':** Create a new grid by arranging the segments horizontally. The order must be reversed from the input order (e.g., bottom segment first, then middle, then top). Insert a single column of magenta pixels between each pair of horizontally arranged segments.
    *   **If the input layout was 'horizontal row':** Create a new grid by stacking the segments vertically. The order must be the same as the input order (e.g., left segment first, then middle, then right). Insert a single row of magenta pixels between each pair of stacked segments.
5.  **Return Output Grid:** The newly constructed grid is the final output.