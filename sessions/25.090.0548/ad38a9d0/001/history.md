
## train_1

**input:**
```
6 6 7 7 6 6 7 7 7
7 6 7 7 7 6 6 7 7
7 7 7 6 7 7 7 7 6
7 7 6 6 6 7 6 7 6
7 6 7 6 7 7 6 7 6
7 6 7 7 7 7 7 7 7
7 6 7 7 7 7 7 6 6
7 7 7 7 6 6 6 7 6
7 7 7 7 6 6 6 7 7
```


**output:**
```
4 4 7 7 8 8 7 7 7
7 4 7 7 7 8 8 7 7
7 7 7 3 7 7 7 7 2
7 7 3 3 3 7 9 7 2
7 2 7 3 7 7 9 7 2
7 2 7 7 7 7 7 7 7
7 2 7 7 7 7 7 4 4
7 7 7 7 5 5 5 7 4
7 7 7 7 5 5 5 7 7
```


## train_2

**input:**
```
7 7 7 7 7 7 7 7 7
7 6 7 7 6 7 7 7 7
6 6 6 7 6 7 6 6 7
7 6 7 7 7 7 7 6 7
7 7 7 7 7 7 7 7 7
7 7 7 7 6 6 7 7 7
7 7 7 7 7 6 6 7 6
7 6 6 6 7 7 7 7 6
7 6 6 6 7 7 7 7 6
```


**output:**
```
7 7 7 7 7 7 7 7 7
7 3 7 7 9 7 7 7 7
3 3 3 7 9 7 4 4 7
7 3 7 7 7 7 7 4 7
7 7 7 7 7 7 7 7 7
7 7 7 7 8 8 7 7 7
7 7 7 7 7 8 8 7 2
7 5 5 5 7 7 7 7 2
7 5 5 5 7 7 7 7 2
```

## Perception

The input grids consist of a background color, orange (7), and several distinct foreground objects composed of gray (6) pixels. The output grids retain the same orange (7) background pixels in their original positions. The key transformation involves the gray (6) objects. Each contiguous block of gray pixels in the input is identified as a single object. In the output, each of these objects is replaced by a block of the exact same shape and size, but filled with a new color. The specific color used for replacement depends on the properties (size, shape, bounding box) of the original gray object. Different gray objects can map to different colors.

## Facts


```yaml
task_context:
  grid_size: ثابت (input and output grids have the same dimensions)
  background_color: orange (7)
  foreground_color: gray (6)
  action: replace_object_color

objects:
  - type: contiguous block of pixels
  - property: color (always gray (6) in input)
  - property: size (number of pixels)
  - property: shape (spatial arrangement of pixels)
  - property: bounding_box (minimum rectangle enclosing the object)

transformation_rules:
  - condition: pixel color is orange (7)
    action: keep pixel color orange (7)
  - condition: pixel color is gray (6)
    action:
      - identify the contiguous object the pixel belongs to
      - determine the object's properties (size, bounding_box)
      - apply a mapping rule based on properties to determine the output color
      - replace the gray (6) pixel with the determined output color

mapping_rules_observed: # (Based on object properties -> output color)
  - object_properties: { size: 2 } # (e.g., 1x2 or 2x1)
    output_color: maroon (9)
  - object_properties: { size: 3, bounding_box: { height: 2, width: 2 } } # (L-tromino)
    output_color: yellow (4)
  - object_properties: { size: 3, bounding_box: { height: 3, width: 1 } } # (1x3 or 3x1 line)
    output_color: red (2)
  - object_properties: { size: 3, bounding_box: { height: 1, width: 3 } } # (1x3 or 3x1 line)
    output_color: red (2)
  - object_properties: { size: 4 } # (e.g., 2x2 square, L-tetromino)
    output_color: azure (8)
  - object_properties: { size: 5 } # (e.g., T-pentomino)
    output_color: green (3)
  - object_properties: { size: 6, bounding_box: { height: 2, width: 3 } } # (2x3 or 3x2 rectangle)
    output_color: gray (5)
  - object_properties: { size: 6, bounding_box: { height: 3, width: 2 } } # (2x3 or 3x2 rectangle)
    output_color: gray (5)
  - object_properties: { size: 6, bounding_box: other } # (e.g., 5x8 bounding box observed)
    output_color: red (2)

relationships:
  - pixels within a contiguous gray block share the same fate (map to the same output color)
  - the output color is determined solely by the properties of the gray object it replaces
  - background pixels are invariant
```


## Natural Language Program

1.  Initialize the output grid as a copy of the input grid.
2.  Identify all distinct, contiguous objects composed of gray (6) pixels in the input grid. Treat pixels connected only diagonally as separate objects.
3.  For each identified gray object:
    a.  Determine its size (number of pixels).
    b.  Determine its bounding box (height and width of the smallest rectangle enclosing it).
    c.  Apply the following rules to determine the replacement color based on the object's size (N) and bounding box dimensions (H x W):
        i.  If N = 2, the replacement color is maroon (9).
        ii. If N = 3:
            - If H = 2 and W = 2 (L-tromino shape), the replacement color is yellow (4).
            - If (H = 1 and W = 3) or (H = 3 and W = 1) (line shape), the replacement color is red (2).
        iii. If N = 4, the replacement color is azure (8).
        iv. If N = 5, the replacement color is green (3).
        v.  If N = 6:
            - If (H = 2 and W = 3) or (H = 3 and W = 2) (rectangle shape), the replacement color is gray (5).
            - Otherwise, the replacement color is red (2).
        vi. (If other sizes/shapes are encountered, define appropriate rules or handle as errors/defaults).
    d.  In the output grid, change the color of all pixels corresponding to the current gray object to the determined replacement color.
4.  Return the modified output grid.
