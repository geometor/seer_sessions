
## train_1

**input:**
```
0 4 0 0 0 0 2 0 0
0 0 0 0 0 2 0 0 0
0 0 0 0 2 0 2 0 0
0 0 0 0 0 0 0 2 0
0 0 0 4 0 0 0 0 0
0 0 0 0 0 0 0 0 3
```


**output:**
```
0 0 0 0 0 0 2 0 0
0 0 0 0 0 2 0 0 0
0 0 0 0 2 0 2 0 0
0 0 0 0 0 0 0 2 0
0 0 0 0 0 0 0 0 4
0 0 0 0 0 0 0 4 4
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 7 0 0 0
0 0 0 0 1 0 0 0 7 0 0
0 0 2 0 0 0 0 0 7 7 0
0 0 0 0 0 0 0 7 0 0 7
0 0 0 3 0 0 7 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 7 0 0 0 0 0 0 0
0 0 0 0 2 0 0 0 0 0 0
8 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 7 0 0 0
0 0 0 0 0 0 0 0 7 0 0
0 0 0 0 0 0 0 0 7 7 0
0 0 0 0 0 0 0 7 0 0 7
2 0 0 0 0 0 7 0 0 0 0
2 2 0 0 0 0 0 0 0 0 0
2 2 2 0 0 0 0 0 0 0 0
2 2 2 2 0 0 0 0 0 0 0
2 2 2 2 2 0 0 0 0 0 0
```


## train_3

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 6
0 0 0 0 0 0 0 0 8 8 8 0 0 0
0 0 0 0 0 0 0 8 0 0 0 0 0 0
0 0 0 0 0 0 8 8 0 0 0 6 0 0
0 0 0 0 0 8 0 0 8 0 0 0 0 0
0 0 0 0 0 8 0 0 0 8 0 0 0 0
0 0 0 0 0 8 0 0 0 0 8 0 0 0
0 0 0 0 0 0 0 0 0 0 0 8 0 0
0 0 0 0 0 0 0 0 0 0 0 0 8 0
0 0 0 0 0 0 0 0 0 0 0 0 0 8
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 3 0 0 0 6 0 0 0 0 0 6
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 8 8 8 0 0 0
0 0 0 0 0 0 0 8 0 0 0 0 0 0
0 0 0 0 0 0 8 8 0 0 0 0 0 0
0 0 0 0 0 8 0 0 8 0 0 0 0 0
0 0 0 0 0 8 0 0 0 8 0 0 0 0
0 0 0 0 0 8 0 0 0 0 8 0 0 0
0 0 0 0 0 0 0 0 0 0 0 8 0 0
0 0 0 0 0 0 0 0 0 0 0 0 8 0
0 0 0 0 0 0 0 0 0 0 0 0 0 8
0 0 0 0 0 0 0 0 0 0 0 0 0 6
0 0 0 0 0 0 0 0 0 0 0 0 6 6
0 0 0 0 0 0 0 0 0 0 0 6 6 6
0 0 0 0 0 0 0 0 0 0 6 6 6 6
```


## train_4

**input:**
```
9 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 8 0 0 0 0 0 0
0 0 0 0 8 0 8 0 0 0
0 0 0 0 0 8 0 0 0 0
0 0 0 0 8 0 0 0 7 0
0 7 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 4 0 0 8 0 0 0 3 0
```


**output:**
```
7 7 7 7 7 0 0 0 0 0
7 7 7 7 0 0 0 0 0 0
7 7 7 0 0 0 0 0 0 0
7 7 0 8 0 0 0 0 0 0
7 0 0 0 8 0 8 0 0 0
0 0 0 0 0 8 0 0 0 0
0 0 0 0 8 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

*   **Perception:**
    *   Each input grid contains multiple non-white colors, often scattered.
    *   Each output grid retains some pixels from the input grid in their original locations, while other pixels are removed, and a new geometric shape is added in one of the corners.
    *   There appears to be one "static" color in each pair, whose pixels remain unchanged. All other non-white colors are "dynamic".
    *   The dynamic pixels are removed from their original positions.
    *   A new shape (either a square or a triangle) is drawn in one corner of the grid.
    *   The color of the new shape is determined by one of the dynamic colors – specifically, the dynamic color that appeared most frequently in the input. If there's a tie in frequency, the color with the higher index seems to be chosen. Let's call this the "actor color".
    *   The size of the new shape (side length N for triangles, N x N for squares) is determined by the total count (N) of all dynamic pixels in the input.
    *   The type of shape (square or triangle), its corner location, and its orientation depend specifically on the *actor color's index*.
        *   Actor Red (2): Results in a N-side triangle in the Bottom-Left corner, pointing Up-Right.
        *   Actor Yellow (4): Results in a 2x2 square in the Bottom-Right corner (specifically when N=2).
        *   Actor Magenta (6): Results in a N-side triangle in the Bottom-Right corner, pointing Up-Left.
        *   Actor Orange (7): Results in a N-side triangle in the Top-Left corner, pointing Down-Right.
    *   The final output combines the preserved static pixels and the newly drawn shape on a white background.

