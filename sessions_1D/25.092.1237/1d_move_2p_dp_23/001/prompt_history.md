
## train_1

**input:**
```
0 3 3 3 3 3 0 0 8 0 0
```


**output:**
```
0 0 0 3 3 3 3 3 8 0 0
```


## train_2

**input:**
```
3 3 3 3 3 0 0 8 0 0 0
```


**output:**
```
0 0 3 3 3 3 3 8 0 0 0
```


## train_3

**input:**
```
0 4 4 4 4 4 0 0 8 0 0
```


**output:**
```
0 0 0 4 4 4 4 4 8 0 0
```

Okay, let's analyze the task based on the provided examples.

## Perception of Elements

1.  **Grid Structure:** All examples are 1-dimensional arrays (or 1xN grids).
2.  **Colors Present:** The colors involved are white (0), green (3), yellow (4), and azure (8).
3.  **Key Anchor:** The azure pixel (8) seems to be a crucial element, acting as a separator or anchor point in the array. Its position relative to other elements changes, but its value remains constant.
4.  **Main Object:** There is always a contiguous block of a single non-zero, non-eight color (green '3' or yellow '4'). This block's relative order with respect to the azure pixel (8) is maintained.
5.  **Background/Filler:** The white pixels (0) appear to be background or filler elements. Their positions change significantly between input and output.
6.  **Transformation Focus:** The transformation seems to involve rearranging the white pixels (0) that appear *before* the azure pixel (8) in the input array.

## Facts


```yaml
task_type: array_manipulation_1d
components:
  - type: anchor_pixel
    color: azure # 8
    role: acts as a separator for rearranging elements
    count: 1 per array
  - type: background_pixel
    color: white # 0
    role: rearranged based on position relative to the anchor
  - type: object_pixel
    color: varies (green '3', yellow '4')
    role: maintains relative order with anchor and other object pixels
    properties:
      - form contiguous blocks before the anchor
elements_before_anchor:
  - type: background_pixels
    color: white # 0
  - type: object_pixels
    color: varies (green '3', yellow '4')
elements_after_anchor:
  - type: potentially_any_pixels (in examples, only white '0')
transformation:
  - action: identify_anchor
    target: azure pixel (8)
  - action: partition_array
    based_on: anchor position
    creates:
      - prefix (elements before anchor)
      - anchor (the '8' pixel)
      - suffix (elements after anchor)
  - action: partition_prefix
    based_on: color
    creates:
      - prefix_background (white '0' pixels from prefix)
      - prefix_objects (non-'0' pixels from prefix, maintaining relative order)
  - action: reconstruct_array
    order:
      - prefix_background
      - prefix_objects
      - anchor
      - suffix
```


## Natural Language Program

1.  Identify the position (index) of the azure pixel (color 8) in the input array.
2.  Divide the input array into three segments:
    *   `prefix`: All elements *before* the azure pixel.
    *   `anchor`: The azure pixel (8) itself.
    *   `suffix`: All elements *after* the azure pixel.
3.  Within the `prefix` segment, separate the elements into two groups, maintaining the relative order within each group:
    *   `prefix_zeros`: All white pixels (color 0).
    *   `prefix_non_zeros`: All pixels that are not white (color 0).
4.  Construct the output array by concatenating the segments in the following order:
    *   `prefix_zeros`
    *   `prefix_non_zeros`
    *   `anchor`
    *   `suffix`
