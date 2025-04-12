
## train_1

**input:**
```
0 0 0 2 2 0 0 0 0 0
0 0 0 2 0 0 0 0 0 0
0 0 0 0 1 1 0 0 0 0
0 0 0 0 1 0 0 0 0 0
0 0 0 0 0 0 1 0 0 0
0 0 0 0 0 1 1 0 0 0
0 0 0 0 0 0 0 2 0 0
0 0 0 0 0 0 2 2 0 0
1 0 0 0 0 0 0 0 0 0
2 3 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 2 2 3 3 3 0 0
0 0 0 2 3 3 3 3 0 0
0 0 0 3 1 1 0 3 0 0
0 0 0 3 1 0 0 3 0 0
0 0 0 3 0 0 1 3 0 0
0 0 0 3 0 1 1 3 0 0
0 0 0 3 3 3 3 2 0 0
0 0 0 3 3 3 2 2 0 0
1 0 0 0 0 0 0 0 0 0
2 3 0 0 0 0 0 0 0 0
```

Okay, let's break down this first example.

## Initial Perception

The input grid contains several small, distinct shapes made of colors 1 (light blue) and 2 (red), scattered on a black background (color 0). There's also a single instance of color 3 (dark blue?) in the bottom-left corner, adjacent to a color 2 cell.

The output grid retains all the original shapes in their exact positions and colors. The significant change is the addition of color 3 (dark blue?), which now fills a rectangular area in the center-right portion of the grid. This filling seems selective: it only replaces the background color 0 within this rectangle, leaving the original shapes (colors 1 and 2) within that area untouched. The objects outside this filled rectangle, including the original color 3 cell, also remain unchanged.

The filled rectangle appears to correspond to the bounding box encompassing a specific subset of the initial shapes. Notably, the color used for filling (3) is the same color that appeared only once in the input grid. The shapes that seem to define the bounding box are the four 'L'-shaped objects, each composed of exactly three cells. The smaller objects (a single cell '1' and a two-cell '2'-'3' object) seem excluded from determining the fill area.

## Observed Facts (YAML)

```yaml
# Facts observed from train_1 example
grid_properties:
  size: [10, 10]
  background_color: 0
colors:
  present_in_input: [0, 1, 2, 3]
  present_in_output: [0, 1, 2, 3]
  added_to_output: [3] # Color 3 is added extensively
  unique_input_color: 3 # Appears only once at (9, 1) in input
objects_input:
  - type: shape
    color: 2
    location: [[0, 3], [0, 4], [1, 3]]
    size: 3
    shape_desc: L-shape (inverted)
  - type: shape
    color: 1
    location: [[2, 4], [2, 5], [3, 4]]
    size: 3
    shape_desc: L-shape
  - type: shape
    color: 1
    location: [[4, 6], [5, 5], [5, 6]]
    size: 3
    shape_desc: L-shape
  - type: shape
    color: 2
    location: [[6, 7], [7, 6], [7, 7]]
    size: 3
    shape_desc: L-shape (inverted)
  - type: shape
    color: 1
    location: [[8, 0]]
    size: 1
    shape_desc: single cell
  - type: shape
    color: [2, 3] # Multi-color object
    location: [[9, 0], [9, 1]]
    size: 2
    shape_desc: horizontal line
transformation:
  action: fill_region
  fill_color: 3
  region_definition:
    method: bounding_box
    source_objects: objects with size 3
    coordinates: # Calculated bounding box of size-3 objects
      min_row: 0
      max_row: 7
      min_col: 3
      max_col: 7
  fill_rule: replace background (0) only
  preservation:
    - all original non-zero cells retain their color and position.
    - objects outside the filled region are unaffected.
```

## Natural Language Program

1.  Identify all contiguous groups of non-zero cells (objects) in the input grid.
2.  For each object, determine its size (number of cells).
3.  Find the color value that appears exactly once in the entire input grid; designate this as the `fill_color`.
4.  Select only those input objects whose size is exactly 3.
5.  Calculate the minimal bounding box that encloses all the selected size-3 objects (find min/max row and min/max column).
6.  Initialize the output grid as a copy of the input grid.
7.  Iterate through each cell within the calculated bounding box area.
8.  If a cell within the bounding box has the background color (0) in the input grid, update its color to the `fill_color` in the output grid.
9.  Return the modified output grid.
