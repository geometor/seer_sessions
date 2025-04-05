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
