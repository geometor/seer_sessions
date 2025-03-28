
## train_1

**input:**
```
0 0 0 3 0 0 0 0 0 0
0 0 1 3 1 0 0 0 0 0
0 4 4 5 0 0 0 0 0 0
0 0 0 1 0 0 0 0 0 0
0 0 0 7 2 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 5 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 3 0 0 0 0 0 0
0 0 1 3 1 0 0 0 0 0
0 4 4 5 0 0 0 0 0 0
0 0 0 1 0 0 0 0 0 0
0 0 0 7 2 0 0 0 0 0
0 0 0 0 0 0 3 0 0 0
0 0 0 0 0 1 3 1 0 0
0 0 0 0 4 4 0 0 0 0
0 0 0 0 0 0 1 0 0 0
0 0 0 0 0 0 7 2 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 3 3 0 0 0 0 0 0 0 0
0 0 2 2 0 0 0 0 0 0 0 0
0 0 2 5 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 5 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 3 3 0 0 0 0 0 0 0 0
0 0 2 2 0 0 0 0 0 0 0 0
0 0 2 5 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 3 3 0 0 0 0
0 0 0 0 0 0 2 2 0 0 0 0
0 0 0 0 0 0 2 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```


## train_3

**input:**
```
0 0 0 1 0 0 0 0 0 0
0 0 0 1 1 0 0 0 0 0
0 0 0 5 2 0 0 0 0 0
0 0 0 0 2 3 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 5 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 1 0 0 0 0 0 0
0 0 0 1 1 0 0 0 0 0
0 0 0 5 2 0 0 0 0 0
0 0 0 0 2 3 0 0 0 0
0 0 1 0 0 0 0 0 0 0
0 0 1 1 0 0 0 0 0 0
0 0 0 2 0 0 0 0 0 0
0 0 0 2 3 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

Okay, let's break down this task.

**Perception**

1.  **Input Structure:** Each input grid contains various colored pixels on a white background. Critically, there are always exactly two gray (5) pixels present.
2.  **Objects:** There appears to be one primary "source" object composed of connected non-white pixels. One of the gray pixels is part of this source object. The second gray pixel is always isolated, acting as a single-pixel "target marker" object.
3.  **Transformation:** The core transformation is a copy-and-translate operation. The source object (excluding its internal gray pixel) is copied.
4.  **Translation Vector:** The translation is determined by the relative positions of the two gray pixels. The gray pixel *within* the source object acts as an "anchor point," and the isolated gray pixel acts as the "target point." The copy is placed such that where the anchor point *was*, the target point *now is*.
5.  **Output Structure:** The output grid contains the original source object unchanged. It also contains the translated copy of the source object's non-gray pixels. The isolated gray target marker pixel from the input is overwritten, either by a pixel from the copied object or by the background color (white) if no part of the copied object lands on its position.

**Facts**


```yaml
facts:
  - grid_elements:
      - type: background
        color: white (0)
      - type: pixel
        color: various (1-9)
  - key_pixels:
      - type: gray_pixel
        color: gray (5)
        count: 2
        roles:
          - role: anchor_point
            description: Belongs to a larger connected component (source_object).
          - role: target_point
            description: Is isolated (forms a 1x1 object).
  - objects:
      - type: source_object
        description: A connected component of non-white pixels containing the anchor_point gray pixel.
        properties:
          - shape: variable
          - colors: multiple, including gray (5)
      - type: target_marker
        description: The isolated gray pixel at the target_point.
        properties:
          - shape: 1x1 pixel
          - color: gray (5)
  - relationships:
      - type: spatial
        description: The relative position between the anchor_point and target_point defines a translation vector.
        vector: target_point_location - anchor_point_location
  - actions:
      - action: identify_gray_pixels
        input: input_grid
        output: locations of the two gray pixels
      - action: identify_source_object_and_anchor
        input: input_grid, gray_pixel_locations
        output: source_object (set of pixel coords and colors), anchor_point_location
      - action: identify_target_point
        input: gray_pixel_locations, anchor_point_location
        output: target_point_location
      - action: calculate_translation
        input: anchor_point_location, target_point_location
        output: offset_vector (dr, dc)
      - action: copy_and_translate
        input: input_grid, source_object, offset_vector, target_point_location
        output: output_grid
        steps:
          - Initialize output_grid as a copy of input_grid.
          - Set pixel at target_point_location in output_grid to white (0).
          - For each pixel (r, c) with color 'col' in source_object:
              - If 'col' is NOT gray (5):
                  - Calculate destination: (dest_r, dest_c) = (r + dr, c + dc)
                  - If (dest_r, dest_c) is within grid bounds:
                      - Set output_grid[dest_r, dest_c] = col
```


**Natural Language Program**

1.  **Find Gray Pixels:** Locate the coordinates of the two gray (5) pixels in the input grid.
2.  **Identify Anchor and Target:** Determine which gray pixel is part of a larger connected component of non-white pixels (this is the "anchor point" and its component is the "source object") and which gray pixel is isolated (this is the "target point"). Use connectivity analysis (considering adjacent non-white pixels, including diagonals if necessary, although side-adjacency seems sufficient based on examples) to distinguish them.
3.  **Calculate Offset:** Compute the row and column difference needed to move from the anchor point's coordinates to the target point's coordinates. This is the translation vector (`offset = target_point - anchor_point`).
4.  **Initialize Output:** Create a new grid identical to the input grid. This will be modified to become the output grid.
5.  **Clear Target Marker:** In the new grid, change the color of the pixel at the target point's coordinates to white (0).
6.  **Copy Source Object (excluding anchor):** Iterate through every pixel belonging to the identified source object.
7.  **Translate and Draw:** For each pixel from the source object *that is not the gray anchor point pixel*:
    a.  Calculate its destination coordinates by adding the translation vector (from step 3) to its original coordinates.
    b.  Check if the calculated destination coordinates are within the bounds of the grid.
    c.  If they are within bounds, update the pixel at the destination coordinates in the new grid with the color of the current source object pixel. This will overwrite any existing pixel, including the white pixel potentially placed in step 5.
8.  **Final Output:** The modified grid is the final output.
