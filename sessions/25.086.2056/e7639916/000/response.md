## Perception
The input grids consist of a white background (0) with a few scattered azure pixels (8). The output grids retain the original azure pixels and add blue pixels (1). These blue pixels form the perimeter of the smallest rectangle that encloses all the azure pixels present in the input grid. The blue pixels only replace the white background pixels; they do not overwrite the original azure pixels if an azure pixel happens to lie on the calculated perimeter.

## Facts

```yaml
task_type: drawing
elements:
  - role: background
    color: white (0)
    count: majority
  - role: markers
    color: azure (8)
    count: few (>=2)
    distribution: scattered
  - role: drawing
    color: blue (1)
    shape: rectangular_perimeter
    relationship: encloses all 'markers'
    placement: replaces 'background' pixels only

transformation:
  - action: find_all
    target: 'markers' (azure pixels)
  - action: calculate_bounding_box
    based_on: coordinates of all 'markers'
    result: minimum and maximum row and column indices (min_row, max_row, min_col, max_col)
  - action: draw_perimeter
    shape: rectangle defined by the bounding box
    color: blue (1)
    condition: draw only on 'background' (white) pixels within the perimeter boundary
  - action: preserve
    target: original 'markers' (azure pixels)

output_grid:
  size: same as input
  content: input grid + blue rectangular perimeter around azure markers
```


## Natural Language Program
1.  Identify the coordinates (row, column) of all azure (8) pixels in the input grid.
2.  Determine the minimum and maximum row indices and the minimum and maximum column indices among these azure pixel coordinates. These define the bounding box.
3.  Create an output grid as a copy of the input grid.
4.  Iterate through the cells along the perimeter of the calculated bounding box (top row, bottom row, leftmost column, rightmost column within the box boundaries).
5.  For each cell on the perimeter, check if the corresponding cell in the input grid is white (0).
6.  If the input cell is white (0), change its color to blue (1) in the output grid.
7.  Leave all other cells (including the original azure pixels, even if they fall on the perimeter) unchanged from the input grid.