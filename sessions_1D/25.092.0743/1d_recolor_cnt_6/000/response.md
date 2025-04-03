## Perception
The input grids consist of a single row containing white (0) pixels and yellow (4) pixels. The yellow pixels form contiguous horizontal segments (objects) separated by white pixels. The output grids maintain the same dimensions and the positions of the white pixels. The yellow pixels in the input are replaced by other colors in the output. The color used for replacement depends on the size (length) of the contiguous horizontal yellow segment in the input.

## Facts

```yaml
elements:
  - type: background
    color: white (0)
    role: static, remains unchanged in the output.
  - type: object
    color: yellow (4)
    definition: contiguous horizontal sequence of one or more yellow pixels.
    properties:
      - size: the number of pixels in the sequence (length).
    actions:
      - transformed: each yellow object is replaced by an object of the same size and position but with a different color.
    transformation_rule:
      - condition: size = 1
        output_color: gray (5)
      - condition: size = 2
        output_color: orange (7)
      - condition: size = 3
        output_color: magenta (6)
relationships:
  - The transformation applies independently to each identified yellow object based solely on its size.
  - The position and size of the objects are preserved during the color transformation.
```


## Natural Language Program
1.  Identify all contiguous horizontal segments (objects) of yellow (4) pixels in the input grid.
2.  For each identified yellow object:
    a.  Determine its size (number of pixels).
    b.  If the size is 1, replace all pixels of this object with gray (5).
    c.  If the size is 2, replace all pixels of this object with orange (7).
    d.  If the size is 3, replace all pixels of this object with magenta (6).
3.  Leave all white (0) pixels unchanged.
4.  The output grid has the same dimensions as the input grid, with the yellow objects recolored according to their original size.