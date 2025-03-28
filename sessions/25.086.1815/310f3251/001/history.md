
## train_1

**input:**
```
0 0 0 0
0 0 5 0
0 0 0 0
0 5 0 0
```


**output:**
```
0 2 0 0 0 2 0 0 0 2 0 0
0 0 5 0 0 0 5 0 0 0 5 0
2 0 0 0 2 0 0 0 2 0 0 0
0 5 0 0 0 5 0 0 0 5 0 0
0 2 0 0 0 2 0 0 0 2 0 0
0 0 5 0 0 0 5 0 0 0 5 0
2 0 0 0 2 0 0 0 2 0 0 0
0 5 0 0 0 5 0 0 0 5 0 0
0 2 0 0 0 2 0 0 0 2 0 0
0 0 5 0 0 0 5 0 0 0 5 0
2 0 0 0 2 0 0 0 2 0 0 0
0 5 0 0 0 5 0 0 0 5 0 0
```


## train_2

**input:**
```
0 0 0
0 0 6
6 0 0
```


**output:**
```
0 2 0 0 2 0 0 2 0
0 0 6 0 0 6 0 0 6
6 0 0 6 0 0 6 0 0
0 2 0 0 2 0 0 2 0
0 0 6 0 0 6 0 0 6
6 0 0 6 0 0 6 0 0
0 2 0 0 2 0 0 2 0
0 0 6 0 0 6 0 0 6
6 0 0 6 0 0 6 0 0
```


## train_3

**input:**
```
0 0 0 0 0
0 8 0 0 0
0 8 0 0 0
0 0 0 0 0
0 0 0 0 0
```


**output:**
```
2 0 0 0 0 2 0 0 0 0 2 0 0 0 0
2 8 0 0 0 2 8 0 0 0 2 8 0 0 0
0 8 0 0 0 0 8 0 0 0 0 8 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
2 0 0 0 0 2 0 0 0 0 2 0 0 0 0
2 8 0 0 0 2 8 0 0 0 2 8 0 0 0
0 8 0 0 0 0 8 0 0 0 0 8 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
2 0 0 0 0 2 0 0 0 0 2 0 0 0 0
2 8 0 0 0 2 8 0 0 0 2 8 0 0 0
0 8 0 0 0 0 8 0 0 0 0 8 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


## train_4

**input:**
```
0 0 0 0
0 0 0 0
0 0 0 0
1 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 2 0 0 0 2 0 0 0 2
1 0 0 0 1 0 0 0 1 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 2 0 0 0 2 0 0 0 2
1 0 0 0 1 0 0 0 1 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 2 0 0 0 2 0 0 0 2
1 0 0 0 1 0 0 0 1 0 0 0
```


## train_5

**input:**
```
0 0
0 7
```


**output:**
```
2 0 2 0 2 0
0 7 0 7 0 7
2 0 2 0 2 0
0 7 0 7 0 7
2 0 2 0 2 0
0 7 0 7 0 7
```

*   **Perception**:
    *   The output grid dimensions are consistently 3 times the input grid dimensions in both height and width.
    *   The output grid appears to be a 3x3 tiling of a modified version of the input grid. Let's call this modified version the "base tile".
    *   The base tile has the same dimensions as the input grid.
    *   Comparing the input grid to the top-left subgrid (base tile) of the output grid reveals two main changes:
        1.  All non-white pixels from the input grid are preserved in their original positions in the base tile.
        2.  New red (color 2) pixels are introduced into the base tile at specific locations. These locations were originally white (color 0) in the input grid.
    *   The position of the new red pixels relative to the original non-white pixels seems crucial.
    *   Observing examples 1, 2, 3, and 5 (colors Gray-5, Magenta-6, Azure-8, Orange-7), the red pixel appears diagonally up-left (row-1, col-1) relative to the original non-white pixel, provided this position is within the grid bounds and was originally white.
    *   Observing example 4 (color Blue-1), the red pixel appears at a different relative position: up 1 and right 3 (row-1, col+3), again provided the position is within bounds and was originally white.
    *   This suggests a rule where each non-white pixel in the input potentially generates a red pixel in the base tile at a relative offset, but only if the target location is valid (within bounds) and was originally white. The specific offset depends on the color of the original non-white pixel. Blue (1) uses (-1, 3), while the other observed non-white colors (5, 6, 7, 8) use (-1, -1).
    *   The final output is constructed by repeating the generated base tile in a 3x3 arrangement.

*   **Facts**:
    
```yaml
    grid_transformation:
      - operation: resize_and_tile
        factor: 3 # Output grid is 3x larger in each dimension
        tiling: 3x3
      - operation: create_base_tile
        source: input_grid
        target_dimensions: same_as_input
        steps:
          - step: initialize_tile
            color: white (0)
          - step: process_pixels
            actions:
              - action: copy_non_white_pixels
                description: Copy all pixels with color != 0 from input to the base tile at the same coordinates.
              - action: generate_red_pixels
                based_on: non_white_pixels_in_input
                color_to_generate: red (2)
                conditions:
                  - rule: standard_offset
                    applies_to_colors: [5, 6, 7, 8] # Gray, Magenta, Orange, Azure (and presumably others not 1)
                    relative_offset: {dr: -1, dc: -1} # Up-Left
                    placement_condition: Target cell (r-1, c-1) must be within grid bounds and white (0) in the input grid.
                  - rule: blue_offset
                    applies_to_colors: [1] # Blue
                    relative_offset: {dr: -1, dc: +3} # Up 1, Right 3
                    placement_condition: Target cell (r-1, c+3) must be within grid bounds and white (0) in the input grid.
                target_location: base_tile[r + dr, c + dc]
    ```


*   **Natural Language Program**:
    1.  Define a "base tile" grid with the same height and width as the input grid, initially filled with white pixels (0).
    2.  Iterate through each pixel at position (row `r`, column `c`) in the input grid.
    3.  Let `C` be the color of the input pixel `Input(r, c)`.
    4.  If `C` is not white (i.e., `C != 0`):
        a.  Set the corresponding pixel in the base tile to this color: `BaseTile(r, c) = C`.
        b.  Determine the target offset `(dr, dc)` for placing a potential red pixel:
            *   If `C` is blue (1), set `dr = -1`, `dc = 3`.
            *   Otherwise (if `C` is any other non-white color), set `dr = -1`, `dc = -1`.
        c.  Calculate the potential target coordinates for the red pixel: `nr = r + dr`, `nc = c + dc`.
        d.  Check if the target coordinates `(nr, nc)` are within the bounds of the input grid dimensions.
        e.  If the coordinates are within bounds AND the original input pixel at that location `Input(nr, nc)` is white (0), then set the corresponding pixel in the base tile to red (2): `BaseTile(nr, nc) = 2`.
    5.  Create the final output grid with dimensions 3 times the height and 3 times the width of the input grid.
    6.  Fill the output grid by tiling the completed base tile 3 times horizontally and 3 times vertically.
