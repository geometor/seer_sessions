
## train_1

**input:**
```
0 0 0 0 0 1 0 0 0 0
0 0 0 0 0 0 0 0 0 0
1 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 1
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 1 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 1 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 1
```


**output:**
```
0 0 0 0 7 1 6 0 0 0
2 0 0 0 0 8 0 0 0 0
1 6 0 0 0 0 0 0 0 2
8 0 0 0 0 0 0 0 7 1
0 0 0 0 0 2 0 0 0 8
0 0 0 0 7 1 6 0 0 0
0 0 0 0 0 8 0 0 0 0
0 0 2 0 0 0 0 0 0 0
0 7 1 6 0 0 0 0 0 2
0 0 8 0 0 0 0 0 7 1
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 1 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 1
0 0 0 0 0 0 0 0 0 0
0 0 0 1 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 1 0 0
0 0 0 0 0 0 0 0 0 0
0 1 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 2 0 0 0
0 0 0 0 0 7 1 6 0 0
0 0 0 0 0 0 8 0 0 2
0 0 0 0 0 0 0 0 7 1
0 0 0 2 0 0 0 0 0 8
0 0 7 1 6 0 0 0 0 0
0 0 0 8 0 0 0 2 0 0
0 0 0 0 0 0 7 1 6 0
0 2 0 0 0 0 0 8 0 0
7 1 6 0 0 0 0 0 0 0
```

Okay, let's break down this task.

**Perception**

1.  **Input/Output Grids:** Both input and output grids have the same dimensions (10x10 in the examples).
2.  **Input Colors:** The input grids contain only white (0) background pixels and blue (1) pixels. The blue pixels appear as isolated single points.
3.  **Output Colors:** The output grids contain the original blue (1) pixels at their original locations. Additionally, new colors appear around these blue pixels: red (2), orange (7), magenta (6), and azure (8). The background remains white (0).
4.  **Transformation Pattern:** The transformation seems centered around the blue pixels found in the input. Each blue pixel acts as a "source" that colors its immediate orthogonal (up, down, left, right) neighbors in the output grid, provided those neighbors are within the grid boundaries.
5.  **Color Mapping:** There's a consistent mapping based on the relative position to the blue pixel:
    *   The pixel *above* the blue pixel becomes red (2).
    *   The pixel *below* the blue pixel becomes azure (8).
    *   The pixel *to the left* of the blue pixel becomes orange (7).
    *   The pixel *to the right* of the blue pixel becomes magenta (6).
6.  **Boundary Conditions:** If a potential neighbor position is outside the grid (e.g., trying to color the cell above a blue pixel in the top row), no coloring occurs for that specific direction.
7.  **Overlapping:** In the given examples, the blue pixels are sufficiently far apart that the colored neighborhoods do not overlap. The rule for overlapping colored pixels is not explicitly demonstrated but is not needed for these examples. The original blue pixels are preserved in the output.

**Facts**


```yaml
task_type: pattern_coloring
grid_properties:
  - dimensions: constant (input and output grids have the same height and width)
  - background_color: white (0)
input_objects:
  - object_type: pixel
    color: blue (1)
    shape: single_pixel
    distribution: scattered, non-adjacent in examples
output_objects:
  - object_type: pixel
    color: blue (1)
    origin: copied from input
    location: same as input
  - object_type: pixel pattern
    shape: cross-like (up to 4 pixels orthogonally adjacent to a source blue pixel)
    colors: [red (2), azure (8), orange (7), magenta (6)]
    relationship_to_input_blue:
      - red (2): located 1 step above the blue pixel
      - azure (8): located 1 step below the blue pixel
      - orange (7): located 1 step left of the blue pixel
      - magenta (6): located 1 step right of the blue pixel
transformation_rule:
  - type: local_coloring
  - source: blue (1) pixels in the input
  - target: orthogonal neighbors of the source pixels
  - conditions: target pixel must be within grid boundaries
  - color_assignment: deterministic based on relative position (Up->Red, Down->Azure, Left->Orange, Right->Magenta)
  - preservation: source blue pixels are kept in the output
  - background_handling: background white pixels remain white unless colored by the rule
```


**Natural Language Program**

1.  Create a new grid with the same dimensions as the input grid, initially copying all pixel values from the input grid.
2.  Iterate through each pixel of the input grid by its row (r) and column (c).
3.  If the pixel at input grid location (r, c) is blue (1):
    a.  Identify the location above: (r-1, c). If this location is within the grid boundaries, set the pixel at this location in the *output* grid to red (2).
    b.  Identify the location below: (r+1, c). If this location is within the grid boundaries, set the pixel at this location in the *output* grid to azure (8).
    c.  Identify the location to the left: (r, c-1). If this location is within the grid boundaries, set the pixel at this location in the *output* grid to orange (7).
    d.  Identify the location to the right: (r, c+1). If this location is within the grid boundaries, set the pixel at this location in the *output* grid to magenta (6).
4.  After checking all pixels in the input grid, return the final output grid.
