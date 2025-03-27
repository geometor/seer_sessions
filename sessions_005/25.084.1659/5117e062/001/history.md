
## train_1

**input:**
```
0 0 0 0 0 0 0 0 2 0 0 0 0
0 0 0 0 0 0 0 2 2 2 0 0 0
0 0 0 0 0 0 0 0 2 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 3 3 0 0 0 0 0 0 0 0
0 0 3 8 0 0 0 0 0 0 0 0 0
0 0 0 3 3 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 1 0 1 0 0 0
0 0 0 0 0 0 0 1 1 1 0 0 0
0 0 0 0 0 0 0 1 1 1 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 3 3
3 3 0
0 3 3
```


## train_2

**input:**
```
0 0 3 0 0 0 0 0 0 0 4 0 0
0 3 3 3 0 0 0 0 0 4 8 4 0
0 3 3 0 0 0 0 0 0 0 4 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 2 0 0 0 0 0 0 0 0
0 0 0 0 2 2 2 0 0 0 0 0 0
0 0 0 0 0 2 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 6 6 0 0
0 0 0 0 0 0 0 0 6 0 6 0 0
0 0 0 0 0 0 0 0 6 6 6 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 4 0
4 4 4
0 4 0
```


## train_3

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 2 2 0 0 0 0 0 0 0 0 0
0 0 8 0 0 0 0 0 3 0 3 0 0
0 2 2 0 0 0 0 0 3 3 3 0 0
0 0 0 0 0 0 0 0 0 0 3 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 1 0 1 0 0 0 0 0 0 0
0 0 0 1 1 1 0 0 0 0 0 0 0
0 0 0 0 1 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
2 2 2
0 2 0
2 2 0
```

Okay, let's break down this task.

**Perception**

1.  **Input Grid:** The input grids are consistently 13x13. They contain several small, distinct objects composed of non-white pixels, scattered on a white background.
2.  **Objects:** The objects are typically simple shapes. Notably, in each example, exactly one object contains an azure (8) pixel, usually near its center. This object is composed primarily of another color (green in train_1, yellow in train_2, red in train_3). Other objects exist but do not contain azure pixels.
3.  **Output Grid:** The output grids are always 3x3.
4.  **Transformation:** The transformation seems to focus specifically on the azure pixel and its immediate surroundings. The output grid appears to be a direct copy of the 3x3 area centered on the azure pixel in the input grid, with one modification: the central azure pixel itself is replaced.
5.  **Color Replacement:** The azure pixel in the center of the 3x3 output is replaced by the dominant non-white, non-azure color found within that 3x3 neighborhood in the input. In all examples, this replacement color is the primary color of the object containing the azure pixel (green, yellow, red respectively).

**Facts YAML**


```yaml
task_description: Identify the azure pixel, extract its 3x3 neighborhood, and replace the central azure pixel with the dominant neighboring color.
grid_properties:
  input_size: 13x13
  output_size: 3x3
  background_color: 0 (white)
objects:
  - type: marker_pixel
    color: 8 (azure)
    occurrence: exactly one per input grid
    role: defines the center of the transformation area
  - type: primary_object
    description: The object containing the azure pixel.
    properties:
      - has a primary color (non-white, non-azure)
      - contains the azure pixel
  - type: other_objects
    description: Other distinct shapes in the input grid.
    properties:
      - do not contain azure pixels
      - seem irrelevant to the transformation
transformation_area:
  shape: square
  size: 3x3
  location: centered on the azure pixel in the input grid
actions:
  - action: locate
    target: azure pixel (8)
    result: coordinates (row, col)
  - action: extract
    target: 3x3 neighborhood around the azure pixel's coordinates
    result: 3x3 subgrid from input
  - action: identify_replacement_color
    source: the extracted 3x3 subgrid
    method: find the most frequent color that is not white (0) and not azure (8)
    result: replacement_color
  - action: generate_output
    size: 3x3
    method: copy the extracted 3x3 subgrid, replacing the central pixel (originally azure) with the replacement_color
```


**Natural Language Program**

1.  Scan the input grid to find the coordinates (row `r`, column `c`) of the single azure (8) pixel.
2.  Define a 3x3 area in the input grid centered at `(r, c)`. This area includes pixels from `(r-1, c-1)` to `(r+1, c+1)`.
3.  Extract this 3x3 subgrid from the input grid.
4.  Examine the colors within this extracted 3x3 subgrid. Identify the dominant color present that is *not* white (0) and *not* azure (8). Let this be the `replacement_color`.
5.  Create a new 3x3 output grid.
6.  Copy the pixels from the extracted 3x3 subgrid to the output grid, with one exception: place the `replacement_color` at the center position (1, 1) of the output grid (corresponding to the original azure pixel's position within the 3x3 subgrid).
