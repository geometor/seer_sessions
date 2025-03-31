
## train_1

**input:**
```
9 0 0 0 0 7 7 0 9 0
0 0 9 0 0 0 9 9 9 0
7 7 0 3 3 3 3 7 9 7
0 3 7 3 3 3 3 9 3 7
0 3 9 3 3 0 0 0 3 9
9 3 3 3 3 0 0 9 3 0
3 3 3 3 3 9 0 0 3 7
3 3 3 3 3 0 9 9 3 0
0 9 0 3 3 3 9 9 9 9
7 9 7 9 0 0 7 7 0 0
```


**output:**
```
9 0 0 0 0 7 7 0 9 0
0 0 9 0 0 0 9 9 9 0
7 7 0 3 3 3 3 7 9 7
0 3 7 3 3 3 3 9 3 7
0 3 9 3 3 3 3 0 3 9
9 3 3 3 3 3 3 3 3 0
3 3 3 3 3 3 3 3 3 3
3 3 3 3 3 3 3 3 3 3
0 9 0 3 3 3 3 9 9 9
7 9 7 9 0 0 7 7 0 0
```


## train_2

**input:**
```
6 6 8 8 8 0 8 0 6 0
0 8 0 0 6 6 6 6 8 0
6 6 0 1 1 1 1 0 6 6
0 0 1 1 1 1 1 1 0 0
8 1 1 1 1 1 1 1 0 0
6 1 1 1 1 1 1 1 6 0
6 1 1 1 1 1 1 1 6 8
0 8 1 1 1 8 6 8 0 0
6 8 6 0 6 0 8 0 6 8
8 6 0 6 0 6 6 8 0 8
```


**output:**
```
6 6 8 8 8 0 8 0 6 0
0 8 0 0 6 6 6 6 8 0
6 6 0 1 1 1 1 0 6 6
0 0 1 1 1 1 1 1 0 0
8 1 1 1 1 1 1 1 1 0
6 1 1 1 1 1 1 1 1 0
6 1 1 1 1 1 1 1 1 8
0 8 1 1 1 1 1 1 0 0
6 8 6 0 6 0 8 0 6 8
8 6 0 6 0 6 6 8 0 8
```


## train_3

**input:**
```
1 1 0 1 1 0 0 0 4 1
4 4 0 4 2 2 1 4 4 4
4 0 2 2 2 2 2 2 1 0
0 4 2 2 2 0 0 1 1 0
0 0 1 2 2 2 1 0 1 0
0 4 0 2 2 0 2 0 0 0
2 2 2 2 2 2 2 2 2 2
4 1 4 1 2 2 4 4 1 4
0 4 4 4 2 1 1 4 4 1
4 0 4 4 0 4 1 1 4 0
```


**output:**
```
1 1 0 1 1 0 0 0 4 1
4 4 0 4 2 2 1 4 4 4
4 0 2 2 2 2 2 2 1 0
0 4 2 2 2 2 2 2 1 0
0 0 1 2 2 2 2 0 1 0
0 4 0 2 2 2 2 0 0 0
2 2 2 2 2 2 2 2 2 2
4 1 4 1 2 2 4 4 1 4
0 4 4 4 2 2 1 4 4 1
4 0 4 4 0 4 1 1 4 0
```

*   **Perception:** The task involves identifying the largest contiguous block of a single non-white color within the input grid. This block acts like a container or boundary. Any pixel, regardless of its original color (including white/background), that falls "inside" this boundary is changed to the color of the boundary block itself. Pixels outside this boundary, and pixels that are part of the boundary block, remain unchanged. The concept of "inside" is determined by whether a pixel, if treated as empty space (along with all other pixels not part of the largest block), can reach the edge of the grid without crossing the largest block.

*   **Facts:**
    
```yaml
    major_object:
      description: The largest contiguous area of any single non-white color.
      properties:
        - color: The color C of the pixels forming this object.
        - size: The count of pixels in the object.
        - location: The set of coordinates {(r, c), ...} occupied by the object.
      selection_criterion: Maximum size among all contiguous non-white objects.
    enclosed_cells:
      description: Cells considered "inside" the major_object.
      identification:
        - Create a mask grid where major_object cells have color C and all others are white (0).
        - Identify all white cells in the mask grid that are not reachable from the grid boundary by traversing only white cells.
      location: The set of coordinates {(r, c), ...} of these enclosed cells.
    transformation:
      action: Fill enclosed cells.
      input: Original grid.
      output: Modified grid.
      rule: For each cell (r, c) corresponding to an enclosed_cell location, set its color to C in the output grid. All other cells retain their original color from the input grid.
    background_color: white (0) - Does not form objects of interest but can be part of the enclosed region.
    other_objects: Smaller contiguous non-white areas or individual pixels not part of the major object. They are treated as background when determining enclosure, and their color might be overwritten if they fall within the enclosed region.
    ```


*   **Natural Language Program:**
    1.  Find all contiguous areas of non-white pixels in the input grid.
    2.  Determine the area with the largest number of pixels (the "largest object"). Record its color, `C`.
    3.  Create a temporary grid (mask) of the same size as the input. Mark the locations of the largest object's pixels with `True` and all other locations with `False`.
    4.  Identify all `False` locations on the boundary of the mask grid.
    5.  Starting from these boundary `False` locations, perform a flood fill or breadth-first search to find all reachable `False` locations by moving only through adjacent `False` locations (horizontally and vertically). Mark these as "externally reachable".
    6.  Initialize the output grid as a copy of the input grid.
    7.  Iterate through every cell `(r, c)` in the grid. If the corresponding location `(r, c)` in the mask is `False` AND it was *not* marked as "externally reachable" in step 5, change the color of the cell `(r, c)` in the output grid to `C`.
    8.  The final state of the output grid is the result.
