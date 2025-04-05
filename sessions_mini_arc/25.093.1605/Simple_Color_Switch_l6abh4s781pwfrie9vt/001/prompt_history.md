
## train_1

**input:**
```
3 0 0 0 5
0 3 0 5 0
0 0 6 0 0
0 5 0 3 0
5 0 0 0 3
```


**output:**
```
5 0 0 0 3
0 5 0 3 0
0 0 6 0 0
0 3 0 5 0
3 0 0 0 5
```


## train_2

**input:**
```
5 0 0 0 6
0 5 0 6 0
0 0 1 0 0
0 6 0 5 0
6 0 0 0 5
```


**output:**
```
6 0 0 0 5
0 6 0 5 0
0 0 1 0 0
0 5 0 6 0
5 0 0 0 6
```


## train_3

**input:**
```
2 0 0 0 7
0 2 0 7 0
0 0 3 0 0
0 7 0 2 0
7 0 0 0 2
```


**output:**
```
7 0 0 0 2
0 7 0 2 0
0 0 3 0 0
0 2 0 7 0
2 0 0 0 7
```

**Perception:**

The input and output data are presented as 5x5 grids containing single-digit integers. Comparing the input and output grids reveals a consistent transformation across all examples. The content of each row remains identical between the input and output, but the vertical order of the rows is inverted. For instance, the top row of the input becomes the bottom row of the output, the second row from the top becomes the second row from the bottom, and so on, with the middle row remaining in the same position. This suggests a vertical flip operation applied to the entire grid.

**Facts:**


```yaml
Objects:
  - Input_Grid:
      type: 2D array
      properties:
        - dimensions: 5x5
        - elements: integers
  - Output_Grid:
      type: 2D array
      properties:
        - dimensions: 5x5
        - elements: integers
  - Row:
      type: 1D array
      properties:
        - elements: integers
        - position: index within the grid (0 to 4)

Actions:
  - Vertical_Flip:
      description: Reverses the order of rows in the grid.

Relationships:
  - The Output_Grid is a transformation of the Input_Grid.
  - For an N x M grid (here N=5), Row `i` of the Input_Grid becomes Row `N-1-i` of the Output_Grid.
  - The elements within each row maintain their original horizontal positions.
```


**Natural Language Program:**

1.  Receive the input grid.
2.  Reverse the vertical order of the rows in the input grid.
3.  Output the grid with the reversed row order.
