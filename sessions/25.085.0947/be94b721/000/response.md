## Perception
The input grids contain multiple distinct shapes (objects), each composed of a single, non-white color. The background is white (color 0). The output grid contains only one of the shapes from the input grid. By comparing the shapes in the input and output across the examples, I observe that the shape present in the output is always the one that has the largest area (most pixels) in the input grid. The output grid is cropped to the bounding box of this largest shape.

## Facts


```yaml
- task: Identify and isolate the largest object
  description: >
    The task involves processing an input grid containing multiple distinct objects,
    each defined by a contiguous block of non-white pixels of the same color.
    The goal is to identify the object with the largest area (pixel count) and
    output only that object, cropped to its bounding box.
  examples:
    - id: train_1
      input_objects:
        - object: L-shape
          color: azure (8)
          pixel_count: 7
        - object: C-shape
          color: orange (7)
          pixel_count: 6
        - object: square
          color: red (2)
          pixel_count: 4
      selected_object:
        object: L-shape
        color: azure (8)
        reason: Largest pixel count (7)
      output: Cropped azure L-shape
    - id: train_2
      input_objects:
        - object: cross-shape
          color: green (3)
          pixel_count: 5
        - object: rectangle
          color: yellow (4)
          pixel_count: 6
        - object: L-shape
          color: magenta (6)
          pixel_count: 3
      selected_object:
        object: rectangle
        color: yellow (4)
        reason: Largest pixel count (6)
      output: Cropped yellow rectangle
    - id: train_3
      input_objects:
        - object: T-shape
          color: orange (7)
          pixel_count: 4
        - object: S-shape
          color: red (2)
          pixel_count: 7
        - object: L-shape
          color: azure (8)
          pixel_count: 4
      selected_object:
        object: S-shape
        color: red (2)
        reason: Largest pixel count (7)
      output: Cropped red S-shape
    - id: train_4
      input_objects:
        - object: S-shape
          color: red (2)
          pixel_count: 7
        - object: L-shape
          color: green (3)
          pixel_count: 4
        - object: triangle-shape
          color: blue (1)
          pixel_count: 5
      selected_object:
        object: S-shape
        color: red (2)
        reason: Largest pixel count (7)
      output: Cropped red S-shape
  rules:
    - rule: Identify all distinct contiguous non-white objects in the input grid.
    - rule: Calculate the area (number of pixels) for each identified object.
    - rule: Determine the object with the maximum area. (Assume no ties based on examples).
    - rule: Create the output grid containing only the pixels belonging to the largest object.
    - rule: Crop the output grid to the minimal bounding box enclosing the largest object.

```


## Natural Language Program

1.  Find all connected components of non-white pixels in the input grid. Each component represents a distinct object.
2.  For each object, calculate its size by counting the number of pixels it contains.
3.  Identify the object with the largest size.
4.  Determine the minimum bounding box coordinates (top-left and bottom-right corners) that enclose this largest object within the input grid.
5.  Create a new output grid whose dimensions match the dimensions of the bounding box.
6.  Copy the pixels corresponding to the largest object from the input grid into the new output grid, adjusting their coordinates relative to the top-left corner of the bounding box. Fill the rest of the output grid (if any, corresponding to the background within the original object's structure but outside the object's pixels) with the background color (white, 0).