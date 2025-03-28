
## train_1

**input:**
```
2 2 2 2 2 2 2 2 2 2 2 2 2 2 2
2 2 2 2 0 2 2 2 0 2 2 0 0 2 2
2 0 0 2 0 2 2 0 0 0 2 0 0 2 2
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 5 5 0 0 0 0 0 0 0 0 0 0 0 0
0 5 5 0 0 0 0 0 0 0 5 0 0 0 0
5 5 5 5 0 0 0 5 0 0 5 0 0 5 5
0 5 5 0 0 0 5 5 5 0 5 0 5 5 5
```


**output:**
```
2 2 2 2 2 2 2 2 2 2 2 2 2 2 2
2 2 2 2 1 2 2 2 1 2 2 1 1 2 2
2 1 1 2 1 2 2 1 1 1 2 1 1 2 2
1 1 1 0 1 0 0 0 0 0 1 1 1 1 0
0 0 0 0 0 0 0 0 0 0 0 1 1 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
2 2 2 2 2 2 2 2 2 2 2 2 2 2 2
2 0 2 2 2 2 2 2 2 2 2 2 2 2 0
2 0 0 2 2 2 0 0 0 2 2 2 2 2 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 5 0
0 0 0 0 0 0 5 0 0 0 0 0 0 5 0
0 5 5 5 0 0 5 5 0 0 0 0 0 5 0
0 5 5 5 0 0 5 5 5 0 0 0 0 5 0
```


**output:**
```
2 2 2 2 2 2 2 2 2 2 2 2 2 2 2
2 1 2 2 2 2 2 2 2 2 2 2 2 2 1
2 1 1 2 2 2 1 1 1 2 2 2 2 2 1
0 1 1 1 0 0 1 1 1 0 0 0 0 0 1
0 0 0 0 0 0 0 0 0 0 0 0 0 0 1
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

Okay, let's break down this task.

**Perception:**

1.  **Grid Size:** The input and output grids have the same dimensions (10x15 in both examples).
2.  **Color Palette:**
    *   Input uses white (0), red (2), and gray (5).
    *   Output uses white (0), blue (1), and red (2).
3.  **Key Changes:**
    *   Red pixels (2) seem to remain in their original positions.
    *   Gray pixels (5) in the input are consistently replaced with white pixels (0) in the output.
    *   Some white pixels (0) in the input are changed to blue pixels (1) in the output, while others remain white (0).
4.  **Pattern Focus:** The transformation centers around the white (0) pixels. The change from white (0) to blue (1) appears related to the proximity of red (2) pixels. Specifically, white pixels that are adjacent (horizontally, vertically, or diagonally) to at least one red pixel turn blue. White pixels not adjacent to any red pixels remain white.

**Facts:**


```yaml
# YAML representation of task observations

# Grid properties
grid_dimensions_preserved: true

# Color transformations
color_map:
  input: [0, 2, 5]  # white, red, gray
  output: [0, 1, 2] # white, blue, red

color_rules:
  - color: red (2)
    input_state: present
    output_state: preserved # Remains red (2) in the same location.
  - color: gray (5)
    input_state: present
    output_state: changed   # Changes to white (0).
  - color: white (0)
    input_state: present
    output_state: conditional_change # Can change to blue (1) or remain white (0).

# Conditions for white (0) transformation
white_to_blue_condition:
  type: adjacency
  target_color: red (2)
  adjacency_type: [horizontal, vertical, diagonal] # 8 neighbors
  rule: If an input white (0) pixel has at least one red (2) neighbor, it becomes blue (1) in the output.

white_remains_white_condition:
  type: adjacency
  target_color: red (2)
  adjacency_type: [horizontal, vertical, diagonal] # 8 neighbors
  rule: If an input white (0) pixel has no red (2) neighbors, it remains white (0) in the output.

# Objects/Structures - Less critical for this rule but observable
objects:
  - type: border
    color: red (2)
    location: top row (consistent)
  - type: distinct_shapes
    color: red (2)
    location: upper/middle grid area
  - type: distinct_shapes
    color: gray (5)
    location: lower grid area
    output_behavior: removed (become white)

```


**Natural Language Program:**

1.  Create a new grid with the same dimensions as the input grid.
2.  Iterate through each pixel (cell) of the input grid using its row and column index.
3.  For the current pixel at `(row, col)`:
    a.  If the input pixel's color is red (2), set the corresponding pixel in the new grid to red (2).
    b.  If the input pixel's color is gray (5), set the corresponding pixel in the new grid to white (0).
    c.  If the input pixel's color is white (0):
        i.  Examine all 8 neighboring pixels (horizontally, vertically, and diagonally adjacent) in the *input* grid.
        ii. If any of these neighbors have the color red (2), set the corresponding pixel at `(row, col)` in the new grid to blue (1).
        iii. If none of the neighbors have the color red (2), set the corresponding pixel at `(row, col)` in the new grid to white (0).
4.  The completed new grid is the output.
