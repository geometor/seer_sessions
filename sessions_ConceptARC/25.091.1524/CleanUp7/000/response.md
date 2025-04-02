## Perception

1.  **Grid Structure:** The input and output are both 2D grids of pixels with different colors. The size of the grid remains constant between input and output.
2.  **Color Palette:** The colors involved are white (0), green (3), yellow (4), magenta (6), and azure (8). White seems to be the background color.
3.  **Key Color:** The color azure (8) appears in all input examples but is completely absent in the corresponding output examples.
4.  **Affected Colors:** In each example, pixels of *another* color (green in ex 1, yellow in ex 2, magenta in ex 3) that are adjacent (including diagonals) to the azure pixels in the input are also removed (changed to white) in the output.
5.  **Unaffected Pixels:** Pixels that are not azure (8) and are not adjacent to any azure pixel retain their original color in the output. White (0) pixels also seem unaffected unless they replace a removed pixel.
6.  **Transformation:** The core transformation involves identifying all azure (8) pixels and all non-white pixels adjacent to them, and then replacing all these identified pixels with white (0).

## Facts


```yaml
task_description: "Identify and remove azure (8) pixels and any non-white pixels adjacent (including diagonals) to them, replacing them with white (0)."
grid_properties:
  - size_preservation: True # Grid dimensions do not change.
  - background_color: 0 # White is the default/background color.
objects:
  - type: primary_target
    color: 8 # azure
    description: "The main object/color to be removed."
  - type: secondary_target
    color: non-zero # Any color other than white (0) and azure (8).
    description: "Pixels of these colors are potentially affected if adjacent to the primary target."
relationships:
  - type: adjacency
    scope: 8-connectivity # Includes horizontal, vertical, and diagonal neighbors.
    condition: "A secondary target pixel is adjacent to a primary target pixel."
actions:
  - name: identify_primary
    target: pixels with color 8
    result: set of coordinates for all azure pixels.
  - name: identify_adjacent_secondary
    target: pixels with non-zero, non-8 color
    condition: adjacent (8-connectivity) to any pixel identified in 'identify_primary'
    result: set of coordinates for adjacent non-white, non-azure pixels.
  - name: remove_pixels
    target_coordinates: union of coordinates from 'identify_primary' and 'identify_adjacent_secondary'
    action: change pixel color to 0 (white).
  - name: preserve_pixels
    target_coordinates: all coordinates not in 'remove_pixels' target set.
    action: keep original pixel color.
```


## Natural Language Program

1.  Initialize the output grid as a copy of the input grid.
2.  Create two sets to store the coordinates of pixels to be changed to white: `azure_coords` and `adjacent_coords`.
3.  Iterate through each pixel (cell) of the input grid using its row and column index.
4.  If a pixel's color is azure (8), add its coordinates (row, col) to the `azure_coords` set.
5.  After identifying all azure pixels, iterate through each pixel of the input grid again.
6.  For each pixel that is *not* white (0) and *not* azure (8):
    a.  Check its 8 neighbors (horizontal, vertical, and diagonal).
    b.  If any neighbor's coordinates are present in the `azure_coords` set, add the current pixel's coordinates (row, col) to the `adjacent_coords` set.
7.  Combine the coordinates from `azure_coords` and `adjacent_coords` into a single set of `pixels_to_remove`.
8.  Iterate through all coordinates in the `pixels_to_remove` set. For each coordinate (row, col), set the color of the corresponding pixel in the output grid to white (0).
9.  Return the modified output grid.