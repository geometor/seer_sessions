**Perception**

1.  **Input/Output Structure:** Both input and output grids have the same dimensions (14x14 in all examples).
2.  **Color Palette:** The primary colors involved are white (0), blue (1), red (2), green (3), and gray (5).
3.  **Dominant Feature:** A thick horizontal band of gray (5) pixels is present in the middle of the input grid in all examples. This band seems largely static, although some pixels *above* it change.
4.  **Dynamic Elements:** The non-white, non-gray pixels (blue, red, green) appear scattered above and below the gray band in the input.
5.  **Transformation Observation:**
    *   In the output grid, all the original blue, red, and green pixels disappear (replaced by white).
    *   Some white pixels located directly *above* the gray band change to gray in the output.
    *   Comparing input and output, the white pixels that change to gray seem to correspond to the columns where blue, red, or green pixels existed *above* the gray band in the input.
    *   Pixels below the gray band seem to disappear without affecting the gray band or the pixels above it.
    *   The transformation appears column-specific.

**YAML Facts**


```yaml
elements:
  - type: grid
    properties:
      - dimensions: constant (e.g., 14x14)
  - type: color
    values:
      - white: 0
      - blue: 1
      - red: 2
      - green: 3
      - gray: 5
  - type: object
    name: gray_band
    description: A contiguous horizontal band of gray pixels, typically multiple rows thick, located in the middle rows of the grid.
    properties:
      - color: gray (5)
      - shape: horizontal rectangle/band
      - location: middle rows
      - static: mostly unchanged, forms a boundary
  - type: object
    name: colored_pixels
    description: Individual pixels with colors blue(1), red(2), or green(3).
    properties:
      - color: blue(1), red(2), green(3)
      - location: scattered above and below the gray_band
      - interaction: pixels above the gray_band affect the grid above the band; all colored_pixels are removed in the output.

actions:
  - name: identify_boundary
    input: input_grid
    output: location of the top row of the gray_band
  - name: detect_pixels_above_boundary
    input: input_grid, gray_band_top_row
    output: list of columns containing colored_pixels above the gray_band
  - name: modify_pixels_above_band
    input: input_grid, gray_band_top_row, columns_with_pixels_above
    output: modified_grid (pixels directly above the gray_band in detected columns are changed to gray)
  - name: remove_colored_pixels
    input: input_grid (or modified_grid)
    output: final_grid (all original blue, red, green pixels replaced with white)

relationships:
  - type: spatial
    description: Colored pixels exist relative to the gray band (above or below).
  - type: causal
    description: The presence of a colored pixel *above* the gray band in a specific column causes the pixel directly *above* the gray band in that same column to change to gray.
  - type: state_change
    description: Colored pixels are removed (become white). Specific white pixels above the gray band become gray.

constants:
  - name: background_color
    value: white (0)
  - name: band_color
    value: gray (5)
  - name: active_colors
    value: [blue(1), red(2), green(3)]

output_grid_composition:
  - Retains the original gray band.
  - Retains most original white pixels.
  - Replaces all original blue, red, and green pixels with white.
  - Changes specific white pixels directly above the gray band to gray, based on the rule.
```


**Natural Language Program**

1.  Initialize the output grid as a copy of the input grid.
2.  Identify the horizontal band of gray (5) pixels. Determine the row index of the top edge of this band.
3.  Iterate through each column of the input grid.
4.  For the current column, scan the rows *above* the top edge of the gray band. Check if any pixel in this upper section of the column has a color of blue (1), red (2), or green (3).
5.  If such a colored pixel is found in the current column above the gray band:
    *   Locate the pixel in the output grid that is in the same column and in the row immediately *above* the top edge of the gray band.
    *   Change the color of this specific pixel in the output grid to gray (5).
6.  After checking all columns, iterate through the entire output grid. Change any pixel that still has the color blue (1), red (2), or green (3) to white (0).
7.  The resulting grid is the final output.