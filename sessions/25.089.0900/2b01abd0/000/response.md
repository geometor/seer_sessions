**Perception:**

1.  **Input/Output Structure:** Both input and output are 2D grids of pixels with different colors.
2.  **Key Feature:** A prominent horizontal blue line (color 1) exists in all examples, dividing the grid into an upper and a lower section. This blue line remains unchanged in the output.
3.  **Transformation:** The core transformation appears to be a reflection across the horizontal blue line, combined with a color swap.
4.  **Objects:** Objects are contiguous blocks of non-white (color 0) and non-blue (color 1) pixels. These objects exist either entirely above or entirely below the blue line in the input.
5.  **Reflection Action:**
    *   Objects *above* the blue line in the input are reflected *below* the blue line in the output. The reflection is symmetrical with respect to the blue line's row index.
    *   Objects *below* the blue line in the input are reflected *above* the blue line in the output.
    *   The original objects are removed from their initial positions in the output grid, leaving white pixels (color 0) behind, unless overwritten by a reflected object.
6.  **Color Swapping:** During the reflection, specific pairs of colors are swapped:
    *   Example 1: Azure (8) swaps with Yellow (4).
    *   Example 2: Red (2) swaps with Green (3).
    *   Example 3: Gray (5) swaps with Magenta (6).
7.  **Symmetry:** The reflection preserves the shape and relative positions of the pixels within an object, but flips it vertically across the blue line. The distance of each pixel from the blue line remains the same but on the opposite side.

**YAML Facts:**


```yaml
elements:
  - type: grid
    description: Input and output are 2D grids of colored pixels.
  - type: line
    color: blue (1)
    orientation: horizontal
    role: separator & axis_of_reflection
    persistence: remains unchanged between input and output
  - type: object
    description: Contiguous block of non-white (0), non-blue (1) pixels.
    location: Located entirely above or entirely below the blue line in the input.
    properties:
      - color
      - shape
      - position_relative_to_blue_line
actions:
  - name: find_blue_line
    input: input_grid
    output: row_index_of_blue_line
  - name: identify_objects
    input: input_grid
    criteria: contiguous pixels not color 0 or 1
    output: list_of_objects (with their pixels, colors, locations)
  - name: reflect_and_swap_color
    input: object, blue_line_row_index
    process:
      - determine if object is above or below the blue line
      - calculate new row index for each pixel based on reflection across blue_line_row_index
      - swap color of each pixel based on predefined pairs
    output: reflected_object (with new locations and swapped colors)
  - name: construct_output_grid
    process:
      - start with a white grid of the same dimensions as the input
      - copy the blue line from the input to the output
      - place the reflected_and_swapped objects onto the output grid
color_swaps:
  - pair: [azure (8), yellow (4)]
  - pair: [red (2), green (3)]
  - pair: [gray (5), magenta (6)]
relationships:
  - input_object maps to reflected_output_object
  - pixel distance from blue line is preserved but mirrored
  - specific color pairs are mutually swapped during reflection
```


**Natural Language Program:**

1.  Initialize the output grid as a copy of the input grid, filled with the background color (white, 0).
2.  Identify the row index of the horizontal blue line (color 1) in the input grid.
3.  Copy the blue line from the input grid to the same row index in the output grid.
4.  Iterate through each pixel in the input grid.
5.  If a pixel is *not* white (0) and *not* blue (1):
    a.  Determine its original row (`r_orig`) and column (`c`).
    b.  Determine its original color (`color_orig`).
    c.  Calculate the vertical distance (`dist`) from the pixel's row to the blue line's row (`blue_line_row`). `dist = r_orig - blue_line_row`.
    d.  Calculate the reflected row index (`r_refl`) by flipping the distance: `r_refl = blue_line_row - dist`.
    e.  Determine the swapped color (`color_swapped`) based on the original color:
        *   If `color_orig` is azure (8), `color_swapped` is yellow (4).
        *   If `color_orig` is yellow (4), `color_swapped` is azure (8).
        *   If `color_orig` is red (2), `color_swapped` is green (3).
        *   If `color_orig` is green (3), `color_swapped` is red (2).
        *   If `color_orig` is gray (5), `color_swapped` is magenta (6).
        *   If `color_orig` is magenta (6), `color_swapped` is gray (5).
        *   (Assume other colors, if any, remain unchanged, although none are present in examples).
    f.  Place the `color_swapped` pixel at the calculated reflected position (`r_refl`, `c`) in the output grid.
6.  Return the completed output grid.