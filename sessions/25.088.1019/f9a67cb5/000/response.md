Okay, let's analyze the task examples.

## Perception of Task Elements

1.  **Grid Structure:** The inputs and outputs are 2D grids containing pixels of different colors: white (0), red (2), and azure (8).
2.  **Key Colors:**
    *   **White (0):** Represents empty or background space.
    *   **Red (2):** Seems to be the active or "spreading" color. There is always exactly one red pixel in the input.
    *   **Azure (8):** Acts as fixed barriers or walls. These pixels remain unchanged between input and output.
3.  **Transformation:** The core transformation involves the red color spreading from its initial position. This spread fills adjacent white areas.
4.  **Boundaries:** The spread of the red color is stopped by the azure pixels and the edges of the grid. It does not cross or replace azure pixels.
5.  **Connectivity:** The red color spreads to orthogonally adjacent (up, down, left, right) white pixels. It appears to be a "flood fill" or "paint bucket" type operation.
6.  **Initial State:** The input always contains static azure barriers, a background of white, and a single red starting pixel.
7.  **Final State:** The output retains the azure barriers and the original red pixel. White pixels reachable from the initial red pixel via a path of white pixels (without crossing azure pixels or grid boundaries) are changed to red. White pixels not reachable remain white.

## YAML Facts


```yaml
task_type: fill
grid_properties:
  dimensionality: 2D
  boundary: grid_edges_act_as_boundaries
objects:
  - object_type: color_pixel
    color_name: white
    color_value: 0
    role: background_or_fillable_area
  - object_type: color_pixel
    color_name: red
    color_value: 2
    role: starting_point_or_fill_color
    count_in_input: 1
  - object_type: color_pixel
    color_name: azure
    color_value: 8
    role: barrier_or_static_element
    properties: immutable
relationships:
  - relationship_type: adjacency
    connectivity: orthogonal (4-way)
    relevant_for: fill_spread
actions:
  - action_type: flood_fill
    start_condition: single red pixel location
    fill_area_condition: white pixels orthogonally connected to the start or already filled pixels
    boundary_condition: azure pixels or grid edges stop the fill
    result: filled white pixels change color to red
invariants:
  - azure pixel locations and color
  - location of the original red pixel (its color remains red)
  - white pixels not reachable by the flood fill remain white
```


## Natural Language Program

1.  Initialize the output grid as a copy of the input grid.
2.  Find the coordinates (row, column) of the single red (2) pixel in the input grid. This is the starting point.
3.  Create a list or queue for processing, initially containing only the starting point coordinates.
4.  Create a set to keep track of visited coordinates to avoid redundant processing, initially containing the starting point.
5.  While the processing list/queue is not empty:
    a.  Remove a coordinate (r, c) from the list/queue.
    b.  Examine the four orthogonal neighbors (up, down, left, right) of the current coordinate (r, c).
    c.  For each neighbor (nr, nc):
        i.   Check if the neighbor is within the grid boundaries.
        ii.  Check if the neighbor has not already been visited.
        iii. Check if the color of the neighbor pixel in the *input* grid is white (0).
        iv.  If all conditions (i, ii, iii) are true:
            1.  Change the color of the pixel at (nr, nc) in the *output* grid to red (2).
            2.  Add the neighbor coordinate (nr, nc) to the visited set.
            3.  Add the neighbor coordinate (nr, nc) to the processing list/queue.
6.  Return the modified output grid.