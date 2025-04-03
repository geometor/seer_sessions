## Perception

The input grids consist of a white (0) background with several distinct, contiguous objects made of yellow (4) pixels.
The output grids maintain the same structure and background color, but the yellow objects have changed color.
Comparing the inputs and outputs across the examples reveals a consistent pattern: the final color of an object depends on its size (the number of pixels it contains).

*   In example 1, a single yellow pixel becomes red (2). Two adjacent yellow pixels become azure (8). Three adjacent yellow pixels become gray (5).
*   This pattern holds true for all yellow objects in all three examples.
*   Objects of size 1 (one yellow pixel) consistently become red (2).
*   Objects of size 2 (two contiguous yellow pixels) consistently become azure (8).
*   Objects of size 3 (three contiguous yellow pixels) consistently become gray (5).
*   The white background pixels remain unchanged.

The transformation rule involves identifying each distinct yellow object, determining its size, and then recoloring all pixels within that object based on a size-to-color mapping.

## Facts


```yaml
elements:
  - type: background
    color: white (0)
    relation: remains unchanged in the output
  - type: object
    color: yellow (4)
    shape: variable (contiguous blocks)
    properties:
      - size: number of pixels in the contiguous block
    action:
      - find_contiguous_objects: Identify all distinct groups of connected yellow pixels.
      - measure_size: Count the number of pixels in each identified object.
      - recolor_by_size: Change the color of all pixels within each object based on its size.
        mapping:
          - size: 1
            output_color: red (2)
          - size: 2
            output_color: azure (8)
          - size: 3
            output_color: gray (5)
relationships:
  - The transformation applies independently to each yellow object.
  - The final color of an object depends solely on its pixel count (size).
  - The relative positions of the objects remain the same.
```


## Natural Language Program

1.  Identify all distinct contiguous objects composed of yellow (4) pixels in the input grid. Treat pixels connected horizontally or vertically as part of the same object.
2.  For each identified yellow object, count the total number of pixels it contains (determine its size).
3.  Create the output grid by copying the input grid.
4.  For each identified yellow object in the input grid:
    *   If the object size is 1, change the color of its pixel(s) in the output grid to red (2).
    *   If the object size is 2, change the color of its pixel(s) in the output grid to azure (8).
    *   If the object size is 3, change the color of its pixel(s) in the output grid to gray (5).
5.  Leave all other pixels (the white background) unchanged in the output grid.