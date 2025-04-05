import collections

"""
Transforms an input list of 12 digits by shifting the positions of all '0' elements two steps to the left (with wrap-around) 
and filling the remaining positions with the non-zero elements from the input list, preserving their original relative order.
"""

def transform(input_list_str: str) -> str:
    """
    Applies the described transformation to the input list string.

    Args:
        input_list_str: A string representing the input list of 12 digits, space-separated.

    Returns:
        A string representing the transformed list of 12 digits, space-separated.
    """
    # Parse the input string into a list of integers
    input_list = [int(x) for x in input_list_str.split()]
    list_length = 12

    # Initialize the output list with placeholders (e.g., None)
    output_list = [None] * list_length

    # Store non-zero elements in their original order
    non_zero_elements = []
    # Store the target indices for the zero elements
    zero_target_indices = []

    # First pass: Identify non-zero elements and calculate target indices for zeros
    for i, element in enumerate(input_list):
        if element == 0:
            # Calculate the target index for the zero, shifting left by 2 with wrap-around
            target_index = (i - 2) % list_length
            zero_target_indices.append(target_index)
        else:
            # Collect non-zero elements
            non_zero_elements.append(element)

    # Second pass: Place the zeros in their calculated target positions in the output list
    for index in zero_target_indices:
        output_list[index] = 0

    # Third pass: Fill the remaining placeholder positions with the non-zero elements
    non_zero_iter = iter(non_zero_elements) # Use an iterator for sequential filling
    for i in range(list_length):
        if output_list[i] is None: # If the position is not filled by a zero
            try:
                output_list[i] = next(non_zero_iter)
            except StopIteration:
                # This should not happen if the input length and logic are correct
                print("Error: Ran out of non-zero elements unexpectedly.")
                break # Or handle error appropriately

    # Convert the output list back to a space-separated string
    output_str = " ".join(map(str, output_list))
    return output_str
