## Perception

1.  **Input Grid Structure:** The input grids typically consist of a repeating background pattern covering most of the grid.
2.  **Noise Elements:** Superimposed onto this background pattern are one or more solid, monochromatic rectangular blocks ("noise blocks") using colors distinct from the background pattern. These blocks overwrite the underlying pattern.
3.  **Output Grid Structure:** The output grid is a rectangular subgrid extracted from the input.
4.  **Content Preservation:** The output grid contains only colors belonging to the input's background pattern; the colors from the "noise blocks" are excluded.
5.  **Extraction Logic:** The output seems to be a "clean" sample of the background pattern, extracted from the top-left region of the input grid.
6.  **Size Determination:** The dimensions (height H, width W) of the output grid appear to be determined by the dimensions of the largest "noise block" (the one with the greatest area) found in the input. Specifically:
    *   The output height matches the height of the largest noise block.
    *   The output width matches the width of the largest noise block *unless* that block is not square, in which case the output width is one less than the block's width.
7.  **Position Determination:** The extraction point (top-left corner) for the output subgrid seems to correspond to the top-left starting point of the fundamental repeating unit of the background pattern within the input grid (e.g., (0,0) or (1,1)).

## Facts


```yaml
elements:
  - role: background
    description: A repeating pattern of pixels forming the base layer of the input grid.
    properties:
      - composed_of: specific set of colors (e.g., {3,4,5,6} in ex1; {0,1,2} in ex2; {4,5,6} in ex3)
      - structure: typically a small rectangular unit repeated across the grid
  - role: noise
    description: Solid, monochromatic rectangular blocks overlaying the background pattern.
    properties:
      - shape: rectangle
      - content: single color, distinct from background colors
      - size: variable (e.g., 5x6, 7x7 in ex1; 10x10, 6x6 in ex2; 3x3, 6x6, 6x13 in ex3)
      - count: one or more per input grid
  - role: output_grid
    description: The target grid generated from the input.
    properties:
      - content: subset of the input grid's background pattern
      - origin: extracted from the top-left region of the input grid
      - size: determined by the largest noise block in the input

relationships:
  - type: determines_size
    source: largest noise block (by area)
    target: output_grid
    details: >
      Let the largest noise block have dimensions H x W.
      Output height is H.
      Output width is W if H == W (block is square).
      Output width is W - 1 if H != W (block is not square).
  - type: determines_content
    source: background pattern
    target: output_grid
    details: The output grid is composed solely of pixels matching the background pattern colors.
  - type: determines_location
    source: background pattern start coordinate
    target: output_grid extraction point
    details: The top-left corner for extracting the output subgrid corresponds to the top-left corner (r_start, c_start) where the repeating unit of the background pattern begins in the input grid.

actions:
  - IdentifyNoiseBlocks: Find all maximal monochromatic rectangular regions larger than 1x1.
  - IdentifyLargestNoiseBlock: Select the noise block with the maximum area (height * width).
  - CalculateOutputDimensions: Compute the target H_out and W_out based on the largest noise block's dimensions and shape (square vs. non-square).
  - FindPatternStart: Determine the (r_start, c_start) coordinates of the top-left instance of the background pattern's repeating unit.
  - ExtractSubgrid: Copy the portion of the input grid from `input[r_start : r_start + H_out, c_start : c_start + W_out]`.
```


## Natural Language Program

1.  Analyze the input grid to identify all distinct maximal monochromatic rectangular blocks larger than 1x1 (these are the "noise blocks"). Keep track of their colors, locations, and dimensions (height H, width W).
2.  Determine the set of "noise colors" used by these blocks. All other colors present in the grid are considered "background colors".
3.  Calculate the area (H * W) for each identified noise block.
4.  Find the noise block with the largest area. Let its dimensions be H_max x W_max.
5.  Calculate the dimensions of the output grid (H_out x W_out):
    a.  Set H_out = H_max.
    b.  If H_max is equal to W_max (the largest noise block is square), set W_out = W_max.
    c.  If H_max is not equal to W_max (the largest noise block is not square), set W_out = W_max - 1.
6.  Identify the starting coordinates (r_start, c_start) of the fundamental repeating unit of the background pattern in the top-left region of the input grid (this is typically (0,0) or (1,1) based on the examples).
7.  Extract the subgrid from the input grid starting at (r_start, c_start) with dimensions H_out x W_out. This subgrid is the final output.