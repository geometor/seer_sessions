
## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 3 3 3 3 3 3 3 3 0 0 0 0 0 0 0 0 0 0 0 0
0 0 3 0 0 0 0 0 0 3 0 0 0 0 0 0 0 0 0 0 0 0
0 0 3 0 2 2 2 2 0 3 0 0 0 0 2 2 2 2 0 0 0 0
0 0 3 0 2 2 2 2 0 3 0 0 0 0 2 2 2 2 0 0 0 0
0 0 3 0 2 2 2 2 0 3 0 0 0 0 2 2 2 2 0 0 0 0
0 0 3 0 2 2 2 2 0 3 0 0 0 0 2 2 2 2 0 0 0 0
0 0 3 0 0 0 0 0 0 3 0 0 0 0 0 0 0 0 0 0 0 0
0 0 3 3 3 3 3 3 3 3 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 3 3 3 3 3 3 3 3 0 0 3 3 3 3 3 3 3 3 0 0
0 0 3 0 0 0 0 0 0 3 0 0 3 0 0 0 0 0 0 3 0 0
0 0 3 0 2 2 2 2 0 3 0 0 3 0 2 2 2 2 0 3 0 0
0 0 3 0 2 2 2 2 0 3 0 0 3 0 2 2 2 2 0 3 0 0
0 0 3 0 2 2 2 2 0 3 0 0 3 0 2 2 2 2 0 3 0 0
0 0 3 0 2 2 2 2 0 3 0 0 3 0 2 2 2 2 0 3 0 0
0 0 3 0 0 0 0 0 0 3 0 0 3 0 0 0 0 0 0 3 0 0
0 0 3 3 3 3 3 3 3 3 0 0 3 3 3 3 3 3 3 3 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 0 0 0 0 0
0 0 0 4 0 0 0
0 0 4 0 4 0 0
0 4 0 1 0 4 0
4 0 1 1 1 0 4
0 4 0 1 0 4 0
0 0 4 0 4 0 0
0 0 0 4 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 1 0 0 0
0 0 1 1 1 0 0
0 0 0 1 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0
0 0 0 4 0 0 0
0 0 4 0 4 0 0
0 4 0 1 0 4 0
4 0 1 1 1 0 4
0 4 0 1 0 4 0
0 0 4 0 4 0 0
0 0 0 4 0 0 0
0 0 0 0 0 0 0
0 0 0 4 0 0 0
0 0 4 0 4 0 0
0 4 0 1 0 4 0
4 0 1 1 1 0 4
0 4 0 1 0 4 0
0 0 4 0 4 0 0
0 0 0 4 0 0 0
0 0 0 0 0 0 0
```

Okay, let's break down the transformation logic for these examples.

**Perception of Elements:**

1.  **Grid Structure:** Both input and output are 2D grids of integers. The integer '0' represents the background color. Non-zero integers represent different foreground colors/parts of objects.
2.  **Objects:** The non-zero cells form distinct shapes or objects within the grid.
3.  **Object Composition:** Some objects appear nested; one shape (defined by one color) surrounds or encloses another shape (defined by a different color). For example, in `train_1`, the shape made of '3's encloses the shape made of '2's. In `train_2`, the '4's enclose the '1's.
4.  **Isolated Objects:** Inputs can contain multiple separate objects. Some might be simple (one color), while others are composite (enclosing/enclosed).
5.  **Transformation:** The transformation identifies one specific composite object (the enclosing one) from the input, copies it entirely (including the enclosed parts), and places the copy adjacent to the original in the output grid. Other isolated objects present in the input are discarded in the output.
6.  **Copy Placement:** The placement of the copy (either to the right or below the original) and the size of the gap (number of zero rows/columns) between the original and the copy seem dependent on the properties of the selected object.

**YAML Fact Document:**


```yaml
task_name: object_duplication_with_contextual_placement
description: Identify a specific composite object (one shape enclosing another) in the input grid, duplicate it, and place the copy adjacent to the original based on object properties. Discard other objects.

elements:
  - element: grid
    description: A 2D array of integers representing pixels.
    properties:
      - background_color: 0
      - foreground_colors: non-zero integers

  - element: object
    description: A connected component of non-zero cells.
    properties:
      - colors: list of unique non-zero integers within the object
      - bounding_box: coordinates of the minimum rectangle containing the object
      - width: width of the bounding box
      - height: height of the bounding box
      - type: simple (one color) or composite (enclosing/enclosed)

relationships:
  - relationship: encloses
    description: An object A encloses object B if B is fully contained within the bounding box of A, and A's cells form a boundary around B. Object A and B must have different primary colors.
    domain: object (composite, outer)
    range: object (inner)

actions:
  - action: identify_target_object
    description: Select the unique object from the input grid that encloses another object.
    input: input_grid
    output: target_object

  - action: determine_inner_color
    description: Find the primary color of the object enclosed by the target_object.
    input: target_object
    output: inner_color

  - action: calculate_gap
    description: The gap size between the original and copied object is equal to the inner_color.
    input: inner_color
    output: gap_size

  - action: determine_placement
    description: Decide placement direction (right or below) and calculate copy position based on target_object dimensions (width W, height H) and gap_size.
    input:
      - target_object (bounding box: r1, c1, r2, c2)
      - width (W)
      - height (H)
      - gap_size
    output:
      - placement_direction ('right' or 'below')
      - copy_top_left_corner (r_copy, c_copy)
    logic: |
      If H > W:
        placement_direction = 'below'
        copy_top_left_corner = (r2 + 1 + gap_size, c1)
      Else (W >= H):
        placement_direction = 'right'
        copy_top_left_corner = (r1, c2 + 1 + gap_size)

  - action: copy_object
    description: Extract the subgrid corresponding to the target_object's bounding box.
    input:
      - input_grid
      - target_object (bounding box)
    output: object_pattern (subgrid)

  - action: construct_output
    description: Create the output grid by placing the object_pattern copy into the input grid structure at the calculated position. Discard non-target objects from the input.
    input:
      - input_grid (containing only the target object and background)
      - object_pattern
      - copy_top_left_corner
    output: output_grid

```


**Natural Language Program:**

1.  Parse the input grid to identify all distinct connected objects formed by non-zero cells.
2.  Identify the specific "target" object which consists of an outer shape of one color enclosing an inner shape of a different color. Disregard any other objects in the input grid.
3.  Determine the bounding box of this target object (the smallest rectangle enclosing all its cells). Note its dimensions: width (W) and height (H).
4.  Identify the color of the *inner*, enclosed shape within the target object. Let this color value be `inner_color`.
5.  Calculate the gap size to be used between the original object and its copy: `gap = inner_color`.
6.  Determine the placement direction for the copy:
    *   If the target object's height (H) is greater than its width (W), the copy will be placed *below* the original.
    *   Otherwise (if width W is greater than or equal to height H), the copy will be placed to the *right* of the original.
7.  Calculate the top-left coordinate for placing the copy:
    *   If placing below: `copy_row = original_bottom_row + 1 + gap`, `copy_col = original_left_col`.
    *   If placing right: `copy_row = original_top_row`, `copy_col = original_right_col + 1 + gap`.
8.  Create the output grid, initially containing only the identified target object from the input grid (all other input objects are removed, replaced by the background color 0).
9.  Copy the pattern of the target object (defined by its bounding box) and paste this pattern into the output grid starting at the calculated top-left coordinate for the copy.
