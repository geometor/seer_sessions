
## train_1

**input:**
```
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
2 2 2 0 0 0 0 0
2 2 2 0 0 0 0 0
2 1 1 1 0 0 0 0
0 1 1 1 0 0 0 0
0 1 1 1 0 0 0 0
0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
2 2 2 0 0 0 0 0
2 2 2 0 0 0 0 0
1 1 1 0 0 0 0 0
1 1 1 0 0 0 0 0
1 1 1 0 0 0 0 0
0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 4 4 4 4 0
0 0 0 4 4 4 4 0
0 0 0 4 4 3 3 3
0 0 0 4 4 3 3 3
0 0 0 0 0 3 3 3
```


**output:**
```
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 4 4 4 4 0
0 0 0 4 4 4 4 0
0 0 0 4 3 3 3 0
0 0 0 4 3 3 3 0
0 0 0 0 3 3 3 0
```


## train_3

**input:**
```
0 4 4 4 0 0 0 0
0 4 4 4 0 0 0 0
0 4 4 4 6 6 6 6
0 0 0 6 6 6 6 6
0 0 0 6 6 6 6 6
0 0 0 6 6 6 6 6
0 0 0 6 6 6 6 6
0 0 0 0 0 0 0 0
```


**output:**
```
4 4 4 0 0 0 0 0
4 4 4 0 0 0 0 0
4 4 4 6 6 6 6 6
0 0 0 6 6 6 6 6
0 0 0 6 6 6 6 6
0 0 0 6 6 6 6 6
0 0 0 6 6 6 6 6
0 0 0 0 0 0 0 0
```


## train_4

**input:**
```
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 5 5 5 0 0 0
0 0 5 1 5 0 0 0
0 0 5 5 5 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 5 5 5 0 0 0
0 0 1 5 5 0 0 0
0 0 5 5 5 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
```

Okay, let's analyze the task examples.

**Perception of Elements:**

The task involves grids containing two distinct non-white colored objects. The transformation depends on the specific pair of colors present. There appear to be two main types of transformations:
1.  **Object Shift:** One of the objects shifts its position horizontally (specifically, one column to the left). The object retains its color, overwriting pixels in its new path. Its original location becomes white.
2.  **Color Bleed:** One object remains static, while specific pixels of the *other* object, adjacent to the first, change their color to match the first object's color.

The key seems to be identifying which color pair triggers which transformation, which object is affected, and the precise rule for the change (which object shifts, or exactly which pixels change color).

**Observations:**

*   Each input grid contains exactly two non-white colors.
*   The relative positions vary: one object might be lower-right, or one might be inside the other.
*   The transformation rule depends on the specific pair of colors involved.
    *   Pairs {Blue(1), Red(2)} and {Yellow(4), Magenta(6)} result in the object with the *lower* color index (Blue=1, Yellow=4) shifting left by one column.
    *   Pairs {Green(3), Yellow(4)} and {Blue(1), Gray(5)} result in a "color bleed" where the color with the *lower* index (Green=3, Blue=1) changes the color of specific adjacent pixels of the *higher* index object.
*   For the "Color Bleed" cases:
    *   {Green(3), Yellow(4)}: Yellow pixels adjacent to Green pixels change to Green if the Green neighbor is directly to the right or directly below the Yellow pixel.
    *   {Blue(1), Gray(5)}: The single Gray pixel adjacent to the Blue pixel(s) that has the minimum column index (with row index as a tie-breaker) changes to Blue.

**YAML Facts:**

```
yaml
task_type: object_transformation
components:
  - role: grid
    elements:
      - role: background
        color: white
      - role: object
        count: 2 # Exactly two distinct non-white objects per grid
        properties:
          - color: non-white (1-9)
          - shape: variable (L-shape, rectangle, C-shape, single pixel)
          - connectivity: contiguous pixels of the same color

relationships:
  - type: color_pair_dependency
    description: The transformation rule is determined by the specific pair of non-white colors present.
  - type: spatial
    description: Objects can be adjacent, or one can enclose the other.

actions:
  - name: identify_colors
    inputs: input_grid
    outputs: color1, color2
  - name: determine_rule_type
    inputs: color1, color2
    outputs: action_type ('shift' or 'bleed'), lower_color_object, higher_color_object
    logic: |
      Based on the set {color1, color2}:
      If {1, 2} or {4, 6}, action_type is 'shift', lower_color_object is the actor.
      If {1, 5} or {3, 4}, action_type is 'bleed', lower_color_object dictates change on higher_color_object.
  - name: execute_shift
    inputs: input_grid, lower_color_object
    outputs: output_grid
    description: Translate the lower_color_object one column left, overwriting existing cells. Original object location becomes white.
  - name: execute_bleed
    inputs: input_grid, lower_color_object, higher_color_object, color_pair
    outputs: output_grid
    description: |
      Identify pixels P of higher_color_object adjacent to lower_color_object.
      If color_pair is {1, 5}:
        Find the single pixel P with min column index (tie-break min row). Change P to lower_color.
      If color_pair is {3, 4}:
        Find all pixels P that have a lower_color neighbor directly right OR directly below. Change these P to lower_color.

```

**Natural Language Program:**

1.  Identify the two unique non-white colors present in the input grid. Call them C1 and C2.
2.  Determine the color with the lower index (C_low = min(C1, C2)) and the color with the higher index (C_high = max(C1, C2)).
3.  Identify the object composed of C_low pixels (Object_low) and the object composed of C_high pixels (Object_high).
4.  Check the specific pair of colors {C_low, C_high}:
    a.  **If the pair is {1, 2} (Blue, Red) OR {4, 6} (Yellow, Magenta):**
        i.  The transformation is **Shift Left**.
        ii. Create the output grid by copying the input grid.
        iii. Find all coordinates originally occupied by Object_low. Clear these locations in the output grid (set to white/0).
        iv. Calculate the new coordinates for Object_low by subtracting 1 from the column index of each original pixel.
        v.  Fill these new coordinates in the output grid with the color C_low, overwriting any existing colors at those locations.
    b.  **If the pair is {1, 5} (Blue, Gray) OR {3, 4} (Green, Yellow):**
        i.  The transformation is **Color Bleed**.
        ii. Create the output grid by copying the input grid.
        iii. Find all pixels P belonging to Object_high that are adjacent (sharing an edge or corner) to any pixel belonging to Object_low. These are the candidate pixels.
        iv. **If the pair is {1, 5}:**
            1. From the candidate pixels, find the single pixel P that has the minimum column index. If multiple candidates share the minimum column index, choose the one among them with the minimum row index.
            2. Change the color of this selected pixel P in the output grid from C_high (Gray) to C_low (Blue).
        v.  **If the pair is {3, 4}:**
            1. For each candidate pixel P (color Yellow), check its neighbours.
            2. If P has a neighbour Q (color Green) located directly to its right (relative coordinate (0, 1)) OR directly below it (relative coordinate (1, 0)), then mark P for change.
            3. Change the color of all marked pixels P in the output grid from C_high (Yellow) to C_low (Green).
5.  Return the modified output grid.
