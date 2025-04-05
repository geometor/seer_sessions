import copy

"""
Transforms an input sequence of integers by moving the last element to the position 
of the first non-zero element found in the sequence. If all elements are zero, 
the last element (which is 0) is effectively inserted at index 0, resulting in no change.

1. Take the input sequence of integers.
2. Identify the value of the last element in the sequence.
3. Find the index of the first element in the sequence (scanning from left to right, 
   starting at index 0) that has a value other than zero.
4. If no non-zero element is found (i.e., the sequence consists entirely of zeros), 
   use index 0 as the target index. Otherwise, use the index found in step 3.
5. Remove the last element from the sequence.
6. Insert the identified last element's value into the sequence at the target index 
   determined in step 4.
7. The resulting sequence is the output.
"""

def find_first_non_zero_index(sequence):
    """
    Finds the index of the first non-zero element in a sequence.

    Args:
        sequence: A list of numbers.

    Returns:
        The index of the first non-zero element, or 0 if all elements are zero.
    """
    for index, value in enumerate(sequence):
        if value != 0:
            return index
    # If no non-zero element is found, return 0
    return 0

def transform(input_sequence):
    """
    Applies the transformation rule to the input sequence.

    Args:
        input_sequence: A list of integers.

    Returns:
        A new list of integers representing the transformed sequence.
    """
    # Create a mutable copy of the input sequence
    output_sequence = list(input_sequence)

    # Handle empty or single-element lists gracefully (no change)
    if len(output_sequence) < 2:
        return output_sequence

    # 1. Identify the value of the last element
    last_element_value = output_sequence[-1]

    # 2. Find the index of the first non-zero element *before* removing the last element
    #    (The logic assumes we find the index in the *original* sequence context)
    insertion_index = find_first_non_zero_index(output_sequence)

    # 3. Remove the last element from the sequence
    del output_sequence[-1]

    # 4. Insert the identified last element's value at the target index
    output_sequence.insert(insertion_index, last_element_value)

    # 5. Return the resulting sequence
    return output_sequence