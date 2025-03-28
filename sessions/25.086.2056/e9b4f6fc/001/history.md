
## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 8 8 8 8 8 8 8 0 0 0 0
0 0 8 8 2 4 8 8 8 0 0 0 0
0 0 8 2 2 4 4 4 8 0 0 0 0
0 0 8 8 8 8 8 8 8 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 1 4 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 3 2 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
8 8 8 8 8 8 8
8 8 3 1 8 8 8
8 3 3 1 1 1 8
8 8 8 8 8 8 8
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 6 8 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 2 1 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 3 3 3 3 3 3 3 0 4 5 0 0
0 3 5 5 5 5 3 3 0 0 0 0 0
0 3 3 1 1 5 3 3 0 0 0 0 0
0 3 8 1 1 3 3 3 0 0 0 0 0
0 3 8 8 8 8 3 3 0 0 0 0 0
0 3 3 3 3 3 3 3 0 0 0 0 0
0 3 3 3 3 3 3 3 0 0 0 0 0
```


**output:**
```
3 3 3 3 3 3 3
3 4 4 4 4 3 3
3 3 2 2 4 3 3
3 6 2 2 3 3 3
3 6 6 6 6 3 3
3 3 3 3 3 3 3
3 3 3 3 3 3 3
```


## train_3

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 2 4 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 1 4 4 1 0 0 0 0 0 0 0 0
0 8 8 4 1 0 0 0 0 0 0 0 0
0 8 8 1 1 0 0 0 0 0 0 0 0
0 1 1 1 1 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 3 8 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
1 2 2 1
3 3 2 1
3 3 1 1
1 1 1 1
```


## train_4

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 3 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 1 4 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 8 8 8 8 8 8 0 0 0
0 0 0 0 8 8 4 8 8 8 0 0 0
0 0 0 0 8 4 4 4 8 8 0 0 0
0 0 0 0 8 3 4 3 8 8 0 0 0
0 0 0 0 8 3 3 3 8 8 0 0 0
0 0 0 0 8 8 8 8 8 8 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
8 8 8 8 8 8
8 8 1 8 8 8
8 1 1 1 8 8
8 2 1 2 8 8
8 2 2 2 8 8
8 8 8 8 8 8
```

Okay, let's analyze the task examples.

**Perception of Elements:**

1.  **Input Grids:** The input grids are relatively large (13x13 or similar) and mostly sparse, filled with the background color (White/0).
2.  **Main Object:** Each input grid contains one large, prominent, contiguous object composed of a single 'frame' color, enclosing other colors or being a solid block. This object appears to be the primary focus.
    *   train_1: Azure(8) frame.
    *   train_2: Green(3) frame.
    *   train_3: Blue(1) frame (L-shape).
    *   train_4: Azure(8) frame.
3.  **Scattered Elements:** Outside the main object, there are several small, isolated groups of 1 or 2 non-background pixels. Crucially, some of these pixels are directly adjacent (horizontally or vertically) to each other, forming color pairs.
    *   train_1: Adjacent pairs (Blue(1), Yellow(4)) and (Green(3), Red(2)).
    *   train_2: Adjacent pairs (Magenta(6), Azure(8)), (Red(2), Blue(1)), (Yellow(4), Gray(5)).
    *   train_3: Adjacent pairs (Red(2), Yellow(4)) and (Green(3), Azure(8)). Note: Blue(1) and Yellow(4) are present but *not* adjacent.
    *   train_4: Adjacent pairs (Red(2), Green(3)) and (Blue(1), Yellow(4)).
4.  **Output Grids:** The output grids are smaller and correspond in size and shape to the bounding box of the main object identified in the input. The content of the output grid is derived from the content within the main object's bounding box in the input, but with color transformations applied.
5.  **Color Transformation:** The colors *inside* the main object (including its frame) in the input are systematically changed to produce the output. The rule for this change seems to be defined by the adjacent color pairs found scattered outside the main object. If color `A` is adjacent to color `B` in a scattered pair, then color `B` within the main object transforms into color `A` in the output. Colors within the main object that do not participate in such a mapping (either as the source `B` or are not found in any scattered pair) retain their original color in the output.

**YAML Facts:**


```yaml
task_description: Apply color transformations to the largest object based on external color pairings.
elements:
  - type: grid
    role: input
    properties:
      - Contains a background color (White/0).
      - Contains one largest contiguous non-background object (main_object).
      - Contains small, scattered non-background pixel groups (scattered_elements) outside the main_object.
      - Some scattered_elements consist of adjacent pairs of different colors.
  - type: grid
    role: output
    properties:
      - Smaller than the input grid.
      - Dimensions match the bounding box of the input's main_object.
      - Contains pixels derived from the main_object after color transformation.
objects:
  - id: main_object
    description: The largest contiguous block of non-background pixels in the input grid.
    properties:
      - Has a specific frame_color.
      - Encloses internal_pixels of various colors (can be same as frame_color).
      - Has a bounding_box.
  - id: scattered_elements
    description: Small groups (1 or 2 pixels) of non-background colors outside the main_object's bounding box.
  - id: adjacent_pairs
    description: Pairs of non-background pixels within scattered_elements that are orthogonally adjacent.
    properties:
      - Each pair consists of two colors (color_A, color_B).
      - Defines a mapping rule: color_B maps to color_A.
relationships:
  - type: extraction
    source: input_grid.main_object.bounding_box
    target: output_grid
    description: The output grid corresponds spatially to the bounding box of the main object.
  - type: color_mapping
    source: adjacent_pairs
    target: main_object_pixels
    description: The adjacent pairs define how colors within the main object (including its frame) are transformed. If (color_A, color_B) form an adjacent pair, then color_B pixels within the main object become color_A in the output. Pixels with colors not found as color_B in any adjacent pair retain their original color.
actions:
  - action: find_largest_object
    input: input_grid
    output: main_object, bounding_box
    description: Identify the largest contiguous non-background object and its bounding box.
  - action: find_adjacent_pairs
    input: input_grid, bounding_box
    output: color_map (dictionary)
    description: Find all orthogonally adjacent non-background pixel pairs outside the bounding_box. Create a mapping dictionary where {color_B: color_A} if color_A is adjacent to color_B.
  - action: extract_subgrid
    input: input_grid, bounding_box
    output: subgrid (pixels within main_object's bounding box)
  - action: apply_color_map
    input: subgrid, color_map
    output: output_grid
    description: Create the output grid by applying the color_map to each pixel in the subgrid. If a pixel's color is a key in the color_map, change it to the corresponding value. Otherwise, keep the original color.

```


**Natural Language Program:**

1.  Identify the largest contiguous object in the input grid that is not the background color (White/0). Determine its bounding box.
2.  Examine the areas of the input grid *outside* this bounding box. Find all pairs of orthogonally adjacent pixels where both pixels are non-background colors.
3.  For each such adjacent pair (pixel_A with color_A, pixel_B with color_B), establish a color transformation rule: color_B transforms into color_A. Store these rules (e.g., in a dictionary mapping B -> A).
4.  Create a new grid whose dimensions match the bounding box identified in step 1.
5.  Fill this new grid by copying the pixels from the input grid that fall within the identified bounding box.
6.  Iterate through each pixel in the new grid. For each pixel, check its color:
    *   If the color exists as a key (color_B) in the transformation rules established in step 3, change the pixel's color to the corresponding value (color_A).
    *   If the color does not exist as a key in the transformation rules, leave the pixel's color unchanged.
7.  The resulting grid is the final output.
