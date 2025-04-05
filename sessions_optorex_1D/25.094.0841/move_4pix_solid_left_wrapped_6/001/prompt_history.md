
## train_1

**input:**
```
6 6 0 0 0 0 6 6 6 6 6 6
```


**output:**
```
0 0 6 6 6 6 6 6 6 6 0 0
```


## train_2

**input:**
```
0 0 9 9 9 9 0 0 0 0 0 0
```


**output:**
```
9 9 0 0 0 0 0 0 0 0 9 9
```


## train_3

**input:**
```
0 0 0 0 0 9 0 0 0 0 0 0
```


**output:**
```
0 9 0 0 0 0 0 0 0 0 0 0
```


## train_4

**input:**
```
0 0 0 0 0 7 7 7 0 0 0 0
```


**output:**
```
0 7 7 7 0 0 0 0 0 0 0 0
```


## train_5

**input:**
```
7 7 7 7 0 0 0 0 0 7 7 7
```


**output:**
```
0 0 0 0 0 7 7 7 7 7 7 7
```


## train_6

**input:**
```
0 0 0 0 0 0 0 0 0 9 9 0
```


**output:**
```
0 0 0 0 0 9 9 0 0 0 0 0
```


## train_7

**input:**
```
9 0 0 0 0 0 0 0 9 9 9 9
```


**output:**
```
0 0 0 0 9 9 9 9 9 0 0 0
```

## Perception

1.  **Input/Output Format:** Both input and output are strings representing sequences of single-digit integers separated by spaces.
2.  **Sequence Length:** The length of the sequence is constant across all examples (12 elements).
3.  **Element Preservation:** The non-zero digits present in the input are exactly the same non-zero digits present in the output, and their relative order is preserved. The number of zeros is also preserved.
4.  **Transformation:** The core transformation involves rearranging the elements. Specifically, the subsequence of non-zero elements is extracted from the input and then placed back into a sequence of zeros at a new starting position.
5.  **Repositioning Rule:** The placement seems to involve a cyclic shift of the non-zero subsequence. The amount of this shift depends on the *count* of non-zero elements.
6.  **Shift Calculation:**
    *   Identify the index of the *first* non-zero element in the input (`first_nz_idx_in`).
    *   Count the total number of non-zero elements (`N`).
    *   Determine a `shift_amount` based on `N` using the observed pattern:
        *   N=1 => shift=8
        *   N=2 => shift=8
        *   N=3 => shift=8
        *   N=4 => shift=8
        *   N=5 => shift=4
        *   N=7 => shift=5
        *   N=8 => shift=2
    *   The starting index for the non-zero subsequence in the output (`output_start_idx`) is calculated as `(first_nz_idx_in + shift_amount) % 12`.
7.  **Placement:** The extracted non-zero subsequence is placed into an initially all-zero output sequence of length 12, starting at `output_start_idx`, wrapping around the end of the sequence if necessary.

## Facts


```yaml
task_elements:
  - object: input_sequence
    properties:
      - type: list of integers
      - length: 12
      - elements: single digits (0-9)
  - object: output_sequence
    properties:
      - type: list of integers
      - length: 12
      - elements: single digits (0-9)
      - derived_from: input_sequence
  - object: non_zero_subsequence
    properties:
      - type: list of integers
      - elements: non-zero digits from input_sequence
      - order: preserved relative order from input_sequence
      - count: N (number of non-zero elements)
  - object: zero_elements
    properties:
      - value: 0
      - count: 12 - N
relationship:
  - type: transformation
    applies_to: input_sequence
    results_in: output_sequence
    steps:
      - action: identify_and_extract
        actor: system
        input: input_sequence
        output: non_zero_subsequence, first_nz_idx_in, N
        details: Finds all non-zero elements, notes their order, finds the index of the first one, and counts them.
      - action: determine_shift
        actor: system
        input: N (count of non-zero elements)
        output: shift_amount
        details: Calculates shift based on N using a predefined mapping {1: 8, 2: 8, 3: 8, 4: 8, 5: 4, 7: 5, 8: 2}.
      - action: calculate_start_position
        actor: system
        input: first_nz_idx_in, shift_amount, sequence_length (12)
        output: output_start_idx
        details: Computes (first_nz_idx_in + shift_amount) % 12.
      - action: construct_output
        actor: system
        input: non_zero_subsequence, output_start_idx, sequence_length (12)
        output: output_sequence
        details: Creates a list of 12 zeros, then places the non_zero_subsequence into it starting at output_start_idx, wrapping around cyclically.
```


## Natural Language Program

1.  Read the input string and convert it into a list of 12 integers.
2.  Create a new list containing only the non-zero integers from the input list, maintaining their original relative order. Let this be the `non_zero_sequence`.
3.  Count the number of elements in the `non_zero_sequence`. Let this count be `N`.
4.  Find the index of the first non-zero element in the original input list. Let this be `first_nz_idx_in`. Handle the case where there are no non-zero elements (although not present in examples, the output would be all zeros).
5.  Determine the `shift_amount` based on the value of `N` according to the following rules:
    *   If `N` is 1, 2, 3, or 4, the `shift_amount` is 8.
    *   If `N` is 5, the `shift_amount` is 4.
    *   If `N` is 7, the `shift_amount` is 5.
    *   If `N` is 8, the `shift_amount` is 2.
    *   (Assume these cover all relevant cases based on provided examples).
6.  Calculate the starting index for placing the `non_zero_sequence` in the output list: `output_start_idx = (first_nz_idx_in + shift_amount) % 12`.
7.  Create the output list, initially filled with 12 zeros.
8.  Iterate through the `non_zero_sequence`. For each element, place it into the output list at the position `(output_start_idx + current_index_in_non_zero_sequence) % 12`.
9.  Convert the output list back into a space-separated string.
