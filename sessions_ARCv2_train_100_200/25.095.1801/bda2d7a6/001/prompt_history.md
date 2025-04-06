
## train_1

**input:**
```
8 8 8 8 8 8 8 8
8 0 0 0 0 0 0 8
8 0 5 5 5 5 0 8
8 0 5 8 8 5 0 8
8 0 5 8 8 5 0 8
8 0 5 5 5 5 0 8
8 0 0 0 0 0 0 8
8 8 8 8 8 8 8 8
```


**output:**
```
5 5 5 5 5 5 5 5
5 8 8 8 8 8 8 5
5 8 0 0 0 0 8 5
5 8 0 5 5 0 8 5
5 8 0 5 5 0 8 5
5 8 0 0 0 0 8 5
5 8 8 8 8 8 8 5
5 5 5 5 5 5 5 5
```


## train_2

**input:**
```
0 0 0 0 0 0
0 7 7 7 7 0
0 7 6 6 7 0
0 7 6 6 7 0
0 7 7 7 7 0
0 0 0 0 0 0
```


**output:**
```
6 6 6 6 6 6
6 0 0 0 0 6
6 0 7 7 0 6
6 0 7 7 0 6
6 0 0 0 0 6
6 6 6 6 6 6
```


## train_3

**input:**
```
3 3 3 3 3 3
3 2 2 2 2 3
3 2 0 0 2 3
3 2 0 0 2 3
3 2 2 2 2 3
3 3 3 3 3 3
```


**output:**
```
0 0 0 0 0 0
0 3 3 3 3 0
0 3 2 2 3 0
0 3 2 2 3 0
0 3 3 3 3 0
0 0 0 0 0 0
```

## Perception of Elements

The task involves transforming 2D grids of colored cells (represented by digits). Each input grid consists of nested rectangular or square structures defined by different colors. The output grid maintains the same structure (shape and arrangement of regions) but with the colors systematically changed. Typically, three dominant colors define the nested layers: an outer border color, an intermediate color, and an inner shape color.

## Facts


```yaml
task_type: grid_transformation
input_data:
  type: 2D grid
  cell_type: integer (representing color)
  structure: nested rectangular/square regions
output_data:
  type: 2D grid
  cell_type: integer (representing color)
  structure: same spatial structure as input
transformation:
  type: color substitution
  logic: cyclic permutation of three key colors
key_colors:
  - name: Color A
    identification: Color of the outermost border cells.
  - name: Color B
    identification: Color filling the region immediately inside the border (A) and surrounding the innermost shape (C).
  - name: Color C
    identification: Color forming the innermost distinct rectangular/square shape.
relationships:
  - Input and output grids have identical dimensions.
  - The spatial position of each color region is preserved.
actions:
  - Identify the three key colors (A, B, C) based on their spatial roles (Outer, Middle, Inner).
  - Replace every instance of Color A in the input grid with Color C in the output grid.
  - Replace every instance of Color B in the input grid with Color A in the output grid.
  - Replace every instance of Color C in the input grid with Color B in the output grid.
```


## Natural Language Program

1.  Receive the input grid.
2.  Determine the color of the cells forming the outermost border of the grid; designate this as Color A.
3.  Examine the non-border cells. Identify the color that forms the most central or innermost distinct rectangular/square shape; designate this as Color C.
4.  Identify the color that predominantly fills the region between the border (Color A) and the innermost shape (Color C); designate this as Color B.
5.  Create a new output grid of the same dimensions as the input grid.
6.  For each cell in the input grid:
    a.  If the cell's color is Color A, set the corresponding cell in the output grid to Color C.
    b.  If the cell's color is Color B, set the corresponding cell in the output grid to Color A.
    c.  If the cell's color is Color C, set the corresponding cell in the output grid to Color B.
    d.  (Implicitly, if a color is not A, B, or C, it remains unchanged, though this doesn't occur in the provided examples where all cells belong to A, B, or C).
7.  Return the completed output grid.
