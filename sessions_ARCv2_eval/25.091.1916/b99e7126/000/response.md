**Perception**

1.  **Grid Structure:** The input and output grids are large (29x29 in all examples) and exhibit a clear, repeating structure. They are composed of 4x4 blocks. Each 4x4 block consists of a 3x3 inner pattern surrounded by a 1-pixel border.
2.  **Repeating Blocks:** The grid is tiled with these 4x4 blocks. The border color (separating the 3x3 patterns) is consistent within each grid (red in examples 1 & 2, blue in example 3).
3.  **Pattern Types:** Within each grid, there are typically two distinct 3x3 patterns present:
    *   A "base" or "default" pattern that appears most frequently.
    *   One or more instances of a "variant" pattern.
4.  **Transformation:** The core transformation involves the "variant" pattern influencing adjacent "base" patterns. Specifically, if a block containing the base pattern shares a side (horizontally or vertically, not diagonally) with a block containing the variant pattern in the *input* grid, that base pattern block is replaced by the variant pattern block in the *output* grid.
5.  **Propagation:** This replacement seems to be a single-step process based on the initial configuration. Blocks that change from base to variant do not immediately trigger further changes in the same step.
6.  **Invariance:** The border pixels remain unchanged throughout the transformation.

**Facts (YAML)**


```yaml
grid_properties:
  structure: Tiled grid of 4x4 blocks.
  block_composition: Each 4x4 block has a 1-pixel border and a 3x3 inner pattern.
  border_color: Consistent within each example (e.g., red=2, blue=1). Remains unchanged in output.
objects:
  - type: PatternBlock
    description: A 4x4 section of the grid, consisting of a 3x3 pattern and its surrounding 1-pixel border.
  - type: BasePattern
    description: The most frequently occurring 3x3 pattern within the grid's blocks.
    example_1: [[4,4,4],[4,1,4],[4,4,4]] (yellow/blue)
    example_2: [[8,8,8],[3,8,3],[8,8,8]] (azure/green)
    example_3: [[4,2,4],[2,4,2],[4,2,4]] (yellow/red)
  - type: VariantPattern
    description: A 3x3 pattern that differs from the BasePattern, present in one or more blocks in the input.
    example_1: [[3,1,3],[3,1,3],[3,3,3]] (green/blue)
    example_2: [[1,8,1],[1,1,1],[1,8,1]] (blue/azure)
    example_3: [[4,8,4],[8,8,8],[8,4,8]] (yellow/azure)
relationships:
  - type: Adjacency
    description: Two PatternBlocks are adjacent if they share a horizontal or vertical side (sharing only a corner does not count).
action:
  - type: PatternReplacement
    description: If a BasePattern block is adjacent to a VariantPattern block in the input grid, the BasePattern block's 3x3 pattern is replaced by the VariantPattern's 3x3 pattern in the output grid.
    condition: Adjacency between BasePattern block and VariantPattern block (based on input state).
    target: The 3x3 area of the BasePattern block.
    result: The target area becomes identical to the VariantPattern's 3x3 area.
constraints:
  - Border pixels are never modified.
  - The replacement is based solely on the input grid's configuration.
```


**Natural Language Program**

1.  Initialize the output grid as a copy of the input grid.
2.  Identify the dimensions of the input grid and confirm it follows a 4x4 block structure (3x3 pattern + 1 border).
3.  Determine the border color by examining pixels at grid indices like (0,0), (0,4), (4,0), etc.
4.  Extract all unique 3x3 patterns present within the 4x4 blocks (excluding the border pixels).
5.  Count the occurrences of each unique 3x3 pattern. Identify the most frequent pattern as the "Base Pattern" and any other pattern(s) as the "Variant Pattern". (Assume only one type of Variant Pattern exists for propagation).
6.  Create a conceptual map of the grid, representing each 4x4 block and noting whether it contains the Base Pattern or the Variant Pattern in the *input* grid.
7.  Iterate through each 4x4 block location (e.g., by the top-left corner coordinates like (r, c) where r and c are multiples of 4) in the conceptual map.
8.  For each block that contains the Base Pattern:
    a.  Check its four orthogonal neighbors (up, down, left, right) in the *input* conceptual map.
    b.  If any of these neighbors contains the Variant Pattern:
        i.  Locate the 3x3 area corresponding to the current Base Pattern block in the *output* grid.
        ii. Replace this 3x3 area in the *output* grid with the 3x3 Variant Pattern.
9.  Return the modified output grid.