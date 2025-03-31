**Perception of Elements:**

1.  **Objects:** The primary objects are 3x3 blocks of uniform, non-white color.
2.  **Background:** The background is white (0).
3.  **Separators:** Single rows or columns of pixels separate the 3x3 blocks. These separators can be white (0) or a non-white color (e.g., Yellow(4), Gray(5), Orange(7)).
4.  **Arrangement:** The 3x3 blocks are consistently arranged in groups of four, forming a larger 2x2 pattern (Top-Left, Top-Right, Bottom-Left, Bottom-Right). Let's label these A, B, C, D respectively.
5.  **Interaction:** The transformation rule depends entirely on the nature of the separators (vertical and horizontal) between the four blocks in a group.

**YAML Facts:**


```yaml
task_elements:
  - element: Grid
    properties:
      - Contains 3x3 blocks of non-white color.
      - Contains white background pixels (0).
      - Contains single-pixel-width separator rows/columns.
  - element: 3x3 Block
    properties:
      - Uniform, non-white color.
      - Always size 3x3.
    grouping:
      - Arranged in groups of four (2x2 pattern).
      - Let the blocks in a group be A(TL), B(TR), C(BL), D(BR).
  - element: Separator
    properties:
      - Single pixel width (row or column).
      - Located between the four blocks in a group.
      - Can be white (0) or non-white (colored).
    relationships:
      - Vertical Separator: Between A/C and B/D.
      - Horizontal Separator: Between A/B and C/D.
transformation_logic:
  - condition: Vertical separator is non-white, Horizontal separator is white.
    action: Swap colors horizontally.
    details: Block A gets color of B, B gets color of A. Block C gets color of D, D gets color of C.
  - condition: Horizontal separator is non-white, Vertical separator is white.
    action: Swap colors vertically.
    details: Block A gets color of C, C gets color of A. Block B gets color of D, D gets color of B.
  - condition: Both Vertical and Horizontal separators are white.
    action: Propagate unique color.
    details: Find the counts of each color among blocks A, B, C, D. If one color is unique (count=1), change all four blocks (A, B, C, D) to that unique color.
unchanged_elements:
  - Background pixels (white).
  - Separator pixels (both white and non-white).
```


**Natural Language Program:**

1.  Identify all groups of four 3x3 non-white blocks arranged in a 2x2 super-structure (Top-Left A, Top-Right B, Bottom-Left C, Bottom-Right D) within the input grid. These groups are separated by a single column (between A/C and B/D) and a single row (between A/B and C/D).
2.  For each identified group of four blocks:
    a.  Determine the color of the vertical separator column and the horizontal separator row.
    b.  **If the vertical separator is a non-white color AND the horizontal separator is white (0):** The transformation rule is a horizontal color swap. In the output grid, block A takes the original color of block B, block B takes the original color of block A, block C takes the original color of block D, and block D takes the original color of block C.
    c.  **If the horizontal separator is a non-white color AND the vertical separator is white (0):** The transformation rule is a vertical color swap. In the output grid, block A takes the original color of block C, block C takes the original color of block A, block B takes the original color of block D, and block D takes the original color of block B.
    d.  **If both the vertical and horizontal separators are white (0):** The transformation rule is unique color propagation. Count the occurrences of each distinct color present in the four blocks (A, B, C, D). Identify the color that appears exactly once. In the output grid, change the color of all four blocks (A, B, C, D) to this unique color.
3.  Copy all other pixels (background white pixels and the separator pixels themselves) from the input grid to the output grid without modification.
4.  The final output grid contains the modified block colors and the unchanged background/separator pixels.