
## train_1

**input:**
```
5 5 5 0 0 5 5 5 5 5 5 5
```


**output:**
```
5 5 0 0 5 5 5 5 5 5 5 5
```


## train_2

**input:**
```
5 0 0 0 0 0 0 5 5 5 5 5
```


**output:**
```
0 0 0 0 0 0 5 5 5 5 5 5
```


## train_3

**input:**
```
4 4 4 4 4 4 4 4 4 4 4 0
```


**output:**
```
4 4 4 4 4 4 4 4 4 4 0 4
```


## train_4

**input:**
```
7 7 7 7 7 0 0 7 7 7 7 7
```


**output:**
```
7 7 7 7 0 0 7 7 7 7 7 7
```


## train_5

**input:**
```
0 0 0 0 0 0 0 0 8 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 8 0 0 0 0
```


## train_6

**input:**
```
6 6 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
6 0 0 0 0 0 0 0 0 0 0 6
```


## train_7

**input:**
```
0 0 0 0 0 0 0 7 7 7 0 0
```


**output:**
```
0 0 0 0 0 0 7 7 7 0 0 0
```

**Perception of the Elements:**

The task involves transforming an input sequence of single-digit integers into an output sequence of the same length. The transformation appears to be a reordering operation where a single element from the input sequence is removed from its original position and appended to the end. The core challenge lies in identifying which specific element needs to be moved based on the properties of the input sequence. The properties influencing the choice of the element seem related to the counts of zero and unique non-zero elements within the sequence, and potentially the position of the first zero.

**YAML Facts:**


```yaml
objects:
  - input_sequence: A list of single-digit integers.
  - output_sequence: A list of single-digit integers derived from the input.
  - element: An individual integer within the sequence.
  - zero: The integer 0.
  - non_zero_element: An integer other than 0.

properties:
  - length: The number of elements in the sequence (constant between input and output).
  - count_of_zeros: The total number of zeros in the input sequence.
  - count_of_unique_non_zeros: The number of distinct non-zero integers in the input sequence.
  - index_of_first_zero: The position (0-based index) of the first occurrence of 0 in the input sequence.
  - index_to_move: The position (0-based index) of the element selected for relocation.
  - element_to_move: The value of the element at the `index_to_move`.

actions:
  - count_elements: Determine the frequency of specific elements (like 0) or categories (like unique non-zeros).
  - find_first_index: Locate the index of the first occurrence of a specific element (like 0).
  - identify_element_to_move: Determine which element needs to be relocated based on sequence properties.
  - remove_element_at_index: Delete the element from its original position.
  - append_element: Add the removed element to the end of the sequence.

relationships:
  - transformation_rule: Defines how the `input_sequence` is modified to produce the `output_sequence`. The rule depends conditionally on `count_of_zeros`, `count_of_unique_non_zeros`, and `index_of_first_zero`.
```


**Natural Language Program:**

1.  Receive the `input_sequence` of integers.
2.  Calculate the `count_of_unique_non_zeros` by finding how many distinct integers greater than zero are present in the `input_sequence`.
3.  Calculate the `count_of_zeros` by counting the occurrences of the integer 0 in the `input_sequence`.
4.  Initialize `index_to_move` to 0.
5.  Check if `count_of_unique_non_zeros` is exactly 1 AND `count_of_zeros` is exactly 2.
6.  If the condition in step 5 is true:
    a.  Find the `index_of_first_zero` in the `input_sequence`.
    b.  Set `index_to_move` to `index_of_first_zero - 1`.
7.  Identify the `element_to_move` located at the determined `index_to_move` in the `input_sequence`.
8.  Create a new sequence by removing the element at `index_to_move` from the `input_sequence`.
9.  Append the `element_to_move` to the end of the new sequence.
10. Return the modified sequence as the `output_sequence`.
```python
import collections

"""
Transforms a sequence of integers based on specific conditions related to the count of zeros and unique non-zero elements.

1. Parses the input string into a list of integers.
2. Counts the occurrences of zero and the number of unique non-zero elements.
3. Determines the index of the element to move:
   - Defaults to index 0.
   - If there is exactly one unique non-zero element AND exactly two zeros, the index becomes the position immediately before the first zero.
4. Removes the element at the determined index.
5. Appends the removed element to the end of the sequence.
6. Formats the modified sequence back into a space-separated string.
"""

def transform(input_string: str) -> str:
    """
    Applies the transformation rule to the input sequence string.

    Args:
        input_string: A space-separated string of integers.

    Returns:
        A space-separated string of integers representing the transformed sequence.
    """
    # 1. Receive the `input_sequence` of integers (parse from string)
    input_list = [int(x) for x in input_string.split()]
    output_list = list(input_list) # Work on a copy

    if not output_list:
        return "" # Handle empty input

    # 2. Calculate the `count_of_unique_non_zeros`
    unique_non_zeros = {x for x in output_list if x != 0}
    count_of_unique_non_zeros = len(unique_non_zeros)

    # 3. Calculate the `count_of_zeros`
    counts = collections.Counter(output_list)
    count_of_zeros = counts[0]

    # 4. Initialize `index_to_move` to 0.
    index_to_move = 0

    # 5. Check if `count_of_unique_non_zeros` is exactly 1 AND `count_of_zeros` is exactly 2.
    if count_of_unique_non_zeros == 1 and count_of_zeros == 2:
        # 6a. Find the `index_of_first_zero`
        try:
            index_of_first_zero = output_list.index(0)
            # 6b. Set `index_to_move` if the first zero is not at the beginning
            if index_of_first_zero > 0:
                 index_to_move = index_of_first_zero - 1
            # If index_of_first_zero is 0, the default index_to_move=0 is used.
        except ValueError:
            # This case shouldn't happen if count_of_zeros == 2, but handle defensively
            pass 

    # 7. Identify the `element_to_move` (will be done during removal)
    # 8. Create a new sequence by removing the element at `index_to_move`
    # 9. Append the `element_to_move` to the end of the new sequence.
    if 0 <= index_to_move < len(output_list):
        element_to_move = output_list.pop(index_to_move)
        output_list.append(element_to_move)
    # else: handle potential index out of bounds if logic were different,
    # but current logic ensures index_to_move is valid or 0 for non-empty lists.


    # 10. Return the modified sequence as the `output_sequence` (formatted as string)
    return " ".join(map(str, output_list))

```
```python
import numpy as np

"""
Transforms a sequence of integers by moving the first element to the end of the sequence.
"""

def transform(input_sequence):
    """
    Moves the first element of the input sequence to the end.

    Args:
        input_sequence: A list or NumPy array of integers.

    Returns:
        A NumPy array representing the transformed sequence.
    """
    # Handle potential NumPy array input by converting to list for easier manipulation
    if isinstance(input_sequence, np.ndarray):
        output_list = input_sequence.tolist()
    elif isinstance(input_sequence, list):
        output_list = list(input_sequence) # Make a copy to avoid modifying the original input if it's a list
    else:
        # Handle other potential types or raise an error if needed
        # For now, assume it's list-like or convertible
        try:
            output_list = list(input_sequence)
        except TypeError:
            raise TypeError("Input must be a list, NumPy array, or list-like sequence.")


    # Check if the sequence is empty
    if not output_list:
        return np.array([]) # Return an empty NumPy array

    # Identify and remove the first element
    # Using pop(0) removes the element and returns it
    element_to_move = output_list.pop(0)

    # Append the removed element to the end
    output_list.append(element_to_move)

    # Return the modified sequence as a NumPy array (consistent output type)
    return np.array(output_list)

```
