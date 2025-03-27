
## train_1

**input:**
```
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 2 2 2 5 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 2 0 0
0 0 0 0 2 0 0
0 0 0 0 2 0 0
0 3 3 3 5 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 0
0 5 2
0 0 0
```


**output:**
```
0 0 0
0 5 3
0 2 0
```


## train_3

**input:**
```
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 5 0 0
0 0 0 0 2 0 0
0 0 0 0 2 0 0
```


**output:**
```
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 2 2 5 0 0
0 0 0 0 3 0 0
0 0 0 0 3 0 0
```


## train_4

**input:**
```
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 2 0 0 0
0 0 0 5 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 3 0 0 0
0 0 0 5 2 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
```


## train_5

**input:**
```
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 2 2 5 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
```


**output:**
```
0 0 0 2 0 0 0
0 0 0 2 0 0 0
0 3 3 5 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
```

Okay, let's break down this task.

**Perception**

1.  **Input Grid:** Contains white (0) background pixels, a single gray (5) pixel, and one or more red (2) pixels.
2.  **Red Pixels:** The red pixels always form a contiguous shape (line or block) connected to the gray pixel. This connection can be horizontal or vertical.
3.  **Gray Pixel:** Acts as a fixed point or pivot. It does not change color or position.
4.  **Output Grid:** The original red pixels change color to green (3) but remain in their initial positions. New red pixels (2) appear in the output grid. The position of these new red pixels seems related to the original red pixels and the gray pivot.
5.  **Transformation:** The overall transformation appears to involve two distinct actions centered around the gray pixel:
    *   **Color Change:** The original red (2) pixels become green (3).
    *   **Replication/Rotation:** A new copy of the original red shape, still colored red (2), is placed on the grid. This new shape's position is rotated 90 degrees counter-clockwise relative to the gray pivot point, compared to the original red shape's position.

**Facts**


```yaml
elements:
  - type: background
    color: white (0)
  - type: pivot
    color: gray (5)
    count: 1
    persistent: true # position and color unchanged
  - type: shape
    color: red (2) # input color
    attributes:
      - contiguous
      - connected_to: pivot (gray 5) # adjacent (not diagonal)
    actions:
      - change_color_to: green (3) # in original position
      - replicate_and_rotate:
          angle: 90 degrees
          direction: counter-clockwise
          center: pivot (gray 5)
          new_color: red (2)
  - type: transformed_shape
    color: green (3) # output color
    position: same as input red shape
  - type: new_shape
    color: red (2) # output color
    position: rotated position of input red shape

relationships:
  - input red shape is adjacent (cardinal directions) to the gray pivot
  - output green shape occupies the same position as the input red shape
  - output red shape's position is a 90-degree counter-clockwise rotation of the input red shape around the gray pivot

grid_properties:
  - size: variable (up to 30x30)
  - background_color: white (0)
```


**Natural Language Program**

1.  Initialize the output grid as a copy of the input grid.
2.  Locate the coordinates `(r_gray, c_gray)` of the single gray (5) pixel.
3.  Identify the coordinates `(r_red, c_red)` of all red (2) pixels in the input grid.
4.  For each identified red pixel at `(r_red, c_red)`:
    a.  Change the pixel color at `(r_red, c_red)` in the output grid to green (3).
    b.  Calculate the relative position of this red pixel with respect to the gray pivot: `dr = r_red - r_gray`, `dc = c_red - c_gray`.
    c.  Calculate the new relative position after a 90-degree counter-clockwise rotation: `dr_new = -dc`, `dc_new = dr`.
    d.  Calculate the new absolute position on the grid: `r_new = r_gray + dr_new`, `c_new = c_gray + dc_new`.
    e.  If the calculated position `(r_new, c_new)` is within the bounds of the grid, change the pixel color at `(r_new, c_new)` in the output grid to red (2). (Ensure this step does not overwrite the original gray pixel, although the rotation logic should naturally prevent this).
