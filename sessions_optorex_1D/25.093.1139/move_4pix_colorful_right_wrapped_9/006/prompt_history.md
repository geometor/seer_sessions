
## train_1

**input:**
```
1 1 0 0 0 0 0 8 2 8 3 7
```


**output:**
```
2 8 3 7 1 1 0 0 0 0 0 8
```


## train_2

**input:**
```
0 0 0 9 8 2 7 1 3 0 0 0
```


**output:**
```
3 0 0 0 0 0 0 9 8 2 7 1
```


## train_3

**input:**
```
0 0 0 0 0 2 3 8 5 2 9 0
```


**output:**
```
5 2 9 0 0 0 0 0 0 2 3 8
```


## train_4

**input:**
```
0 0 0 9 4 7 7 6 1 0 0 0
```


**output:**
```
1 0 0 0 0 0 0 9 4 7 7 6
```


## train_5

**input:**
```
0 0 4 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 4 0 0 0 0 0
```


## train_6

**input:**
```
0 0 0 0 4 1 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 4 1 0 0
```


## train_7

**input:**
```
5 6 0 0 0 0 2 1 2 7 9 4
```


**output:**
```
2 7 9 4 5 6 0 0 0 0 2 1
```

*   **Perception:**
    *   The input and output are both sequences of 12 space-separated single digits.
    *   The transformation rearranges the elements of the input sequence to produce the output sequence.
    *   Observing the examples, it appears the sequence is split into two parts. The split occurs after the 8th element.
    *   The first part consists of the first 8 elements, and the second part consists of the last 4 elements.
    *   In the output, the order of these two parts is reversed: the last 4 elements from the input appear first, followed by the first 8 elements from the input.
    *   The internal order of elements within each part remains unchanged.

*   **Facts:**
    
```yaml
    task_type: sequence_manipulation
    input:
        type: list
        element_type: integer
        length: 12
    output:
        type: list
        element_type: integer
        length: 12
        relationship: rearrangement_of_input
    transformation:
        actions:
            - split:
                description: Divide the input list into two sub-lists.
                parameters:
                    - split_point: index 8 (after the 8th element)
                results:
                    - part_1: elements from index 0 to 7
                    - part_2: elements from index 8 to 11
            - concatenate:
                description: Combine the two sub-lists in a specific order.
                parameters:
                    - order: [part_2, part_1]
                result: output_list
    ```


*   **Natural Language Program:**
    1.  Take the input sequence of 12 numbers.
    2.  Divide the sequence into two parts: the first 8 numbers (Part 1) and the last 4 numbers (Part 2).
    3.  Construct the output sequence by placing Part 2 first, followed by Part 1.
    4.  Format the resulting sequence as space-separated digits.
```python
import math # not strictly needed for this task, but included as per template example

# Helper functions

def parse_input_string(input_str: str) -> list[int]:
    """Parses a space-separated string of digits into a list of integers."""
    return [int(digit) for digit in input_str.split()]

def format_output_list(output_list: list[int]) -> str:
    """Formats a list of integers into a space-separated string."""
    return " ".join(map(str, output_list))

# Main transformation function

def transform(input_str: str) -> str:
    """
    Takes a sequence of 12 space-separated digits, splits it into two parts
    (the first 8 digits and the last 4 digits), and returns a new sequence
    formed by concatenating the last 4 digits followed by the first 8 digits.
    """

    # Parse the input string into a list of numbers
    numbers = parse_input_string(input_str)

    # Define the split point
    split_index = 8

    # Check if the input list has the expected length (optional, for robustness)
    if len(numbers) != 12:
        # Handle error or unexpected input length if necessary
        # For this task, we assume valid input based on examples
        pass 

    # Split the list into two parts based on the split index
    part1 = numbers[:split_index] # First 8 elements
    part2 = numbers[split_index:] # Last 4 elements

    # Concatenate the parts in the reverse order: part2 then part1
    rearranged_list = part2 + part1

    # Format the rearranged list back into a space-separated string
    output_str = format_output_list(rearranged_list)

    return output_str

```
```python
"""
Transforms an input sequence (list or NumPy array) of 12 integers by splitting
it into two parts: the first 8 elements and the last 4 elements. It then
constructs and returns a new sequence (formatted as a space-separated string)
by concatenating the last 4 elements followed by the first 8 elements.
"""

import numpy as np # Import numpy, as the execution environment seems to use it

def format_output_list(output_list: list[int]) -> str:
    """Formats a list of integers into a space-separated string."""
    return " ".join(map(str, output_list))

def transform(input_sequence) -> str:
    """
    Applies the split-and-swap transformation to the input sequence.

    Args:
        input_sequence: A list or NumPy array containing 12 integers.

    Returns:
        A string representing the rearranged sequence, with elements separated
        by spaces.
    """

    # Ensure input is a list for consistent slicing (handles numpy arrays)
    if isinstance(input_sequence, np.ndarray):
        numbers = input_sequence.tolist()
    else:
        # Assume it's already list-like if not ndarray
        numbers = list(input_sequence) 

    # Define the split point (after the 8th element)
    split_index = 8

    # Check if the input list has the expected length (optional, for robustness)
    # if len(numbers) != 12:
        # Handle error or unexpected input length if necessary
        # Based on the problem description, we assume valid input length
        # pass

    # Split the list into two parts based on the split index
    part1 = numbers[:split_index] # First 8 elements (index 0 to 7)
    part2 = numbers[split_index:] # Last 4 elements (index 8 to 11)

    # Concatenate the parts in the reverse order: part2 then part1
    rearranged_list = part2 + part1

    # Format the rearranged list back into a space-separated string
    output_str = format_output_list(rearranged_list)

    return output_str
```
```python
"""
Transforms an input sequence (list or NumPy array) of 12 integers by splitting
it into two parts: the first 8 elements and the last 4 elements. It then
constructs and returns a new sequence (formatted as a space-separated string)
by concatenating the last 4 elements followed by the first 8 elements.
"""

import numpy as np # Import numpy as input might be an ndarray

def format_output_list(output_list) -> str:
    """Formats a list/array of items into a space-separated string."""
    # Ensure all elements are strings before joining
    return " ".join(map(str, output_list))

def transform(input_sequence):
    """
    Applies the split-and-swap transformation to the input sequence.

    Args:
        input_sequence: A list or NumPy array containing 12 integers.

    Returns:
        A string representing the rearranged sequence, with elements separated
        by spaces.
    """
    # Ensure input is treated as a list or sequence compatible with slicing
    # No explicit conversion needed if slicing works directly on input type
    numbers = input_sequence

    # Define the split point (after the 8th element)
    split_index = 8

    # Split the sequence into two parts using slicing
    # Part 1 contains elements from index 0 up to (but not including) split_index
    part1 = numbers[:split_index]
    # Part 2 contains elements from split_index to the end
    part2 = numbers[split_index:]

    # Concatenate the parts in the reverse order: part2 then part1
    # This works for lists and numpy arrays (though array concatenation might differ)
    # If input is guaranteed list or converted, simple list concatenation is fine.
    # If input could be np.array, np.concatenate might be safer, but + often works element-wise
    # Let's assume list concatenation is intended based on the logic. If input is np.array,
    # slicing might return views or copies, but list conversion ensures consistency.
    # Using list() ensures we are dealing with lists for concatenation.
    rearranged_list = list(part2) + list(part1)

    # Format the rearranged list back into a space-separated string
    output_str = format_output_list(rearranged_list)

    return output_str
```
