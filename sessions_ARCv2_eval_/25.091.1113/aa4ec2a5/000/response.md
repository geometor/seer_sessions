**Perception**

1.  **Input/Output Structure:** The inputs and outputs are grids of pixels, predominantly yellow (4), with distinct blue (1) shapes present in the input. The output grids maintain the overall dimensions and the yellow background but modify the blue shapes.
2.  **Object Identification:** The core objects in the input are contiguous regions of blue (1) pixels, set against a uniform yellow (4) background.
3.  **Transformation - Bordering:** In the output, every blue shape from the input is surrounded by a one-pixel thick border of red (2) pixels. This border replaces adjacent yellow pixels or expands the shape's footprint slightly where it touches the grid edge.
4.  **Transformation - Interior Filling:** The pixels that were originally blue (1) in the input undergo a conditional change based on the topology of the shape:
    *   **Shapes with Holes:** If a blue shape in the input completely encloses one or more regions of the yellow (4) background (i.e., it has "holes"), its interior is filled differently. The pixels that were originally blue (1) become azure (8). The pixels that formed the enclosed yellow (4) "holes" become magenta (6).
    *   **Shapes without Holes:** If a blue shape in the input does not enclose any background pixels (it is "solid"), the pixels that were originally blue (1) remain blue (1) in the output.
5.  **Background:** Pixels that were yellow (4) in the input and are not part of the new red (2) border remain yellow (4) in the output.

**Facts**


```yaml
elements:
  - object: grid
    description: A 2D array of pixels with color values 0-9.
  - object: background
    color: yellow (4)
    description: The predominant color in the input grid, filling space not occupied by shapes.
  - object: shape
    color: blue (1)
    property: contiguous
    description: Regions of connected blue pixels in the input grid.
  - object: hole
    color: yellow (4)
    property: enclosed
    description: Regions of background color completely surrounded by a single blue shape in the input.
    relationship: located inside a shape.
  - object: border
    color: red (2)
    property: thickness_1px
    description: A one-pixel thick frame generated around each original blue shape in the output.
    relationship: surrounds the area of the original shape.
  - object: filled_interior
    description: The area within the border corresponding to the original blue shape.
    conditional_color:
      - condition: original shape had holes
        color: azure (8)
      - condition: original shape had no holes
        color: blue (1)
  - object: filled_hole_area
    color: magenta (6)
    description: The area within the border corresponding to the original holes (enclosed yellow pixels).
    condition: Only exists if the original shape had holes.
    relationship: located inside the filled_interior (azure).

actions:
  - identify: Find all distinct contiguous blue (1) shapes in the input grid.
  - analyze: For each blue shape, determine if it encloses any yellow (4) background pixels (holes).
  - create_border: For each identified shape, draw a red (2) border around its perimeter in the output grid.
  - fill_interior:
      if shape has holes:
        fill original blue pixel locations with azure (8).
        fill original hole locations with magenta (6).
      else:
        fill original blue pixel locations with blue (1).
  - copy_background: Preserve yellow (4) pixels from the input that are not part of any shape or its generated border.
```


**Natural Language Program**

1.  Initialize the output grid as a copy of the input grid.
2.  Identify all separate, contiguous regions (shapes) of blue (1) pixels in the input grid.
3.  For each identified blue shape:
    a.  Determine the set of coordinates occupied by the blue pixels (`shape_pixels`).
    b.  Find all yellow (4) pixels that are adjacent (including diagonals) to any pixel in `shape_pixels`. These form the potential border locations. Change the color of these adjacent yellow pixels in the output grid to red (2).
    c.  Analyze the topology of the original blue shape to detect if it fully encloses any regions of yellow (4) pixels ("holes"). Record the coordinates of these enclosed yellow pixels (`hole_pixels`).
    d.  If the shape has holes (i.e., `hole_pixels` is not empty):
        i.  Change the color of the pixels at `shape_pixels` coordinates in the output grid to azure (8).
        ii. Change the color of the pixels at `hole_pixels` coordinates in the output grid to magenta (6).
    e.  If the shape does not have holes:
        i.  Leave the color of the pixels at `shape_pixels` coordinates in the output grid as blue (1).
4.  Return the modified output grid.