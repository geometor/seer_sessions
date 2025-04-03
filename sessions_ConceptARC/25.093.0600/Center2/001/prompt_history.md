
## train_1

**input:**
```
3 1 4 2 7 8 9
```


**output:**
```
2
```


## train_2

**input:**
```
8 3 3 3 7 3 3 3 4
```


**output:**
```
7
```


## train_3

**input:**
```
4 3 1 3 4
```


**output:**
```
1
```

*   **Perception of Elements:**
    *   The input is a sequence of integers represented as a space-separated string.
    *   The output is a single integer.
    *   The transformation involves analyzing the frequency of each number in the input sequence.
    *   Specifically, it focuses on identifying numbers that appear exactly once (unique numbers).
    *   The position (index) of these unique numbers in the original sequence is important.
    *   The final output is the unique number located at the median index among all indices where unique numbers appear.

*   **YAML Facts:**
    
```yaml
    task_elements:
      - object: input_string
        properties:
          - format: space-separated integers
          - example_1: "3 1 4 2 7 8 9"
          - example_2: "8 3 3 3 7 3 3 3 4"
          - example_3: "4 3 1 3 4"
      - object: integer_list
        properties:
          - derived_from: input_string by parsing
          - example_1: [3, 1, 4, 2, 7, 8, 9]
          - example_2: [8, 3, 3, 3, 7, 3, 3, 3, 4]
          - example_3: [4, 3, 1, 3, 4]
      - object: number_counts
        properties:
          - derived_from: integer_list by counting occurrences
          - example_1: {3:1, 1:1, 4:1, 2:1, 7:1, 8:1, 9:1}
          - example_2: {8:1, 3:6, 7:1, 4:1}
          - example_3: {4:2, 3:2, 1:1}
      - object: unique_numbers
        properties:
          - description: Numbers from integer_list with a count of exactly 1
          - example_1: [3, 1, 4, 2, 7, 8, 9]
          - example_2: [8, 7, 4]
          - example_3: [1]
      - object: unique_number_indices
        properties:
          - description: List of 0-based indices where unique numbers appear in the original integer_list
          - example_1: [0, 1, 2, 3, 4, 5, 6]
          - example_2: [0, 4, 8] # Index of 8 is 0, index of 7 is 4, index of 4 is 8
          - example_3: [2]     # Index of 1 is 2
      - object: median_index
        properties:
          - description: The index corresponding to the median position within the sorted unique_number_indices list. If the list has an even length, the lower of the two middle indices is chosen.
          - calculated_from: unique_number_indices
          - example_1: 3 # Median index of [0, 1, 2, 3, 4, 5, 6] is index 3
          - example_2: 4 # Median index of [0, 4, 8] is index 4
          - example_3: 2 # Median index of [2] is index 2
      - object: output_integer
        properties:
          - derived_from: The element in the original integer_list located at the median_index
          - example_1: 2
          - example_2: 7
          - example_3: 1

    relationships:
      - input_string is parsed into integer_list
      - number_counts are derived from integer_list
      - unique_numbers are identified using number_counts
      - unique_number_indices are found by locating unique_numbers in integer_list
      - median_index is calculated from unique_number_indices
      - output_integer is the element from integer_list at the median_index
    ```


*   **Natural Language Program:**
    1.  Parse the input string into a list of integers.
    2.  Count the occurrences of each integer in the list.
    3.  Create a list containing the 0-based indices of all integers that appear exactly once in the original list.
    4.  Determine the median index from this list of indices. If there is an even number of such indices, use the index corresponding to the lower-median position (equivalent to `floor((length - 1) / 2)` of the sorted indices list, which effectively selects the middle element's index directly since the indices are already collected in order).
    5.  Retrieve the integer from the original list located at this calculated median index.
    6.  Output the retrieved integer.
