
## train_1

**input:**
```
1 1 1 8 0 0 0 0 0 0
1 8 1 1 0 1 8 8 1 8
8 2 8 1 0 8 1 8 2 8
1 1 1 8 0 8 8 8 8 1
8 1 8 8 0 8 1 2 8 2
0 0 0 0 0 8 8 8 1 8
0 0 0 0 0 1 1 8 1 8
0 8 2 2 0 8 1 1 8 2
0 2 2 1 0 0 0 0 0 0
0 2 1 8 0 0 0 0 0 0
```


**output:**
```
8 2 2
2 2 1
2 1 8
```


## train_2

**input:**
```
0 0 0 0 0 0 8 8 8 8
0 8 8 8 8 0 8 2 2 8
0 8 1 8 8 0 8 8 8 8
0 8 8 2 8 0 8 2 1 8
0 8 8 8 8 0 8 8 8 8
0 0 0 0 0 0 0 0 0 0
0 0 0 8 8 8 8 8 8 0
0 0 0 8 8 8 2 8 8 0
0 0 0 8 2 8 1 8 8 0
0 0 0 8 1 8 8 8 8 0
```


**output:**
```
8 8 8 8
8 2 2 8
8 8 8 8
8 2 1 8
8 8 8 8
```


## train_3

**input:**
```
2 8 8 8 0 0 0 0 0 0
8 8 1 8 0 0 0 0 0 0
1 8 8 8 0 0 0 0 0 0
8 8 8 2 0 0 1 8 8 2
8 2 8 1 0 0 8 8 1 8
8 1 8 8 0 0 8 2 8 8
0 0 0 0 0 0 8 8 8 1
0 0 0 0 0 0 1 8 8 8
0 0 0 0 0 0 8 8 1 8
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
2 8 8 8
8 8 1 8
1 8 8 8
8 8 8 2
8 2 8 1
8 1 8 8
```

Okay, here's my analysis of the provided examples, focusing on perception, factual documentation, and a natural language program description of the transformation.

**Perception of Elements:**

The task involves extracting a subgrid from the input grid. This subgrid appears to be defined by the largest contiguous block of non-zero pixels *excluding* any black (0) pixels on the edges. The output grid's dimensions and content are determined by this specific block. There appears to be some flexibility about which subgrid to extract.

**YAML Block (Facts):**


```yaml
objects:
  - input_grid:
      type: grid
      properties:
        rows: 10  # Example 1
        cols: 10  # Example 1
        colors: [0, 1, 2, 8] # Example 1
  - output_grid:
      type: grid
      properties:
        rows: 3 # Example 1
        cols: 3  # Example 1
        colors: [1, 2, 8] # Example 1

  - sub_grid:
      type: grid
      properties:
          colors: [1,2,8]

actions:
  - extract:
      input: input_grid
      output: output_grid
      description: Extracts a specific region from the input_grid.

relationships:
  - subgrid_within_input:
      subject: sub_grid
      object: input_grid
      description: The sub_grid is a region contained within the input_grid.

  - subgrid_defines_output:
      subject: sub_grid
      object: output_grid
      description: The output is equal to the extracted sub_grid.
```


**Natural Language Program:**

1.  **Identify Boundaries:** Scan the input grid to find the outermost rows and columns which contain one or more black (0) pixels, and the non-zero pixels adjacent to them.
2.  **Define Inner Region:** Define a rectangular region within the input grid. This region *excludes* all rows and columns that are included in step 1.
3.  **Extract Subgrid:** Create the output grid by copying all pixels within the region identified in step 2, preserving their colors and relative positions.

In short: Find the largest rectangle that contains all the digits that is not surrounded by any zeros.

