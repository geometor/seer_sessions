
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

Okay, let's analyze the provided examples.

## Perception

1.  **Input/Output Size:** Both input and output grids are 10x10 in both examples.
2.  **Colors:** The input grids contain white (0) and gray (5) pixels. The output grids contain white (0), gray (5), and azure (8) pixels.
3.  **Key Object:** The central element in the input is a shape made of gray (5) pixels. This shape appears to be a frame or boundary, enclosing a region of white (0) pixels. The frame is not always fully closed; it has gaps.
    *   In `train_1`, the gray shape resembles a large 'C' connected to a horizontal line segment below it. The gap is on the top edge.
    *   In `train_2`, the gray shape is a rectangle with a gap in the middle of the bottom edge.
4.  **Transformation:**
    *   The original gray (5) frame remains unchanged in the output grid.
    *   The white (0) region *inside* the gray frame is filled with azure (8) pixels.
    *   There are additional azure (8) pixels extending outwards from the location of the gap(s) in the original gray frame.
        *   In `train_1`, the gap was on the top edge, and a vertical line of azure pixels extends *upwards* from the gap location to the top edge of the grid.
        *   In `train_2`, the gap was on the bottom edge, and a vertical line of azure pixels extends *downwards* from the gap location to the bottom edge of the grid.
5.  **Inferred Logic:** The process seems to involve identifying the gray boundary, filling the area it encloses with azure, identifying gaps in the boundary that are adjacent to the filled area, and extending the azure color outwards from these gaps towards the grid edge.

## Facts


```yaml
task_context:
  grid_size_input: [10, 10]
  grid_size_output: [10, 10]
  colors_input: [white, gray]
  colors_output: [white, gray, azure]

elements:
  - object: frame
    description: A contiguous shape made of gray (5) pixels acting as a boundary.
    properties:
      - color: gray (5)
      - shape: variable, generally forms a perimeter
      - connectivity: contiguous
      - may_contain_gaps: true
  - object: interior_region
    description: The area(s) of white (0) pixels enclosed by the gray frame.
    properties:
      - color: white (0)
      - location: inside the boundary defined by the frame
  - object: background
    description: The area of white (0) pixels outside the gray frame.
    properties:
      - color: white (0)
      - location: outside the boundary defined by the frame
  - object: filled_shape
    description: The shape formed by azure (8) pixels in the output.
    properties:
      - color: azure (8)
      - comprises:
          - the filled interior_region
          - extensions originating from gaps in the frame

relationships:
  - type: spatial
    description: The gray frame encloses the interior_region.
  - type: adjacency
    description: Gaps in the frame are white pixels adjacent to both the frame (gray) and the filled interior (azure).

actions:
  - action: identify_frame
    description: Locate the contiguous block of gray (5) pixels.
  - action: identify_interior
    description: Determine the white (0) pixels enclosed by the frame.
  - action: fill_interior
    input: interior_region
    output: interior_region pixels changed to azure (8)
    color_change: white (0) -> azure (8)
  - action: identify_gaps
    description: Find white (0) pixels adjacent to both frame pixels (gray, 5) and filled interior pixels (azure, 8).
  - action: extend_from_gaps
    description: For each gap pixel, draw a line of azure (8) pixels outwards towards the grid edge.
    details: The direction of extension is perpendicular to the local orientation of the frame at the gap.
```


## Natural Language Program

1.  Copy the input grid to the output grid.
2.  Identify the contiguous object composed of gray (5) pixels (the "frame").
3.  Identify all white (0) pixels that are enclosed within the boundary formed by the gray frame (the "interior"). A flood fill starting from a known interior point, bounded by the gray pixels, can achieve this. Alternatively, flood fill from the grid edges/corners with a temporary marker, and any remaining white pixels are interior.
4.  Change the color of all identified interior pixels in the output grid from white (0) to azure (8).
5.  Scan the output grid to find all white (0) pixels ("gap pixels") that meet these conditions:
    a.  The pixel is orthogonally adjacent to at least one gray (5) frame pixel.
    b.  The pixel is orthogonally adjacent to at least one azure (8) pixel (which was part of the filled interior).
6.  For each identified gap pixel at coordinates `(r, c)`:
    a.  Determine the orthogonal direction `(dr, dc)` that points from an adjacent interior azure pixel towards the gap pixel `(r, c)`. This defines the extension direction.
    b.  Starting from the gap pixel `(r, c)`, continue changing pixels to azure (8) in the direction `(dr, dc)` (i.e., `(r + k*dr, c + k*dc)` for `k=0, 1, 2,...`) until the boundary of the grid is reached.
