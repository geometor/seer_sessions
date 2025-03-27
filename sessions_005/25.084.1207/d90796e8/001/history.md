
## train_1

**input:**
```
5 0 0 0 0 0
0 0 3 2 0 0
0 0 0 0 0 0
0 3 0 0 0 2
0 2 0 0 0 0
5 0 0 3 0 0
0 0 0 0 0 0
```


**output:**
```
5 0 0 0 0 0
0 0 8 0 0 0
0 0 0 0 0 0
0 8 0 0 0 2
0 0 0 0 0 0
5 0 0 3 0 0
0 0 0 0 0 0
```


## train_2

**input:**
```
3 2 0
0 0 0
0 5 0
```


**output:**
```
8 0 0
0 0 0
0 5 0
```


## train_3

**input:**
```
0 0 0 0 0 2 0
3 0 0 0 0 0 3
5 0 2 3 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 2 0
3 2 0 0 0 3 0
0 0 0 5 0 0 0
```


**output:**
```
0 0 0 0 0 2 0
3 0 0 0 0 0 3
5 0 0 8 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
8 0 0 0 0 8 0
0 0 0 5 0 0 0
```

Okay, let's break down this task.

## Perception

1.  **Grid Size**: The input and output grids have the same dimensions in all examples.
2.  **Color Palette**: The primary colors involved in the transformation are green (3), red (2), azure (8), and white (0). Gray (5) also appears but seems unaffected by the core transformation rule.
3.  **Core Change**: The central observation is that certain green pixels change to azure, and certain red pixels change to white.
4.  **Trigger Condition**: This change appears to be triggered by adjacency. Specifically, a green pixel changes if it's next to (sharing an edge, not just diagonally) a red pixel, and a red pixel changes if it's next to a green pixel.
5.  **Specific Changes**:
    *   Green (3) becomes Azure (8) if adjacent to Red (2).
    *   Red (2) becomes White (0) if adjacent to Green (3).
6.  **No Change**: Pixels that are not green or red, or are green/red but do not meet the adjacency condition with the other color, remain unchanged. This includes gray pixels, white pixels, green pixels not next to red, and red pixels not next to green.
7.  **Simultaneity**: The check for adjacency seems to happen based on the *input* state. A green pixel changing to azure doesn't prevent an adjacent red pixel from changing to white based on the original presence of that green pixel.

## Facts


```yaml
task_type: pixel_transformation
grid_properties:
  - size_preservation: input and output grids have identical dimensions.
objects:
  - color: 3 # green
    role: conditional_source
    condition: changes if adjacent (von Neumann neighborhood) to a red (2) pixel.
    becomes: 8 # azure
  - color: 2 # red
    role: conditional_source
    condition: changes if adjacent (von Neumann neighborhood) to a green (3) pixel.
    becomes: 0 # white
  - color: 8 # azure
    role: conditional_target
    origin: green (3) pixels meeting the condition.
  - color: 0 # white
    role: background / conditional_target
    origin_as_target: red (2) pixels meeting the condition.
    behavior_as_background: remains unchanged if originally white.
  - color: 5 # gray
    role: static
    behavior: remains unchanged.
relationships:
  - type: adjacency
    definition: sharing an edge (up, down, left, or right neighbor), also known as von Neumann neighborhood.
    critical_pair: [green (3), red (2)]
    effect: triggers color transformation based on the rules above.
actions:
  - name: transform_pixel_color
    inputs: pixel color, neighboring pixel colors (based on input grid state)
    outputs: potentially new pixel color
    rules:
      - if pixel is green (3) AND has an adjacent red (2) neighbor: output azure (8)
      - if pixel is red (2) AND has an adjacent green (3) neighbor: output white (0)
      - otherwise: output original pixel color
```


## Natural Language Program

1.  Create a new grid with the same dimensions as the input grid.
2.  Iterate through each pixel (cell) of the input grid using its row and column index.
3.  For the current pixel at `(row, col)`:
    a.  Check its color in the input grid.
    b.  **If the color is green (3):**
        i.  Examine its adjacent neighbors (up, down, left, right) in the *input* grid.
        ii. If any adjacent neighbor has the color red (2), set the color of the corresponding pixel at `(row, col)` in the *new* grid to azure (8).
        iii. Otherwise (no adjacent red neighbor), copy the original green (3) color to the corresponding pixel in the *new* grid.
    c.  **Else if the color is red (2):**
        i.  Examine its adjacent neighbors (up, down, left, right) in the *input* grid.
        ii. If any adjacent neighbor has the color green (3), set the color of the corresponding pixel at `(row, col)` in the *new* grid to white (0).
        iii. Otherwise (no adjacent green neighbor), copy the original red (2) color to the corresponding pixel in the *new* grid.
    d.  **Else (if the color is not green or red):**
        i.  Copy the original color of the pixel at `(row, col)` from the input grid to the corresponding pixel in the *new* grid.
4.  After iterating through all pixels, the new grid represents the final output.
