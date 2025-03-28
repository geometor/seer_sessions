
## train_1

**input:**
```
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 3 8 8 3 8 8 8 8 8 8 8 8
8 8 8 8 3 3 3 3 8 8 8 8 8 8 8 8
8 8 8 8 3 3 3 3 8 8 8 8 8 8 8 8
8 8 8 8 3 8 8 3 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 6 6 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 1 1 1 8 8 8 8 8 8 8 8
8 8 8 8 8 1 1 8 8 8 8 8 8 8 8 8
8 8 8 8 8 1 1 8 8 8 8 8 8 8 8 8
8 6 6 8 8 1 1 8 8 8 8 8 8 8 8 8
8 8 8 8 8 1 1 1 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
```


**output:**
```
3 6 6 3
3 3 3 3
3 3 3 3
3 6 6 3
```


## train_2

**input:**
```
2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2
2 1 2 2 2 1 2 2 2 2 2 2 2 2 2 2
2 1 1 1 1 1 2 2 3 2 2 3 2 2 2 2
2 1 2 2 2 1 2 2 3 3 3 3 2 2 2 2
2 2 2 2 2 2 2 2 3 3 3 3 2 2 2 2
2 2 2 2 2 2 2 2 3 3 3 3 2 2 2 2
2 2 8 8 8 2 2 2 3 3 3 3 2 2 2 2
2 2 2 2 2 2 2 2 3 2 2 3 2 2 2 2
2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2
2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2
2 2 2 4 4 4 4 4 4 4 4 4 2 2 2 2
2 2 2 2 4 4 4 4 4 4 4 2 2 2 2 2
2 2 2 2 4 4 4 4 4 4 4 2 2 2 2 2
2 2 2 4 4 4 4 4 4 4 4 4 2 2 2 2
2 2 2 2 2 2 2 2 2 2 2 2 2 8 8 8
2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2
```


**output:**
```
1 8 8 8 1
1 1 1 1 1
1 8 8 8 1
```


## train_3

**input:**
```
4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4
4 4 4 4 4 4 4 4 4 4 4 4 4 4 6 4
4 4 4 4 4 4 4 4 4 4 4 4 4 4 6 4
4 4 4 4 1 1 1 1 1 1 4 4 4 4 6 4
4 4 4 4 4 4 1 1 1 4 4 4 4 4 4 4
4 4 4 4 4 4 1 1 1 4 4 4 4 4 4 4
4 4 4 4 4 4 1 1 1 4 4 4 4 4 4 4
4 4 4 4 1 1 1 1 1 1 4 4 4 4 4 4
4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4
4 4 4 4 4 4 4 4 4 2 4 4 2 4 4 4
4 4 3 3 4 4 4 4 4 2 4 4 2 4 4 4
4 4 3 3 4 4 4 4 4 2 4 4 2 4 4 4
4 4 3 3 4 4 4 4 4 2 2 2 2 4 4 4
4 4 4 4 4 4 4 4 4 2 2 2 2 4 4 4
4 4 4 4 4 4 4 4 4 2 4 4 2 4 4 4
4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4
```


**output:**
```
1 1 1 1 1 1
3 3 1 1 1 6
3 3 1 1 1 6
3 3 1 1 1 6
1 1 1 1 1 1
```

*   **Perception:** The task requires identifying specific objects within a larger input grid and extracting them into a smaller output grid. The input grids contain multiple shapes of various colors against a dominant background color. The output grid contains only a subset of these shapes, arranged within a minimal bounding box. The key challenge is determining the criteria for selecting which objects are kept. Two selection criteria seem apparent: 1) objects whose bounding box contains pixels of the input grid's background color, and 2) objects whose specific shape appears more than once in the input grid. The background color of the output grid seems determined by the color of the object selected based on the first criterion.

*   **Facts:**
    
```yaml
    task_type: object_selection_and_extraction
    background_color_determination: most_frequent_color_in_input
    objects:
      definition: contiguous_blocks_of_same_non_background_color
      properties:
        - color
        - pixel_coordinates
        - bounding_box
        - shape (relative coordinates within bounding box)
        - contains_background_color (boolean: true if any pixel within bounding_box, not part of the object, matches background_color)
        - shape_frequency (integer: count of objects with the identical shape in the input)
    selection_criteria:
      - rule_1: object_contains_background_color == true
      - rule_2: object_shape_frequency > 1
      - logic: keep_object_if (rule_1 OR rule_2)
    output_grid_generation:
      - step_1: identify_all_kept_objects
      - step_2: determine_minimal_bounding_box_containing_all_kept_objects
      - step_3: identify_fill_object (the single kept_object where rule_1 == true)
      - step_4: determine_fill_color (color of fill_object)
      - step_5: create_output_grid (dimensions of bounding_box, initialized with fill_color)
      - step_6: place_kept_objects (copy pixels of each kept_object into output_grid at relative positions, overwriting fill_color)
    relationships:
      - input_background_color informs object_contains_background_color property.
      - object_shape property is used to calculate object_shape_frequency.
      - selection_criteria determines which objects are kept.
      - kept_objects determine the output_bounding_box and the content of the output_grid.
      - fill_object determines the output_grid's initial background (fill_color).
    ```


*   **Natural Language Program:**
    1.  Determine the background color by finding the most frequent pixel color in the input grid.
    2.  Identify all distinct objects in the input grid, where an object is a connected group of pixels of the same color, excluding the background color.
    3.  For each object:
        a.  Determine its bounding box.
        b.  Determine its shape (the pattern of its pixels relative to its top-left corner).
        c.  Check if its bounding box contains any pixels of the background color that are not part of the object itself. Mark the object as `contains_background`.
    4.  Count how many times each unique object shape appears in the input grid. Store this frequency for each object.
    5.  Select objects to keep based on the following criteria: Keep an object if it `contains_background` OR if its shape frequency is greater than 1.
    6.  Find the single object that was kept *because* it `contains_background`. Let its color be the `fill_color`. (Assume there is exactly one such object).
    7.  Calculate the minimal bounding box that encloses all the kept objects.
    8.  Create a new output grid with the dimensions of this minimal bounding box.
    9.  Initialize all pixels of the output grid with the `fill_color`.
    10. For each kept object, copy its pixels into the output grid, placing them relative to the top-left corner of the minimal bounding box, overwriting the existing `fill_color` pixels.
