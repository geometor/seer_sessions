
## train_1

**input:**
```
0 9 9 9 0 0 0 0 9 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 9 9 9 0 0 0 9 9 9 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 2 2 2 0 0 0 0 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 2 2 2 0 0 0 2 2 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


## train_3

**input:**
```
0 2 2 2 0 0 2 0 0 0 0 0 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 2 2 2 0 2 2 2 0 0 0 2 2 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

*   **Perception:**
    *   The input and output grids appear to be 1-dimensional arrays or single rows.
    *   Each grid contains objects composed of non-white pixels (maroon '9' or red '2') separated by white '0' pixels.
    *   In each example, there is one object that is larger (3 pixels wide) than the others (1 pixel wide). The color of the larger object is the same as the smaller objects within that example.
    *   The transformation seems to identify the largest object as a "pattern".
    *   It then finds all single-pixel objects of the *same color* as the pattern object.
    *   Each of these single-pixel objects is replaced by a copy of the pattern object.
    *   The replacement is centered: the copied pattern is placed such that its center pixel occupies the position of the original single pixel.
    *   The original pattern object and the background pixels remain unchanged.

*   **Facts:**
    
```yaml
    task_type: object_transformation
    grid_dimensionality: 1D # Based on examples, appears effectively 1D
    background_color: white (0)
    objects:
      - type: contiguous_block
        color: non-white (varies per example, e.g., maroon, red)
        properties:
          - size (pixel count)
          - position (indices)
    relationships:
      - pattern_object: The object with the largest size (pixel count). Assumed unique in these examples.
      - target_objects: Objects consisting of a single pixel with the same color as the pattern_object.
    actions:
      - identify: Find all non-white objects.
      - identify: Determine the pattern_object (largest).
      - identify: Find all target_objects (single pixel, same color as pattern).
      - replace: For each target_object, replace it with a copy of the pattern_object.
      - positioning: Center the copied pattern_object at the index of the original target_object.
      - preserve: Keep the original pattern_object and background pixels unchanged.
    constraints:
      - Replacement only occurs for single-pixel objects matching the pattern color.
      - The pattern object itself is not modified or replaced.
    ```


*   **Natural Language Program:**
    1.  Parse the input grid to identify all contiguous objects of non-white pixels, noting their color, size (number of pixels), and position (indices).
    2.  Find the object with the largest size. Designate this as the `pattern_object`. Record its shape/pixel sequence and color.
    3.  Identify all objects that consist of exactly one pixel and have the same color as the `pattern_object`. Designate these as `target_objects`. Record their positions (indices).
    4.  Create a copy of the input grid to serve as the output grid.
    5.  For each `target_object` identified in step 3:
        a.  Determine the index `i` of the `target_object`.
        b.  Determine the length `L` of the `pattern_object`.
        c.  Calculate the start index for the replacement: `start_index = i - floor(L / 2)`.
        d.  Calculate the end index for the replacement: `end_index = i + floor(L / 2)`.
        e.  Place the `pattern_object` into the output grid spanning the indices from `start_index` to `end_index`. Ensure boundary conditions are handled if necessary (though not apparent in these examples).
    6.  Return the modified output grid.
