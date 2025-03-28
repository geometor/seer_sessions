
## train_1

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


## train_2

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

Okay, let's break down the task.

**Perception of Elements:**

1.  **Grid Structure:** The inputs and outputs are 2D grids of pixels with different colors (represented by integers 0-9). The background is predominantly white (0).
2.  **Objects:** In each input grid, there are typically two distinct non-white entities:
    *   A larger, multi-colored, connected object (let's call it the "pattern object"). This object always contains at least one gray (5) pixel.
    *   A single, isolated gray (5) pixel (let's call it the "marker pixel").
3.  **Transformation:** The output grid retains the original pattern object in its initial position. A modified copy of the pattern object is added to the grid.
4.  **Copy Placement:** The position of the copied object seems determined by the location of the marker pixel in the input. Specifically, the marker pixel's location in the input corresponds to the location where the gray pixel *from within the pattern object* should be placed in the output copy.
5.  **Modification:** The copied object is identical to the original pattern object, except that the gray pixel within the pattern object is replaced with a white (0) pixel in the copied version. The original marker pixel location is overwritten by the corresponding pixel from the copied pattern object (which might be white or another color, depending on the pattern object's structure relative to its internal gray pixel).

**YAML Facts:**


```yaml
task_description: "Copy a pattern object to a new location specified by a marker pixel, modifying the copy."
elements:
  - type: grid
    properties:
      - background_color: white (0)
      - contains: objects
  - type: object
    identifier: pattern_object
    properties:
      - composed_of: multiple connected non-white pixels
      - contains: at least one gray (5) pixel
      - location: variable
      - persistence: remains unchanged in the output
  - type: object
    identifier: marker_pixel
    properties:
      - composed_of: single gray (5) pixel
      - location: variable, separate from pattern_object
      - role: indicates target location for a specific part of the pattern_object
  - type: object
    identifier: copied_object
    properties:
      - exists_in: output only
      - structure: identical to pattern_object, except for one modification
      - modification: the gray pixel corresponding to the one in pattern_object is replaced by white (0)
      - location: determined by marker_pixel and the relative position of the gray pixel within pattern_object
relationships:
  - type: positional_mapping
    source: marker_pixel location (input)
    target: gray pixel location within copied_object (output)
    details: The input marker pixel's coordinates define where the gray pixel from the original pattern_object should land in the output's copied version.
actions:
  - action: identify
    target: pattern_object
    criteria: largest connected non-white component containing a gray pixel
  - action: identify
    target: marker_pixel
    criteria: single isolated gray pixel
  - action: identify
    target: gray_pixel_in_pattern
    criteria: gray pixel within the bounds of pattern_object
  - action: calculate_offset
    input1: gray_pixel_in_pattern coordinates
    input2: pattern_object top-left corner coordinates
    output: relative_offset (row_offset, col_offset)
  - action: calculate_copy_origin
    input1: marker_pixel coordinates
    input2: relative_offset
    output: copied_object top-left corner coordinates
  - action: copy_and_modify
    source: pattern_object
    destination_grid: output grid
    destination_origin: copied_object top-left corner coordinates
    modification: replace pixel at relative_offset within the copy with white (0)
    preserve_original: yes
```


**Natural Language Program:**

1.  Initialize the output grid as a copy of the input grid.
2.  Identify the main connected "pattern object" (composed of non-white pixels and containing at least one gray pixel). Determine its bounding box and the coordinates of the gray pixel(s) within it. Assuming there is only one such gray pixel.
3.  Identify the single, isolated "marker pixel" (which is gray). Determine its coordinates.
4.  Calculate the relative offset (row\_offset, col\_offset) of the gray pixel within the pattern object with respect to the pattern object's top-left corner.
5.  Calculate the target top-left corner coordinates for the copied object by subtracting the relative offset from the marker pixel's coordinates:
    *   `copy_row = marker_row - row_offset`
    *   `copy_col = marker_col - col_offset`
6.  Iterate through each pixel (`pixel_color`) of the original pattern object at its relative position (`rel_row`, `rel_col`) within its bounding box.
7.  Determine the corresponding absolute coordinates (`target_row`, `target_col`) in the output grid where this pixel should be copied:
    *   `target_row = copy_row + rel_row`
    *   `target_col = copy_col + rel_col`
8.  Check if the current relative position (`rel_row`, `rel_col`) matches the relative offset (`row_offset`, `col_offset`) of the gray pixel found in step 4.
9.  If it matches, set the pixel color at (`target_row`, `target_col`) in the output grid to white (0).
10. If it does not match, set the pixel color at (`target_row`, `target_col`) in the output grid to the `pixel_color` from the original pattern object. Ensure this write operation stays within the grid boundaries.
