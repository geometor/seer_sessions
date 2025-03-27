
## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0
0 0 8 2 0 0 0 0 6 6 6 0
0 0 2 8 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 8 2 0 0
6 6 6 0 0 0 0 0 2 8 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 7 7 0 0 0 0 0 0
0 0 0 0 7 7 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
7 7
7 7
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 0 0
0 0 5 0 0 0 0 0 0 0 0
0 0 5 0 0 0 0 4 0 0 0
0 0 5 0 0 0 0 4 0 2 0
0 0 5 0 0 0 0 4 0 2 0
0 0 5 0 0 0 0 0 0 2 0
0 0 0 0 5 0 0 0 0 2 0
0 0 0 0 5 0 0 0 0 0 0
4 0 0 0 5 0 0 0 0 0 0
4 0 0 0 5 0 0 0 0 0 0
4 0 0 0 5 0 0 0 0 0 0
```


**output:**
```
2
2
2
2
```


## train_3

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 6 6 6 0 0 0 0 0 0 0 0
0 0 0 6 0 0 0 0 2 2 2 0 0
0 0 0 0 0 0 0 0 2 3 2 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 2 1 2 0
0 0 0 0 0 0 0 0 0 1 1 1 0
0 2 2 2 0 0 0 0 0 0 0 0 0
0 2 3 2 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 6 6 6 0 0 0 0
0 0 0 0 0 0 0 6 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
2 1 2
1 1 1
```

Okay, let's break down this ARC task.

## Perception

1.  **Input/Output Structure:** The input is a grid containing various colored pixels (0-9), with 0 representing the white background. The output is also a grid, typically smaller than the input, containing a subset or transformation of the input's colored pixels.
2.  **Objects:** The non-white pixels in the input grid form distinct contiguous regions or "objects". These objects can be composed of a single color or multiple colors. Connectivity seems to be based on adjacent cells (up, down, left, right - 4-way).
3.  **Transformation Goal:** The task seems to involve selecting one specific object (or information derived from it) from the input grid based on certain criteria and presenting it as the output.
4.  **Selection Criteria:** The selection appears linked to the minimum color index present in the input (excluding the white background color 0).
5.  **Output Generation:** The way the output grid is generated depends on whether one or multiple objects contain this minimum color, and whether the selected object is mono-colored or multi-colored.
    *   If a single object contains the minimum color:
        *   If it's multi-colored, the output is the object itself, cropped to its bounding box. (Example 3)
        *   If it's mono-colored, the output is a vertical column containing all the pixels of that object. (Example 2)
    *   If multiple objects contain the minimum color: The task seems to switch criteria and look for a unique object that is a "solid square" (a square region filled entirely with a single color). The output is this solid square object. (Example 1)

## Facts


```yaml
task_type: object_selection_and_transformation

definitions:
  - object: A maximal connected component of non-white pixels (color > 0) using 4-way adjacency (up, down, left, right).
  - background_color: 0 (white).
  - minimum_color (c_min): The smallest color index (> 0) present anywhere in the input grid.
  - bounding_box: The smallest rectangle enclosing all pixels of an object.
  - solid_square: An object whose bounding box has equal height and width, consists of only one color, and contains no background pixels within that bounding box.

observations:
  - Input grids contain multiple distinct objects against a white background.
  - The output grid is derived from a single object selected from the input.
  - The primary selection criterion involves the minimum_color (c_min).

selection_rules:
  - Find all objects containing c_min. Let this set be O_min.
  - Rule_A (len(O_min) == 1): Select the single object 'obj' in O_min.
  - Rule_B (len(O_min) > 1): Select the unique object 'obj' from *all* input objects that is a solid_square.

output_generation:
  - If Rule_A applies:
    - If 'obj' contains multiple colors: Output the subgrid corresponding to the bounding_box of 'obj'.
    - If 'obj' contains only c_min: Output a vertical column (height = number of pixels in 'obj', width = 1) filled with c_min.
  - If Rule_B applies:
    - Output the subgrid corresponding to the bounding_box of the selected solid_square 'obj'.

examples_analysis:
  - train_1:
      - c_min: 2 (red).
      - Objects containing c_min: Two (red/azure shapes).
      - len(O_min) > 1 -> Rule_B applies.
      - Solid square object: The orange 2x2 square (color 7).
      - Output: The 2x2 orange square.
  - train_2:
      - c_min: 2 (red).
      - Objects containing c_min: One (the red L-shape).
      - len(O_min) == 1 -> Rule_A applies.
      - Selected object 'obj' (red L-shape) has only one color (c_min=2).
      - Number of pixels in 'obj': 4.
      - Output: A 4x1 vertical column of red (color 2).
  - train_3:
      - c_min: 1 (blue).
      - Objects containing c_min: One (the red/blue/green shape).
      - len(O_min) == 1 -> Rule_A applies.
      - Selected object 'obj' (red/blue/green shape) has multiple colors.
      - Output: The bounding box of 'obj' cropped from the input.
```


## Natural Language Program

1.  Identify all distinct connected components (objects) of non-white pixels in the input grid, using 4-way adjacency. Record the pixels belonging to each object.
2.  Find the minimum color index `c_min` present among all non-white pixels in the input grid.
3.  Identify all objects found in step 1 that contain at least one pixel with the color `c_min`. Let this collection of objects be `O_min`.
4.  **Check the number of objects in `O_min`:**
    a.  **If `O_min` contains exactly one object (`obj`):**
        i.  Examine the colors of the pixels within `obj`.
        ii. **If `obj` contains pixels of multiple different colors:** Determine the minimum bounding box that encloses `obj`. The output grid is the subgrid cropped from the input grid corresponding to this bounding box.
        iii. **If `obj` contains pixels of only one color (which must be `c_min`):** Count the total number of pixels `n` in `obj`. The output grid is a single vertical column of height `n` and width 1, filled entirely with color `c_min`.
    b.  **If `O_min` contains more than one object:**
        i.  Iterate through *all* objects identified in step 1 (not just those in `O_min`).
        ii. For each object, check if it qualifies as a "solid square":
            *   It must consist of pixels of only one single color.
            *   Its bounding box must have equal height and width.
            *   All pixels within its bounding box must belong to the object (no background pixels within the box).
        iii. Identify the unique object that satisfies the "solid square" criteria. Let this be `obj_sq`.
        iv. Determine the bounding box of `obj_sq`. The output grid is the subgrid cropped from the input grid corresponding to this bounding box.
