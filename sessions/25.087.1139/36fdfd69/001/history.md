
## train_1

**input:**
```
8 0 0 0 0 8 0 0 8 8 8 8 8 0 0 0
0 8 0 0 0 0 0 0 0 8 0 8 0 8 0 0
0 0 8 8 8 0 8 8 8 8 8 8 0 8 0 8
0 0 8 0 8 0 0 0 0 8 0 8 8 2 8 0
0 0 2 8 2 2 2 8 0 0 0 2 8 2 8 0
8 0 2 8 2 8 8 8 0 0 0 8 0 0 8 8
8 0 0 8 8 0 8 8 8 8 0 8 8 0 0 0
8 0 8 0 8 0 8 0 8 8 0 8 8 8 0 8
8 0 0 0 8 0 0 0 0 0 0 0 0 0 0 0
8 0 8 8 2 8 8 8 0 8 0 0 0 8 8 8
8 0 2 8 8 2 8 8 0 8 0 0 8 8 0 8
0 8 0 0 0 8 8 0 0 2 8 8 0 8 8 8
8 0 0 8 8 8 8 0 0 2 8 2 0 0 0 8
0 8 8 0 8 8 8 0 0 0 8 0 8 8 8 8
8 8 8 0 8 0 8 0 0 0 8 8 8 8 8 8
```


**output:**
```
8 0 0 0 0 8 0 0 8 8 8 8 8 0 0 0
0 8 0 0 0 0 0 0 0 8 0 8 0 8 0 0
0 0 8 8 8 0 8 8 8 8 8 8 0 8 0 8
0 0 8 0 8 0 0 0 0 8 0 4 4 2 8 0
0 0 2 4 2 2 2 8 0 0 0 2 4 2 8 0
8 0 2 4 2 4 4 8 0 0 0 8 0 0 8 8
8 0 0 8 8 0 8 8 8 8 0 8 8 0 0 0
8 0 8 0 8 0 8 0 8 8 0 8 8 8 0 8
8 0 0 0 8 0 0 0 0 0 0 0 0 0 0 0
8 0 4 4 2 4 8 8 0 8 0 0 0 8 8 8
8 0 2 4 4 2 8 8 0 8 0 0 8 8 0 8
0 8 0 0 0 8 8 0 0 2 4 4 0 8 8 8
8 0 0 8 8 8 8 0 0 2 4 2 0 0 0 8
0 8 8 0 8 8 8 0 0 0 8 0 8 8 8 8
8 8 8 0 8 0 8 0 0 0 8 8 8 8 8 8
```


## train_2

**input:**
```
1 0 0 0 0 1 1 0 0 0 0 0 0 1 0 0 0 1
1 1 2 1 1 1 1 1 1 0 0 1 0 1 1 1 0 0
1 1 1 2 1 2 2 2 2 0 1 1 1 0 0 1 1 0
1 0 2 1 2 2 2 2 2 0 1 0 0 0 1 1 1 1
0 1 1 1 0 0 1 1 1 0 0 0 1 0 1 1 0 0
1 0 1 0 0 1 1 0 0 0 1 1 1 1 0 0 0 0
1 0 1 0 0 0 1 0 1 0 0 0 0 0 1 1 0 1
0 0 0 1 0 0 1 0 0 0 1 0 0 0 1 2 1 0
0 1 0 1 1 0 0 0 0 1 0 0 0 0 2 2 1 1
0 0 0 0 0 1 0 0 0 0 0 0 0 0 1 1 0 0
0 1 1 0 1 1 2 1 2 1 2 1 0 1 0 0 0 0
0 0 0 0 0 0 1 1 1 1 1 0 0 1 1 0 0 1
0 0 0 0 0 1 1 2 1 2 2 0 0 1 0 1 1 1
0 1 0 0 0 0 0 0 1 1 0 1 0 1 1 1 0 0
0 0 1 0 0 0 1 0 0 1 0 0 0 0 0 1 1 0
0 0 0 0 0 0 1 1 1 0 1 0 1 0 0 1 1 1
1 0 0 1 0 0 1 1 1 0 1 1 0 0 0 0 0 1
```


**output:**
```
1 0 0 0 0 1 1 0 0 0 0 0 0 1 0 0 0 1
1 1 2 4 4 4 4 4 4 0 0 1 0 1 1 1 0 0
1 1 4 2 4 2 2 2 2 0 1 1 1 0 0 1 1 0
1 0 2 4 2 2 2 2 2 0 1 0 0 0 1 1 1 1
0 1 1 1 0 0 1 1 1 0 0 0 1 0 1 1 0 0
1 0 1 0 0 1 1 0 0 0 1 1 1 1 0 0 0 0
1 0 1 0 0 0 1 0 1 0 0 0 0 0 1 1 0 1
0 0 0 1 0 0 1 0 0 0 1 0 0 0 4 2 1 0
0 1 0 1 1 0 0 0 0 1 0 0 0 0 2 2 1 1
0 0 0 0 0 1 0 0 0 0 0 0 0 0 1 1 0 0
0 1 1 0 1 1 2 4 2 4 2 1 0 1 0 0 0 0
0 0 0 0 0 0 4 4 4 4 4 0 0 1 1 0 0 1
0 0 0 0 0 1 4 2 4 2 2 0 0 1 0 1 1 1
0 1 0 0 0 0 0 0 1 1 0 1 0 1 1 1 0 0
0 0 1 0 0 0 1 0 0 1 0 0 0 0 0 1 1 0
0 0 0 0 0 0 1 1 1 0 1 0 1 0 0 1 1 1
1 0 0 1 0 0 1 1 1 0 1 1 0 0 0 0 0 1
```


