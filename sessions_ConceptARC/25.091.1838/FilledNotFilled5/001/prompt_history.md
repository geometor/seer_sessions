
## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 0 0
0 3 3 3 3 3 3 3 3 3 0
0 3 0 0 0 0 0 0 0 3 0
0 3 0 0 0 0 0 0 0 3 0
0 3 0 0 0 0 0 0 0 3 0
0 3 0 0 0 0 0 0 0 3 0
0 3 0 0 0 0 0 0 0 3 0
0 3 0 0 0 0 0 0 0 3 0
0 3 3 3 3 3 3 3 3 3 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0
0 3 3 3 3 3 3 3 3 3 0
0 3 3 3 3 3 3 3 3 3 0
0 3 3 3 3 3 3 3 3 3 0
0 3 3 3 3 3 3 3 3 3 0
0 3 3 3 3 3 3 3 3 3 0
0 3 3 3 3 3 3 3 3 3 0
0 3 3 3 3 3 3 3 3 3 0
0 3 3 3 3 3 3 3 3 3 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 2 0 0 0 0 0 0
0 0 0 0 2 2 2 0 0 0 0 0
0 0 0 2 2 2 2 2 0 0 0 0
0 0 2 2 2 2 2 2 2 0 0 0
0 0 0 2 2 2 2 2 0 0 0 0
0 0 0 0 2 2 2 0 0 0 0 0
0 0 0 0 0 2 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 2 0 0 0 0 0 0
0 0 0 0 2 0 2 0 0 0 0 0
0 0 0 2 0 0 0 2 0 0 0 0
0 0 2 0 0 0 0 0 2 0 0 0
0 0 0 2 0 0 0 2 0 0 0 0
0 0 0 0 2 0 2 0 0 0 0 0
0 0 0 0 0 2 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

Okay, let's analyze the provided examples.

**Perception of the Elements:**

1.  **Example 1 (train_1):**
    *   The input grid contains a hollow square frame made of green pixels (3) on a white background (0).
    *   The output grid shows the same frame, but the hollow area inside the frame has been filled with green pixels (3).
    *   The transformation involves identifying the hollow region enclosed by the green frame and filling it with the same green color.

2.  **Example 2 (train_2):**
    *   The input grid contains a solid diamond shape made of red pixels (2) on a white background (0).
    *   The output grid shows a hollow diamond shape. The outermost layer of red pixels from the input remains, but the interior red pixels have been changed to the background color (white, 0).
    *   The transformation involves identifying the interior pixels of the solid red shape and changing them to the background color, effectively hollowing out the shape.

**General Observation:**

The task seems to involve identifying a single, primary colored object on a background. The transformation depends on whether this object is initially "hollow" (contains an enclosed background area) or "solid" (does not contain an enclosed background area). If the object is hollow, it gets filled with its own color. If the object is solid, its interior is removed (changed to the background color), making it hollow. The "background" color is consistently white (0) in the examples. The "object" color varies (green or red).

**YAML Facts:**


```yaml
task_type: object_transformation
input_features:
  - grid: 2D array of integers (colors)
  - background_color: dominant color, typically white (0)
  - primary_object: contiguous shape of a single non-background color
properties:
  - object_color: color of the primary object
  - object_state:
      type: categorical
      values: [hollow, solid]
      definition:
        hollow: contains one or more regions of background_color fully enclosed by object_color pixels.
        solid: does not contain any background_color regions fully enclosed by object_color pixels.
transformation: conditional_fill_or_hollow
conditions:
  - if: object_state == hollow
    action: fill_hollow_region
    parameters:
      fill_color: object_color
      target_pixels: enclosed background_color pixels
  - if: object_state == solid
    action: hollow_solid_object
    parameters:
      hollow_color: background_color
      target_pixels: interior object_color pixels (pixels whose 8 neighbors are all object_color)
output_features:
  - grid: transformed 2D array
relationship: the output grid dimensions are the same as the input grid dimensions. The transformation modifies pixels based on the object's state (hollow/solid) and geometry.
```


**Natural Language Program:**

1.  Identify the background color (typically white, 0) and the primary object's color (the single non-background color present).
2.  Determine if the primary object in the input grid is "hollow" or "solid":
    *   Check if there are any background-colored pixels completely surrounded by object-colored pixels (using 4-way adjacency/flood fill from the border is a good way to test: any background pixel *not* reached by a flood fill starting from the border background pixels is enclosed).
    *   If such enclosed background pixels exist, the object is "hollow".
    *   Otherwise, the object is "solid".
3.  If the object is "hollow":
    *   Identify all enclosed background-colored pixels (the "holes").
    *   Change the color of these "hole" pixels to the object's color. Keep all other pixels unchanged.
4.  If the object is "solid":
    *   Identify all "interior" pixels of the object. An interior pixel is an object-colored pixel where all 8 of its immediate neighbors (Moore neighborhood) are also the object's color.
    *   Change the color of these "interior" pixels to the background color (white, 0). Keep all other pixels unchanged.
5.  The resulting grid is the output.
