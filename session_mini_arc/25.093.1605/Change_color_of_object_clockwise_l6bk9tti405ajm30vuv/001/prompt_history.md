
## train_1

**input:**
```
0 3 3 3 0
0 0 3 0 0
2 0 0 4 4
0 0 8 0 0
0 8 8 0 0
```


**output:**
```
0 2 2 2 0
0 0 2 0 0
8 0 0 3 3
0 0 4 0 0
0 4 4 0 0
```


## train_2

**input:**
```
5 0 3 3 0
0 0 3 3 0
2 0 0 0 0
2 0 0 0 6
2 0 0 6 6
```


**output:**
```
2 0 5 5 0
0 0 5 5 0
6 0 0 0 0
6 0 0 0 3
6 0 0 3 3
```


## train_3

**input:**
```
4 4 0 7 7
4 4 0 0 7
0 0 0 0 7
0 0 9 0 0
0 0 9 0 0
```


**output:**
```
9 9 0 4 4
9 9 0 0 4
0 0 0 0 4
0 0 7 0 0
0 0 7 0 0
```

Okay, I will analyze the provided examples to understand the transformation task.

## Perception of Elements:

*   **Input/Output Format:** Both input and output are 2D grids (matrices) containing single-digit non-negative integers.
*   **Grid Size:** The dimensions of the output grid are identical to the input grid.
*   **Cells:** Cells contain integer values. Zero ('0') appears to function as a background color or empty space. Non-zero integers represent different categories or 'colors'.
*   **Transformation Type:** The transformation modifies the values (colors) of the non-zero cells while preserving the positions of zero and non-zero cells. The set of unique non-zero values present in the input is the same as the set of unique non-zero values in the output.
*   **Core Logic:** The transformation seems to depend on the frequency (count) of each unique non-zero value in the input grid. It looks like a re-mapping or permutation of the non-zero values based on their frequency ranking.

## YAML Facts:


```yaml
task_elements:
  - element: Grid
    properties:
      - type: 2D Array
      - content: single-digit integers (0-9)
      - role: input and output container
  - element: Cell Value
    properties:
      - type: integer
      - range: 0-9
      - meaning: 0 represents background, non-zero represents distinct objects/colors
  - element: Non-zero Value Group
    properties:
      - identifier: the unique non-zero integer value
      - property: frequency (count of occurrences in the input grid)
relationships:
  - type: Preservation
    description: Grid dimensions and the positions of zero cells are preserved between input and output.
  - type: Value Mapping
    description: Each unique non-zero value in the input is mapped to a unique non-zero value in the output. The set of unique non-zero values remains the same.
    basis: The mapping is determined by the frequency ranking of the non-zero values in the input grid.
actions:
  - action: Analyze Input Grid
    steps:
      - Identify all unique non-zero values.
      - Count the frequency of each unique non-zero value.
  - action: Determine Value Mapping
    steps:
      - Create a ranked list of input values based on frequency (descending order). Break ties by sorting values in ascending order.
      - Create a ranked list of target values based on frequency (ascending order). Break ties by sorting values in descending order.
      - Establish a one-to-one mapping between the i-th element of the input rank list and the i-th element of the target rank list.
  - action: Generate Output Grid
    steps:
      - Create a new grid with the same dimensions as the input.
      - Iterate through each cell of the input grid.
      - If the input cell value is 0, set the corresponding output cell value to 0.
      - If the input cell value is non-zero, find its mapped value using the established mapping and set the corresponding output cell value to the mapped value.
```


## Natural Language Program:

1.  **Identify and Count:** Find all unique non-zero integer values present in the input grid and count how many times each unique value appears (its frequency).
2.  **Rank Input Values:** Create an ordered list of these unique non-zero values (`RankedInputValues`). Sort this list primarily based on frequency in descending order (most frequent first). If two values have the same frequency, sort them secondarily by their numerical value in ascending order (smaller number first).
3.  **Rank Target Values:** Create a second ordered list of the same unique non-zero values (`RankedTargetValues`). Sort this list primarily based on frequency in ascending order (least frequent first). If two values have the same frequency, sort them secondarily by their numerical value in descending order (larger number first).
4.  **Create Mapping:** Build a mapping rule where the value at index `i` in `RankedInputValues` maps to the value at index `i` in `RankedTargetValues`.
5.  **Transform Grid:** Construct the output grid by examining each cell of the input grid. If a cell contains 0, place 0 in the corresponding cell of the output grid. If a cell contains a non-zero value `V`, find the value that `V` maps to using the mapping rule created in step 4, and place that mapped value in the corresponding cell of the output grid.
