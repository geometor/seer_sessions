
## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
5 5 5 5 5 5 0 0 0 0
0 0 0 0 0 0 0 5 0 0
0 0 0 0 0 0 0 5 0 0
0 0 0 0 0 0 0 5 0 0
0 0 0 0 0 0 0 5 0 0
0 0 5 5 5 0 0 5 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
1 1 1 1 1 1 0 0 0 0
0 0 0 0 0 0 0 4 0 0
0 0 0 0 0 0 0 4 0 0
0 0 0 0 0 0 0 4 0 0
0 0 0 0 0 0 0 4 0 0
0 0 2 2 2 0 0 4 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 5 0 0 0 0 0
0 0 0 0 5 0 0 0 0 0
0 5 0 0 5 0 0 0 0 0
0 5 0 0 5 0 0 0 0 0
0 5 0 0 5 0 0 5 0 0
0 5 0 0 5 0 0 5 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 1 0 0 0 0 0
0 0 0 0 1 0 0 0 0 0
0 4 0 0 1 0 0 0 0 0
0 4 0 0 1 0 0 0 0 0
0 4 0 0 1 0 0 2 0 0
0 4 0 0 1 0 0 2 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


## train_3

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 5 0 0
0 5 5 5 5 0 0 5 0 0
0 0 0 0 0 0 0 5 0 0
0 0 0 0 0 0 0 5 0 0
0 5 5 5 5 5 0 5 0 0
0 0 0 0 0 0 0 5 0 0
0 0 0 0 0 0 0 5 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 1 0 0
0 2 2 2 2 0 0 1 0 0
0 0 0 0 0 0 0 1 0 0
0 0 0 0 0 0 0 1 0 0
0 4 4 4 4 4 0 1 0 0
0 0 0 0 0 0 0 1 0 0
0 0 0 0 0 0 0 1 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


## train_4

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 5 0 0 0 0 0 0 0 0
0 5 0 0 5 0 0 0 0 0
0 5 0 0 5 0 0 0 0 0
0 5 0 0 5 0 0 5 0 0
0 5 0 0 5 0 0 5 0 0
0 5 0 0 5 0 0 5 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0
0 1 0 0 0 0 0 0 0 0
0 1 0 0 4 0 0 0 0 0
0 1 0 0 4 0 0 0 0 0
0 1 0 0 4 0 0 2 0 0
0 1 0 0 4 0 0 2 0 0
0 1 0 0 4 0 0 2 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

## Perception

1.  **Input/Output Structure:** The input and output are grids of the same dimensions (10x10 in all examples).
2.  **Color Palette:** The input grids use white (0) for the background and gray (5) for objects. The output grids use white (0) for the background and blue (1), red (2), and yellow (4) for objects.
3.  **Object Identification:** The gray pixels in the input form distinct connected components (objects). These objects appear to be lines or simple L-shapes.
4.  **Transformation:** The core transformation involves changing the color of the gray objects. The background remains unchanged. The shape and position of each object are preserved.
5.  **Color Assignment Logic:** The color assigned to each object in the output depends on the order in which the objects are encountered when scanning the grid (top-to-bottom, left-to-right).
    *   The first gray object encountered is always changed to blue (1).
    *   There are always exactly three gray objects in the examples.
    *   The assignment of red (2) and yellow (4) to the second and third objects depends on their relative vertical positions.
        *   Typically, the second object becomes yellow (4) and the third becomes red (2).
        *   However, if the second object is located entirely above the third object (its maximum row index is less than the minimum row index of the third object), the colors are swapped: the second object becomes red (2) and the third becomes yellow (4). This occurs in `train_3`.

## YAML Facts


```yaml
task_context:
  description: Recolor gray objects based on their scan order and relative positions.
  grid_properties:
    - dimensions_preserved: True
    - background_color: white (0)
    - background_preserved: True
input_elements:
  - element_type: objects
    color: gray (5)
    count: 3 (in all examples)
    shape: varies (lines, L-shapes)
    properties:
      - connectedness: pixels are adjacent (including diagonals likely count based on standard object finding)
      - location: scattered within the grid
output_elements:
  - element_type: objects
    color: blue (1), red (2), yellow (4)
    count: 3 (same as input)
    shape: same as corresponding input object
    location: same as corresponding input object
transformation_rules:
  - rule: Identify distinct gray (5) objects.
  - rule: Determine the scan order of objects (based on top-most, then left-most pixel).
  - rule: Recolor objects based on order and relative position:
      - 1st object: becomes blue (1).
      - 2nd and 3rd objects:
          - Condition: Check if the bounding box of the 2nd object is entirely above the bounding box of the 3rd object (max_row(obj2) < min_row(obj3)).
          - If Condition True: 2nd object becomes red (2), 3rd object becomes yellow (4).
          - If Condition False: 2nd object becomes yellow (4), 3rd object becomes red (2).
relationships:
  - type: spatial_order
    description: Objects are ordered based on top-to-bottom, left-to-right scanning.
  - type: relative_position
    description: The vertical positioning of the 2nd and 3rd objects in the scan order determines their final color assignment (red or yellow).
  - type: color_mapping
    description: Gray objects map to blue, red, or yellow based on derived rules.
```


## Natural Language Program

1.  Initialize the output grid as a copy of the input grid.
2.  Find all connected components (objects) consisting of gray pixels (color 5) in the input grid. Treat pixels touching side-by-side or diagonally as connected.
3.  Determine the order of these objects by finding the top-most, then left-most pixel belonging to each object. Sort the objects based on this scan order (first by row index, then by column index of this representative pixel).
4.  Identify the first, second, and third objects according to this scan order.
5.  Recolor the pixels belonging to the first object to blue (1) in the output grid.
6.  Determine the bounding box (minimum row, minimum column, maximum row, maximum column) for the second object and the third object.
7.  Compare the maximum row index of the second object's bounding box with the minimum row index of the third object's bounding box.
8.  If the maximum row of the second object is less than the minimum row of the third object (meaning the second object is entirely above the third):
    a.  Recolor the pixels belonging to the second object to red (2) in the output grid.
    b.  Recolor the pixels belonging to the third object to yellow (4) in the output grid.
9.  Otherwise (if the second object is not entirely above the third):
    a.  Recolor the pixels belonging to the second object to yellow (4) in the output grid.
    b.  Recolor the pixels belonging to the third object to red (2) in the output grid.
10. Return the modified output grid.
