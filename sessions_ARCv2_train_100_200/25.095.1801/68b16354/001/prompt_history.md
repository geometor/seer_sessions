
## train_1

**input:**
```
7 3 3 1 2
1 8 2 4 1
2 7 8 7 2
7 7 4 1 8
8 1 7 7 1
```


**output:**
```
8 1 7 7 1
7 7 4 1 8
2 7 8 7 2
1 8 2 4 1
7 3 3 1 2
```


## train_2

**input:**
```
8 1 2 1 4
4 4 2 4 8
3 7 2 4 8
2 7 7 8 7
8 7 7 4 8
```


**output:**
```
8 7 7 4 8
2 7 7 8 7
3 7 2 4 8
4 4 2 4 8
8 1 2 1 4
```


## train_3

**input:**
```
2 7 4 3 4 8 3
2 3 7 1 2 3 3
8 7 4 3 2 2 4
1 1 2 1 4 4 7
2 4 3 1 1 4 1
4 8 7 4 4 8 2
7 3 8 4 3 2 8
```


**output:**
```
7 3 8 4 3 2 8
4 8 7 4 4 8 2
2 4 3 1 1 4 1
1 1 2 1 4 4 7
8 7 4 3 2 2 4
2 3 7 1 2 3 3
2 7 4 3 4 8 3
```

## Perception

The input is a grid of single-digit integers, represented as space-separated numbers on multiple lines. The output is also a grid of single-digit integers with the same dimensions and content as the input grid. The transformation appears to be a rearrangement of the rows within the grid. Specifically, the order of the rows in the input grid is reversed to produce the output grid. The first row of the input becomes the last row of the output, the second row of the input becomes the second-to-last row of the output, and so on, until the last row of the input becomes the first row of the output. The content and order of numbers within each row remain unchanged.

## Facts


```yaml
objects:
  - name: input_grid
    type: grid
    properties:
      - elements: single-digit integers
      - structure: rows and columns
      - content: identical to output_grid content, but rows are ordered differently
  - name: output_grid
    type: grid
    properties:
      - elements: single-digit integers
      - structure: rows and columns
      - content: identical to input_grid content, but rows are ordered differently
  - name: rows
    type: sequence
    properties:
      - elements: single-digit integers
      - parent: input_grid or output_grid
      - relationship_to_other_rows: ordered sequence within the grid
relationships:
  - type: transformation
    source: input_grid
    target: output_grid
    action: reverse_row_order
actions:
  - name: reverse_row_order
    description: The sequence of rows in the input grid is inverted to produce the sequence of rows in the output grid.
    input: sequence of rows (from input_grid)
    output: reversed sequence of rows (for output_grid)
```


## Natural Language Program

1.  Read the input as a grid of numbers, treating each line as a row.
2.  Reverse the order of the rows in the grid.
3.  Output the grid with the reversed row order.
