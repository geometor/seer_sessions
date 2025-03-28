Okay, let's break down these examples.

**Perception of Elements:**

1.  **Blue Line:** Each example features a single, straight line composed entirely of blue (1) pixels. This line is either perfectly horizontal or perfectly vertical. It seems to act as a separator or an axis.
2.  **Objects:** In each input grid, besides the blue line and the white (0) background, there is at least one distinct shape or object composed of other colors. These objects are located entirely on one side of the blue line.
3.  **Color Pairs:** The objects are composed of specific color pairs:
    *   Example 1: Azure (8) and Yellow (4)
    *   Example 2: Red (2) and Green (3)
    *   Example 3: Gray (5) and Magenta (6)
4.  **Transformation:** The primary transformation appears to be a reflection of the object(s) across the blue line.
5.  **Color Swapping:** During the reflection, the colors within the object are swapped according to the pairs identified above (8<->4, 2<->3, 5<->6).
6.  **Conditional Removal:** A key difference is observed:
    *   In Example 1 (vertical blue line), the original object remains in the output along with its reflection.
    *   In Examples 2 and 3 (horizontal blue lines), the original object is *removed* (replaced by white pixels) in the output, leaving only the reflection.

**YAML Facts:**


```yaml
task_description: Reflect objects across a central blue line, swapping specific color pairs, and conditionally removing the original object based on the line's orientation.

elements:
  - type: background
    color: white (0)
  - type: axis
    color: blue (1)
    shape: straight line (horizontal or vertical)
    role: acts as a mirror/axis of reflection
  - type: object
    location: entirely on one side of the blue axis
    composition: contiguous pixels of specific color pairs
    color_pairs:
      - [red (2), green (3)]
      - [yellow (4), azure (8)]
      - [gray (5), magenta (6)]

actions:
  - name: identify_axis
    input: input_grid
    output: blue line coordinates and orientation (horizontal/vertical)
  - name: identify_objects
    input: input_grid, axis_coordinates
    output: list of objects (pixel coordinates and colors) located on one side of the axis
  - name: reflect_object
    input: object, axis
    output: coordinates of the reflected object
    constraints:
      - reflection is geometric (horizontal reflection for vertical axis, vertical reflection for horizontal axis)
  - name: swap_colors
    input: reflected_object, color_pairs
    output: reflected_object with swapped colors (e.g., 2 becomes 3, 3 becomes 2; 4 becomes 8, 8 becomes 4; 5 becomes 6, 6 becomes 5)
  - name: place_reflection
    input: output_grid, color_swapped_reflection
    output: output_grid with the reflected object added
  - name: conditional_removal
    input: output_grid, original_object, axis_orientation
    output: output_grid
    condition: if axis is horizontal, replace original_object pixels with white (0)

relationships:
  - The blue line divides the grid into two regions.
  - Objects exist exclusively in one region relative to the blue line.
  - The transformation maps an object from one region to the other via reflection across the blue line.
  - Color transformation (swapping) is coupled with the spatial transformation (reflection).
  - The persistence or removal of the original object depends on the orientation of the blue line axis.

output_grid_composition:
  - Contains the original blue axis.
  - Contains the color-swapped reflection of the input object(s).
  - If the axis was vertical, it also contains the original object(s).
  - If the axis was horizontal, the area of the original object(s) is replaced with the background color (white).
  - Background pixels remain unchanged unless overwritten by a reflection or cleared due to original object removal.
```


**Natural Language Program:**

1.  Initialize the output grid as a copy of the input grid.
2.  Identify the single straight line of blue (1) pixels. Determine its orientation (horizontal or vertical) and its position (row index if horizontal, column index if vertical).
3.  Identify all distinct objects composed of non-white (0) and non-blue (1) pixels.
4.  For each identified object:
    a.  Check if the object lies entirely on one side of the blue line.
    b.  If it does, calculate the coordinates for the reflection of this object across the blue line.
    c.  For each pixel in the reflected position:
        i.  Determine the color of the corresponding pixel in the original object.
        ii. Apply a color swap based on the following pairs: Red (2) <-> Green (3), Yellow (4) <-> Azure (8), Gray (5) <-> Magenta (6). If the original color is not in these pairs, keep the original color (though this case is not present in the examples).
        iii. Place the swapped color pixel at the calculated reflected coordinate in the output grid.
    d.  If the blue line's orientation is **horizontal**, overwrite the pixels of the original object in the output grid with white (0). (If the orientation is vertical, leave the original object untouched in the output grid).
5.  Return the modified output grid.