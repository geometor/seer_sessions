
## train_1

**input:**
```
0 0 0 0 1 2 3 4 7 2 0 0
```


**output:**
```
0 0 0 0 0 1 2 3 4 7 2 0
```


## train_2

**input:**
```
0 0 0 5 2 3 2 2 4 8 4 7
```


**output:**
```
7 0 0 0 5 2 3 2 2 4 8 4
```


## train_3

**input:**
```
0 0 0 0 0 0 4 7 4 7 2 0
```


**output:**
```
0 0 0 0 0 0 0 4 7 4 7 2
```


## train_4

**input:**
```
2 2 6 0 0 0 0 0 2 2 7 4
```


**output:**
```
4 2 2 6 0 0 0 0 0 2 2 7
```


## train_5

**input:**
```
2 1 1 6 6 3 0 0 0 0 5 9
```


**output:**
```
9 2 1 1 6 6 3 0 0 0 0 5
```


## train_6

**input:**
```
0 0 1 5 8 7 1 7 9 5 0 0
```


**output:**
```
0 0 0 1 5 8 7 1 7 9 5 0
```


## train_7

**input:**
```
6 4 0 0 0 0 0 0 0 3 6 9
```


**output:**
```
9 6 4 0 0 0 0 0 0 0 3 6
```

Okay, let's break down the transformation logic.

**Perception of Task Elements:**

*   The input and output are both sequences (lists) of single-digit integers.
*   The length of the output list is always the same as the length of the input list.
*   The transformation involves rearranging the elements of the input list. Specifically, the position of the *last* element seems to change based on its value, while the relative order of the other elements is preserved.
*   There appear to be two distinct transformation behaviors, conditional on whether the last element of the input is zero or non-zero.

**Facts (YAML):**


```yaml
objects:
  - name: input_list
    type: List[int]
    description: The input sequence of integers.
  - name: output_list
    type: List[int]
    description: The transformed sequence of integers.
  - name: last_element
    type: int
    description: The integer value at the last position of the input_list.
  - name: base_list
    type: List[int]
    description: The input_list excluding its last element.
properties:
  - object: last_element
    name: value
    description: The numerical value of the last element (specifically whether it is 0 or not).
  - object: base_list
    name: first_non_zero_index
    description: The index of the first element in the base_list that is not 0. If all elements are 0, this index is considered 0.
relationships:
  - type: derivation
    source: input_list
    target: last_element
    description: last_element is the final item in input_list.
  - type: derivation
    source: input_list
    target: base_list
    description: base_list consists of all elements of input_list except the last one.
actions:
  - name: remove_last
    object: input_list
    result: base_list, last_element
    description: Separate the input_list into the last_element and the remaining base_list.
  - name: find_insertion_point
    object: base_list
    condition: last_element == 0
    result: index
    description: Determine the index of the first non-zero element in the base_list (or index 0 if none exists).
  - name: insert_element
    target: base_list
    element: last_element
    position: index
    result: output_list
    description: Insert the last_element into the base_list at a specific index (either index 0 or the first_non_zero_index) to produce the output_list.
conditions:
  - name: check_last_element_value
    based_on: last_element.value
    outcomes:
      - value_is_zero: Determines the insertion logic (find first non-zero index).
      - value_is_non_zero: Determines the insertion logic (insert at beginning).
```


**Natural Language Program:**

1.  Examine the input list and identify its last element.
2.  Create a temporary list containing all elements from the input list *except* the last one, maintaining their original relative order.
3.  Check the value of the identified last element:
    *   **If the last element is 0:** Find the index of the first element in the temporary list that is not zero. If all elements in the temporary list are zero, use index 0. Insert the original last element (the 0) into the temporary list at this determined index.
    *   **If the last element is not 0:** Insert the original last element at the very beginning (index 0) of the temporary list.
