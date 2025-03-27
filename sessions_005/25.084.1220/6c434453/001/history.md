
## train_1

**input:**
```
0 0 0 0 1 1 1 0 0 0
1 1 0 0 1 0 1 0 0 0
1 1 0 0 1 1 1 0 0 0
0 0 0 0 0 0 0 0 1 0
0 0 0 0 0 0 0 1 1 1
0 1 1 1 0 0 0 0 1 0
0 1 0 1 0 0 0 0 0 0
0 1 1 1 0 0 1 0 0 0
0 0 0 0 0 0 1 1 1 0
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 2 0 0 0 0
1 1 0 0 2 2 2 0 0 0
1 1 0 0 0 2 0 0 0 0
0 0 0 0 0 0 0 0 1 0
0 0 0 0 0 0 0 1 1 1
0 0 2 0 0 0 0 0 1 0
0 2 2 2 0 0 0 0 0 0
0 0 2 0 0 0 1 0 0 0
0 0 0 0 0 0 1 1 1 0
0 0 0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
1 1 1 0 0 0 0 0 0 0
1 0 1 0 0 0 0 1 0 0
1 1 1 0 0 0 1 1 1 0
0 0 0 0 0 0 0 1 0 0
0 1 0 0 0 0 0 0 0 0
1 1 1 0 0 0 0 0 0 0
0 1 0 1 1 1 0 0 0 0
0 0 0 1 0 1 0 0 1 1
0 0 0 1 1 1 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 2 0 0 0 0 0 0 0 0
2 2 2 0 0 0 0 1 0 0
0 2 0 0 0 0 1 1 1 0
0 0 0 0 0 0 0 1 0 0
0 1 0 0 0 0 0 0 0 0
1 1 1 0 0 0 0 0 0 0
0 1 0 0 2 0 0 0 0 0
0 0 0 2 2 2 0 0 1 1
0 0 0 0 2 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

*   **Perception:**
    *   The input grids contain white (0) and blue (1) pixels.
    *   The blue pixels form distinct contiguous shapes or objects against the white background.
    *   The output grids introduce red (2) pixels, while some blue (1) and all white (0) pixels from the input remain.
    *   Comparing input and output, the red pixels appear in locations that were white (0) in the input.
    *   These locations seem to be "holes" or enclosed spaces within the blue shapes.
    *   Specifically, red pixels appear only within blue shapes that contain exactly one enclosed white area (a "hole").
    *   Blue shapes without any holes, or potentially shapes with multiple holes (though none are observed in the examples), remain unchanged.
    *   The original blue pixels that form the boundary of the filled hole remain blue in the output.

*   **Facts:**
    
```yaml
    task_elements:
      - item: grid
        description: Both input and output are 2D grids of pixels.
        properties:
          colors: [white (0), blue (1)] in input; [white (0), blue (1), red (2)] in output.
          size: Consistent between input and output for each example (e.g., 10x10).
      - item: object
        name: blue_shape
        description: A contiguous area of blue (1) pixels in the input grid.
        properties:
          - connectivity: Pixels are considered contiguous if they share an edge (not just a corner).
          - can_contain_holes: May fully enclose areas of white (0) pixels.
      - item: object
        name: hole
        description: A contiguous area of white (0) pixels completely surrounded by blue (1) pixels belonging to a single blue_shape.
        properties:
          - color: white (0) in input.
          - location: Within the boundary of a blue_shape.
          - single_enclosing_shape: Must be enclosed by only one distinct blue_shape.
      - item: action
        name: identify_shapes_and_holes
        description: Find all distinct blue_shapes and identify any holes within each shape. Count the number of holes for each shape.
      - item: action
        name: fill_single_hole
        description: If a blue_shape contains exactly one hole, change the color of the pixels corresponding to that hole from white (0) to red (2) in the output grid.
      - item: relationship
        description: The red (2) pixels in the output grid correspond precisely to the pixels of the single hole found within certain blue_shapes in the input grid. Blue_shapes with no holes or more than one hole remain unchanged, as does the background.
    ```


*   **Natural Language Program:**
    1.  Identify all distinct contiguous shapes formed by blue (1) pixels in the input grid.
    2.  For each identified blue shape:
        a.  Find all contiguous areas of white (0) pixels that are completely enclosed by the blue pixels of that shape (these are the "holes").
        b.  Count the number of distinct holes found within the shape.
    3.  Initialize the output grid as a copy of the input grid.
    4.  Iterate through each blue shape identified in step 1.
    5.  If a blue shape has exactly one hole (as determined in step 2b):
        a.  Identify the coordinates of all white (0) pixels that constitute this single hole.
        b.  In the output grid, change the color of these specific pixels from white (0) to red (2).
    6.  Leave all other pixels in the output grid unchanged from their input values (blue shapes with zero or multiple holes remain blue, and the background remains white).
    7.  The resulting grid is the final output.
