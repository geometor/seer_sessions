```python
"""
Rearrange elements in a 1D NumPy array, moving all zero elements to the beginning while preserving the relative order of non-zero elements, and return the result as a space-separated string.
"""

import numpy as np

# Helper function to partition elements based on a condition
def partition_elements(elements, condition_func):
    """Partitions elements into two lists based on a condition function."""
    true_list = []
    false_list = []
    for element in elements:
        if condition_func(element):
            true_list.append(element)
        else:
            false_list.append(element)
    return true_list, false_list

def transform(input_array: np.ndarray) -> str:
    """
    Moves all 0 elements to the beginning of a NumPy array while maintaining 
    the relative order of the non-zero elements, returning a space-separated string.

    Args:
        input_array: A 1-dimensional NumPy array of integers.

    Returns:
        A string with elements rearranged according to the rule, 
        space-separated.
    """
    
    # 1. Define the condition for partitioning (is the element zero?)
    is_zero = lambda x: x == 0

    # 2. Partition the input array elements into zeros and non-zeros
    #    The partition_elements helper preserves the relative order within each group.
    #    zeros_list will contain elements where condition is true (element == 0)
    #    non_zeros_list will contain elements where condition is false (element != 0)
    zeros_list, non_zeros_list = partition_elements(input_array, is_zero)

    # 3. Concatenate the lists: zeros first, then non-zeros.
    final_list = zeros_list + non_zeros_list

    # 4. Convert each integer element in the final list to its string representation.
    string_list = [str(num) for num in final_list]

    # 5. Join the list of strings with spaces.
    output_str = ' '.join(string_list)

    # 6. Return the final space-separated string.
    return output_str

```