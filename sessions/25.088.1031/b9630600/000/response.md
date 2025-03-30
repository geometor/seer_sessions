**Perception:**

The input grids consistently feature one or more hollow rectangular shapes constructed from green (3) pixels against a white (0) background. These rectangles vary in size and position across the examples. The corresponding output grids show the same green rectangles, but the white pixels enclosed within the boundaries of each rectangle have been filled with green (3) pixels. Pixels outside these rectangular areas remain unchanged (white). The core transformation is the filling of the interior area of these hollow green rectangles.

**Facts:**


```yaml
facts:
  - setup:
      description: The input grid consists of a white background (0) containing one or more distinct objects.
      background_color: white
      objects:
        - object_description: Hollow rectangular shapes.
          shape: Rectangle
          color: green
          property: Hollow (boundary pixels are green, interior pixels are white)
          count: variable (1 or more per example)
          connectivity: Contiguous green pixels forming the rectangle boundary.
  - transformation:
      description: The interior region enclosed by each hollow green rectangle is filled with green.
      action: Identify each hollow green rectangle.
      action_detail: Fill the area strictly inside the boundaries of each identified rectangle.
      target_pixels: white pixels located within the enclosed area of a green rectangle.
      fill_color: green
      unchanged_pixels:
        - All original green pixels forming the rectangle boundaries.
        - All white pixels located outside the boundaries of any rectangle.
  - output:
      description: The output grid contains the original green rectangles, but now they are filled solid green.
      resulting_objects: Solid green rectangles.
      background_color: white (remains unchanged where it was not inside a rectangle).
```


**Natural Language Program:**

1.  Initialize the output grid as a copy of the input grid.
2.  Scan the input grid to identify all distinct hollow rectangular objects formed by contiguous green (3) pixels enclosing an area of white (0) pixels.
3.  For each identified hollow green rectangle:
    *   Determine the coordinates defining the interior region (the white pixels enclosed by the green border).
    *   Iterate through each pixel coordinate within this determined interior region.
    *   Change the color of the pixel at that coordinate in the output grid to green (3).
4.  Return the modified output grid.