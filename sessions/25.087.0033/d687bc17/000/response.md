**Perception**

The input and output are grids of colored pixels. Each grid features a distinct border, one pixel thick, on all four sides (top, bottom, left, right). The colors of these border segments remain consistent between the input and output grids. The central area within the border is mostly white (0), containing scattered individual pixels of various colors.

The core transformation affects only the colored pixels located within the central area (excluding the border). These inner pixels appear to move towards the border segment that shares their color. If a pixel's color matches the top border's color, it moves straight up. If it matches the bottom border, it moves straight down. If it matches the left border, it moves straight left. If it matches the right border, it moves straight right. The movement stops when the pixel reaches the position immediately adjacent to the relevant border segment (i.e., the inner edge of the border).

Pixels whose colors do not match any of the four border colors are removed (turned white) in the output grid. The original positions of the pixels that moved or were removed become white in the output. The border pixels themselves are unchanged.

**Facts**


```yaml
elements:
  - type: grid
    properties:
      - structure: border (1px thick) surrounding a central area
      - background_color: white (0)

  - type: border_pixels
    properties:
      - location: top row, bottom row, leftmost column, rightmost column
      - role: static frame, determines movement direction for inner pixels
      - segments:
          - name: top_border
            location: row 0
            color: varies per example
          - name: bottom_border
            location: last row
            color: varies per example
          - name: left_border
            location: column 0
            color: varies per example
          - name: right_border
            location: last column
            color: varies per example

  - type: inner_pixels
    properties:
      - location: grid cells excluding the border
      - initial_state: mostly white (0) with scattered colored pixels
      - color: varies (0-9)

actions:
  - name: identify_border_colors
    inputs: input grid
    outputs: colors of top, bottom, left, right border segments

  - name: process_inner_pixels
    inputs: 
      - input grid
      - border colors
    description: Iterate through each pixel in the central area (excluding border).
    steps:
      - for each non-white inner pixel:
        - check if its color matches any border color:
          - if match top_border_color:
              action: move_pixel
              direction: up
              target_row: 1
          - if match bottom_border_color:
              action: move_pixel
              direction: down
              target_row: grid_height - 2
          - if match left_border_color:
              action: move_pixel
              direction: left
              target_column: 1
          - if match right_border_color:
              action: move_pixel
              direction: right
              target_column: grid_width - 2
          - if no match:
              action: remove_pixel (set to white) at original location

  - name: construct_output_grid
    inputs: 
      - input grid (for border)
      - processed inner pixel locations and colors
    description: Create the output grid by combining the original border with the final state of the inner area after pixel movements and removals. Initialize the inner area as white, then place the moved pixels at their target locations.

relationships:
  - The color of an inner pixel determines its behavior (move or remove) based on its relationship (match or no match) with the border colors.
  - The direction of movement for a matching inner pixel is determined by which border segment (top, bottom, left, right) its color matches.
  - The final position of a moved pixel is adjacent to the corresponding border segment.
```


**Natural Language Program**

1.  Initialize the output grid as a copy of the input grid.
2.  Identify the color of the top border (from input grid, row 0).
3.  Identify the color of the bottom border (from input grid, last row).
4.  Identify the color of the left border (from input grid, column 0).
5.  Identify the color of the right border (from input grid, last column).
6.  Iterate through each cell (pixel) in the input grid, excluding the border rows and columns (i.e., from row 1 to height-2, and column 1 to width-2).
7.  For each cell within this inner area:
    a.  Get the color of the pixel at the current cell `(r, c)`.
    b.  If the pixel color is not white (0):
        i.   Set the pixel at the original location `(r, c)` in the *output* grid to white (0).
        ii.  Check if the pixel color matches the top border color. If yes, set the pixel at location `(1, c)` in the *output* grid to this color.
        iii. Else, check if the pixel color matches the bottom border color. If yes, set the pixel at location `(grid_height - 2, c)` in the *output* grid to this color.
        iv.  Else, check if the pixel color matches the left border color. If yes, set the pixel at location `(r, 1)` in the *output* grid to this color.
        v.   Else, check if the pixel color matches the right border color. If yes, set the pixel at location `(r, grid_width - 2)` in the *output* grid to this color.
        vi.  (If the color matched none of the borders, it has already been effectively removed by step 7.b.i).
8.  Return the modified output grid.