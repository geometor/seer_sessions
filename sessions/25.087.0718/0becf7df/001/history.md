
## train_1

**input:**
```
4 2 0 0 0 0 0 0 0 0
3 7 0 0 0 0 4 0 0 0
0 0 0 0 0 3 4 4 0 0
0 0 0 0 0 3 2 4 0 0
0 0 0 7 7 3 2 4 0 0
0 0 0 7 3 3 2 0 0 0
0 0 0 7 0 0 2 2 0 0
0 0 0 7 7 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
4 2 0 0 0 0 0 0 0 0
3 7 0 0 0 0 2 0 0 0
0 0 0 0 0 7 2 2 0 0
0 0 0 0 0 7 4 2 0 0
0 0 0 3 3 7 4 2 0 0
0 0 0 3 7 7 4 0 0 0
0 0 0 3 0 0 4 4 0 0
0 0 0 3 3 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
1 3 0 0 0 0 0 0 0 0
2 8 0 0 0 0 1 0 0 0
0 0 0 0 1 1 1 0 0 0
0 0 0 0 1 1 1 0 0 0
0 0 3 3 3 3 1 8 0 0
0 0 3 3 2 0 8 8 0 0
0 0 0 0 2 0 8 8 0 0
0 0 0 0 2 0 0 0 0 0
0 0 0 0 2 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
1 3 0 0 0 0 0 0 0 0
2 8 0 0 0 0 3 0 0 0
0 0 0 0 3 3 3 0 0 0
0 0 0 0 3 3 3 0 0 0
0 0 1 1 1 1 3 2 0 0
0 0 1 1 8 0 2 2 0 0
0 0 0 0 8 0 2 2 0 0
0 0 0 0 8 0 0 0 0 0
0 0 0 0 8 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


## train_3

**input:**
```
9 4 0 0 0 0 0 0 0 0
7 6 0 0 0 9 9 0 0 0
0 0 0 0 0 7 9 0 0 0
0 0 0 0 0 4 0 0 0 0
0 0 0 0 7 4 0 0 0 0
0 0 0 6 6 7 0 0 0 0
0 0 0 7 6 6 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
9 4 0 0 0 0 0 0 0 0
7 6 0 0 0 4 4 0 0 0
0 0 0 0 0 6 4 0 0 0
0 0 0 0 0 9 0 0 0 0
0 0 0 0 6 9 0 0 0 0
0 0 0 7 7 6 0 0 0 0
0 0 0 6 7 7 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

Okay, let's analyze the task examples.

## Perception of Elements

1.  **Grid Structure:** Input and output are grids of pixels with different colors (represented by numbers 0-9). The background is white (0).
2.  **Objects:** Each grid contains multiple distinct "objects," which are contiguous areas of non-white pixels. In all examples, there seem to be exactly two main objects.
3.  **Object Characteristics:** Objects have varying shapes and contain multiple colors.
4.  **Transformation:** The transformation modifies the colors within *one* of the objects, leaving the other object and the background unchanged.
5.  **Identifying the Target Object:** The object that gets modified is consistently the one whose bounding box *does not* include the top-left corner (0,0). The object whose bounding box *does* include (0,0) remains unchanged.
6.  **Color Modification:** The modification involves swapping pairs of colors within the target object.
7.  **Determining Swap Pairs:** The specific colors involved in the swaps, and how they are paired, appears to be determined by the set of unique non-white colors present in the *unchanged* object (the one at the top-left). All examples show exactly four unique non-white colors in this object.
8.  **Pairing Logic:** Let the four unique colors from the unchanged object, sorted numerically, be `c1, c2, c3, c4`.
    *   If `c1 + c4 == c2 + c3`, the swaps applied to the target object are `c1 <-> c4` and `c2 <-> c3`. (Example 3)
    *   Otherwise, the swaps applied to the target object are `c1 <-> c3` and `c2 <-> c4`. (Examples 1 and 2)

## Documented Facts


```yaml
task_elements:
  - description: Input and Output are grids of colored pixels.
    type: grid_structure
  - description: Grids contain a background color (white, 0) and multiple non-white pixels forming objects.
    type: content
  - description: Objects are contiguous areas of non-white pixels.
    type: object_definition
  - description: Each example grid contains exactly two distinct non-white objects.
    type: object_count
  - description: One object's bounding box includes the top-left coordinate (0,0).
    id: obj_tl
    type: object_property
    feature: position_relation
    value: includes (0,0)
  - description: The other object's bounding box does not include the top-left coordinate (0,0).
    id: obj_target
    type: object_property
    feature: position_relation
    value: does_not_include (0,0)
  - description: The object 'obj_tl' remains unchanged in the output.
    type: transformation_effect
    target: obj_tl
    effect: unchanged
  - description: The object 'obj_target' has its colors modified in the output.
    type: transformation_effect
    target: obj_target
    effect: color_swap
  - description: The background pixels remain unchanged.
    type: transformation_effect
    target: background
    effect: unchanged
relationships_and_actions:
  - description: The set of unique non-white colors within 'obj_tl' determines the color swapping rule.
    type: rule_dependency
    source: obj_tl
    target: obj_target
    rule_aspect: color_set
  - description: The color swapping rule involves pairing the four unique colors found in 'obj_tl'.
    type: action_detail
    action: color_swap
    detail: pairing
  - description: Let the sorted unique colors from 'obj_tl' be S = [c1, c2, c3, c4]. A conditional check determines the pairs.
    type: rule_logic
    condition: c1 + c4 == c2 + c3
  - description: If the condition (c1 + c4 == c2 + c3) is true, the swap pairs are (c1, c4) and (c2, c3).
    type: rule_outcome
    condition_state: true
    pairs: [(c1, c4), (c2, c3)]
  - description: If the condition (c1 + c4 == c2 + c3) is false, the swap pairs are (c1, c3) and (c2, c4).
    type: rule_outcome
    condition_state: false
    pairs: [(c1, c3), (c2, c4)]
  - description: The determined color swap pairs are applied pixel-wise only within 'obj_target'.
    type: action_application
    action: color_swap
    scope: obj_target
```


## Natural Language Program

1.  Identify all distinct, contiguous objects composed of non-white pixels in the input grid.
2.  Locate the object whose bounding box includes the top-left pixel (coordinate 0,0). Call this the "source object".
3.  Locate the object whose bounding box does *not* include the top-left pixel. Call this the "target object". (Assume there is exactly one source and one target object).
4.  Find the set of unique non-white colors present within the source object.
5.  Sort these unique colors numerically. Let the sorted list be `[c1, c2, c3, c4]`.
6.  Determine the two pairs of colors to be swapped:
    *   Check if the sum of the first and fourth color (`c1 + c4`) is equal to the sum of the second and third color (`c2 + c3`).
    *   If the sums are equal, the swap pairs are `(c1, c4)` and `(c2, c3)`.
    *   If the sums are *not* equal, the swap pairs are `(c1, c3)` and `(c2, c4)`.
7.  Create the output grid by starting with a copy of the input grid.
8.  For every pixel within the bounds of the target object:
    *   Get the input color of the pixel.
    *   Check if this color matches one of the colors in the determined swap pairs.
    *   If it matches a color in a pair, change the pixel's color in the output grid to the *other* color in that same pair.
    *   If the pixel's color is not part of any swap pair (e.g., if it was white, although target objects are defined as non-white), leave it unchanged.
9.  Pixels belonging to the source object and background pixels remain unchanged from the input grid.
10. The final modified grid is the output.
