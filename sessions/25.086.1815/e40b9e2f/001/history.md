
## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 3 0 0 0 0 0 0 0 0
0 0 6 6 0 0 0 0 0 0
0 0 6 6 0 0 0 0 0 0
0 0 0 6 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 3 6 0 3 0 0 0 0 0
0 0 6 6 6 0 0 0 0 0
0 6 6 6 0 0 0 0 0 0
0 3 0 6 3 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 7 0 0 0 0 0
0 0 0 4 7 4 0 0 0 0
0 0 0 7 4 7 0 0 0 0
0 0 0 4 7 4 0 0 0 0
0 0 0 0 0 0 4 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 4 0 7 0 4 0 0 0
0 0 0 4 7 4 0 0 0 0
0 0 7 7 4 7 7 0 0 0
0 0 0 4 7 4 0 0 0 0
0 0 4 0 7 0 4 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


## train_3

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 9 0 0 0
0 0 0 8 8 8 0 0 0 0
0 0 0 8 8 8 0 0 0 0
0 0 0 8 8 8 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 9 0 0 0 9 0 0 0
0 0 0 8 8 8 0 0 0 0
0 0 0 8 8 8 0 0 0 0
0 0 0 8 8 8 0 0 0 0
0 0 9 0 0 0 9 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

Okay, let's analyze the task examples.

**Perception of Elements:**

1.  **Background:** The consistent background color is white (0).
2.  **Objects:** Each input grid contains at least two distinct non-white colors. Typically, one color forms a larger contiguous object, while the other color(s) appear as smaller objects, often single pixels.
    *   Example 1: A magenta (6) object and a green (3) pixel.
    *   Example 2: An orange (7) object and several yellow (4) pixels (some connected, one separate).
    *   Example 3: An azure (8) object and a maroon (9) pixel.
3.  **Transformation:** The transformation involves adding new pixels. The color of the newly added pixels matches the color of the smaller, non-dominant object(s) in the input. The position of these new pixels is determined by the location of the largest object. Specifically, new pixels are added to white cells that are directly adjacent (horizontally or vertically) to the largest object.
4.  **Invariance:** The original objects (both the largest one and the smaller 'seed' ones) remain unchanged in their original positions in the output grid.

**YAML Facts:**


```yaml
task_description: Add pixels of a 'seed' color to empty cells adjacent to the largest object.
definitions:
  - name: grid
    type: 2D array of integers 0-9
  - name: background_color
    value: 0 (white)
  - name: object
    type: contiguous group of non-background pixels of the same color
  - name: largest_object
    criteria: The object with the highest pixel count.
  - name: main_color
    source: The color of the largest_object.
  - name: seed_pixel
    criteria: Any non-background pixel not belonging to the largest_object.
  - name: seed_color
    source: The color of a seed_pixel. (Assumption based on examples: only one seed_color per task instance).
  - name: adjacency
    type: Cardinal (up, down, left, right neighbors).
actions:
  - identify:
      target: all non-background colors present in the input grid.
  - identify:
      target: the largest_object in the input grid.
      result: main_object, main_color.
  - identify:
      target: the color(s) of all seed_pixels.
      result: seed_color(s).
  - iterate:
      target: each pixel in the input grid.
      condition: If the pixel color is background_color (0).
      sub_actions:
        - check_neighbors:
            target: the current background pixel.
            condition: If any cardinal neighbor belongs to the main_object (has main_color).
            effect: Change the color of the current pixel in the output grid to the seed_color.
  - preserve:
      target: All original pixels from the input grid remain in the output grid unless modified by the adjacency rule.
relationships:
  - The placement of new pixels (of seed_color) depends on the location of the main_object.
  - New pixels are placed only in background_color cells.
  - New pixels are placed adjacent (cardinally) to the main_object.
```


**Natural Language Program:**

1.  Initialize the output grid as a copy of the input grid.
2.  Identify all distinct non-white colors present in the input grid.
3.  Find the largest contiguous object (by pixel count) composed of a single color. Identify this object's color as the `main_color`.
4.  Identify the color(s) of all other non-white pixels present in the input grid. Call this the `seed_color`. (Based on the examples, assume there's only one such `seed_color` per grid).
5.  Iterate through each cell `(row, col)` of the input grid.
6.  If the cell `(row, col)` contains the background color (white, 0):
    a.  Check its four cardinal neighbors: `(row-1, col)`, `(row+1, col)`, `(row, col-1)`, `(row, col+1)`.
    b.  If any of these neighbors exist within the grid boundaries and contain the `main_color`:
        i.  Change the color of the cell `(row, col)` in the output grid to the `seed_color`.
7.  Return the modified output grid.
