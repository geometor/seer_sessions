
## train_1

**input:**
```
2 0 0 3 3 0 0 4 4 0 0
2 0 0 0 0 5 0 0 0 0 0
2 0 0 0 0 5 0 0 6 6 0
2 0 0 0 0 0 0 8 0 0 0
2 0 7 7 0 0 0 8 0 0 0
```


**output:**
```
2 3 3 4 4 0 0 0 0 0 0
2 5 0 0 0 0 0 0 0 0 0
2 5 6 6 0 0 0 0 0 0 0
2 0 0 8 0 0 0 0 0 0 0
2 7 7 8 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 0 0 8 8
3 0 0 4 0 0
3 0 0 4 0 0
0 0 0 0 0 6
1 1 0 0 0 6
0 0 0 0 0 0
0 0 5 5 0 0
0 0 0 0 0 0
0 0 0 0 0 0
2 2 2 2 2 2
```


**output:**
```
0 0 0 0 0 0
0 0 0 0 0 0
0 0 0 0 0 0
0 0 0 0 0 0
0 0 0 0 0 0
0 0 0 0 0 0
3 0 0 4 8 8
3 0 0 4 0 6
1 1 5 5 0 6
2 2 2 2 2 2
```


## train_3

**input:**
```
0 4 4 0 0 0 0 0 0 2
0 0 0 5 5 0 0 6 0 2
0 0 0 0 0 0 0 6 0 2
0 9 0 0 8 8 0 0 0 2
0 9 0 0 0 0 0 0 0 2
```


**output:**
```
0 0 0 0 0 0 0 4 4 2
0 0 0 0 0 0 5 5 6 2
0 0 0 0 0 0 0 0 6 2
0 0 0 0 0 0 9 8 8 2
0 0 0 0 0 0 9 0 0 2
```

Okay, let's analyze the `train_1` example pair.

**Perception of Elements:**

*   The input and output are grids (represented as lines of space-separated integers), likely representing rows of a 2D structure or individual 1D arrays. For `train_1`, each line seems to be processed independently.
*   Each line contains integer values, primarily single digits, including zero.
*   The core operation appears to involve rearranging the non-zero elements within each line while keeping the very first element fixed.
*   Zeroes seem to act as empty space or placeholders.

**YAML Facts:**


```yaml
task_name: shift_non_zeros_left_preserving_first
data_type: grid_of_integers
dimensionality: primarily_1D_processing # Each row/list processed independently
objects:
  - name: grid_row
    properties:
      - elements: list_of_integers
      - length: integer
  - name: element
    properties:
      - value: integer
      - position: index (integer)
      - is_zero: boolean
      - is_first: boolean
relationships:
  - type: spatial
    between: elements
    details: elements are ordered sequentially within a row
actions:
  - name: identify_fixed_element
    inputs: grid_row
    outputs: element (the first one)
  - name: filter_non_zeros
    inputs: grid_row (excluding the first element)
    outputs: list_of_non_zero_elements (maintaining relative order)
  - name: construct_output_row
    inputs:
      - fixed_element
      - filtered_non_zero_elements
      - original_row_length
    outputs: new_grid_row
    process: place fixed_element at start, append filtered_non_zero_elements, pad with zeros to match original length
constraints:
  - The first element of each input row remains in the first position of the output row.
  - The relative order of the non-zero elements (excluding the first) is preserved.
  - The length of the output row is the same as the length of the input row.
```


**Natural Language Program:**

For each input row:
1.  Store the value of the first element.
2.  Create a list containing all non-zero elements from the second position to the end of the input row, maintaining their original relative order.
3.  Construct the output row by starting with the stored first element.
4.  Append the list of non-zero elements (from step 2) immediately after the first element.
5.  Append zeros to the end of the output row until its length matches the length of the original input row.
