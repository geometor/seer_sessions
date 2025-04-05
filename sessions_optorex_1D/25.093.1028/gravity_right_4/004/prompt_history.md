
## train_1

**input:**
```
0 5 0 0 0 8 9 0 0 0 4 0
```


**output:**
```
0 0 0 0 0 0 0 0 5 8 9 4
```


## train_2

**input:**
```
9 3 8 7 3 2 1 0 0 0 0 4
```


**output:**
```
0 0 0 0 9 3 8 7 3 2 1 4
```


## train_3

**input:**
```
0 0 0 8 3 0 1 3 0 0 3 0
```


**output:**
```
0 0 0 0 0 0 0 8 3 1 3 3
```


## train_4

**input:**
```
4 3 0 7 6 7 0 1 0 0 0 2
```


**output:**
```
0 0 0 0 0 4 3 7 6 7 1 2
```


## train_5

**input:**
```
0 3 6 0 3 8 0 0 1 8 0 0
```


**output:**
```
0 0 0 0 0 0 3 6 3 8 1 8
```


## train_6

**input:**
```
0 0 0 0 0 5 0 0 5 2 0 5
```


**output:**
```
0 0 0 0 0 0 0 0 5 5 2 5
```


## train_7

**input:**
```
0 0 9 5 0 4 3 0 0 2 8 9
```


**output:**
```
0 0 0 0 0 9 5 4 3 2 8 9
```

**Perception of Task Elements:**

The task involves rearranging a sequence of integers. The input consists of a list of integers, containing both zeros and non-zero values. The output is a list of the same length, where all the zero elements from the input are moved to the beginning of the list, and all the non-zero elements are moved to the end, preserving their original relative order.

**Facts:**


```yaml
Input:
  type: sequence
  elements: integers
  properties:
    - contains zeros
    - contains non-zero integers
    - fixed length (e.g., 12 in examples)

Output:
  type: sequence
  elements: integers
  properties:
    - same length as input
    - same multiset of elements as input (same numbers, same counts)
    - structured arrangement

Transformation:
  action: rearrange elements
  rule: partition based on value (zero vs. non-zero)
  constraints:
    - relative order of non-zero elements is preserved
    - all zeros are grouped together at the beginning
    - all non-zeros are grouped together at the end

Relationships:
  - Input element maps to an output element.
  - The position of an element in the output depends on its value (zero or non-zero) and its original position relative to other non-zero elements.
  - The count of zeros in the input equals the count of leading zeros in the output.
  - The sequence of non-zero elements in the input is identical to the sequence of trailing non-zero elements in the output.
```


**Natural Language Program:**

1.  Accept an input sequence of integers.
2.  Create a new, empty sequence to store the non-zero elements, maintaining their original relative order.
3.  Initialize a counter for the number of zero elements to zero.
4.  Iterate through the input sequence:
    a.  If the current element is zero, increment the zero counter.
    b.  If the current element is non-zero, append it to the sequence of non-zero elements.
5.  Construct the final output sequence:
    a.  Start with a sequence consisting of the counted number of zeros.
    b.  Append the sequence of collected non-zero elements to the end of the zero sequence.
6.  Return the constructed output sequence.
```python
import numpy as np  # numpy is commonly used, though not strictly required for this specific logic

"""
Rearranges a sequence of integers by moving all zero elements to the beginning 
of the sequence while preserving the relative order of the non-zero elements.
"""

def transform(input_list: list[int]) -> list[int]:
    """
    Moves all zero elements to the front of a list of integers, 
    preserving the relative order of non-zero elements.

    Args:
        input_list: A list of integers.

    Returns:
        A new list with zeros moved to the front.
    """

    # 1. Initialize lists to store zeros and non-zeros
    zeros = []
    non_zeros = []

    # 2. Iterate through the input sequence
    for element in input_list:
        # 3a. If the element is zero, add it to the zeros list (or just count it)
        if element == 0:
            zeros.append(0) 
        # 3b. If the element is non-zero, append it to the non-zeros list
        else:
            non_zeros.append(element)

    # 4. Construct the final output sequence by concatenating zeros and non_zeros
    output_list = zeros + non_zeros

    # 5. Return the constructed output sequence
    return output_list

# Example usage (demonstration, not part of the required function structure):
# input_str_1 = "0 5 0 0 0 8 9 0 0 0 4 0"
# input_list_1 = [int(x) for x in input_str_1.split()]
# output_list_1 = transform(input_list_1)
# print(f"Input 1: {input_list_1}")
# print(f"Output 1: {output_list_1}") # Expected: [0, 0, 0, 0, 0, 0, 0, 0, 5, 8, 9, 4]

# input_str_2 = "9 3 8 7 3 2 1 0 0 0 0 4"
# input_list_2 = [int(x) for x in input_str_2.split()]
# output_list_2 = transform(input_list_2)
# print(f"Input 2: {input_list_2}")
# print(f"Output 2: {output_list_2}") # Expected: [0, 0, 0, 0, 9, 3, 8, 7, 3, 2, 1, 4]
```
```python
import numpy as np  # Import numpy, anticipating potential array inputs

"""
Rearranges a sequence of integers by moving all zero elements to the beginning 
of the sequence while preserving the relative order of the non-zero elements.
"""

def get_zeros(sequence):
  """Extracts all zero elements from the sequence."""
  return [element for element in sequence if element == 0]

def get_non_zeros(sequence):
  """Extracts all non-zero elements from the sequence, preserving relative order."""
  return [element for element in sequence if element != 0]

def transform(input_sequence: list[int] | np.ndarray) -> list[int]:
    """
    Moves all zero elements to the front of a sequence (list or 1D NumPy array) 
    of integers, preserving the relative order of non-zero elements.

    Args:
        input_sequence: A list or 1D NumPy array of integers.

    Returns:
        A new list with zeros moved to the front.
    """
    
    # 1. Extract all zero elements from the input sequence.
    #    The number of zeros determines the length of the leading zero block.
    zeros_list = get_zeros(input_sequence)
    
    # 2. Extract all non-zero elements, maintaining their original relative order.
    #    This sequence will form the trailing block in the output.
    non_zeros_list = get_non_zeros(input_sequence)
    
    # 3. Concatenate the list of zeros and the list of non-zeros.
    #    The zeros come first, followed by the non-zeros in their preserved order.
    output_sequence = zeros_list + non_zeros_list
    
    # 4. Return the resulting rearranged sequence.
    return output_sequence

```