*   **Facts:**
    
```yaml
    task_type: object_transformation
    
    components:
      - role: background
        color: white (0)
      - role: static_pixels
        description: Pixels of a specific color that remain unchanged between input and output. Only one such color exists per example pair.
        properties:
          - color: Varies (red(2), orange(7), azure(8))
          - persistence: Position is maintained from input to output.
      - role: dynamic_pixels
        description: All non-white pixels that are not static. These are removed from their original locations.
        properties:
          - color: Varies (multiple colors possible)
          - persistence: Removed from original location.
          - role: contributes_to_size (N)
            value: The total count of all dynamic pixels determines the size parameter N for the output shape.
          - role: determines_actor_color (A)
            value: The dynamic color with the highest frequency (count) becomes the actor color A. Tie-breaking favors higher color index.
      - role: output_shape
        description: A geometric shape drawn in a corner of the output grid.
        properties:
          - color: Determined by the actor color A.
          - size: Determined by the total count N of dynamic pixels.
          - type: Square (if A=4 and N=2) or Triangle (otherwise, based on tested examples).
          - corner_location: Determined by the actor color A (e.g., A=2 -> BL, A=4 -> BR, A=6 -> BR, A=7 -> TL).
          - orientation: Determined by the actor color A (e.g., A=2 -> Up-Right, A=6 -> Up-Left, A=7 -> Down-Right).
    
    relationships:
      - type: identification
        from: input_grid
        to: static_pixels
        rule: Find the color S whose pixel locations are identical in input and output.
      - type: identification
        from: input_grid
        to: dynamic_pixels
        rule: All non-white pixels not belonging to the static color S.
      - type: calculation
        from: dynamic_pixels
        to: size_parameter_N
        rule: N = count(dynamic_pixels).
      - type: selection
        from: dynamic_pixels
        to: actor_color_A
        rule: A = color within dynamic_pixels with max frequency (count). Tie-break using highest color index.
      - type: determination
        from: actor_color_A, size_parameter_N
        to: output_shape properties (type, corner, orientation)
        rule: Based on specific rules mapping A (and potentially N) to shape characteristics (e.g., A=2 -> BL Triangle Up-Right size N; A=4 & N=2 -> BR Square size 2x2).
      - type: composition
        from: static_pixels, output_shape
        to: output_grid
        rule: Combine static pixels and the generated output shape on a white background of the original grid dimensions.
    ```


*   **Natural Language Program:**
    1.  Identify the "static color" `S` by finding which non-white color's pixels have the exact same coordinates in both the input and output grids. Store the locations of these static pixels.
    2.  Identify all "dynamic pixels" in the input grid: these are all non-white pixels that do not have the static color `S`.
    3.  Count the total number `N` of dynamic pixels.
    4.  Determine the frequency (count) of each color present among the dynamic pixels.
    5.  Identify the "actor color" `A` as the dynamic color with the highest frequency. If two or more dynamic colors share the highest frequency, choose the one with the largest color index as `A`.
    6.  Initialize the output grid as a white grid with the same dimensions as the input grid.
    7.  Place the identified static pixels (color `S`) onto the output grid at their original locations.
    8.  Determine the corner, shape type, orientation, and size based on the actor color `A` and the count `N`:
        *   If `A` is Red (2): Draw a right-angled triangle of side length `N` using color `A`, located in the Bottom-Left corner, with the hypotenuse facing Up-Right.
        *   If `A` is Yellow (4) and `N` is 2: Draw a 2x2 square using color `A`, located in the Bottom-Right corner.
        *   If `A` is Magenta (6): Draw a right-angled triangle of side length `N` using color `A`, located in the Bottom-Right corner, with the hypotenuse facing Up-Left.
        *   If `A` is Orange (7): Draw a right-angled triangle of side length `N` using color `A`, located in the Top-Left corner, with the hypotenuse facing Down-Right.
        *   (Define behavior for other potential actor colors or the case where A=Yellow(4) but N is not 2, if necessary based on test cases).
    9.  Draw the determined shape onto the output grid. Existing static pixels should not be overwritten (though based on examples, the shape area seems distinct from static pixel locations).
