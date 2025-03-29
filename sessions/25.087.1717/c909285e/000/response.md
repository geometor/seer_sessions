## Perception

1.  **Input/Output Sizes:** The input grids are significantly larger than the output grids (e.g., 26x26 -> 7x7, 24x24 -> 7x7, 28x28 -> 7x7). The output grids in the examples are consistently 7x7.
2.  **Input Structure:** The input grids display intricate patterns, often involving repeating rows or columns, and horizontal/vertical lines of specific colors (like azure-8 or gray-5). They seem composed of tiled or repeating smaller motifs.
3.  **Output Structure:** The output grids appear to be contiguous, rectangular subgrids extracted directly from the corresponding input grids.
4.  **Framing Pattern:** In each example, the output subgrid is clearly demarcated within the input grid by a rectangular frame (border) of a single, solid color. The color of this frame is different in each example (red-2, green-3, magenta-6).
5.  **Frame Identification:** The key task seems to be identifying this unique framing color and its location within the input grid. This frame color is not white (0) or gray (5) in the examples provided. The frame completely encloses the region that becomes the output.
6.  **Extraction:** Once the frame is identified, the transformation involves simply extracting the rectangular area bounded by and including the frame.

## Facts


```yaml
task_type: extraction
components:
  - role: input_grid
    description: A large 2D grid containing patterns and lines.
  - role: output_grid
    description: A smaller 2D grid which is a subgrid of the input.
  - role: frame
    description: A rectangular border within the input grid.
    properties:
      - color: A single, solid color that forms the entire border (top, bottom, left, right edges). This color varies between examples (red, green, magenta).
      - location: Defines the top-left and bottom-right corners of the subgrid to be extracted.
      - contiguity: The frame pixels are contiguous along each edge.
      - uniqueness: In each example, there appears to be only one such frame formed by a single color enclosing a varied internal pattern.
actions:
  - name: find_frame
    description: Scan the input grid to locate the unique rectangular frame formed by a single color.
    input: input_grid
    output: frame_color, frame_location (top, left, bottom, right coordinates)
  - name: extract_subgrid
    description: Extract the rectangular region from the input grid defined by the frame's location.
    input: input_grid, frame_location
    output: output_grid
relationship:
  - type: identity
    description: The output_grid is identical to the subgrid identified and extracted from the input_grid based on the discovered frame.
```


## Natural Language Program

1.  Iterate through each possible color `C` present in the input grid (excluding common background colors like white-0 might be a useful heuristic, but check all colors if necessary).
2.  For each color `C`, search the input grid for all occurrences of rectangular regions where the *entire border* (top row, bottom row, leftmost column, rightmost column of the region) consists *only* of pixels with color `C`.
3.  Identify the unique rectangular region `R` that satisfies this framing condition. (There should be only one such region per input grid according to the examples).
4.  Determine the coordinates (top row, left column, bottom row, right column) of this framed region `R`.
5.  Extract the subgrid corresponding to region `R` from the input grid. This extracted subgrid is the output grid.