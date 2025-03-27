
## train_1

**input:**
```
0 0 0 0 0 0 5 5 5 5
0 6 6 6 6 0 5 5 5 5
0 8 8 6 8 0 5 5 5 5
0 6 8 8 8 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 5 5 5 5 0 0
0 0 0 0 5 5 5 5 0 0
0 0 0 0 5 5 5 5 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 6 6 6 6
0 6 6 6 6 0 8 8 6 8
0 8 8 6 8 0 6 8 8 8
0 6 8 8 8 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 6 6 6 6 0 0
0 0 0 0 8 8 6 8 0 0
0 0 0 0 6 8 8 8 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 2 2 2 0 0 0 0 0 0
0 2 4 4 0 0 0 0 0 0
0 4 4 4 0 0 0 0 0 0
0 0 0 0 0 0 5 5 5 0
0 0 0 0 0 0 5 5 5 0
0 0 0 0 0 0 5 5 5 0
0 0 5 5 5 0 0 0 0 0
0 0 5 5 5 0 0 0 0 0
0 0 5 5 5 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0
0 2 2 2 0 0 0 0 0 0
0 2 4 4 0 0 0 0 0 0
0 4 4 4 0 0 0 0 0 0
0 0 0 0 0 0 2 2 2 0
0 0 0 0 0 0 2 4 4 0
0 0 0 0 0 0 4 4 4 0
0 0 2 2 2 0 0 0 0 0
0 0 2 4 4 0 0 0 0 0
0 0 4 4 4 0 0 0 0 0
```

*   **Perception**
    The input grid contains multiple distinct objects composed of non-white pixels. One of these objects has a unique structure and uses multiple colors (excluding gray). The other objects are composed solely of gray pixels and often have simpler shapes (like rectangles or squares in the examples). The transformation identifies the unique, non-gray object as a "pattern" and the gray objects as "targets". Each target object in the input is replaced by a copy of the pattern object in the output. The original pattern object remains in its original position in the output. The replacement aligns the top-left corner of the pattern copy with the top-left corner of the bounding box of the gray object being replaced.

*   **Facts**
    
```yaml
    elements:
      - object: pattern_object
        description: The single contiguous block of non-white pixels that is not composed entirely of gray (color 5). It can be multi-colored.
        properties:
          - shape: Variable, defined by its pixel arrangement.
          - colors: Contains colors other than white (0) and gray (5).
          - count: Exactly one per input grid.
      - object: target_object
        description: Contiguous blocks of pixels composed entirely of gray (color 5).
        properties:
          - shape: Variable, often simple rectangles/squares in examples.
          - colors: Exclusively gray (5).
          - count: One or more per input grid.
      - object: background
        description: Pixels with the white color (0).
    relationships:
      - type: spatial
        description: pattern_object and target_objects occupy distinct locations within the input grid.
      - type: identification
        description: The pattern_object is identified by its non-gray composition, while target_objects are identified by their exclusively gray composition.
    actions:
      - action: identify
        actor: system
        input: input_grid
        output: pattern_object, list_of_target_objects
        description: Segment the grid into objects and classify them based on color composition (gray vs. non-gray).
      - action: replace
        actor: system
        input: target_object, pattern_object
        output: modified_grid_area
        description: For each target_object, determine its top-left corner coordinates. Copy the pattern_object and place it onto the output grid such that the pattern_object's top-left corner aligns with the target_object's original top-left corner.
      - action: preserve
        actor: system
        input: pattern_object, background
        output: final_output_grid
        description: Ensure the original pattern_object and unchanged background pixels are present in the final output grid along with the replaced target areas.
    ```


*   **Natural Language Program**
    1.  Initialize the output grid as a copy of the input grid.
    2.  Identify all contiguous objects of non-white pixels in the input grid.
    3.  Find the unique object that contains colors other than gray (5). This is the `pattern_object`. Store its pixel data and its top-left coordinates.
    4.  Identify all objects composed exclusively of gray (5) pixels. These are the `target_objects`.
    5.  For each `target_object`:
        a.  Determine the coordinates of its top-left pixel.
        b.  Iterate through the pixels of the `pattern_object`. For each pixel in the `pattern_object` at relative coordinates (dx, dy) from its own top-left corner:
            i.  Calculate the corresponding coordinates in the output grid: (target_top_left_row + dx, target_top_left_col + dy).
            ii. Overwrite the pixel at these output grid coordinates with the color of the `pattern_object` pixel at (dx, dy).
    6.  Return the modified output grid.
