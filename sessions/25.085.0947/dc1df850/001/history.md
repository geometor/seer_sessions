
## train_1

**input:**
```
0 0 0 0 0 0 0 2
0 0 0 0 0 0 0 0
0 0 0 3 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 8 0
0 0 0 0 0 0 0 0
0 0 2 0 0 0 0 0
0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 1 2
0 0 0 0 0 0 1 1
0 0 0 3 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 8 0
0 1 1 1 0 0 0 0
0 1 2 1 0 0 0 0
0 1 1 1 0 0 0 0
```


## train_2

**input:**
```
2 0 0 0 0
0 0 0 2 0
0 0 0 0 0
0 6 0 0 0
0 0 0 0 0
```


**output:**
```
2 1 1 1 1
1 1 1 2 1
0 0 1 1 1
0 6 0 0 0
0 0 0 0 0
```


## train_3

**input:**
```
0 0 0 0 0
0 2 0 0 0
0 0 0 0 0
0 0 0 0 0
```


**output:**
```
1 1 1 0 0
1 2 1 0 0
1 1 1 0 0
0 0 0 0 0
```

*   **Perception of Task Elements:**
    *   The input grids contain a background of white pixels (0) and a few scattered pixels of other colors (red, green, azure, magenta).
    *   The output grids are the same size as the input grids.
    *   The key transformation involves changing some white pixels (0) to blue pixels (1).
    *   The original non-white pixels from the input grid remain unchanged in the output grid.
    *   Observing the examples, the blue pixels (1) always appear in the immediate vicinity (8 neighbours) of the red pixels (2) present in the input grid.
    *   Specifically, for each red pixel in the input, any adjacent white pixel (including diagonals) is turned into a blue pixel in the output.
    *   If a pixel location is adjacent to multiple red pixels, it still becomes blue.
    *   Pixels of colors other than red (like green, azure, magenta) do not cause any changes to their neighbouring white pixels.

*   **Facts:**
    
```yaml
    task_elements:
      - element: grid
        properties:
          - type: 2D array of integers (0-9)
          - background_color: white (0)
      - element: pixel
        properties:
          - color: integer (0-9)
          - position: (row, column) coordinate
      - element: red_pixel
        properties:
          - color: 2
        relationship:
          - type: source_of_change
            target: adjacent white pixels
      - element: white_pixel
        properties:
          - color: 0
        relationship:
          - type: potential_target_of_change
            condition: adjacency to a red pixel
      - element: blue_pixel
        properties:
          - color: 1
        relationship:
          - type: result_of_change
            source: white pixel adjacent to a red pixel
      - element: other_colored_pixel
        properties:
          - color: not 0, 1, or 2
        relationship:
          - type: static
            description: Does not change and does not cause changes.

    transformation:
      action: identify_pixels
        target_color: red (2)
      action: for_each_identified_pixel
        sub_action: find_adjacent_pixels
          target_position: position of the red pixel
          neighbourhood: 8 adjacent cells (including diagonals)
        sub_action: filter_adjacent_pixels
          condition: pixel color is white (0)
        sub_action: change_color
          target_pixels: filtered adjacent white pixels
          new_color: blue (1)
      action: copy_unchanged_pixels
        description: All pixels not identified as white and adjacent to red retain their original color.
    ```


*   **Natural Language Program:**
    1.  Create a copy of the input grid to serve as the output grid.
    2.  Iterate through each pixel in the input grid.
    3.  If a pixel's color is red (2):
        a.  Identify its 8 neighbouring pixels (horizontally, vertically, and diagonally adjacent).
        b.  For each neighbour that exists within the grid boundaries:
            i.  Check the color of this neighbouring pixel *in the original input grid*.
            ii. If the neighbour's color is white (0), change the color of the corresponding pixel in the *output grid* to blue (1).
    4.  Return the modified output grid.
