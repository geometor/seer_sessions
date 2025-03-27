
## train_1

**input:**
```
2 4 2 2 5 2 4 5
2 5 5 4 4 2 2 2
4 5 5 2 2 2 2 4
2 2 4 2 5 4 2 5
2 4 2 2 5 2 4 5
2 5 5 4 4 2 2 2
4 5 5 2 2 2 2 4
2 2 4 2 5 4 2 5
```


**output:**
```
2 4
2 5
```


## train_2

**input:**
```
4 3 6 4 0 6
6 0 0 3 3 4
6 4 4 3 3 0
0 3 6 0 4 6
0 6 3 0 4 3
3 4 4 6 6 0
```


**output:**
```
4 3
6 0
```


## train_3

**input:**
```
3 2 1 3 4 1
1 4 4 2 2 3
1 3 3 2 2 4
4 2 1 4 3 1
4 1 2 4 3 2
2 3 3 1 1 4
2 4 4 1 1 3
3 1 2 3 4 2
3 2 1 3 4 1
1 4 4 2 2 3
1 3 3 2 2 4
4 2 1 4 3 1
```


**output:**
```
3 2
1 4
```

## Perception

The task involves transforming an input grid of varying dimensions into a fixed-size 2x2 output grid. By examining the examples:

1.  **train_1:** The 8x8 input grid becomes a 2x2 output grid `[[2, 4], [2, 5]]`. These values correspond exactly to the pixels at the top-left corner (row 0, col 0; row 0, col 1; row 1, col 0; row 1, col 1) of the input grid. The repetition observed within the input grid (top 4 rows repeated) seems irrelevant to the output generation.
2.  **train_2:** The 6x6 input grid becomes a 2x2 output grid `[[4, 3], [6, 0]]`. Again, these values match the top-left 2x2 section of the input grid.
3.  **train_3:** The 12x6 input grid becomes a 2x2 output grid `[[3, 2], [1, 4]]`. This also matches the top-left 2x2 section of the input grid.

The consistent pattern across all examples is the extraction of the 2x2 subgrid located at the top-left corner (indices [0:2, 0:2]) of the input grid.

## Facts


```yaml
elements:
  - element: input_grid
    attributes:
      - type: 2D array of integers (pixels)
      - colors: red, yellow, blue, green, gray, magenta, orange, azure, maroon, white
      - dimensions: variable height and width (e.g., 8x8, 6x6, 12x6)
  - element: output_grid
    attributes:
      - type: 2D array of integers (pixels)
      - colors: same as input
      - dimensions: fixed 2x2
relationship:
  - type: extraction
    source: input_grid
    target: output_grid
    details: The output grid is a subgrid extracted from the input grid.
extraction_details:
  - location: top-left corner
  - coordinates: rows 0 to 1, columns 0 to 1
  - size: 2 rows, 2 columns
```


## Natural Language Program

1.  Identify the input grid.
2.  Extract the subgrid consisting of the pixels at row 0, column 0; row 0, column 1; row 1, column 0; and row 1, column 1.
3.  The extracted 2x2 subgrid is the output grid.