4.  The modified temporary list is the final output list.
```python
import collections

"""
Transformation Rule:

1. Separate the input list into its last element and the remaining 'base' list (all elements except the last).
2. Check the value of the last element:
   a. If the last element is 0:
      i. Find the index of the first non-zero element in the 'base' list.
      ii. If no non-zero element exists in the 'base' list, use index 0.
      iii. Insert the last element (0) into the 'base' list at this found index.
   b. If the last element is not 0:
      i. Insert the last element at the beginning (index 0) of the 'base' list.
3. The resulting modified 'base' list is the output list.
"""

def find_first_non_zero_index(data_list):
    """
    Finds the index of the first non-zero element in a list.
    Returns 0 if all elements are zero or the list is empty.
    """
    for index, value in enumerate(data_list):
        if value != 0:
            return index
    # If no non-zero element is found, return 0
    return 0

def transform(input_list_str):
    """
    Applies the transformation rule to the input list string.

    Args:
        input_list_str: A string representing a space-separated list of integers.

    Returns:
        A string representing the space-separated transformed list of integers.
    """
    # Convert string input to a list of integers
    input_list = [int(x) for x in input_list_str.split()]

    # Handle empty or single-element lists (though not in examples, good practice)
    if not input_list:
        return ""
    if len(input_list) == 1:
        return input_list_str # No change possible

    # 1. Separate the last element and the base list
    last_element = input_list[-1]
    base_list = input_list[:-1]

    # 2. Check the value of the last element and determine insertion point
    if last_element == 0:
        # 2.a Find the index for insertion (first non-zero or 0)
        insertion_index = find_first_non_zero_index(base_list)
        # Insert the last element (0) at the determined index
        output_list = base_list[:insertion_index] + [last_element] + base_list[insertion_index:]
    else:
        # 2.b Insert the non-zero last element at the beginning
        output_list = [last_element] + base_list

    # Convert the output list back to a space-separated string
    output_str = " ".join(map(str, output_list))

    return output_str

```
```python
import numpy as np
import collections # Although not strictly needed with the current numpy approach, good to keep in mind

"""
Transformation Rule:

1. Receive the input sequence (which can be a list or NumPy array of integers).
2. Identify the `last_element` of the input sequence.
3. Create a `base_sequence` containing all elements from the input sequence *except* the `last_element`, preserving their relative order.
4. Evaluate the value of the `last_element`:
   a. If the `last_element` is 0:
      i. Find the index (`insertion_index`) of the first non-zero element within the `base_sequence`.
      ii. If the `base_sequence` contains only zeros or is empty, set the `insertion_index` to 0.
      iii. Construct the `output_sequence` by inserting the `last_element` (0) into the `base_sequence` at the determined `insertion_index`.
   b. If the `last_element` is not 0:
      i. Set the `insertion_index` to 0.
      ii. Construct the `output_sequence` by inserting the `last_element` at the beginning (index 0) of the `base_sequence`.
5. Return the constructed `output_sequence`.
"""

def find_first_non_zero_index(data_sequence):
    """
    Finds the index of the first non-zero element in a sequence (list or numpy array).
    Returns 0 if all elements are zero or the sequence is empty.
    """
    # Use np.nonzero which returns a tuple of arrays, one for each dimension.
    # For a 1D array, we look at the first element of the tuple.
    non_zero_indices = np.nonzero(data_sequence)[0]
    if non_zero_indices.size > 0:
        # Return the first index found
        return non_zero_indices[0]
    else:
        # If no non-zero element is found (or sequence is empty), return 0
        return 0

def transform(input_sequence: np.ndarray) -> np.ndarray:
    """
    Applies the transformation rule to the input numpy array sequence.
    """
    # Handle empty or single-element sequences
    if input_sequence.size <= 1:
        return input_sequence.copy() # Return a copy to avoid modifying original

    # 1. & 2. Separate the last element and the base sequence
    # Ensure input is treated as a numpy array
    if not isinstance(input_sequence, np.ndarray):
         input_sequence = np.array(input_sequence)

    last_element = input_sequence[-1]
    base_sequence = input_sequence[:-1]

    # 4. Evaluate the last element and determine insertion logic
    if last_element == 0:
        # 4.a Find the index for insertion (first non-zero or 0)
        insertion_index = find_first_non_zero_index(base_sequence)
        # Construct the output sequence using numpy insertion
        # np.insert(array, index, value)
        output_sequence = np.insert(base_sequence, insertion_index, last_element)
    else:
        # 4.b Insert the non-zero last element at the beginning
        # np.insert automatically handles index 0 correctly
        output_sequence = np.insert(base_sequence, 0, last_element)

    # 5. Return the constructed sequence
    return output_sequence

```
```python
import numpy as np

"""
Transformation Rule:

1. Receive the input sequence of integers.
2. Separate the input sequence into two parts: the `last_element` (the final integer) and the `base_sequence` (all preceding integers in their original order).
3. Evaluate the value of the `last_element`:
    a. If the `last_element` is 0:
        i. Scan the `base_sequence` from the beginning to find the index of the *first* element that is not zero.
        ii. If a non-zero element is found, note its index as the `insertion_index`.
        iii. If all elements in the `base_sequence` are zero (or the `base_sequence` is empty), set the `insertion_index` to 0.
        iv. Construct the output sequence by inserting the `last_element` (the 0) into the `base_sequence` at the determined `insertion_index`.
    b. If the `last_element` is not 0:
        i. Set the `insertion_index` to 0.
        ii. Construct the output sequence by inserting the `last_element` into the `base_sequence` at the beginning (index 0).
4. The constructed sequence is the final output.
"""

def find_first_non_zero_index(data_sequence: np.ndarray) -> int:
    """
    Finds the index of the first non-zero element in a numpy array.
    Returns 0 if all elements are zero or the sequence is empty.
    """
    # np.nonzero returns a tuple of arrays, one for each dimension.
    # For a 1D array, we look at the first element of the tuple.
    non_zero_indices = np.nonzero(data_sequence)[0]
    if non_zero_indices.size > 0:
        # Return the first index found
        return non_zero_indices[0]
    else:
        # If no non-zero element is found (or sequence is empty), return 0
        return 0

def transform(input_sequence: np.ndarray) -> np.ndarray:
    """
    Applies the transformation rule to the input numpy array sequence.
    """
    # Ensure input is a numpy array
    if not isinstance(input_sequence, np.ndarray):
         input_sequence = np.array(input_sequence)

    # Handle empty or single-element sequences - no transformation possible/needed
    if input_sequence.size <= 1:
        return input_sequence.copy() # Return a copy to avoid modifying original

    # 1. & 2. Separate the last element and the base sequence
    last_element = input_sequence[-1]
    base_sequence = input_sequence[:-1]

    # 3. Evaluate the last element and determine insertion logic
    if last_element == 0:
        # 3.a If last element is 0
        # Find the index for insertion (first non-zero or 0)
        insertion_index = find_first_non_zero_index(base_sequence)
        # Construct the output sequence using numpy insertion
        output_sequence = np.insert(base_sequence, insertion_index, last_element)
    else:
        # 3.b If last element is non-zero
        # Insert the non-zero last element at the beginning (index 0)
        insertion_index = 0
        output_sequence = np.insert(base_sequence, insertion_index, last_element)

    # 4. Return the constructed sequence
    return output_sequence
```