## train_3

**input:**
```
3 3 0 0 0 0 0 3 0 3 3 0 0 0
0 0 3 0 0 3 3 0 3 0 0 0 3 0
0 0 3 3 0 0 0 3 3 3 0 0 0 0
3 0 0 0 0 0 0 3 3 3 0 0 3 3
0 0 0 2 2 2 2 3 0 0 0 3 0 3
0 3 3 2 2 3 3 2 0 0 0 3 3 0
0 3 0 2 2 2 3 2 0 0 3 0 0 0
0 0 0 0 0 3 3 0 3 0 0 0 0 3
0 0 3 3 0 3 3 0 3 3 0 0 3 3
3 3 3 2 0 3 3 0 0 0 3 0 3 0
0 3 2 3 0 0 0 3 3 0 0 0 3 0
0 3 3 0 3 3 0 0 3 3 0 3 0 3
0 0 3 0 3 3 0 0 3 0 3 3 0 3
0 3 3 0 3 0 3 0 3 0 0 0 0 0
3 0 0 3 0 0 0 0 0 3 3 0 3 3
```


**output:**
```
3 3 0 0 0 0 0 3 0 3 3 0 0 0
0 0 3 0 0 3 3 0 3 0 0 0 3 0
0 0 3 3 0 0 0 3 3 3 0 0 0 0
3 0 0 0 0 0 0 3 3 3 0 0 3 3
0 0 0 2 2 2 2 4 0 0 0 3 0 3
0 3 3 2 2 4 4 2 0 0 0 3 3 0
0 3 0 2 2 2 4 2 0 0 3 0 0 0
0 0 0 0 0 3 3 0 3 0 0 0 0 3
0 0 3 3 0 3 3 0 3 3 0 0 3 3
3 3 4 2 0 3 3 0 0 0 3 0 3 0
0 3 2 4 0 0 0 3 3 0 0 0 3 0
0 3 3 0 3 3 0 0 3 3 0 3 0 3
0 0 3 0 3 3 0 0 3 0 3 3 0 3
0 3 3 0 3 0 3 0 3 0 0 0 0 0
3 0 0 3 0 0 0 0 0 3 3 0 3 3
```

Okay, let's break down the transformation in these examples.

**Perception**

1.  **Color Palette:** The input grids primarily use white (0), red (2), and one other color (azure (8) in Ex1, blue (1) in Ex2, green (3) in Ex3). The output grids introduce yellow (4).
2.  **Conservation:** Most pixels retain their original color from input to output. The grid dimensions remain unchanged.
3.  **Transformation Trigger:** The presence of red (2) pixels seems crucial. Changes only occur in the vicinity of red pixels.
4.  **Affected Colors:** The color that changes is different in each example (azure, blue, green), but it's never the red (2) or white (0) pixels themselves.
5.  **Resulting Color:** The changed pixels consistently become yellow (4).
6.  **Spatial Relationship:** The pixels that change are always adjacent (horizontally, vertically, or diagonally) to at least one red (2) pixel in the input grid.
7.  **Rule:** It appears that any non-red, non-white pixel that has a red pixel as one of its 8 neighbors is changed to yellow. Pixels that are red, white, or not adjacent to red remain unchanged.

**YAML Facts**


```yaml
task_description: Modify pixels based on adjacency to red pixels.
grid_properties:
  - dimensions_preserved: True
  - background_color: white (0) # Predominantly white or unchanged background
objects:
  - type: pixel
    properties:
      - color: varies (0-9)
      - location: (row, col)
      - neighbors: set of 8 adjacent pixels (including diagonals)
actions:
  - name: identify_trigger_pixels
    input: input_grid
    criteria: color == 2 (red)
    output: set of locations of red pixels
  - name: identify_target_pixels
    input: input_grid
    criteria: color != 0 (white) and color != 2 (red)
    output: set of locations of potentially changeable pixels
  - name: check_adjacency
    input: target_pixel_location, trigger_pixel_locations
    process: Determine if any trigger pixel location is within the 8 neighbors of the target pixel location.
    output: boolean (is_adjacent_to_red)
  - name: change_color
    input: pixel_location, output_grid
    condition: pixel at location is a target pixel AND is_adjacent_to_red is true
    effect: Change the color of the pixel at the specified location in the output_grid to 4 (yellow).
relationships:
  - type: adjacency
    between: target_pixel, trigger_pixel
    condition: target_pixel is one of the 8 neighbors of a trigger_pixel
    effect: Potential color change for the target_pixel.
constants:
  - trigger_color: 2 (red)
  - result_color: 4 (yellow)
  - ignored_colors: [0 (white), 2 (red)]
```


**Natural Language Program**

1.  Initialize the output grid as a copy of the input grid.
2.  Iterate through each cell (pixel) of the input grid, noting its row `r` and column `c`.
3.  Let `current_color` be the color of the input cell at `(r, c)`.
4.  If `current_color` is white (0) or red (2), do nothing and proceed to the next cell.
5.  If `current_color` is neither white (0) nor red (2):
    a.  Check all 8 neighboring cells (including diagonals) of the cell at `(r, c)` in the *input* grid. Be careful to stay within the grid boundaries.
    b.  If any of these neighbors has the color red (2):
        i.  Change the color of the cell at `(r, c)` in the *output* grid to yellow (4).
    c.  If none of the neighbors are red (2), the cell at `(r, c)` in the output grid keeps its original `current_color` (which it already has from the initial copy).
6.  After checking all cells, return the modified output grid.
