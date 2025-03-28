
## train_1

**input:**
```
0 0 0 0 8 8
3 0 0 4 0 0
3 0 0 4 0 0
0 0 0 0 0 6
1 1 0 0 0 6
0 0 0 0 0 0
0 0 5 5 0 0
0 0 0 0 0 0
0 0 0 0 0 0
2 2 2 2 2 2
```


**output:**
```
0 0 0 0 0 0
0 0 0 0 0 0
0 0 0 0 0 0
0 0 0 0 0 0
0 0 0 0 0 0
0 0 0 0 0 0
3 0 0 4 8 8
3 0 0 4 0 6
1 1 5 5 0 6
2 2 2 2 2 2
```


## train_2

**input:**
```
2 0 0 3 3 0 0 4 4 0 0
2 0 0 0 0 5 0 0 0 0 0
2 0 0 0 0 5 0 0 6 6 0
2 0 0 0 0 0 0 8 0 0 0
2 0 7 7 0 0 0 8 0 0 0
```


**output:**
```
2 3 3 4 4 0 0 0 0 0 0
2 5 0 0 0 0 0 0 0 0 0
2 5 6 6 0 0 0 0 0 0 0
2 0 0 8 0 0 0 0 0 0 0
2 7 7 8 0 0 0 0 0 0 0
```


## train_3

**input:**
```
0 4 4 0 0 0 0 0 0 2
0 0 0 5 5 0 0 6 0 2
0 0 0 0 0 0 0 6 0 2
0 9 0 0 8 8 0 0 0 2
0 9 0 0 0 0 0 0 0 2
```


**output:**
```
0 0 0 0 0 0 0 4 4 2
0 0 0 0 0 0 5 5 6 2
0 0 0 0 0 0 0 0 6 2
0 0 0 0 0 0 9 8 8 2
0 0 0 0 0 0 9 0 0 2
```

Okay, let's break down this task.

**Perception of the Elements:**

1.  **Grid Structure:** The input and output are 2D grids of colored pixels. The background color is consistently white (0).
2.  **Objects:** Within the grid, there are distinct contiguous blocks of non-white pixels, forming colored objects.
3.  **Special Object:** In each example, there is a red (2) object. This object appears to be static; it does not change position from input to output.
4.  **Other Objects:** All other non-white, non-red objects change their position from input to output.
5.  **Transformation:** The transformation looks like a form of "gravity" or directed movement. The non-red objects move towards the static red object until they are blocked either by the red object itself, another non-red object that has already settled, or the grid boundary (though blockage by other objects or the red barrier seems primary).
6.  **Direction of Movement:**
    *   In `train_1`, the red object is a horizontal line at the bottom. Other objects move downwards.
    *   In `train_2`, the red object is a vertical line on the left. Other objects move leftwards.
    *   In `train_3`, the red object is a vertical line on the right. Other objects move rightwards.
    *   The direction of movement is always towards the static red object.
7.  **Interaction:** Objects maintain their shape and color. They stop moving when they become adjacent (orthogonally or diagonally, based on the examples, orthogonal seems sufficient for blocking) to the red object or another object that has already stopped. They effectively stack or pile up against the red barrier and each other.

**YAML Fact Documentation:**


```yaml
task_description: Simulate gravity towards a static red barrier.
elements:
  - type: grid
    properties:
      background_color: white (0)
      contains: colored objects
  - type: object
    identifier: static_barrier
    properties:
      color: red (2)
      shape: variable (line in examples)
      behavior: remains stationary
      role: acts as a stopping point for moving objects
  - type: object
    identifier: moving_objects
    properties:
      color: any non-white (0), non-red (2) color
      shape: variable, contiguous blocks of same color
      behavior: move towards the static_barrier
      role: subject to the gravity-like transformation
relationships:
  - type: spatial
    description: Moving objects stop when adjacent (orthogonally) to the static_barrier or another previously stopped moving_object in the direction of movement.
actions:
  - name: identify_barrier
    inputs: input_grid
    output: location and extent of the red (2) object(s)
  - name: determine_direction
    inputs: static_barrier position, grid dimensions
    output: direction of movement (down, left, or right)
  - name: identify_movers
    inputs: input_grid
    output: list of all non-white, non-red objects (pixels and their locations)
  - name: simulate_movement
    inputs: input_grid, static_barrier, moving_objects, direction
    output: output_grid
    details: |
      Iteratively move each moving_object one step in the determined direction.
      In each step, check for collisions:
      1. Grid boundaries
      2. Static barrier
      3. Other moving objects (in their current positions for the iteration)
      An object stops if it cannot move one step without a collision.
      Repeat iterations until no object moves in a full iteration.
```


**Natural Language Program:**

1.  Initialize the output grid as a copy of the input grid.
2.  Identify the location of all red (2) pixels; these form the static barrier.
3.  Determine the primary location/edge of the red barrier to infer the direction of movement:
    *   If the red barrier occupies the bottom-most rows containing non-white pixels, the direction is 'down'.
    *   If the red barrier occupies the left-most columns containing non-white pixels, the direction is 'left'.
    *   If the red barrier occupies the right-most columns containing non-white pixels, the direction is 'right'.
    *   (Assume only one primary direction per task instance based on examples).
4.  Identify all non-white (0) and non-red (2) pixels. These are the pixels belonging to moving objects.
5.  Enter a simulation loop that continues as long as any object moved in the previous iteration.
6.  Inside the loop, set a flag `movement_occurred` to `false`.
7.  Iterate through all *moving objects* (it might be more effective to iterate pixel by pixel, or determine object connectivity first). A good order might be processing pixels/objects furthest from the barrier first (e.g., bottom-to-top for 'down', right-to-left for 'left', left-to-right for 'right').
8.  For each moving pixel (or object):
    *   Calculate its potential next position by moving one step in the determined direction.
    *   Check if the potential next position is valid:
        *   Is it within the grid boundaries?
        *   Does it overlap with a red (barrier) pixel in the *original* grid?
        *   Does it overlap with any *other* non-white pixel in the *current state* of the output grid?
    *   If the move is valid (no collisions, within bounds), tentatively mark this pixel/object to move.
9.  After checking all potentially moving pixels/objects, update the output grid by moving all pixels/objects marked for movement: clear their old positions (set to white) and place their color in the new positions. If any pixel/object moved, set `movement_occurred` to `true`.
10. If `movement_occurred` is `true`, repeat step 5 (start the next iteration of the simulation loop).
11. If `movement_occurred` is `false`, the simulation is complete. Return the final state of the output grid.
