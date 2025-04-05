
## train_1

**input:**
```
4 0 0 3 3 2 9 7 7 0 0 0
```


**output:**
```
1 1 1 1 1 1 1 0 0 0 0 0
```


## train_2

**input:**
```
5 0 7 3 7 0 1 0 0 0 4 0
```


**output:**
```
1 1 1 1 1 1 0 0 0 0 0 0
```


## train_3

**input:**
```
8 0 0 0 0 3 8 2 0 4 0 0
```


**output:**
```
1 1 1 1 1 0 0 0 0 0 0 0
```


## train_4

**input:**
```
1 0 0 0 0 7 0 0 7 2 0 4
```


**output:**
```
1 1 1 1 1 0 0 0 0 0 0 0
```


## train_5

**input:**
```
6 0 6 4 1 5 4 4 0 0 0 0
```


**output:**
```
1 1 1 1 1 1 1 0 0 0 0 0
```


## train_6

**input:**
```
0 0 0 0 0 6 6 5 0 9 0 5
```


**output:**
```
1 1 1 1 1 0 0 0 0 0 0 0
```


## train_7

**input:**
```
5 9 0 0 6 1 0 1 5 2 9 0
```


**output:**
```
1 1 1 1 1 1 1 1 0 0 0 0
```

*   **Perception:** The task takes a sequence of 12 single-digit integers as input and produces a sequence of 12 binary digits (0s and 1s) as output. The output sequence always starts with a block of '1's followed by a block of '0's. The length of the block of '1's varies between examples. By comparing the input and output sequences across the examples, it appears that the number of '1's in the output corresponds directly to the count of non-zero numbers in the input sequence.

*   **Facts:**
    
```yaml
    task_type: sequence_transformation
    input:
      data_type: list_of_integers
      length: 12
      range: 0-9
      delimiter: space
    output:
      data_type: list_of_integers
      length: 12
      range: 0-1
      delimiter: space
      pattern: sequence_of_ones_followed_by_zeros
    transformation:
      relationship: input_non_zero_count_determines_output_ones_count
      rule: The number of '1's in the output sequence is equal to the count of non-zero integers in the input sequence. The remaining positions in the output sequence are filled with '0's.
    examples:
      - id: train_1
        input: "4 0 0 3 3 2 9 7 7 0 0 0"
        non_zero_count: 7
        output: "1 1 1 1 1 1 1 0 0 0 0 0"
      - id: train_2
        input: "5 0 7 3 7 0 1 0 0 0 4 0"
        non_zero_count: 6
        output: "1 1 1 1 1 1 0 0 0 0 0 0"
      - id: train_3
        input: "8 0 0 0 0 3 8 2 0 4 0 0"
        non_zero_count: 5
        output: "1 1 1 1 1 0 0 0 0 0 0 0"
      - id: train_7
        input: "5 9 0 0 6 1 0 1 5 2 9 0"
        non_zero_count: 8
        output: "1 1 1 1 1 1 1 1 0 0 0 0"
    ```


*   **Natural Language Program:**
    1.  Accept an input sequence of 12 integers.
    2.  Initialize a counter variable `non_zero_count` to zero.
    3.  Iterate through each integer in the input sequence.
    4.  For each integer, if it is not equal to 0, increment `non_zero_count`.
    5.  Create a new output sequence.
    6.  Append the integer '1' to the output sequence `non_zero_count` times.
    7.  Calculate the number of zeros needed: `zero_count = 12 - non_zero_count`.
    8.  Append the integer '0' to the output sequence `zero_count` times.
    9.  Return the generated output sequence.
```python
import re # Needed for splitting the string

"""
Counts the number of non-zero integers in the input sequence and generates an output sequence consisting of that many '1's followed by '0's to fill the remaining length (total length 12).
"""

def count_non_zeros(input_list):
  """Counts the number of non-zero elements in a list."""
  count = 0
  for num in input_list:
    if num != 0:
      count += 1
  return count

def transform(input_str):
  """
  Transforms an input string of 12 space-separated digits into an output string
  of 12 binary digits based on the count of non-zero digits in the input.
  """
  # 1. Accept an input sequence of 12 integers (as a string).
  # Parse the input string into a list of integers.
  input_list = [int(x) for x in input_str.split()]

  # 2. Initialize a counter variable non_zero_count to zero.
  # 3. Iterate through each integer in the input sequence.
  # 4. For each integer, if it is not equal to 0, increment non_zero_count.
  non_zero_count = count_non_zeros(input_list)

  # 5. Create a new output sequence.
  output_list = []

  # 6. Append the integer '1' to the output sequence non_zero_count times.
  for _ in range(non_zero_count):
    output_list.append(1)

  # 7. Calculate the number of zeros needed: zero_count = 12 - non_zero_count.
  zero_count = 12 - non_zero_count

  # 8. Append the integer '0' to the output sequence zero_count times.
  for _ in range(zero_count):
    output_list.append(0)

  # 9. Return the generated output sequence (formatted as a string).
  output_str = " ".join(map(str, output_list))
  return output_str

```
```python
import numpy as np

"""
Transforms an input sequence of 12 integers into an output sequence of 12 binary digits (0s and 1s). The number of '1's in the output sequence is equal to the count of non-zero integers in the input sequence. The '1's appear at the beginning of the output sequence, followed by '0's to complete the sequence length of 12.
"""

def count_non_zeros(data_sequence):
  """Counts the number of non-zero elements in a sequence (list or NumPy array)."""
  # Use numpy's count_nonzero for efficiency if it's an array,
  # otherwise iterate for lists.
  if isinstance(data_sequence, np.ndarray):
    return np.count_nonzero(data_sequence)
  else:
    count = 0
    for item in data_sequence:
      if item != 0:
        count += 1
    return count

def transform(input_sequence):
  """
  Applies the transformation rule to the input sequence.

  Args:
    input_sequence: A sequence (list or NumPy array) of 12 integers.

  Returns:
    A NumPy array of 12 binary integers (0s and 1s).
  """
  # Ensure the input is treated as a NumPy array for consistency
  # Although the helper function handles lists, the environment likely uses NumPy.
  if not isinstance(input_sequence, np.ndarray):
      input_sequence = np.array(input_sequence)

  # 1. Count the number of non-zero elements in the input sequence.
  non_zero_count = count_non_zeros(input_sequence)

  # 2. Determine the total length (should always be 12 based on examples).
  total_length = len(input_sequence) # Or assume 12 directly

  # 3. Calculate the number of zeros needed.
  zero_count = total_length - non_zero_count

  # 4. Create the output sequence: 'non_zero_count' ones followed by 'zero_count' zeros.
  # Using NumPy makes this construction straightforward.
  output_ones = np.ones(non_zero_count, dtype=int)
  output_zeros = np.zeros(zero_count, dtype=int)
  output_sequence = np.concatenate((output_ones, output_zeros))

  # 5. Return the generated output sequence.
  return output_sequence
```
