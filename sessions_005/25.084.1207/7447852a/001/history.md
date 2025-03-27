
## train_1

**input:**
```
2 0 0 0 2 0 0 0 2 0 0 0 2 0 0
0 2 0 2 0 2 0 2 0 2 0 2 0 2 0
0 0 2 0 0 0 2 0 0 0 2 0 0 0 2
```


**output:**
```
2 0 0 0 2 4 4 4 2 0 0 0 2 0 0
4 2 0 2 0 2 4 2 0 2 0 2 4 2 0
4 4 2 0 0 0 2 0 0 0 2 4 4 4 2
```


## train_2

**input:**
```
2 0 0 0 2 0 0 0 2 0
0 2 0 2 0 2 0 2 0 2
0 0 2 0 0 0 2 0 0 0
```


**output:**
```
2 0 0 0 2 4 4 4 2 0
4 2 0 2 0 2 4 2 0 2
4 4 2 0 0 0 2 0 0 0
```


## train_3

**input:**
```
2 0 0 0 2 0 0 0 2 0 0 0 2 0 0 0 2 0
0 2 0 2 0 2 0 2 0 2 0 2 0 2 0 2 0 2
0 0 2 0 0 0 2 0 0 0 2 0 0 0 2 0 0 0
```


**output:**
```
2 0 0 0 2 4 4 4 2 0 0 0 2 0 0 0 2 4
4 2 0 2 0 2 4 2 0 2 0 2 4 2 0 2 0 2
4 4 2 0 0 0 2 0 0 0 2 4 4 4 2 0 0 0
```

*   **Perception:** The task involves transforming a grid containing white (0) and red (2) pixels. The output grid retains the red pixels in their original positions but changes some of the white pixels to yellow (4). The input grids feature repeating patterns of red pixels forming diagonal structures. The transformation appears to involve identifying certain white pixels based on their proximity to the grid boundaries and their relationship to the red pixels, and then changing them and connected white pixels to yellow.

*   **YAML Facts:**
    
```yaml
    task_description: "Color white areas yellow based on proximity to grid boundaries, constrained by red pixels."
    grid_properties:
      - dimensions: Variable height (always 3 in examples) and width.
      - colors_present_input: [white (0), red (2)]
      - colors_present_output: [white (0), red (2), yellow (4)]
    objects:
      - type: fixed_pixels
        color: red (2)
        properties: Act as barriers or boundaries for the transformation. Their positions remain unchanged.
      - type: background_pixels
        color: white (0)
        properties: Can potentially change color.
      - type: transformed_pixels
        color: yellow (4)
        properties: Result from transforming specific white pixels.
    transformation:
      type: flood_fill
      start_condition: White (0) pixels adjacent (including diagonally) to any grid boundary.
      propagation: Spreads to adjacent (including diagonally) white (0) pixels.
      stop_condition: Does not spread into or across red (2) pixels.
      color_change: White (0) pixels reached by the flood fill are changed to yellow (4).
    relationships:
      - adjacency: 8-connectivity (including diagonals) is used for flood fill propagation and identifying initial starting pixels near boundaries.
      - boundary_proximity: White pixels adjacent to the grid edges initiate the transformation.
    ```


*   **Natural Language Program:**
    1.  Create a copy of the input grid to serve as the output grid.
    2.  Identify all white pixels (color 0) in the input grid that are adjacent (including diagonally) to any cell on the grid's boundary (top, bottom, left, or right edge).
    3.  Initialize a collection (e.g., a queue or list) of "pixels to process" with the coordinates of these boundary-adjacent white pixels. Maintain a set of "visited" coordinates, initially containing the same pixels.
    4.  While the "pixels to process" collection is not empty:
        a.  Remove a pixel coordinate (row, column) from the collection.
        b.  Set the color of this pixel at (row, column) in the output grid to yellow (color 4).
        c.  Examine all 8 neighbors (adjacent and diagonal) of the current pixel.
        d.  For each neighbor:
            i.   If the neighbor is within the grid boundaries, AND
            ii.  If the neighbor's color in the *input* grid is white (color 0), AND
            iii. If the neighbor's coordinate has not been "visited" yet:
                 - Add the neighbor's coordinate to the "pixels to process" collection.
                 - Add the neighbor's coordinate to the "visited" set.
    5.  Return the modified output grid.
