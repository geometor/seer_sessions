
## train_1

**input:**
```
7 7 7 6
6 6 7 6
7 7 6 7
7 6 7 7
7 6 7 6
6 6 6 7
```


**output:**
```
7 7 7 2
2 2 7 2
7 7 2 7
7 2 7 7
7 2 7 2
2 2 2 7
```


## train_2

**input:**
```
6 6 7 6
6 6 7 7
7 7 6 7
```


**output:**
```
2 2 7 2
2 2 7 7
7 7 2 7
```


## train_3

**input:**
```
7 7 6 6 6 6
6 7 6 7 7 7
7 6 7 7 6 7
```


**output:**
```
7 7 2 2 2 2
2 7 2 7 7 7
7 2 7 7 2 7
```

## Perception of Task Elements

The task involves transforming an input grid into an output grid of the same dimensions. The grids contain pixels of different colors. In the provided examples, the input grids contain only two colors: Magenta (6) and Orange (7). The output grids contain Red (2) and Orange (7).

Observing the examples, it's clear that the transformation involves a color substitution. Specifically, every pixel that is Magenta (6) in the input grid is changed to Red (2) in the output grid. All pixels that are Orange (7) in the input grid remain Orange (7) in the output grid. The position of each pixel remains unchanged. This is a simple, pixel-wise color replacement rule.

## YAML Facts


```yaml
task_description: Color replacement based on pixel value.
grid_properties:
  - input_grid:
      colors_present: [Magenta (6), Orange (7)]
      dimensionality: 2D array
      size_constraint: Variable (examples show 6x4, 3x4, 3x6)
  - output_grid:
      colors_present: [Red (2), Orange (7)]
      dimensionality: 2D array
      size_constraint: Same dimensions as the corresponding input grid
transformation:
  type: Pixel-wise color substitution
  rules:
    - condition: Input pixel color is Magenta (6)
      action: Change pixel color to Red (2)
    - condition: Input pixel color is Orange (7)
      action: Keep pixel color as Orange (7)
  scope: Applied to every pixel individually.
relationships:
  - The position of each pixel in the output grid corresponds directly to its position in the input grid.
  - The transformation rule is consistent across all provided examples.
```


## Natural Language Program

1.  Initialize an output grid with the same dimensions as the input grid.
2.  Iterate through each pixel (cell) of the input grid, identified by its row and column index.
3.  For each pixel:
    a.  Check the color (value) of the input pixel.
    b.  If the input pixel's color is Magenta (6), set the color of the corresponding pixel in the output grid (at the same row and column) to Red (2).
    c.  If the input pixel's color is not Magenta (6), set the color of the corresponding pixel in the output grid to the same color as the input pixel.
4.  Return the completed output grid.
