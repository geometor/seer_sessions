
## train_1

**input:**
```
0 0 0 2 2 0 0 0 2 0 0 0 2 2 2 0 0 0 2 2 0 0 0
```


**output:**
```
0 0 0 3 3 0 0 0 7 0 0 0 1 1 1 0 0 0 3 3 0 0 0
```


## train_2

**input:**
```
0 2 0 0 0 2 2 2 0 2 2 0 2 0 2 0 0 0 0 0 0 0 0
```


**output:**
```
0 7 0 0 0 1 1 1 0 3 3 0 7 0 7 0 0 0 0 0 0 0 0
```


## train_3

**input:**
```
0 0 2 2 0 0 0 2 2 2 0 0 0 2 0 0 2 0 0 0 2 0 0
```


**output:**
```
0 0 3 3 0 0 0 1 1 1 0 0 0 7 0 0 7 0 0 0 7 0 0
```

Okay, I will analyze the provided examples to understand the transformation rule.

## Perception

1.  **Input Grid Contents**: The input grids primarily consist of a white (0) background and several distinct "objects" composed of contiguous red (2) pixels. These objects vary in size (number of connected pixels).
2.  **Output Grid Contents**: The output grids retain the white (0) background in the same positions. The locations previously occupied by red (2) pixels are now filled with different colors: blue (1), green (3), or orange (7).
3.  **Transformation Observation**: The core transformation appears to be a recoloring of the red objects based on their size. The white background remains unchanged.
4.  **Color Mapping Rule**: By comparing the input and output across the examples, a consistent pattern emerges:
    *   Red objects consisting of a single pixel (size 1) are transformed into orange (7).
    *   Red objects consisting of two contiguous pixels (size 2) are transformed into green (3).
    *   Red objects consisting of three contiguous pixels (size 3) are transformed into blue (1).
5.  **Object Definition**: An "object" is defined as a group of one or more red (2) pixels that are connected either horizontally or vertically (adjacent sides). Diagonal connections do not seem to constitute a single object based on the examples.

## YAML Facts


```yaml
task_description: Recolor contiguous red objects based on their size.
background_color: 0 # white
input_object_color: 2 # red
output_colors_map:
  1: 7 # orange
  2: 3 # green
  3: 1 # blue
objects:
  - type: contiguous_pixels
    color: 2 # red
    connectivity: von_neumann # horizontal/vertical adjacency
properties:
  - name: size
    description: Number of pixels in the contiguous object.
action:
  type: recolor_objects
  input_color: 2 # red
  rules:
    - condition: object_size == 1
      output_color: 7 # orange
    - condition: object_size == 2
      output_color: 3 # green
    - condition: object_size == 3
      output_color: 1 # blue
  fallback: Keep original color (applies to background)
```


## Natural Language Program

1.  Create a copy of the input grid to serve as the output grid.
2.  Identify all distinct contiguous objects composed of red (2) pixels in the input grid. Use 4-connectivity (only horizontal and vertical neighbors count as connected).
3.  For each identified red object:
    a.  Calculate the size of the object (the number of red pixels it contains).
    b.  Determine the target color based on the object's size:
        *   If the size is 1, the target color is orange (7).
        *   If the size is 2, the target color is green (3).
        *   If the size is 3, the target color is blue (1).
    c.  In the output grid, change the color of all pixels belonging to this object to the determined target color.
4.  Leave all pixels that were originally white (0) unchanged in the output grid.
5.  Return the modified output grid.
