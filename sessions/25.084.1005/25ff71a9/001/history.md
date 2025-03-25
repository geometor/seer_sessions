
## train_1

**input:**
```
0 2 2
0 0 2
0 0 0
```


**output:**
```
0 0 0
0 2 2
0 0 2
```


## train_2

**input:**
```
0 0 0
1 1 1
0 0 0
```


**output:**
```
0 0 0
0 0 0
1 1 1
```


## train_3

**input:**
```
0 1 0
1 1 0
0 0 0
```


**output:**
```
0 0 0
0 1 0
1 1 0
```


## train_4

**input:**
```
1 1 1
0 0 0
0 0 0
```


**output:**
```
0 0 0
1 1 1
0 0 0
```

## Perception

The input and output are grids of the same size (3x3 in all examples).
The grids contain a background color (white, 0) and one or more non-white pixels forming a distinct object (red or blue).
In each example, the transformation involves shifting the entire content of the input grid down by one row.
The pixels originally in the last row of the input grid are effectively removed (or pushed off the grid).
The topmost row of the output grid is filled entirely with the background color (white, 0).
The shape, color, and relative positions of the pixels within the original object are preserved during the shift.

## Facts


```yaml
# Describe facts observed in the examples
# focusing on objects, properties, actions, relationships

# Grid properties
grid_dimensions_input:
  width: 3
  height: 3
grid_dimensions_output:
  width: 3
  height: 3
colors_present: [white, red, blue] # 0, 2, 1
background_color: white # 0

# Object Identification (implicit)
# Objects are contiguous areas of non-background color.
# Examples show single objects, but the rule applies grid-wide.

# Actions / Transformations
- action: shift_grid_content
  direction: down
  amount: 1 row
- action: fill_row
  row_index: 0 # Top row
  fill_color: background_color # white (0)

# Relationships
- The content of output row `i` (where `i > 0`) corresponds to the content of input row `i-1`.
- The content of output row `0` is always the background color, regardless of input content.
- The content of the last input row does not appear in the output.
```


## Natural Language Program

1.  Take the input grid.
2.  Create a new output grid of the same dimensions as the input grid.
3.  Fill the first row (row index 0) of the output grid with the background color (white, 0).
4.  For each subsequent row index `i` in the output grid (from 1 up to height-1):
    *   Copy the content of the row at index `i-1` from the input grid to the row at index `i` in the output grid.
5.  Return the completed output grid.
