
## train_1

**input:**
```
0 0 0 0 0 0 0 0 0
0 2 2 2 0 0 2 2 2
0 2 1 2 0 0 2 1 2
0 2 2 2 0 0 2 2 2
0 0 0 0 0 0 0 0 0
0 4 4 4 0 0 8 8 8
0 4 1 4 0 0 8 1 8
0 4 4 4 0 0 8 8 8
0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 4 4 4 0 0 8 8 8
0 4 1 4 0 0 8 1 8
0 4 4 4 0 0 8 8 8
0 0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 3 3 3 3 3
0 6 6 6 0 0 3 7 7 7 3
0 6 7 6 0 0 3 7 7 7 3
0 6 6 6 0 0 3 7 7 7 3
0 0 0 0 0 0 3 3 3 3 3
5 5 5 5 5 0 0 0 0 0 0
5 5 5 5 5 3 3 3 3 0 0
5 5 7 5 5 3 7 7 3 0 0
5 5 5 5 5 3 7 7 3 0 0
5 5 5 5 5 3 3 3 3 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 6 6 6 0 0 0 0 0 0 0
0 6 7 6 0 0 0 0 0 0 0
0 6 6 6 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
5 5 5 5 5 0 0 0 0 0 0
5 5 5 5 5 0 0 0 0 0 0
5 5 7 5 5 0 0 0 0 0 0
5 5 5 5 5 0 0 0 0 0 0
5 5 5 5 5 0 0 0 0 0 0
```


## train_3

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 4 4 4 4 4 0 0 0 1 1 1
0 4 0 0 0 4 0 0 0 1 0 1
0 4 4 4 4 4 0 0 0 1 0 1
0 0 0 0 0 4 4 4 0 1 0 1
0 0 0 0 0 4 0 4 0 1 1 1
7 7 7 0 0 4 0 4 0 0 0 0
7 0 7 0 0 4 4 4 0 0 0 0
7 0 7 0 0 0 0 0 0 0 0 0
7 0 7 0 0 0 0 0 0 0 0 0
7 7 7 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 1 1 1
0 0 0 0 0 0 0 0 0 1 0 1
0 0 0 0 0 0 0 0 0 1 0 1
0 0 0 0 0 0 0 0 0 1 0 1
0 0 0 0 0 0 0 0 0 1 1 1
7 7 7 0 0 0 0 0 0 0 0 0
7 0 7 0 0 0 0 0 0 0 0 0
7 0 7 0 0 0 0 0 0 0 0 0
7 0 7 0 0 0 0 0 0 0 0 0
7 7 7 0 0 0 0 0 0 0 0 0
```

Okay, let's break down the task based on the provided examples.

**Perception of Elements:**

1.  **Background:** The grid uses white (0) as the background color.
2.  **Objects:** The input grids contain multiple distinct objects composed of non-white pixels. These objects are separated by the white background.
3.  **Object Structure:** The objects in the examples often exhibit a structure with an outer "frame" color and one or more "internal" colors.
    *   In `train_1`, objects are 3x3 squares with a frame color (Red, Yellow, or Azure) and a single internal center pixel (Blue).
    *   In `train_2`, some objects are 3x3 squares with a frame (Magenta or Gray) and a center pixel (Orange). Others are rectangles (Green frame) with a more complex internal shape (Orange).
    *   In `train_3`, objects have a frame color (Yellow, Blue, or Orange) and internal pixels of the background color (White).
4.  **Transformation:** The transformation involves selectively removing *entire* objects from the input grid. Removed objects are replaced with the background color (white).
5.  **Selection Criteria:** The key is to determine *which* objects are removed. Observing the examples, the removal seems dependent on the specific combination of the object's frame color and its internal color(s).
    *   `train_1`: Objects with a Red frame and Blue center are removed. Objects with Yellow/Azure frames and Blue centers are kept.
    *   `train_2`: Objects with a Green frame and Orange internal pixels are removed. Objects with Magenta/Gray frames and Orange centers are kept.
    *   `train_3`: Objects with a Yellow frame and White internal pixels are removed. Objects with Blue/Orange frames and White internal pixels are kept.

**YAML Facts:**


```yaml
task_description: Identify specific types of two-colored objects and remove them, keeping all other objects.

definitions:
  background_color: 0 # white
  object: A contiguous group of non-background pixels.

rules:
  - description: Iterate through each distinct object in the input grid.
  - conditions:
      - object_must_have_two_colors: True
      - define_frame_color: The color forming the outer boundary of the object.
      - define_internal_color: The color(s) enclosed by the frame color.
  - removal_criteria:
      - description: Remove the object if its (Internal Color, Frame Color) pair matches a specific set.
      - pairs_to_remove:
          - internal: 1 # blue
            frame: 2 # red
          - internal: 7 # orange
            frame: 3 # green
          - internal: 0 # white
            frame: 4 # yellow
  - action:
      - if: removal_criteria met
        then: Replace all pixels of the object with the background_color.
      - else: Keep the object unchanged.

output_grid: The modified input grid after applying the removal action based on the criteria.

examples:
  train_1:
    objects:
      - { frame: 2, internal: 1, action: remove }
      - { frame: 2, internal: 1, action: remove }
      - { frame: 4, internal: 1, action: keep }
      - { frame: 8, internal: 1, action: keep }
  train_2:
    objects:
      - { frame: 6, internal: 7, action: keep }
      - { frame: 3, internal: 7, action: remove }
      - { frame: 5, internal: 7, action: keep }
      - { frame: 3, internal: 7, action: remove }
  train_3:
    objects:
      - { frame: 4, internal: 0, action: remove }
      - { frame: 1, internal: 0, action: keep }
      - { frame: 7, internal: 0, action: keep }

```


**Natural Language Program:**

1.  Initialize the output grid as a copy of the input grid.
2.  Identify all distinct objects in the input grid. An object is a connected component of pixels with non-zero colors.
3.  For each identified object:
    a.  Determine the set of unique colors present within the object.
    b.  Check if the object consists of exactly two distinct colors (this includes cases where one of the "colors" is the background color 0, provided it is fully enclosed within the object's non-zero pixels).
    c.  If the object has exactly two colors, identify the 'Frame Color' (the color forming the outer boundary) and the 'Internal Color' (the color enclosed by the frame).
    d.  Check if the (Internal Color, Frame Color) pair matches any of the following specific pairs:
        *   (Blue (1), Red (2))
        *   (Orange (7), Green (3))
        *   (White (0), Yellow (4))
    e.  If a match is found in step (d), locate all pixels belonging to this object in the output grid and change their color to the background color (White, 0).
4.  Return the modified output grid. Objects that did not meet the removal criteria remain unchanged from the input.
