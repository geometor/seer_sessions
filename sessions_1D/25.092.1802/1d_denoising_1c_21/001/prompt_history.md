
## train_1

**input:**
```
0 0 0 3 3 3 3 3 3 3 3 3 3 3 3 0 0 0 3 0 0 0 0 3 0 0 0 0 3 0 0 0
```


**output:**
```
0 0 0 3 3 3 3 3 3 3 3 3 3 3 3 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 0 2 0 0 2 0 0 2 2 2 2 2 2 2 2 2 2 2 2 2 2 0 0 2 0 0 0 2 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 2 2 2 2 2 2 2 2 2 2 2 2 2 2 0 0 0 0 0 0 0 0 0
```


## train_3

**input:**
```
0 0 3 0 0 3 0 0 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 0 0 0 0 3 0 0 3 0
```


**output:**
```
0 0 0 0 0 0 0 0 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 0 0 0 0 0 0 0 0 0
```

**Perception:**

1.  **Grid Structure:** The task operates on grids of pixels, represented by integers 0-9. In the provided examples, the grids appear to be 6x6.
2.  **Colors:** The primary colors involved are white (0) as the background, and one other non-white color per example (green (3) or red (2)).
3.  **Objects:** The non-white pixels form distinct shapes or "objects" within the grid. These objects are connected components of the same color. Connectivity appears to be orthogonal (sharing an edge), not diagonal.
4.  **Transformation:** The core transformation identifies all distinct connected components (objects) of the non-white color. It then determines which of these components is the largest (contains the most pixels). The output grid retains *only* the pixels belonging to this largest component, placed in their original positions. All other pixels in the output grid, including the background and pixels from smaller non-white components, are set to the background color (white/0).
5.  **Goal:** The goal is to isolate the single largest connected object of a non-background color from the input grid.

**YAML Facts:**


```yaml
task_elements:
  - item: grid
    description: Both input and output are 2D grids of pixels with integer values representing colors.
    properties:
      - background_color: white (0)
      - dimensions: Consistent between input and output for each example (e.g., 6x6).
  - item: object
    description: A connected component of non-background pixels.
    properties:
      - color: A single non-white color per example (e.g., green, red).
      - connectivity: Orthogonal (pixels sharing an edge are connected).
      - size: The number of pixels composing the object.
  - item: relationship
    description: Comparison between objects based on size.
    properties:
      - criteria: Largest size (maximum number of pixels).
  - item: action
    description: Filtering the input grid based on object properties.
    steps:
      - Identify all connected components (objects) of non-white pixels.
      - Calculate the size of each component.
      - Select the component with the largest size.
      - Create a new grid initialized with the background color.
      - Place the pixels of the selected largest component onto the new grid at their original positions.
```


**Natural Language Program:**

1.  Initialize the output grid to be the same dimensions as the input grid, filled entirely with the background color (white/0).
2.  Identify all connected components of non-white pixels within the input grid. Treat pixels as connected if they share an edge (orthogonal connectivity).
3.  If no non-white components are found, return the initialized background grid.
4.  Calculate the size (number of pixels) for each identified component.
5.  Determine the maximum size among all components.
6.  Identify the component(s) that have this maximum size. (Based on the examples, assume there is only one such largest component).
7.  For each pixel belonging to the largest component identified in the previous step, copy its color and position from the input grid to the corresponding position in the output grid.
8.  Return the final output grid.
