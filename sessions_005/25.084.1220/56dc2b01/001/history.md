
## train_1

**input:**
```
0 0 0 0 0
3 3 0 0 0
3 0 0 0 0
3 3 0 3 3
0 3 3 3 0
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
2 2 2 2 2
0 0 0 0 0
```


**output:**
```
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
8 8 8 8 8
3 3 0 0 0
3 0 0 0 0
3 3 0 3 3
0 3 3 3 0
2 2 2 2 2
0 0 0 0 0
```


## train_2

**input:**
```
0 3 0 0 0 0 0 0 0 0 2 0 0 0 0 0
0 3 3 3 0 0 0 0 0 0 2 0 0 0 0 0
3 3 0 0 0 0 0 0 0 0 2 0 0 0 0 0
0 3 3 3 0 0 0 0 0 0 2 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 8 0 3 0 0 2 0 0 0 0 0
0 0 0 0 0 8 0 3 3 3 2 0 0 0 0 0
0 0 0 0 0 8 3 3 0 0 2 0 0 0 0 0
0 0 0 0 0 8 0 3 3 3 2 0 0 0 0 0
```


## train_3

**input:**
```
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
2 2 2 2 2
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
3 3 3 3 0
3 0 0 3 0
3 3 0 3 0
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
```


**output:**
```
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
2 2 2 2 2
3 3 3 3 0
3 0 0 3 0
3 3 0 3 0
8 8 8 8 8
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
```

Okay, let's break down this task.

## Perception of Task Elements

1.  **Input/Output Grids:** Both input and output are 2D grids of pixels with colors represented by numbers 0-9.
2.  **Key Objects/Colors:**
    *   A single, contiguous green object (color 3). Its shape varies between examples.
    *   A single red object (color 2), which always appears as a straight line (horizontal or vertical).
    *   A background of white pixels (color 0).
    *   An azure line (color 8) appears only in the output.
3.  **Core Transformation:** The central action is the movement of the green object.
4.  **Movement Trigger/Constraint:** The red line acts as a barrier or destination. The green object moves towards the red line.
5.  **Movement Direction:** The direction is determined by the relative positions of the green object and the red line (up, down, left, or right).
6.  **Stopping Condition:** The green object stops moving when its edge is exactly one pixel away from the edge of the red line. It does not touch or overlap the red line.
7.  **Azure Line Creation:** A new line, colored azure (8), is introduced in the output grid.
8.  **Azure Line Position:** The position of the azure line depends on the direction of movement and the orientation of the red line:
    *   If the red line is *horizontal*, the azure line is also horizontal. It is placed one row away from the final position of the green object, on the side from which the green object arrived (i.e., above if moved down, below if moved up).
    *   If the red line is *vertical*, the azure line is also vertical. It is placed exactly in the middle column of the empty space between the original right edge and the final left edge of the green object (assuming rightward movement).
9.  **Azure Line Extent:** The azure line spans the same rows (if vertical) or columns (if horizontal) as the red line.
10. **Cleanup:** The pixels where the green object was originally located in the input grid are set to the background color (white, 0) in the output grid.

## Facts


```yaml
task_elements:
  - object:
      name: green_shape
      color: 3 (green)
      properties:
        - contiguous
        - variable shape
        - mobile
  - object:
      name: red_barrier
      color: 2 (red)
      properties:
        - contiguous
        - shape: straight line (horizontal or vertical)
        - stationary
        - acts as a movement boundary
  - object:
      name: azure_marker
      color: 8 (azure)
      properties:
        - shape: straight line (horizontal or vertical)
        - appears only in output
        - position depends on green_shape movement and red_barrier orientation
        - extent matches red_barrier extent (width or height)
  - background_color: 0 (white)

actions:
  - action: move
    actor: green_shape
    direction: towards red_barrier (up, down, left, or right)
    termination_condition: bounding box of green_shape is 1 pixel adjacent to bounding box of red_barrier
  - action: create
    object: azure_marker
    location_rule:
      - condition: red_barrier is horizontal
        position:
          - if green_shape moved down: 1 row above final green_shape top edge
          - if green_shape moved up: 1 row below final green_shape bottom edge
        orientation: horizontal
        extent: matches column span of red_barrier
      - condition: red_barrier is vertical
        position:
          - if green_shape moved right: column at (original_green_shape_right_edge + final_green_shape_left_edge) // 2
          # - if green_shape moved left: column at (original_green_shape_left_edge + final_green_shape_right_edge) // 2 # Hypothetical
        orientation: vertical
        extent: matches row span of red_barrier
  - action: clear
    location: original position of green_shape
    result: pixels set to background_color (0)

relationships:
  - green_shape moves relative to red_barrier.
  - final position of green_shape is adjacent (1 pixel gap) to red_barrier.
  - azure_marker position is determined by the final position of green_shape, its original position, and the orientation/extent of red_barrier.
```


## Natural Language Program

1.  Identify the contiguous green object (color 3) and the red line object (color 2) in the input grid. Record the coordinates occupied by each.
2.  Determine the orientation of the red line (horizontal or vertical) and the range of columns or rows it spans.
3.  Determine the bounding box of the green object and the red line.
4.  Calculate the direction the green object must move to get closer to the red line (up, down, left, or right).
5.  Simulate the movement of the green object one pixel at a time in the calculated direction. Stop when the bounding box of the green object is exactly one pixel away from the bounding box of the red line. Record the final coordinates of the green object.
6.  Create a new grid, initially copying the input grid.
7.  Update the new grid by changing the pixels at the *original* coordinates of the green object to the background color (white, 0).
8.  Update the new grid by drawing the green object (color 3) at its calculated *final* coordinates.
9.  Determine the position and extent for the azure line (color 8):
    *   If the red line is horizontal:
        *   The azure line will be horizontal and span the same columns as the red line.
        *   If the green object moved *down*, the azure line's row is `final_top_row - 1`.
        *   If the green object moved *up*, the azure line's row is `final_bottom_row + 1`.
    *   If the red line is vertical:
        *   The azure line will be vertical and span the same rows as the red line.
        *   If the green object moved *right*, the azure line's column is `(original_right_column + final_left_column) // 2`.
        *   If the green object moved *left*, the azure line's column is `(original_left_column + final_right_column) // 2`.
10. Draw the azure line (color 8) onto the new grid at the calculated position and extent.
11. The resulting grid is the output.
