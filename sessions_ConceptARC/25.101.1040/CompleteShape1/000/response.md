## Perception

The task involves modifying input grids by filling in specific rectangular areas composed entirely of white pixels (color 0). The color used to fill these white rectangles appears to be determined by the color of adjacent or aligned non-white shapes. The goal seems to be completing or bridging gaps in existing monochromatic (single-color) lines or shapes.

1.  **Example 1:** A 2x2 white rectangle near the top-center is filled with blue (1). This white rectangle is located directly above a vertical column of white space, which in turn is above a 2x2 blue rectangle near the bottom-center. The filling action appears to extend the lower blue rectangle upwards across the white gap.
2.  **Example 2:** A 1x2 white rectangle near the bottom-center is filled with magenta (6). This white rectangle is located immediately to the right of a 1x2 horizontal segment of magenta pixels. The filling action extends this magenta segment to the right.

The core operation is identifying these "fillable" white rectangles and determining the correct color based on context, specifically looking for monochromatic shapes that are aligned (horizontally or vertically) with the white rectangle and separated only by other white pixels, or directly adjacent.

## Facts


```yaml
Examples:
  - id: train_1
    Input:
      grid_size: [12, 10]
      objects:
        - type: background
          color: white
        - type: shape # Left top
          color: blue
          pixels: [[2,1],[2,2],[3,1],[3,2]]
        - type: shape # Left middle
          color: red
          pixels: [[4,1],[4,2],[7,1],[7,2]]
        - type: shape # Left bottom
          color: blue
          pixels: [[5,1],[5,2],[6,1],[6,2],[8,1],[8,2],[9,1],[9,2]]
        - type: shape # Right top
          color: red
          pixels: [[2,3],[3,3],[2,6],[3,6],[4,7],[4,8],[7,7],[7,8]]
        - type: shape # Right bottom
          color: blue
          pixels: [[5,7],[5,8],[6,7],[6,8],[8,7],[8,8],[9,7],[9,8]]
        - type: shape # Center vertical line (bottom part)
          color: blue
          pixels: [[8,4],[8,5],[9,4],[9,5]]
        - type: shape # Center vertical line (top part - target)
          color: white
          pixels: [[2,4],[2,5],[3,4],[3,5]]
        - type: shape # Center white space separator
          color: white
          pixels: [[4,4],[4,5],[5,4],[5,5],[6,4],[6,5],[7,4],[7,5]]
    Output:
      grid_size: [12, 10]
      objects: # Same as input, except:
        - type: shape # Center vertical line (top part - filled)
          color: blue
          pixels: [[2,4],[2,5],[3,4],[3,5]]
      action:
        - type: fill_rectangle
          target_rectangle: # Center vertical line (top part)
            color: white
            pixels: [[2,4],[2,5],[3,4],[3,5]]
          fill_color: blue
          reason: >
            Completes vertical alignment with the blue shape [[8,4],[8,5],[9,4],[9,5]]
            across the white separator [[4,4]..[7,5]].

  - id: train_2
    Input:
      grid_size: [6, 8]
      objects:
        - type: background
          color: white
        - type: shape # Frame parts
          color: red
          pixels: [[0,1],[0,6],[5,1],[5,6]]
        - type: shape # Frame parts
          color: magenta
          pixels: [[0,2],[0,3],[0,4],[0,5],[1,1],[1,6],[2,1],[2,6],[3,1],[3,6],[4,1],[4,6],[5,2],[5,3]]
        - type: shape # Horizontal line gap (target)
          color: white
          pixels: [[5,4],[5,5]]
    Output:
      grid_size: [6, 8]
      objects: # Same as input, except:
        - type: shape # Horizontal line gap (filled)
          color: magenta
          pixels: [[5,4],[5,5]]
      action:
        - type: fill_rectangle
          target_rectangle: # Horizontal line gap
            color: white
            pixels: [[5,4],[5,5]]
          fill_color: magenta
          reason: >
            Completes horizontal alignment by extending the adjacent magenta shape
            [[5,2],[5,3]] to the right.
```


## Natural Language Program

1.  Initialize the output grid as a copy of the input grid.
2.  Iterate through all possible rectangular subgrids within the input grid.
3.  Identify maximal contiguous rectangular subgrids composed entirely of white pixels (color 0). Let the current white rectangle be `W`.
4.  For each white rectangle `W`:
    a.  **Check for Vertical Completion Below:** Find the highest non-white, monochromatic rectangle `S` located entirely below `W`, such that `S` has the same width and occupies the same columns as `W`. Check if the rectangular region between the bottom edge of `W` and the top edge of `S` consists entirely of white pixels. If such an `S` exists and the separating region is white, fill the region corresponding to `W` in the output grid with the color of `S`. Stop checking for this `W` and proceed to the next white rectangle.
    b.  **Check for Horizontal Completion Left:** Find the rightmost non-white, monochromatic rectangle `S` located entirely to the left of `W`, such that `S` has the same height and occupies the same rows as `W`. Check if `S` is immediately adjacent to `W` (no gap between them). If such an `S` exists, fill the region corresponding to `W` in the output grid with the color of `S`. Stop checking for this `W` and proceed to the next white rectangle.
    c.  **(Implicit)** Similar checks can be defined for vertical completion above and horizontal completion right, if necessary based on other examples, potentially with a defined priority order (e.g., Below > Left > Above > Right).
5.  Return the modified output grid.