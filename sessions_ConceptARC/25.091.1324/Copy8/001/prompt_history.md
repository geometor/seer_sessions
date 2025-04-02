
## train_1

**input:**
```
0 0 0 2 2 0 0 0 0 0 0 0 0 0 0 0 0
0 0 2 2 2 2 0 0 0 0 0 0 0 0 0 0 0
0 2 2 2 2 2 2 0 0 0 0 0 0 0 0 0 0
0 1 1 1 1 1 1 0 0 0 1 1 1 1 1 1 0
0 1 1 1 1 1 1 0 0 0 1 1 1 1 1 1 0
0 1 1 1 1 1 1 0 0 0 1 1 1 1 1 1 0
0 1 1 1 1 1 1 0 0 0 1 1 1 1 1 1 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 2 2 0 0 0 0 0 0 0 2 2 0 0 0
0 0 2 2 2 2 0 0 0 0 0 2 2 2 2 0 0
0 2 2 2 2 2 2 0 0 0 2 2 2 2 2 2 0
0 1 1 1 1 1 1 0 0 0 1 1 1 1 1 1 0
0 1 1 1 1 1 1 0 0 0 1 1 1 1 1 1 0
0 1 1 1 1 1 1 0 0 0 1 1 1 1 1 1 0
0 1 1 1 1 1 1 0 0 0 1 1 1 1 1 1 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 4 4 4 4 4 0 4 4 4 4 4 0
0 4 0 0 0 4 0 4 0 0 0 4 0
0 4 0 0 0 4 0 4 0 0 0 4 0
0 4 4 4 4 4 0 4 4 4 4 4 0
0 4 0 0 0 4 0 4 0 0 0 4 0
0 4 0 0 0 4 0 4 0 0 0 4 0
0 4 4 4 4 4 0 4 4 4 4 4 0
0 3 0 0 0 3 0 0 0 0 0 0 0
0 0 3 0 3 0 0 0 0 0 0 0 0
0 0 0 3 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 4 4 4 4 4 0 4 4 4 4 4 0
0 4 0 0 0 4 0 4 0 0 0 4 0
0 4 0 0 0 4 0 4 0 0 0 4 0
0 4 4 4 4 4 0 4 4 4 4 4 0
0 4 0 0 0 4 0 4 0 0 0 4 0
0 4 0 0 0 4 0 4 0 0 0 4 0
0 4 4 4 4 4 0 4 4 4 4 4 0
0 3 0 0 0 3 0 3 0 0 0 3 0
0 0 3 0 3 0 0 0 3 0 3 0 0
0 0 0 3 0 0 0 0 0 3 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

Okay, let's analyze the provided examples to understand the transformation rule.

**Perception**

*   **Input/Output Structure:** Both examples show input and output grids of the same dimensions. The grids contain a white background (0) and several distinct colored objects.
*   **Objects and Colors:**
    *   Example 1: Contains one red (2) object and two blue (1) objects.
    *   Example 2: Contains two yellow (4) objects and one green (3) object.
*   **Transformation:**
    *   In both examples, there are two objects of one color (blue in Ex1, yellow in Ex2) and one object of another color (red in Ex1, green in Ex2).
    *   The pair of objects (blue/yellow) remain unchanged in their positions from input to output.
    *   The single object (red/green) is copied. The original single object remains in place, and a duplicate appears in the output grid.
    *   The position of the duplicated object seems related to the pair of objects. In Ex1, the original red object is near the top-left blue object. The duplicated red object appears near the top-right blue object, in a similar relative position (above it).
    *   In Ex2, the original green object is below the left yellow object. The duplicated green object appears below the right yellow object, again in a similar relative position.
*   **Spatial Relationship:** The core transformation appears to be identifying a pair of 'anchor' objects and a single 'mobile' object. The relative spatial relationship (e.g., offset vector) between the mobile object and the first anchor object is determined. This same relationship is then applied to the second anchor object to find the position for the *copy* of the mobile object.

**Facts**


```yaml
task_description: Copy a specific object based on its relationship to a pair of identical anchor objects.

examples:
  - id: train_1
    input_grid_size: [10, 17]
    output_grid_size: [10, 17]
    objects:
      - color: red
        count: 1
        role: mobile
        location_relation: Above the first blue object.
      - color: blue
        count: 2
        role: anchor
        description: Rectangular shapes.
    transformation:
      action: copy
      source_object_color: red
      target_location_rule: Maintain the same relative position (above) with respect to the second blue anchor object as the original red object has to the first blue anchor object.

  - id: train_2
    input_grid_size: [11, 13]
    output_grid_size: [11, 13]
    objects:
      - color: green
        count: 1
        role: mobile
        location_relation: Below the first yellow object.
      - color: yellow
        count: 2
        role: anchor
        description: Shapes resembling the number 8.
    transformation:
      action: copy
      source_object_color: green
      target_location_rule: Maintain the same relative position (below) with respect to the second yellow anchor object as the original green object has to the first yellow anchor object.

general_rules:
  - Find all distinct objects (contiguous non-white pixels).
  - Identify the color with exactly two objects (anchor color).
  - Identify the color with exactly one object (mobile color).
  - Determine the 'first' and 'second' anchor objects (e.g., by top-left coordinate).
  - Calculate the positional offset (vector) from the top-left corner of the first anchor object to the top-left corner of the mobile object.
  - Calculate the target position for the copy by adding this offset to the top-left corner of the second anchor object.
  - Copy the pixel pattern of the mobile object to the target position in the output grid.
  - All other pixels remain unchanged from the input.
```


**Natural Language Program**

1.  **Identify Objects:** Scan the input grid to find all contiguous blocks of pixels with the same non-white color. Record each object's color, pixels, and bounding box.
2.  **Categorize Objects:** Group the identified objects by color and count how many objects exist for each color.
3.  **Find Anchor Pair:** Identify the color that has exactly two objects. These are the 'anchor' objects.
4.  **Find Mobile Object:** Identify the color that has exactly one object. This is the 'mobile' object.
5.  **Order Anchors:** Determine which anchor object is the 'first' (e.g., the one whose bounding box's top-left corner has the smallest row index, breaking ties with the smallest column index). Label this `Anchor1` and the other `Anchor2`.
6.  **Calculate Offset:** Compute the vector difference (delta_row, delta_col) between the top-left corner coordinates of the mobile object's bounding box and the top-left corner coordinates of `Anchor1`'s bounding box. `offset = mobile_top_left - anchor1_top_left`.
7.  **Determine Copy Position:** Calculate the target top-left corner coordinates for the copied mobile object by adding the calculated offset to the top-left corner coordinates of `Anchor2`'s bounding box. `copy_target_top_left = anchor2_top_left + offset`.
8.  **Generate Output:** Create a copy of the input grid. Iterate through the pixels of the original mobile object relative to its own top-left corner. For each pixel, calculate its corresponding position relative to the `copy_target_top_left` and place the mobile object's color at that coordinate in the copied grid. The final copied grid is the output.
