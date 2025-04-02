
## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 3 3 3 3 3 3 0 0 0
0 3 0 0 0 0 3 0 0 0
0 3 0 4 4 0 3 0 0 0
0 3 0 0 0 0 3 0 0 0
0 3 3 3 3 3 3 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 4 4 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0
0 3 3 3 3 3 3 0 0 0
0 3 0 0 0 0 3 0 0 0
0 3 0 0 0 0 3 0 0 0
0 3 0 0 0 0 3 0 0 0
0 3 3 3 3 3 3 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 4 4 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 1 1 0
0 2 2 2 2 2 0 1 1 0
0 2 0 0 0 2 0 0 0 0
0 2 0 1 0 2 0 0 0 0
0 2 0 1 0 2 0 0 0 0
0 2 0 0 0 2 0 0 0 0
0 2 2 2 2 2 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 1 1 0
0 2 2 2 2 2 0 1 1 0
0 2 0 0 0 2 0 0 0 0
0 2 0 0 0 2 0 0 0 0
0 2 0 0 0 2 0 0 0 0
0 2 0 0 0 2 0 0 0 0
0 2 2 2 2 2 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


## train_3

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 7 7 7 7 7 7 7 0 0
0 7 0 0 0 0 0 7 0 0
0 7 0 8 8 0 0 7 0 0
0 7 0 0 0 0 8 7 0 0
0 7 0 8 8 0 8 7 0 0
0 7 0 0 0 0 0 7 0 0
0 7 7 7 7 7 7 7 0 0
8 0 0 0 0 0 0 0 0 0
8 0 0 0 0 0 0 8 8 8
```


**output:**
```
0 0 0 0 0 0 0 0 0 0
0 7 7 7 7 7 7 7 0 0
0 7 0 0 0 0 0 7 0 0
0 7 0 0 0 0 0 7 0 0
0 7 0 0 0 0 0 7 0 0
0 7 0 0 0 0 0 7 0 0
0 7 0 0 0 0 0 7 0 0
0 7 7 7 7 7 7 7 0 0
8 0 0 0 0 0 0 0 0 0
8 0 0 0 0 0 0 8 8 8
```

*   **Perception:**
    *   Each input grid contains a large, hollow rectangle composed of a single color (the 'frame' color).
    *   Inside this hollow rectangle, there are one or more smaller objects composed of a different color (the 'content' color).
    *   There might also be objects outside the hollow rectangle, sometimes using the same 'content' color.
    *   The background color is white (0).
    *   The transformation involves removing (setting to white/0) only the objects that are located strictly *inside* the boundary of the hollow rectangle.
    *   The hollow rectangle itself and any objects located outside its boundary remain unchanged in the output grid.

*   **YAML Facts:**
    
```yaml
    task_description: Remove objects located strictly inside a hollow rectangular frame.
    
    elements:
      - type: grid
        description: Input and output are 2D grids of pixels with integer color values.
      - type: object
        name: frame
        description: A large, hollow rectangle made of a single, non-background color. Its position and color vary between examples.
      - type: object
        name: content_objects
        description: One or more contiguous groups of pixels of a single color, different from the frame color and the background color.
      - type: property
        name: location
        values: [inside_frame, outside_frame]
        description: Describes whether a content_object is geometrically contained within the boundaries of the frame, not including the frame pixels themselves.
      - type: background
        color: white
        value: 0

    actions:
      - name: identify_frame
        description: Find the largest hollow rectangular object in the input grid.
      - name: identify_content_objects
        description: Find all objects that are not the frame and not the background.
      - name: determine_location
        description: For each content_object, check if all its pixels are located within the inner area defined by the frame.
      - name: remove_inside_objects
        description: Change the pixels of content_objects identified as 'inside_frame' to the background color (white/0).
      - name: preserve_elements
        description: Keep the frame pixels and the pixels of content_objects identified as 'outside_frame' unchanged.

    relationships:
      - type: spatial
        description: Content objects are either inside or outside the frame.
      - type: transformation
        description: Only content objects inside the frame are affected (removed). The frame and outside objects are preserved.
    ```


*   **Natural Language Program:**
    1.  Identify the largest hollow rectangular object (the "frame") in the input grid. Note its boundaries and color.
    2.  Identify all other distinct objects in the grid (pixels that are not part of the frame and not background/white).
    3.  For each of these other objects, determine if it lies entirely within the inner area bounded by the frame.
    4.  Create the output grid by copying the input grid.
    5.  In the output grid, change the color of all pixels belonging to objects identified in step 3 (those strictly inside the frame) to the background color (white/0).
    6.  Leave all other pixels (the frame pixels and pixels of objects outside the frame) unchanged from their input values.
