import typing

"""
Reflects non-zero elements (excluding the pivot element '2') across the 
pivot's position within a sequence of integers represented as a 
space-separated string. The pivot element '2' remains fixed in its 
original position. Placeholder elements '0' fill any positions not 
occupied by the pivot or reflected elements.
"""

def _parse_input(input_str: str) -> typing.List[int]:
    """Converts the space-separated input string to a list of integers."""
    # Handles potential empty strings or extra spaces between numbers
    return [int(x) for x in input_str.split() if x]

def _format_output(data: typing.List[int]) -> str:
    """Converts the list of integers back to a space-separated string."""
    return " ".join(map(str, data))

def _find_pivot_index(data: typing.List[int], pivot_value: int = 2) -> int:
    """
    Finds the index of the first occurrence of the pivot element. 
    Raises ValueError if the pivot element is not found.
    """
    for i, val in enumerate(data):
        if val == pivot_value:
            return i
    raise ValueError(f"Pivot value {pivot_value} not found in input data.")

def transform(input_str: str) -> str:
    """
    Transforms the input sequence string by reflecting non-zero, non-pivot 
    elements across the position of the pivot element (2).

    Args:
        input_str: A string of space-separated single-digit integers.

    Returns:
        A string representing the transformed sequence, or the original 
        string if the pivot '2' is not found.
    """
    # Define constants for clarity
    pivot_value = 2
    placeholder_value = 0

    # --- Workflow ---

    # 1. Parse Input: Convert the input string into a list of integers.
    input_list = _parse_input(input_str)
    list_length = len(input_list)

    # Handle edge case: empty input list
    if list_length == 0:
        return ""

    # 2. Find Pivot: Locate the index of the pivot element '2'.
    try:
        pivot_index = _find_pivot_index(input_list, pivot_value)
    except ValueError:
        # If pivot is not found, as per ARC rules, often return input unchanged
        # or handle as specified by task constraints (which imply pivot exists here)
        # For robustness, we might log or return input. Let's return input.
        # print(f"Warning: Pivot value {pivot_value} not found in '{input_str}'. Returning original.")
        return input_str 

    # 3. Initialize Output: Create a new list filled with placeholders ('0').
    output_list = [placeholder_value] * list_length

    # 4. Place Pivot: Set the pivot element ('2') in the output list at its original position.
    # Basic bounds check, though pivot_index should be valid if found.
    if 0 <= pivot_index < list_length:
        output_list[pivot_index] = pivot_value
    else:
         # This case indicates an internal logic error if reached after successful find
         print(f"Error: Pivot index {pivot_index} out of bounds.")
         return input_str # Return original on internal error


    # 5. Reflect Movable Elements: Iterate through the input list.
    for i, element in enumerate(input_list):
        # a. Identify Movable Element: Check if it's not the pivot and not a placeholder.
        if element != pivot_value and element != placeholder_value:
            # b. Calculate Reflection Index: Use the formula: new_pos = 2 * pivot_pos - old_pos
            reflected_index = 2 * pivot_index - i

            # c. Place Reflected Element in Output: Only if the calculated index is valid (within bounds).
            if 0 <= reflected_index < list_length:
                # Optional: Check for collisions if the task allowed multiple elements
                # mapping to the same spot. Based on examples, this doesn't happen.
                output_list[reflected_index] = element
            # Else: Elements reflecting outside the bounds are implicitly dropped (remain '0').

    # 6. Format Output: Convert the resulting list back to a space-separated string.
    output_str = _format_output(output_list)

    return output_str