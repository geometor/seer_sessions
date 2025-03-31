
## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 5 5 5 0 5 5 0 0
0 0 5 0 0 0 0 5 0 0
0 0 5 0 0 0 0 5 0 0
0 0 5 0 0 0 0 5 0 0
0 0 5 5 5 5 5 5 0 0
```


**output:**
```
0 0 0 0 0 8 0 0 0 0
0 0 0 0 0 8 0 0 0 0
0 0 0 0 0 8 0 0 0 0
0 0 0 0 0 8 0 0 0 0
0 0 0 0 0 8 0 0 0 0
0 0 5 5 5 8 5 5 0 0
0 0 5 8 8 8 8 5 0 0
0 0 5 8 8 8 8 5 0 0
0 0 5 8 8 8 8 5 0 0
0 0 5 5 5 5 5 5 0 0
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 5 5 5 5 5 5 0 0
0 0 5 0 0 0 0 5 0 0
0 0 5 0 0 0 0 5 0 0
0 0 5 0 0 0 0 5 0 0
0 0 5 0 0 0 0 5 0 0
0 0 5 5 5 0 5 5 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 5 5 5 5 5 5 0 0
0 0 5 8 8 8 8 5 0 0
0 0 5 8 8 8 8 5 0 0
0 0 5 8 8 8 8 5 0 0
0 0 5 8 8 8 8 5 0 0
0 0 5 5 5 8 5 5 0 0
0 0 0 0 0 8 0 0 0 0
0 0 0 0 0 8 0 0 0 0
```

**Perception of Elements:**

The task involves transforming a grid containing a single gray (5) shape on a white (0) background. The gray shape acts as a boundary or container. The transformation involves two main parts:

1.  **Filling the Interior:** The area enclosed by the gray shape, which is initially white, is filled with azure (8) pixels. This suggests a flood-fill or region-filling operation starting from a point inside the shape's boundary.
2.  **Adding an Exterior Line:** A vertical line of azure (8) pixels is added outside the gray shape. This line appears to be aligned with a vertical gap or axis of symmetry in the gray shape. The direction of this line (upwards or downwards) seems dependent on the vertical position of the gray shape within the grid. If the shape is predominantly in the lower half, the line extends upwards from the top edge. If the shape is predominantly in the upper half, the line extends downwards from the bottom edge. The line extends all the way to the grid boundary.

**YAML Facts:**


```yaml
task_description: Fill the interior of a gray shape with azure and add a vertical azure line extending outwards from the shape's gap, directed away from the shape's vertical center.

elements:
  - element: background
    color: white (0)
    role: Canvas for the main object.
  - element: shape
    color: gray (5)
    properties:
      - Forms a single connected component.
      - Acts as a boundary, enclosing a region of the background.
      - Has a vertical gap or opening, typically on one side (right side in examples).
    role: Defines the area to be filled and the reference for the exterior line.
  - element: fill_color
    color: azure (8)
    role: Used to fill the interior region and create the exterior line.

relationships:
  - type: containment
    element1: shape (gray)
    element2: background (white)
    description: The gray shape encloses a region of the white background.
  - type: adjacency
    element1: fill_color (azure)
    element2: shape (gray)
    description: The azure fill touches the inner boundary of the gray shape. The azure line touches the outer boundary (top or bottom edge) of the gray shape.
  - type: spatial
    element1: shape (gray)
    element2: grid
    description: The vertical position of the shape within the grid determines the direction of the exterior azure line.

actions:
  - action: identify_shape
    input: grid
    output: The single connected gray (5) object.
  - action: identify_interior
    input: grid, shape
    output: The white (0) region enclosed by the shape.
  - action: fill_interior
    input: interior_region
    output: Change the color of the interior region to azure (8).
  - action: identify_gap_column
    input: shape
    output: The column index corresponding to the vertical gap/symmetry axis of the shape.
  - action: determine_vertical_position
    input: shape, grid
    output: Whether the shape is primarily in the upper or lower half of the grid.
  - action: determine_extension_edge_and_direction
    input: shape, vertical_position
    output: The starting row (top or bottom edge of the shape) and direction (up or down) for the exterior line.
  - action: draw_exterior_line
    input: grid, gap_column, start_row, direction
    output: Add a vertical azure (8) line in the gap column, starting from the determined edge and extending to the grid boundary in the specified direction.
```


**Natural Language Program:**

1.  Identify the single connected object composed of gray (5) pixels in the input grid.
2.  Identify the region of white (0) pixels that is completely enclosed by the gray object.
3.  Change the color of all pixels within this enclosed region to azure (8).
4.  Determine the column index (or indices) that corresponds to the vertical opening or axis of symmetry of the gray object (where the shape is discontinuous vertically, observed on the right side in the examples). Let this be the `gap_column`.
5.  Find the vertical midpoint or center of mass of the gray object.
6.  Compare the object's vertical midpoint to the grid's vertical midpoint.
7.  If the object's midpoint is in the lower half of the grid:
    *   Find the topmost row (`start_row`) of the gray object within the `gap_column`.
    *   Change the color of pixels in the `gap_column` from `start_row - 1` up to the top edge of the grid (row 0) to azure (8).
8.  If the object's midpoint is in the upper half of the grid (or exactly centered):
    *   Find the bottommost row (`start_row`) of the gray object within the `gap_column`.
    *   Change the color of pixels in the `gap_column` from `start_row + 1` down to the bottom edge of the grid to azure (8).
9.  Leave the original gray (5) object unchanged.
10. The resulting grid is the output.
