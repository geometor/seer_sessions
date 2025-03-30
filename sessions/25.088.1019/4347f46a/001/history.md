
## train_1

**input:**
```
0 0 0 0 0 0 0
0 2 2 2 2 2 0
0 2 2 2 2 2 0
0 2 2 2 2 2 0
0 2 2 2 2 2 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0
0 2 2 2 2 2 0
0 2 0 0 0 2 0
0 2 0 0 0 2 0
0 2 2 2 2 2 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 8 8 8 8 0 0 0 0 0 0 0 0 0 0 0
0 8 8 8 8 0 0 0 0 0 0 0 0 0 0 0
0 8 8 8 8 0 3 3 3 3 3 3 3 0 0 0
0 0 0 0 0 0 3 3 3 3 3 3 3 0 0 0
0 0 0 0 0 0 3 3 3 3 3 3 3 0 0 0
0 0 0 0 0 0 3 3 3 3 3 3 3 0 0 0
0 0 0 0 0 0 3 3 3 3 3 3 3 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 6 6 6 6 6 6 6 0 0 0 7 7 7 0
0 0 6 6 6 6 6 6 6 0 0 0 7 7 7 0
0 0 6 6 6 6 6 6 6 0 0 0 7 7 7 0
0 0 6 6 6 6 6 6 6 0 0 0 7 7 7 0
0 0 0 0 0 0 0 0 0 0 0 0 7 7 7 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 8 8 8 8 0 0 0 0 0 0 0 0 0 0 0
0 8 0 0 8 0 0 0 0 0 0 0 0 0 0 0
0 8 8 8 8 0 3 3 3 3 3 3 3 0 0 0
0 0 0 0 0 0 3 0 0 0 0 0 3 0 0 0
0 0 0 0 0 0 3 0 0 0 0 0 3 0 0 0
0 0 0 0 0 0 3 0 0 0 0 0 3 0 0 0
0 0 0 0 0 0 3 3 3 3 3 3 3 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 6 6 6 6 6 6 6 0 0 0 7 7 7 0
0 0 6 0 0 0 0 0 6 0 0 0 7 0 7 0
0 0 6 0 0 0 0 0 6 0 0 0 7 0 7 0
0 0 6 6 6 6 6 6 6 0 0 0 7 0 7 0
0 0 0 0 0 0 0 0 0 0 0 0 7 7 7 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


## train_3

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0
0 0 5 5 5 5 5 5 5 5 0 0
0 0 5 5 5 5 5 5 5 5 0 0
0 0 5 5 5 5 5 5 5 5 0 0
0 0 5 5 5 5 5 5 5 5 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 4 4 4 4 4 4 0 0 0 0 0
0 4 4 4 4 4 4 0 0 0 0 0
0 4 4 4 4 4 4 0 0 0 0 0
0 4 4 4 4 4 4 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0
0 0 5 5 5 5 5 5 5 5 0 0
0 0 5 0 0 0 0 0 0 5 0 0
0 0 5 0 0 0 0 0 0 5 0 0
0 0 5 5 5 5 5 5 5 5 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 4 4 4 4 4 4 0 0 0 0 0
0 4 0 0 0 0 4 0 0 0 0 0
0 4 0 0 0 0 4 0 0 0 0 0
0 4 4 4 4 4 4 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

## Perception

The input grids contain one or more solid rectangular objects of various colors (red, azure, green, magenta, orange, gray, yellow) on a white background. The background color is always white (0).
The output grids show the same rectangular objects, but their interiors have been changed to white (0). Only the pixels forming the border of each original rectangle retain their original color. The transformation identifies solid, non-white rectangles and effectively "hollows" them out, leaving only the perimeter.

## Facts


```yaml
objects:
  - type: rectangle
    properties:
      - color: any non-white color (1-9)
      - fill: solid
      - shape: rectangular
      - location: anywhere on the grid
      - background: surrounded by white (0) pixels, or grid edges.
relationships:
  - between: input_pixel, output_pixel
    rule: If an input pixel is part of the interior of a solid rectangle (not on its border), its corresponding output pixel becomes white (0).
  - between: input_pixel, output_pixel
    rule: If an input pixel is part of the border of a solid rectangle, its corresponding output pixel retains the original color.
  - between: input_pixel, output_pixel
    rule: If an input pixel is white (0), its corresponding output pixel remains white (0).
actions:
  - name: identify_rectangles
    description: Find all contiguous blocks of non-white pixels that form a solid rectangle.
  - name: hollow_rectangle
    description: For each identified rectangle, change the color of its interior pixels to white (0).
    details:
      - The border pixels (top, bottom, left, right edges) of the rectangle keep their original color.
      - Only pixels that are *not* part of the border are changed to white.
```


## Natural Language Program

1.  Identify all distinct, solid, non-white rectangular objects within the input grid. An object is a contiguous group of pixels of the same non-white color. A rectangle is identified by its top-left and bottom-right coordinates.
2.  For each identified rectangle:
    a.  Determine the coordinates of its border pixels.
    b.  Iterate through all pixels within the bounds of the rectangle (inclusive of the border).
    c.  If a pixel is *not* part of the border (i.e., it is an interior pixel), change its color to white (0) in the output grid.
    d.  If a pixel *is* part of the border, keep its original color in the output grid.
3.  All pixels in the input grid that are not part of any identified rectangle (i.e., the background white pixels) remain white (0) in the output grid.
4.  The output grid has the same dimensions as the input grid.
