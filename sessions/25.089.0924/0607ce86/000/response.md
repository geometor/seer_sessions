## Perception of Task Elements

1.  **Input/Output Structure:** Both input and output are 2D grids of colored pixels (integers 0-9). The dimensions are preserved.
2.  **Key Objects:** The inputs contain multiple distinct rectangular or block-like structures. These structures are composed of various colors and often appear in repeating patterns across the grid. They are separated by the background color (white/0).
3.  **Noise/Imperfections:** Within these block structures, there are often 'incorrect' pixels – colors that deviate from the main pattern of the block. Additionally, there are scattered, isolated non-background pixels outside of these main structures.
4.  **Transformation:** The core transformation involves identifying the repeating block structures, 'cleaning' them by correcting the internal imperfections to match a consistent pattern for that block type, and removing all non-background pixels that are not part of these identified blocks.
5.  **Pattern Standardization:** The output grid contains 'perfected' versions of the block structures found in the input. All instances of a particular block type look identical in the output, suggesting a template-based correction.
6.  **Background:** The background color (white/0) acts as a separator and also replaces all the 'noise' pixels outside the main blocks.

## YAML Fact Sheet


```yaml
Context:
  Task_Type: Noise removal and pattern standardization.
  Grid_Properties: Input and output grids have the same dimensions. Background color is white (0).

Objects:
  - Type: Rectangular Blocks
    Properties:
      - Composed of multiple colors.
      - Appear as distinct units separated by the background color.
      - Have a recognizable internal pattern.
      - Occur multiple times in the input grid, often arranged grid-like.
      - Contain 'imperfections' or 'noise' (pixels deviating from the standard pattern) in the input.
    Examples:
      - Train_1: Blocks with rows of [1, 1, 2, 3, 3] and a bottom row of [8, 8, 8, 8, 8].
      - Train_2: Blocks with rows of [6, 6, 6, 6, 6, 6] and [8, 8, 3, 3, 8, 8].
      - Train_3: Blocks with patterns involving colors 1 (blue), 2 (red), and 3 (green).

  - Type: Noise Pixels
    Properties:
      - Non-background pixels located *outside* the main Rectangular Blocks.
      - Non-background pixels located *inside* the main Rectangular Blocks but deviating from the block's standard pattern.

Actions:
  - Identify: Locate all instances of the repeating Rectangular Block patterns in the input grid.
  - Standardize: Determine the 'canonical' or 'template' pattern for each type of Rectangular Block identified (likely based on the most frequent pixel value at each relative position within observed instances).
  - Clean/Correct: Replace the pixels within each identified block in the input with the pixels from its corresponding canonical template.
  - Remove: Replace all Noise Pixels (both internal to blocks before correction and external) with the background color (white/0).

Relationships:
  - Spatial: Blocks are separated by the background color. Noise pixels can be internal or external to blocks.
  - Transformation: Input blocks (with noise) map to output blocks (standardized templates). Input noise pixels map to background color in the output.

Goal: Produce an output grid containing only the standardized versions of the Rectangular Blocks found in the input, positioned correctly, with all other areas set to the background color.
```


## Natural Language Program

1.  Initialize an output grid with the same dimensions as the input grid, filled entirely with the background color (white/0).
2.  Analyze the input grid to identify all distinct, repeating rectangular block patterns. Note their dimensions and internal color arrangements. These patterns are separated by the background color.
3.  For each distinct block pattern identified, determine its canonical or 'template' form. This template represents the 'clean' version of the block, likely derived from the most common pixel color found at each relative position across all observed instances of that block type in the input.
4.  Scan the input grid to find the top-left coordinate of every occurrence of any identified block pattern (even the noisy/imperfect versions).
5.  For each identified block occurrence at a specific coordinate in the input:
    a.  Retrieve the corresponding canonical template pattern determined in step 3.
    b.  Copy this template pattern onto the output grid, starting at the same top-left coordinate.
6.  Return the completed output grid.