"""
Transforms an input list of 5 integers by sorting the first two elements
ascendingly, keeping the middle element unchanged, sorting the last two
elements descendingly, and concatenating the results.
"""

from typing import List

def transform(input_list: List[int]) -> List[int]:
    """
    Applies a specific reordering transformation to a list of 5 integers.

    Args:
        input_list: A list containing 5 integers.

    Returns:
        A new list with elements reordered according to the rule:
        - First two elements sorted ascendingly.
        - Middle element unchanged.
        - Last two elements sorted descendingly.
    """

    # Ensure the input list has the expected length (based on examples)
    if len(input_list) != 5:
        # Handle error or unexpected input length appropriately
        # For now, we'll assume valid input based on training data
        # In a real scenario, raising an error might be better.
        print(f"Warning: Input list length is {len(input_list)}, expected 5.")
        # Attempt to process anyway if possible, or return input/empty/error
        # For this specific rule, it breaks if not length 5.
        # Let's return the input list as a fallback, though this might not be ideal.
        return input_list # Or raise ValueError("Input list must have length 5")


    # 1. Isolate the first pair of elements (index 0 and 1)
    first_pair = input_list[0:2]

    # 2. Sort the first pair in ascending order
    sorted_first_pair = sorted(first_pair)

    # 3. Isolate the middle element (index 2)
    middle_element = input_list[2] # Keep as a single element

    # 4. Isolate the last pair of elements (index 3 and 4)
    last_pair = input_list[3:5]

    # 5. Sort the last pair in descending order
    sorted_last_pair = sorted(last_pair, reverse=True)

    # 6. Construct the output list by concatenating the parts
    # Note: middle_element needs to be wrapped in a list for concatenation
    output_list = sorted_first_pair + [middle_element] + sorted_last_pair

    # 7. Return the constructed list
    return output_list

# Example Usage (based on train_1)
# input_1 = [9, 0, 1, 6, 8]
# output_1 = transform(input_1)
# print(f"Input: {input_1}")
# print(f"Output: {output_1}") # Expected: [0, 9, 1, 8, 6]

# Example Usage (based on train_2)
# input_2 = [4, 3, 6, 2, 8]
# output_2 = transform(input_2)
# print(f"Input: {input_2}")
# print(f"Output: {output_2}") # Expected: [3, 4, 6, 8, 2]