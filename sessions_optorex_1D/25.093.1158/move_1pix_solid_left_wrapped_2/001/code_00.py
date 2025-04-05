import collections

"""
Performs a circular shift (rotation) of the input sequence one position to the left. 
The element at the first position moves to the last position.
All other elements shift one position forward (e.g., the element at index i moves to index i-1).
"""

def transform(input_str: str) -> str:
    """
    Applies a left circular rotation to a sequence represented as a space-separated string.

    Args:
        input_str: A string containing space-separated digits.

    Returns:
        A string representing the sequence after rotating it one position to the left.
    """
    # Parse the input string into a list of elements (strings)
    elements = input_str.split(' ')

    # Check if the list is empty or has only one element (rotation has no effect)
    if len(elements) <= 1:
        return input_str

    # Perform the left rotation using list slicing
    # Take elements from the second position to the end
    rotated_elements = elements[1:]
    # Append the first element to the end
    rotated_elements.append(elements[0])

    # Join the rotated elements back into a space-separated string
    output_str = ' '.join(rotated_elements)

    return output_str
