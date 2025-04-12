**Perception**

The task involves processing a 2D grid containing various colored pixels. The input grid features multiple small "objects," defined as contiguous blocks of non-white pixels. The output grid retains only a subset of these objects, and the retained objects are always 2x2 squares, filled entirely with the color of the original object. Objects in the input that do not have a bounding box of exactly 2x2 are removed (their pixels are turned white) in the output. The core transformation identifies objects based on their spatial extent (specifically, a 2x2 bounding box) and standardizes their shape to a filled 2x2 square while preserving their color.

**Facts**


```yaml
task_context: Grid transformation focusing on object properties.
components:
  - item: Grid
    attributes:
      - 2D array of integers (0-9) representing colors.
      - Contains background (white, 0) and foreground pixels (non-white).
  - item: Object
    description: A contiguous block of one or more pixels of the same non-white color.
    attributes:
      - color: The integer value (1-9) of the pixels comprising the object.
      - pixels: Set of coordinates (row, col) belonging to the object.
      - bounding_box: The minimal rectangle enclosing all pixels of the object.
        properties:
          - top_left_corner: (min_row, min_col)
          - bottom_right_corner: (max_row, max_col)
          - height: max_row - min_row + 1
          - width: max_col - min_col + 1
relationships:
  - type: Selection criteria
    based_on: Object bounding box dimensions.
    condition: Height must be 2 AND Width must be 2.
actions:
  - action: Identify Objects
    actor: System
    input: Input grid
    output: List of identified objects with their properties (color, pixels, bounding_box).
  - action: Filter Objects
    actor: System
    input: List of identified objects
    condition: Keep only objects where bounding_box height == 2 and bounding_box width == 2.
    output: List of filtered objects.
  - action: Generate Output Grid
    actor: System
    input: Filtered objects and input grid dimensions.
    process: Create a new grid of the same dimensions as the input, initialized to white (0). For each filtered object, fill the 2x2 area defined by its bounding box with the object's color.
    output: Output grid.
```


**Natural Language Program**

1.  Initialize the output grid as a copy of the input grid, entirely filled with the background color (white, 0).
2.  Identify all distinct contiguous objects formed by non-white pixels in the input grid.
3.  For each identified object:
    a.  Determine the color of the object.
    b.  Calculate the bounding box of the object (the smallest rectangle containing all its pixels).
    c.  Measure the height and width of the bounding box.
    d.  Check if the height is exactly 2 pixels and the width is exactly 2 pixels.
4.  If an object's bounding box dimensions are 2x2:
    a.  Locate the top-left corner coordinates of its bounding box in the input grid.
    b.  Fill the corresponding 2x2 area in the output grid (starting from the identified top-left corner) with the color of that object.
5.  Leave all other pixels in the output grid as the background color (white, 0).
6.  Return the final output grid.