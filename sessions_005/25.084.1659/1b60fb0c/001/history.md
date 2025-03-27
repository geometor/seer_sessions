
## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 1 1 1 1 1 0 0
0 0 0 1 1 1 1 1 0 0
0 0 0 0 0 1 0 0 1 1
0 0 0 0 0 1 0 0 1 1
0 0 0 0 0 1 1 1 1 1
0 0 0 0 0 1 0 0 1 1
0 0 0 0 0 1 0 0 1 1
0 0 0 1 1 1 1 1 0 0
0 0 0 1 1 1 1 1 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 1 1 1 1 1 0 0
0 0 0 1 1 1 1 1 0 0
0 2 2 0 0 1 0 0 1 1
0 2 2 0 0 1 0 0 1 1
0 2 2 2 2 1 1 1 1 1
0 2 2 0 0 1 0 0 1 1
0 2 2 0 0 1 0 0 1 1
0 0 0 1 1 1 1 1 0 0
0 0 0 1 1 1 1 1 0 0
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 1 1 1 0 0 0 0
0 0 0 0 1 1 0 0 0 0
0 0 0 0 1 0 0 0 1 0
0 0 0 0 1 1 1 1 1 0
0 0 0 0 1 1 0 1 1 0
0 0 0 0 0 1 0 0 0 0
0 0 0 0 1 1 0 0 0 0
0 0 0 0 1 1 1 0 0 0
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 1 1 1 0 0 0 0
0 0 0 0 1 1 0 0 0 0
0 0 0 0 1 0 0 0 1 0
0 2 2 0 1 1 1 1 1 0
0 2 2 2 1 1 0 1 1 0
0 2 0 0 0 1 0 0 0 0
0 0 0 0 1 1 0 0 0 0
0 0 0 0 1 1 1 0 0 0
0 0 0 0 0 0 0 0 0 0
```


## train_3

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 1 1 1 1 1 0 0
0 0 0 0 0 1 0 0 0 0
0 0 0 0 1 1 1 0 0 1
0 0 0 0 0 1 0 1 0 1
0 0 0 0 0 1 1 1 1 1
0 0 0 0 0 1 0 1 0 1
0 0 0 0 1 1 1 0 0 1
0 0 0 0 0 1 0 0 0 0
0 0 0 1 1 1 1 1 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 1 1 1 1 1 0 0
0 0 0 0 0 1 0 0 0 0
0 2 0 0 1 1 1 0 0 1
0 2 0 2 0 1 0 1 0 1
0 2 2 2 2 1 1 1 1 1
0 2 0 2 0 1 0 1 0 1
0 2 0 0 1 1 1 0 0 1
0 0 0 0 0 1 0 0 0 0
0 0 0 1 1 1 1 1 0 0
```

**Perception:**

1.  **Input/Output Structure:** Both input and output grids are the same size in each example. The background is white (0).
2.  **Objects:** The main object in each input grid is a complex shape composed of blue (1) pixels.
3.  **Transformation:** The transformation modifies the input grid by changing the color of *some* white (0) pixels to red (2). The original blue (1) pixels remain unchanged.
4.  **Pattern:** The white pixels that change to red appear to be those located *inside* the enclosed areas formed by the blue shape. White pixels outside the main blue shape or connected to the grid boundary without crossing the blue shape remain white.
5.  **Enclosure:** The key operation is identifying regions of white pixels that are fully surrounded or enclosed by the blue pixels. These enclosed white regions are then "filled" with red.

**Facts:**


```yaml
task_description: "Identify contiguous regions of white pixels enclosed by blue pixels and change their color to red."
elements:
  - element: "grid"
    description: "A 2D array of pixels with integer values representing colors."
  - element: "pixel"
    description: "A single cell in the grid."
    properties:
      - color: "Represented by integers 0-9. In this task, relevant colors are white (0), blue (1), and red (2)."
      - position: "Coordinates (row, column) within the grid."
  - element: "object"
    description: "A contiguous group of pixels of the same non-white color. In this task, the primary object is the blue shape."
    properties:
      - color: "Blue (1)"
      - shape: "Variable, forms boundaries."
  - element: "region"
    description: "A contiguous group of pixels of the same color."
    properties:
      - color: "White (0) in the input."
      - connectivity: "Pixels are connected horizontally or vertically."
      - relationship_to_boundary: "Can be connected to the grid edge or enclosed by other colors."
actions:
  - action: "identify_enclosed_regions"
    description: "Find all contiguous regions of white (0) pixels that are completely surrounded by blue (1) pixels and do not touch the grid boundary."
    inputs:
      - "input grid"
    outputs:
      - "set of coordinates corresponding to enclosed white pixels"
  - action: "change_color"
    description: "Modify the color of specific pixels."
    inputs:
      - "grid"
      - "set of coordinates"
      - "new color (Red - 2)"
    outputs:
      - "modified grid"
relationships:
  - relationship: "enclosure"
    description: "A region of white pixels is enclosed if any path from a pixel within that region to the grid boundary must cross a blue pixel."
    entities:
      - "white region"
      - "blue object"
      - "grid boundary"
  - relationship: "connectivity"
    description: "Pixels of the same color are connected if they are adjacent horizontally or vertically."
    entities:
      - "pixels"
constants:
  - name: "background_color"
    value: 0 # white
  - name: "boundary_color"
    value: 1 # blue
  - name: "fill_color"
    value: 2 # red
```


**Natural Language Program:**

1.  Initialize the output grid as a copy of the input grid.
2.  Identify all white (0) pixels in the input grid that are connected to any of the four boundaries (top, bottom, left, right) through a path consisting only of white (0) pixels. Mark these pixels as "exterior white". Connectivity is defined by horizontal and vertical adjacency. (A common way to implement this is using a flood fill algorithm starting from all white boundary pixels).
3.  Iterate through all pixels in the input grid.
4.  If a pixel is white (0) and has *not* been marked as "exterior white", then it is an "enclosed white" pixel.
5.  Change the color of this "enclosed white" pixel in the output grid to red (2).
6.  Leave all other pixels (blue pixels and "exterior white" pixels) in the output grid unchanged from their original input color.
7.  Return the modified output grid.
