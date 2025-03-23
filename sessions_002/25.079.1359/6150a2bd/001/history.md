
## train_1

**input:**
```
3 3 8
3 7 0
5 0 0
```


**output:**
```
0 0 5
0 7 3
8 3 3
```


## train_2

**input:**
```
5 5 2
1 0 0
0 0 0
```


**output:**
```
0 0 0
0 0 1
2 5 5
```

Okay, here's my analysis of the provided input-output examples, formatted as a report:

**Perception of Elements:**

The task involves a transformation of a 2D grid of single-digit integers (representing colors) to another 2D grid of the same dimensions. The transformation doesn't seem to involve complex image manipulations, but rather a rearrangement of the existing elements based on some rule related to their values and/or positions. The values are preserved meaning that the colors in input are the same colors in output. The key focus is to identify the mapping of colors position from the input grid to the output grid.

**YAML Block - Facts:**


```yaml
facts:
  - observation: |
      Input and output grids have the same dimensions.
  - observation: |
      All input grid integer values exist on output grid.
  - observation: |
      The transformation is a rearrangement of elements with no change in values.
  - observation: |
      In example 1, input grid values are reordered by inverse value
       i.e. 8 -> 0, 7 -> 1, 5 -> 2, 3 -> 3, 0 -> 5.
  - observation: |
      In example 1, the columns are mirrored top to bottom.
  - observation: |
      In example 2, the columns are mirrored top to bottom.
  - observation: |
      In example 2, input grid values are reordered by inverse value
       i.e. 5 -> 2, 2 -> 5, 1 -> 1, 0 -> 0
```


**Natural Language Program:**

1.  **Reverse Rows**: Reverse the order of the rows in the input grid. The bottom row becomes the top row, the second-to-last row becomes the second row, and so on.
2.  **Sort by value.** Sort the values in the input grid by the inverse.


