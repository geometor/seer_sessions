
## train_1

**input:**
```
0 0 0 2 0 2 0 0 0
0 0 2 3 2 2 0 0 0
0 0 0 0 2 0 0 0 0
0 0 0 0 0 0 0 0 0
1 1 1 1 1 1 1 1 1
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 3 0 3 0 0 0
0 0 3 2 3 3 0 0 0
0 0 0 0 3 0 0 0 0
0 0 0 0 0 0 0 0 0
1 1 1 1 1 1 1 1 1
0 0 0 0 0 0 0 0 0
0 0 0 0 2 0 0 0 0
0 0 2 3 2 2 0 0 0
0 0 0 2 0 2 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 0 0 0 0 1 0 0 0 0 0
0 0 0 0 0 0 1 0 0 0 0 0
0 0 0 0 0 0 1 0 8 0 8 0
0 0 0 0 0 0 1 0 0 8 4 0
0 0 0 0 0 0 1 0 8 8 8 0
0 0 0 0 0 0 1 0 0 0 0 0
0 0 0 0 0 0 1 0 0 0 0 0
0 0 0 0 0 0 1 0 0 0 0 0
0 0 0 0 0 0 1 0 0 0 0 0
0 0 0 0 0 0 1 0 0 0 0 0
0 0 0 0 0 0 1 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 1 0 0 0 0 0
0 0 0 0 0 0 1 0 0 0 0 0
0 0 8 0 8 0 1 0 4 0 4 0
0 0 4 8 0 0 1 0 0 4 8 0
0 0 8 8 8 0 1 0 4 4 4 0
0 0 0 0 0 0 1 0 0 0 0 0
0 0 0 0 0 0 1 0 0 0 0 0
0 0 0 0 0 0 1 0 0 0 0 0
0 0 0 0 0 0 1 0 0 0 0 0
0 0 0 0 0 0 1 0 0 0 0 0
0 0 0 0 0 0 1 0 0 0 0 0
```


## train_3

**input:**
```
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
1 1 1 1 1 1 1 1 1 1 1
0 0 0 0 0 0 0 0 0 0 0
0 0 5 6 6 5 0 0 0 0 0
0 0 6 6 6 6 0 0 0 0 0
0 0 6 0 0 6 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 6 0 0 6 0 0 0 0 0
0 0 6 6 6 6 0 0 0 0 0
0 0 5 6 6 5 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
1 1 1 1 1 1 1 1 1 1 1
0 0 0 0 0 0 0 0 0 0 0
0 0 6 5 5 6 0 0 0 0 0
0 0 5 5 5 5 0 0 0 0 0
0 0 5 0 0 5 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

## Perception

1.  **Blue Line:** Each example features a single, straight line composed entirely of blue (1) pixels. This line can be either horizontal (examples 1 and 3) or vertical (example 2).
2.  **Source Object(s):** On one side of the blue line, there is an object (or multiple disconnected pixels forming a pattern) composed of colors other than white (0) and blue (1).
3.  **Transformation:** The core transformation involves reflecting the source object(s) across the blue line to the other side.
4.  **Reflection Axis:** The blue line acts as the axis of reflection.
5.  **Color Swapping:** During the reflection process, the colors of the pixels in the reflected object are swapped according to specific pairs observed across the examples:
    *   Red (2) becomes Green (3), and Green (3) becomes Red (2). (Example 1)
    *   Azure (8) becomes Yellow (4), and Yellow (4) becomes Azure (8). (Example 2)
    *   Gray (5) becomes Magenta (6), and Magenta (6) becomes Gray (5). (Example 3)
6.  **Preservation:** The original blue line and the original source object(s) remain unchanged in their positions and colors in the output grid. The reflection is additive; it creates a new object without modifying the original.
7.  **Symmetry:** The output grid exhibits symmetry across the blue line, considering the color swaps. The distance of each pixel in the reflected object from the blue line is the same as the distance of its corresponding pixel in the source object.

## Facts


```yaml
version: 1.0
facts:
  - id: blue_line
    type: object
    description: A contiguous straight line of blue (1) pixels.
    properties:
      - orientation: Either horizontal or vertical.
      - role: Acts as the axis of reflection.

  - id: source_object
    type: object
    description: A contiguous or non-contiguous group of pixels with colors other than white (0) or blue (1).
    properties:
      - location: Situated entirely on one side of the blue_line.
      - colors: Composed of pairs like (red/green), (azure/yellow), or (gray/magenta).

  - id: reflection_action
    type: action
    description: Mirroring the source_object across the blue_line.
    parameters:
      - object: source_object
      - axis: blue_line
    results:
      - Creates a reflected_object on the opposite side of the blue_line.
      - Preserves the perpendicular distance from the blue_line for each pixel.

  - id: color_swap_action
    type: action
    description: Modifying the colors of the pixels during the reflection_action.
    conditions: Applies only to the pixels of the reflected_object.
    rules:
      - if color is red (2), change to green (3).
      - if color is green (3), change to red (2).
      - if color is azure (8), change to yellow (4).
      - if color is yellow (4), change to azure (8).
      - if color is gray (5), change to magenta (6).
      - if color is magenta (6), change to gray (5).

  - id: output_grid_composition
    type: relationship
    description: The final output grid contains the original input grid elements plus the newly created reflected_object with swapped colors.
    components:
      - original_input_grid_pixels
      - reflected_object_pixels (with swapped colors)
```


## Natural Language Program

1.  **Identify the Reflection Axis:** Scan the input grid to find the continuous straight line of blue (1) pixels. Determine if it is horizontal or vertical.
2.  **Identify Source Pixels:** Locate all pixels in the input grid that are not white (0) and not part of the blue (1) line. These are the source pixels. Note their coordinates (row, column) and colors. (Assume these pixels will always be entirely on one side of the blue line).
3.  **Create the Output Grid:** Initialize the output grid as an identical copy of the input grid.
4.  **Perform Reflection and Color Swapping:**
    *   For each identified source pixel:
        *   Calculate its reflection coordinates across the blue line.
            *   If the line is horizontal at row `R`: a source pixel at `(r, c)` reflects to `(R + (R - r), c)`.
            *   If the line is vertical at column `C`: a source pixel at `(r, c)` reflects to `(r, C + (C - c))`.
        *   Determine the swapped color for the source pixel based on the following pairs:
            *   Red (2) <-> Green (3)
            *   Azure (8) <-> Yellow (4)
            *   Gray (5) <-> Magenta (6)
        *   Place the swapped color at the calculated reflection coordinates in the output grid.
5.  **Finalize:** The output grid now contains the original elements plus the reflected, color-swapped pattern.
