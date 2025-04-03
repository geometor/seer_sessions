
## train_1

**input:**
```
3 3 3 3 3 3 3 3 3 3 3 3 3 0 0 0 3 0 0 3 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
3 3 3 3 3 3 3 3 3 3 3 3 3 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 0 0 7 0 0 0 7 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


## train_3

**input:**
```
0 0 4 0 0 0 0 4 0 4 4 4 4 4 4 4 4 4 4 4 4 0 0 0 4 0 0 0 4 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 4 4 4 4 4 4 4 4 4 4 4 4 0 0 0 0 0 0 0 0 0 0 0
```

Okay, let's analyze the provided examples.

## Perception

1.  **Grid Structure**: The inputs and outputs are grids of pixels represented by integers (colors). The grid sizes appear consistent within each example pair (6x5 in the provided examples).
2.  **Colors**: Each example uses two colors: white (0) as a background and one other color (green/3, orange/7, or yellow/4) as a foreground or object color.
3.  **Objects**: The foreground color forms distinct contiguous regions or "objects" within the grid. Connectivity seems to be based on adjacent sides (up, down, left, right), not diagonals.
4.  **Transformation**: The core transformation seems to involve identifying these foreground objects and selecting only one of them based on a specific property. In the output, only the pixels belonging to the selected object retain their original color; all other pixels become the background color (white/0).
5.  **Selection Criteria**: By comparing the input objects to the single object remaining in the output, the selection criterion appears to be size. The object with the largest area (number of pixels) is the one that is kept. All smaller objects of the same color are removed (turned into the background color).
6.  **Example Walkthrough (train_3)**:
    *   Input has yellow (4) objects against a white (0) background.
    *   Objects (using 4-way connectivity):
        *   A 2-pixel vertical bar at (1,3)-(2,3).
        *   A 1-pixel object at (2,5).
        *   A 10-pixel object spanning rows 3 and 4.
        *   A 1-pixel object at (5,4).
        *   A 1-pixel object at (6,3).
    *   The largest object is the 10-pixel one.
    *   The output retains only this 10-pixel object, with all other pixels set to white (0). This confirms the "keep largest object" hypothesis using 4-way connectivity. The other examples (train_1, train_2) also follow this pattern when using 4-way connectivity.

## YAML Facts


```yaml
task_context:
  grid_representation: 2D array of integers (0-9) representing colors.
  background_color: 0 (white) is consistently used as the background.
  foreground_color: A single non-zero color is present in each input grid (3, 7, or 4 in examples).
  connectivity: 4-way adjacency (up, down, left, right) defines contiguous objects.

elements:
  - element: grid
    properties:
      - width: variable
      - height: variable
      - pixels: color values (0-9)
  - element: object
    properties:
      - color: non-zero integer
      - pixels: list of coordinates (row, col)
      - size: count of pixels in the object
      - contiguous: defined by 4-way adjacency

transformation:
  action: identify_objects
  input: input grid
  parameters:
    - non_background_color: color != 0
    - connectivity: 4-way
  output: list of objects (pixels, color, size)

  action: select_largest_object
  input: list of objects
  parameters:
    - criteria: maximum size (pixel count)
  output: the single largest object

  action: construct_output_grid
  input:
    - original_input_grid_dimensions
    - largest_object
    - background_color (0)
  process: create a new grid of the same dimensions, fill with background_color, then paint the pixels of the largest_object with its color.
  output: output grid

relationships:
  - an object consists of contiguous pixels of the same non-background color.
  - the output grid contains only the pixels from the single largest input object.
  - all other pixels in the output grid adopt the background color.
```


## Natural Language Program

1.  Identify the background color (which is consistently color 0 / white).
2.  Identify all distinct contiguous objects composed of any single non-background color in the input grid. Use 4-way adjacency (pixels are connected if they share an edge, not just a corner) to determine contiguity.
3.  Calculate the size (number of pixels) of each identified object.
4.  Find the object with the largest size. Assume there is only one unique largest object.
5.  Create a new output grid with the same dimensions as the input grid, initially filled entirely with the background color (0).
6.  For the largest object identified in step 4, set the corresponding pixels in the output grid to the color of that object.
7.  Return the resulting output grid.
