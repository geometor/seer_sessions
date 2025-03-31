
## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 2 7 0 0 0 0 0
0 0 0 2 7 7 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
3 3 3 3 3 3 3 3 3 3
3 3 3 3 3 3 3 3 3 3
3 3 3 3 3 3 3 3 3 3
3 3 3 3 3 3 3 3 3 3
3 3 3 7 7 3 3 3 3 3
3 3 7 7 7 7 3 3 3 3
3 3 3 3 3 3 3 3 3 3
3 3 3 3 3 3 3 3 3 3
3 3 3 3 3 3 3 3 3 3
3 3 3 3 3 3 3 3 3 3
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 2 2 0 0 0 0 0
0 0 0 6 6 0 0 0 0 0
0 0 0 0 6 0 0 0 0 0
0 0 0 0 6 6 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
3 3 3 3 3 3 3 3 3 3
3 3 3 3 6 6 3 3 3 3
3 3 3 3 6 3 3 3 3 3
3 3 3 6 6 3 3 3 3 3
3 3 3 6 6 3 3 3 3 3
3 3 3 3 6 3 3 3 3 3
3 3 3 3 6 6 3 3 3 3
3 3 3 3 3 3 3 3 3 3
3 3 3 3 3 3 3 3 3 3
3 3 3 3 3 3 3 3 3 3
```


## train_3

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 8 8 8 0 0 0 0
0 0 0 0 0 8 0 0 0 0
0 0 0 0 0 2 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
3 3 3 3 3 3 3 3 3 3
3 3 3 3 3 3 3 3 3 3
3 3 3 3 3 3 3 3 3 3
3 3 3 3 3 3 3 3 3 3
3 3 3 8 8 8 3 3 3 3
3 3 3 3 3 8 3 3 3 3
3 3 3 3 3 8 3 3 3 3
3 3 3 8 8 8 3 3 3 3
3 3 3 3 3 3 3 3 3 3
3 3 3 3 3 3 3 3 3 3
```


## train_4

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 4 2 0 0 0 0
0 0 4 4 4 2 0 0 0 0
0 0 0 0 4 2 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
3 3 3 3 3 3 3 3 3 3
3 3 3 3 3 3 3 3 3 3
3 3 3 3 3 3 3 3 3 3
3 3 3 3 4 4 3 3 3 3
3 3 4 4 4 4 4 4 3 3
3 3 3 3 4 4 3 3 3 3
3 3 3 3 3 3 3 3 3 3
3 3 3 3 3 3 3 3 3 3
3 3 3 3 3 3 3 3 3 3
3 3 3 3 3 3 3 3 3 3
```

**Perception**

The task involves transforming an input grid into an output grid of the same dimensions (10x10 in the examples). The transformation primarily affects the colors of the pixels.

1.  **Background Transformation**: The background color, consistently white (0) in the inputs, is uniformly changed to green (3) in the outputs.
2.  **Object Identification**: Each input grid contains a single composite object made of two distinct non-background colors. One of these colors is always red (2). The other color varies across examples (orange (7), magenta (6), azure (8), yellow (4)). Let's call the non-red color the "primary" color.
3.  **Color Replacement**: The core transformation happens within the composite object. The pixels originally colored red (2) are replaced with the primary color identified in that specific input grid. The pixels that were originally the primary color remain unchanged.
4.  **Shape Preservation/Modification**: The overall shape occupied by the non-background colors is preserved, but the internal color distribution changes. Effectively, the primary color "fills" the areas previously occupied by the red color within the same composite object. The red color acts like a marker indicating areas to be filled by the adjacent primary color.

**Facts**


```yaml
task_description: Transforms a grid by changing the background color and filling 'marker' colored areas within shapes with the shape's primary color.

grid_properties:
  - size: Input and output grids have the same dimensions.
  - background_color: Input background is white (0). Output background is green (3).

objects:
  - id: background
    description: The area of the grid with the background color (white 0 in input).
    properties:
      - color: white (0) in input, green (3) in output.
  - id: composite_shape
    description: A single contiguous or non-contiguous shape composed of two non-background colors.
    properties:
      - colors: Always includes red (2) and one other 'primary' color (e.g., orange, magenta, azure, yellow).
    components:
      - id: marker_part
        description: The portion of the composite shape colored red (2).
        properties:
          - color: red (2) in input.
      - id: primary_part
        description: The portion of the composite shape with the non-red color.
        properties:
          - color: Varies per example (e.g., orange 7, magenta 6, azure 8, yellow 4) - referred to as 'primary_color'.

actions:
  - name: change_background
    input: background pixels (white 0)
    output: green (3) pixels
  - name: identify_colors
    input: input grid
    output: Identification of the background color (0), the marker color (2), and the primary color (the other non-zero color).
  - name: fill_marker_area
    input: pixels with marker color (red 2)
    output: pixels changed to the identified primary color for that grid.
    condition: This action applies to all red (2) pixels.

relationships:
  - type: color_correspondence
    description: Red (2) pixels in the input become the 'primary_color' in the output. The 'primary_color' pixels remain the same. White (0) pixels become green (3).
  - type: object_structure
    description: The red (2) and primary color pixels form a combined shape in the input. The transformation modifies the color composition of this shape.
```


**Natural Language Program**

1.  Initialize the output grid as a copy of the input grid.
2.  Identify the two non-background colors present in the input grid. One color will be red (2) (the marker color), and the other will be the primary color (e.g., orange, magenta, azure, yellow).
3.  Iterate through each pixel of the input grid.
4.  If the pixel's color is white (0), change its color to green (3) in the output grid.
5.  If the pixel's color is red (2), change its color to the identified primary color in the output grid.
6.  If the pixel's color is the identified primary color, keep its color the same in the output grid.
7.  Return the modified grid as the final output.
