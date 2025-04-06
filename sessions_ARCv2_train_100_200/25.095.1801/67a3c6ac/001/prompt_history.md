
## train_1

**input:**
```
7 7 7 6 6 6 2
6 7 1 1 7 7 1
7 7 2 1 2 6 6
2 2 7 7 7 2 2
7 2 7 1 2 7 2
6 6 6 2 2 1 1
6 2 6 6 6 6 6
```


**output:**
```
2 6 6 6 7 7 7
1 7 7 1 1 7 6
6 6 2 1 2 7 7
2 2 7 7 7 2 2
2 7 2 1 7 2 7
1 1 2 2 6 6 6
6 6 6 6 6 2 6
```


## train_2

**input:**
```
6 6 6 2
6 1 6 2
7 2 7 2
1 7 2 2
```


**output:**
```
2 6 6 6
2 6 1 6
2 7 2 7
2 2 7 1
```


## train_3

**input:**
```
1 2 7 1 1 1
2 1 7 7 2 6
2 1 2 6 2 1
1 2 1 7 6 2
2 7 1 2 7 1
2 1 6 2 7 7
```


**output:**
```
1 1 1 7 2 1
6 2 7 7 1 2
1 2 6 2 1 2
2 6 7 1 2 1
1 7 2 1 7 2
7 7 2 6 1 2
```

**Perception of Task Elements:**

The task involves processing a 2D grid of numerical digits. The input and output grids consistently share the same dimensions in each example pair. The core transformation appears to operate independently on each row of the input grid. The numbers within each row are rearranged, but the set of numbers within a given row remains the same between the input and output, just in a different order. Comparing the input and output rows suggests a spatial reversal or reflection along the vertical axis.

**Facts:**


```yaml
objects:
  - name: input_grid
    type: 2D array of integers
    properties:
      - rows: ordered sequence of 1D arrays
      - columns: ordered sequence of 1D arrays
      - elements: integers
  - name: output_grid
    type: 2D array of integers
    properties:
      - rows: ordered sequence of 1D arrays
      - columns: ordered sequence of 1D arrays
      - elements: integers
      - dimensions: same as input_grid
  - name: row
    type: 1D array of integers (horizontal slice of the grid)
    properties:
      - elements: integers
      - order: sequence of elements matters

relationships:
  - type: transformation
    applies_to: input_grid
    results_in: output_grid
  - type: correspondence
    from: input_grid row at index `i`
    to: output_grid row at index `i`

actions:
  - name: horizontal_reversal
    operates_on: row
    description: Reverses the order of elements within a row. The first element becomes the last, the second becomes the second-to-last, and so on.
```


**Natural Language Program:**

1.  Iterate through each row of the input grid.
2.  For the current row, reverse the horizontal order of its elements.
3.  Construct the output grid by placing each reversed row at the same row index as its corresponding original row in the input grid.
