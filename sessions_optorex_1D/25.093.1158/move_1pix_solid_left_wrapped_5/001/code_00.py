import collections

"""
Transforms a sequence of integers based on specific conditions related to the count of zeros and unique non-zero elements.

1. Parses the input string into a list of integers.
2. Counts the occurrences of zero and the number of unique non-zero elements.
3. Determines the index of the element to move:
   - Defaults to index 0.
   - If there is exactly one unique non-zero element AND exactly two zeros, the index becomes the position immediately before the first zero.
4. Removes the element at the determined index.
5. Appends the removed element to the end of the sequence.
6. Formats the modified sequence back into a space-separated string.
"""

def transform(input_string: str) -> str:
    """
    Applies the transformation rule to the input sequence string.

    Args:
        input_string: A space-separated string of integers.

    Returns:
        A space-separated string of integers representing the transformed sequence.
    """
    # 1. Receive the `input_sequence` of integers (parse from string)
    input_list = [int(x) for x in input_string.split()]
    output_list = list(input_list) # Work on a copy

    if not output_list:
        return "" # Handle empty input

    # 2. Calculate the `count_of_unique_non_zeros`
    unique_non_zeros = {x for x in output_list if x != 0}
    count_of_unique_non_zeros = len(unique_non_zeros)

    # 3. Calculate the `count_of_zeros`
    counts = collections.Counter(output_list)
    count_of_zeros = counts[0]

    # 4. Initialize `index_to_move` to 0.
    index_to_move = 0

    # 5. Check if `count_of_unique_non_zeros` is exactly 1 AND `count_of_zeros` is exactly 2.
    if count_of_unique_non_zeros == 1 and count_of_zeros == 2:
        # 6a. Find the `index_of_first_zero`
        try:
            index_of_first_zero = output_list.index(0)
            # 6b. Set `index_to_move` if the first zero is not at the beginning
            if index_of_first_zero > 0:
                 index_to_move = index_of_first_zero - 1
            # If index_of_first_zero is 0, the default index_to_move=0 is used.
        except ValueError:
            # This case shouldn't happen if count_of_zeros == 2, but handle defensively
            pass 

    # 7. Identify the `element_to_move` (will be done during removal)
    # 8. Create a new sequence by removing the element at `index_to_move`
    # 9. Append the `element_to_move` to the end of the new sequence.
    if 0 <= index_to_move < len(output_list):
        element_to_move = output_list.pop(index_to_move)
        output_list.append(element_to_move)
    # else: handle potential index out of bounds if logic were different,
    # but current logic ensures index_to_move is valid or 0 for non-empty lists.


    # 10. Return the modified sequence as the `output_sequence` (formatted as string)
    return " ".join(map(str, output_list))
