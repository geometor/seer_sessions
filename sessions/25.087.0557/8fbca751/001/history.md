
## train_1

**input:**
```
0 0 0 0 0 8 0 0 0 0 0 0
0 0 0 0 8 8 0 0 0 0 0 0
0 0 0 0 8 8 8 8 0 0 0 0
0 0 0 0 8 8 8 8 0 0 0 0
0 0 0 0 0 0 0 0 8 8 8 0
0 0 0 0 0 0 0 0 8 8 8 0
0 0 0 0 0 0 0 0 8 8 0 8
0 0 0 0 0 0 0 0 8 8 0 0
```


**output:**
```
0 0 0 0 2 8 2 2 0 0 0 0
0 0 0 0 8 8 2 2 0 0 0 0
0 0 0 0 8 8 8 8 0 0 0 0
0 0 0 0 8 8 8 8 0 0 0 0
0 0 0 0 0 0 0 0 8 8 8 2
0 0 0 0 0 0 0 0 8 8 8 2
0 0 0 0 0 0 0 0 8 8 2 8
0 0 0 0 0 0 0 0 8 8 2 2
```


## train_2

**input:**
```
0 8 0 0 8 0 0 0 0 0 0 0
0 8 8 0 8 0 0 8 0 0 0 0
0 8 8 8 8 8 8 0 0 0 0 0
8 8 0 0 8 8 8 0 0 0 0 0
0 0 0 0 0 0 0 0 0 8 0 0
0 0 0 0 0 0 0 0 0 8 0 0
0 0 0 0 0 0 0 0 8 8 8 8
0 0 0 0 0 0 0 0 0 8 0 0
```


**output:**
```
2 8 2 2 8 2 2 2 0 0 0 0
2 8 8 2 8 2 2 8 0 0 0 0
2 8 8 8 8 8 8 2 0 0 0 0
8 8 2 2 8 8 8 2 0 0 0 0
0 0 0 0 0 0 0 0 2 8 2 2
0 0 0 0 0 0 0 0 2 8 2 2
0 0 0 0 0 0 0 0 8 8 8 8
0 0 0 0 0 0 0 0 2 8 2 2
```


## train_3

**input:**
```
0 0 0 0 0 0 0
0 8 0 0 8 0 0
0 8 8 8 8 0 0
0 0 0 8 0 0 0
0 0 8 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0
0 8 2 2 8 0 0
0 8 8 8 8 0 0
0 2 2 8 2 0 0
0 2 8 2 2 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
```

Okay, here's my analysis of the task based on the provided examples.

**Perception of Task Elements**

1.  **Input Grid:** Primarily composed of a white (0) background and one or more objects made of azure (8) pixels. The azure objects can be disconnected or connected, forming various shapes.
2.  **Output Grid:** Contains the original azure (8) objects and white (0) background pixels from the input. Additionally, some pixels that were originally white (0) in the input have been changed to red (2) in the output.
3.  **Transformation:** The core transformation involves adding red (2) pixels to the grid. The placement of these red pixels appears to be directly related to the position of the azure (8) pixels.
4.  **Key Observation:** Red pixels appear exclusively in locations that were originally white (0) in the input grid. Furthermore, these red pixels are always orthogonally adjacent (sharing a side, not just a corner) to at least one azure (8) pixel. Pixels that were already azure (8) remain unchanged. White pixels not orthogonally adjacent to any azure pixels also remain unchanged.

**YAML Facts**


```yaml
task_description: "Color adjacent white pixels based on proximity to azure pixels."
elements:
  - type: background
    color: white (0)
  - type: object
    color: azure (8)
    description: "Forms shapes or clusters in the input grid."
  - type: added_pixels
    color: red (2)
    description: "Appears in the output grid in locations that were white in the input."
transformation:
  action: "Coloring"
  source_pixels: "White (0) pixels in the input."
  target_pixels: "Red (2) pixels in the output."
  condition:
    - "The input pixel must be white (0)."
    - "The input pixel must be orthogonally adjacent (up, down, left, or right) to at least one azure (8) pixel."
relationships:
  - "Azure (8) pixels remain unchanged between input and output."
  - "White (0) pixels not meeting the adjacency condition remain unchanged."
  - "Red (2) pixels only appear where the adjacency condition is met for a white pixel."
grid_properties:
  - "Grid size can vary."
  - "The relative positions of azure (8) pixels are preserved."
```


**Natural Language Program**

1.  Initialize the output grid as an identical copy of the input grid.
2.  Iterate through each pixel (cell) of the input grid, identifying its row and column index.
3.  For the current pixel at `(row, col)`:
    a.  Check if the color of the pixel in the *input* grid is white (0).
    b.  If it is white (0), then examine its orthogonal neighbors (the pixels directly above, below, left, and right, if they exist within the grid boundaries).
    c.  Check if any of these orthogonal neighbors in the *input* grid have the color azure (8).
    d.  If at least one orthogonal neighbor is azure (8), change the color of the pixel at `(row, col)` in the *output* grid to red (2).
    e.  If the input pixel is not white (0), or if it is white (0) but none of its orthogonal neighbors are azure (8), the corresponding pixel in the output grid keeps its original color (which was set during the initial copy).
4.  After checking all pixels, the final output grid contains the result of the transformation.
