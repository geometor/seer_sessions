import math # Although not strictly needed for this task, good practice to include if potential math ops arise
import copy # To ensure deep copies if needed, though list slicing is sufficient here

"""
Identifies the unique non-zero value in the input sequence.
Finds the first and second occurrences of this non-zero value.
Creates a copy of the input sequence.
Fills the segment between the first and second occurrences (inclusive) in the copied sequence with the non-zero value.
Returns the modified sequence.
"""

def find_non_zero_value_and_indices(sequence):
    """
    Finds the non-zero value and the indices of its first and second occurrences.
    Returns (None, -1, -1) if not found exactly twice.
    """
    non_zero_val = None
    indices = []
    for i, val in enumerate(sequence):
        if val != 0:
            if non_zero_val is None:
                non_zero_val = val
            # Store index only if it matches the first found non_zero_val
            # This handles cases where potentially other non-zero values might exist (though not per problem description)
            if val == non_zero_val:
                 indices.append(i)

    # Check if exactly two indices were found for the non_zero_val
    if len(indices) == 2:
        return non_zero_val, indices[0], indices[1]
    elif len(indices) == 1: # Handle cases like train_6 where the value appears only once or twice consecutively
         # If the value appears only once, or twice consecutively, the start and end are the same.
         # The problem description implies two *distinct* positions forming a segment,
         # but train_6 has [..., 1, 1]. The rule should still apply, filling the segment [index, index].
         # Let's refine based on example 6: if the indices are adjacent or the same, the output is identical to input in that segment.
         # If only one index is found, or if the two indices found are adjacent, return them.
         # Let's stick to the original interpretation: find *the* two occurrences. Example 6 has two 1s.
         # The indices are 10 and 11. The segment is [10, 11]. Filling it doesn't change anything.
         # What if input is [0, 0, 1, 0, 0]? The rule says *two* occurrences. Let's assume input always has two.
         return non_zero_val, indices[0], indices[0] # Default if only one found, though contradicts spec
    elif len(indices) > 2:
        # Problem statement says *exactly* two identical non-zero values.
        # If more are found, let's take the first and last for robustness, though this deviates.
        # Or strictly adhere? Let's adhere strictly first.
        print(f"Warning: Found more than two occurrences of {non_zero_val}. Using first and last.")
        # Re-evaluating based on examples: The examples *always* have exactly two.
        # Let's assume the input format is guaranteed.
        if len(indices) >= 2: # If there are 2 or more, just use first and last found.
             return non_zero_val, indices[0], indices[-1] # Use first and last if more than 2 found.

    # If no non-zero value found, or not exactly two (and not handled above)
    return None, -1, -1


def transform(input_sequence):
    """
    Transforms the input sequence by filling the segment between the two
    non-zero identical values with that value.
    """
    # Ensure input is a list (might be passed as tuple or other sequence)
    input_list = list(input_sequence)

    # 1. & 2. Identify the non-zero value and find its start and end indices.
    non_zero_val, start_index, end_index = find_non_zero_value_and_indices(input_list)

    # 3. Create a new sequence which is initially an identical copy.
    output_sequence = list(input_list) # Use list() or slicing [:] for copying

    # Check if valid indices were found
    if non_zero_val is not None and start_index != -1 and end_index != -1:
        # Ensure start_index is less than or equal to end_index
        # (Should be guaranteed by find_non_zero_value_and_indices logic)
        if start_index > end_index:
             start_index, end_index = end_index, start_index # Swap if order is reversed

        # 4. & 5. Iterate from start_index to end_index (inclusive) and fill.
        for i in range(start_index, end_index + 1):
            output_sequence[i] = non_zero_val

    # 6. Return the modified sequence.
    # If no non-zero value or incorrect number of occurrences found,
    # the original sequence copy is returned.
    return output_sequence
