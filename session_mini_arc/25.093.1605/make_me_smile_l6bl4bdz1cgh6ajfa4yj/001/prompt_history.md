
## train_1

**input:**
```
4 4 4 4 4
4 0 4 0 4
4 4 4 4 4
4 0 0 0 4
4 0 4 0 4
```


**output:**
```
4 4 4 4 4
4 0 4 0 4
4 4 4 4 4
4 0 4 0 4
4 0 0 0 4
```


## train_2

**input:**
```
4 0 4 0 4
4 4 4 4 4
4 0 0 0 4
4 0 4 0 4
4 0 4 0 4
```


**output:**
```
4 0 4 0 4
4 4 4 4 4
4 0 4 0 4
4 0 4 0 4
4 0 0 0 4
```


## train_3

**input:**
```
4 0 4 0 4
4 4 4 4 4
0 0 0 0 0
0 4 4 4 0
0 4 4 4 0
```


**output:**
```
4 0 4 0 4
4 4 4 4 4
0 4 4 4 0
0 4 4 4 0
0 0 0 0 0
```

*   **Perception:**
    *   The input and output are 5x5 grids containing the integers 0 and 4.
    *   The transformation involves rearranging some rows of the input grid to produce the output grid.
    *   Comparing the input and output grids across the examples, the first two rows consistently remain unchanged.
    *   The last three rows of the input grid appear to be reordered in the output grid.
    *   The reordering seems related to the number of zeros present in each of these last three rows. Specifically, the rows are sorted in ascending order based on their zero count. Rows with the same zero count maintain their original relative order (stable sort).

*   **Facts:**
    
```yaml
    task_type: grid_transformation
    components:
      - object: Grid
        properties:
          - type: 2D array of integers
          - dimensions: 5x5
          - elements: [0, 4]
      - object: Row
        properties:
          - type: 1D array of integers
          - length: 5
          - derived_property: zero_count (number of 0s in the row)
    actions:
      - name: Isolate Subgrid
        inputs:
          - Grid
          - row_indices: [2, 3, 4] # 0-indexed
        outputs:
          - Subgrid (containing the last three rows)
      - name: Sort Rows
        inputs:
          - Subgrid
          - sort_key: zero_count
          - sort_order: ascending
          - sort_stability: stable
        outputs:
          - Sorted Subgrid
      - name: Reconstruct Grid
        inputs:
          - Original Grid (first two rows)
          - Sorted Subgrid (last three rows)
        outputs:
          - Output Grid
    relationships:
      - The first two rows of the input Grid map directly to the first two rows of the output Grid.
      - The last three rows of the output Grid are a permutation of the last three rows of the input Grid.
      - The permutation is determined by sorting based on the 'zero_count' property of the rows.
    ```


*   **Natural Language Program:**
    1.  Take the input 5x5 grid.
    2.  Keep the first two rows (rows 0 and 1) unchanged.
    3.  Consider the last three rows (rows 2, 3, and 4) as a subgrid.
    4.  For each row in this subgrid, count the number of zeros it contains.
    5.  Sort these three rows based on their zero counts in ascending order. If two rows have the same zero count, maintain their original relative order.
    6.  Place the sorted three rows into rows 2, 3, and 4 of the output grid.
    7.  Combine the unchanged first two rows and the sorted last three rows to form the final output grid.
