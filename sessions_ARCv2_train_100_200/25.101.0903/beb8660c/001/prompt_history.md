
## train_1

**input:**
```
0 0 0 1
0 0 0 0
2 2 2 0
0 0 0 0
0 3 3 0
0 0 0 0
8 8 8 8
```


**output:**
```
0 0 0 0
0 0 0 0
0 0 0 0
0 0 0 1
0 0 3 3
0 2 2 2
8 8 8 8
```


## train_2

**input:**
```
0 2 2 0 0 0 0
0 0 0 0 3 0 0
1 1 1 0 0 0 0
0 0 0 0 0 0 0
0 5 5 5 5 5 5
0 0 0 0 0 0 0
6 6 6 6 6 0 0
0 0 0 4 4 4 4
0 0 0 0 0 0 0
8 8 8 8 8 8 8
```


**output:**
```
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 3
0 0 0 0 0 2 2
0 0 0 0 1 1 1
0 0 0 4 4 4 4
0 0 6 6 6 6 6
0 5 5 5 5 5 5
8 8 8 8 8 8 8
```


## train_3

**input:**
```
2 2 0
0 4 0
8 8 8
```


**output:**
```
0 0 4
0 2 2
8 8 8
```

## Perception

The input consists of a grid containing various horizontal bars (contiguous segments of a single color) placed on different rows, with a solid horizontal bar of azure (8) always present at the very bottom row. The background is white (0).

The transformation involves rearranging the colored bars located above the azure line. These bars effectively "fall" downwards towards the azure line. As they fall, they also shift horizontally to align with the right edge of the grid. They stack upon the azure line (or upon each other) in a specific order: the bar that was originally lowest (closest to the azure line) ends up at the bottom of the stack (directly above the azure line), the next lowest bar stacks on top of that, and so on, up to the bar that was originally highest, which ends up at the top of the stack. The azure line itself remains unchanged in its position. The final output grid has the same dimensions as the input grid, filled with white except for the unchanged azure line and the rearranged, right-aligned, stacked bars.

## Facts


```yaml
objects:
  - id: background
    type: grid_area
    color: white
  - id: floor
    type: horizontal_line
    color: azure
    location: bottom_row
    persistent: true # Remains unchanged in output
  - id: bars
    type: collection
    elements:
      type: horizontal_segment
      properties:
        color: non-white, non-azure
        location: various rows above the floor
        length: variable
        contiguity: horizontal

actions:
  - name: identify_bars
    input: input_grid
    target: bars above the floor
    output: list_of_bars (with color, length, original_row_index)
  - name: sort_bars
    input: list_of_bars
    criteria: original_row_index (descending - lowest first)
    output: sorted_list_of_bars
  - name: place_bars
    input: sorted_list_of_bars, grid_width, floor_row_index
    target: output_grid
    process: iterate through sorted bars, placing each one aligned to the right edge, stacking vertically upwards from the floor row.
  - name: copy_floor
    input: input_grid floor
    target: output_grid
    process: place the floor line in the same position in the output grid.

relationships:
  - type: spatial
    description: Bars are initially located above the floor.
  - type: order
    description: The final vertical stacking order of bars is the reverse of their initial vertical order.
  - type: alignment
    description: In the output, bars are aligned to the right edge of the grid.

grid_properties:
  - width: constant between input and output
  - height: constant between input and output
```


## Natural Language Program

1.  Initialize the output grid with the same dimensions as the input grid, filled entirely with the white color (0).
2.  Identify the row index of the horizontal azure (8) line (the 'floor') in the input grid.
3.  Copy this azure line from the input grid to the exact same location in the output grid.
4.  Scan the input grid rows *above* the azure line to identify all distinct horizontal, contiguous segments (bars) of non-white, non-azure colors. For each bar found, record its color, its length (number of cells), and its original row index.
5.  Create a list of these identified bars.
6.  Sort this list of bars based on their original row index in *descending* order (i.e., the bar with the highest row index, which was originally lowest/closest to the floor, comes first).
7.  Determine the width of the grid.
8.  Set a variable `current_placement_row` to be the row index immediately above the azure line (`floor_row_index - 1`).
9.  Iterate through the sorted list of bars (from lowest original bar to highest):
    a.  Calculate the starting column index for the current bar to make it align with the right edge: `start_column = grid_width - bar_length`.
    b.  Place the current bar onto the output grid at row `current_placement_row`, spanning columns from `start_column` to `grid_width - 1`, using the bar's color.
    c.  Decrement `current_placement_row` by 1 to prepare for placing the next bar on top.
10. The resulting output grid contains the stacked, right-aligned bars above the unchanged azure floor.
