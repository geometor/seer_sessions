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