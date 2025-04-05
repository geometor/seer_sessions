import copy

def transform(input_list):
    """
    Transforms the input list by filling the gaps between the first and last 
    occurrence of each non-zero digit with that digit.

    1. Start with the input sequence of numbers. Create a copy of this sequence 
       which will become the output sequence.
    2. Find all the unique non-zero numbers present in the input sequence.
    3. For each unique non-zero number identified (let's call it N):
        a. Find all the positions (indices) where N occurs in the original 
           input sequence.
        b. Check if N occurs more than once.
        c. If N occurs more than once:
            i. Determine the index of the first occurrence (first_index).
            ii. Determine the index of the last occurrence (last_index).
            iii. Iterate through all the positions in the *output* sequence 
                 starting from the position immediately after first_index 
                 up to (but not including) the position last_index.
            iv. Change the number at each of these positions in the *output* 
                sequence to N.
    4. After checking and potentially performing the fill operation for all 
       unique non-zero numbers, the final modified output sequence is the result.
    """

    # Helper function to find all indices of a given value
    def find_indices(data_list, value):
        """Finds all indices of a specific value in a list."""
        return [i for i, x in enumerate(data_list) if x == value]

    # 1. Initialize output_list as a copy of the input_list
    output_list = list(input_list) # Use list() for a shallow copy, sufficient here

    # 2. Find unique non-zero numbers in the input list
    non_zero_values = set(val for val in input_list if val != 0)

    # 3. Iterate through each unique non-zero number
    for number_to_fill in non_zero_values:
        # a. Find all indices where this number occurs in the *original* input
        indices = find_indices(input_list, number_to_fill)

        # b. Check if the number occurs more than once
        if len(indices) > 1:
            # c.i. Determine the first index
            first_index = min(indices)
            # c.ii. Determine the last index
            last_index = max(indices)

            # c.iii & c.iv Iterate and fill the gaps in the *output* list
            # Range goes from the element *after* the first occurrence
            # up to (but not including) the last occurrence.
            for i in range(first_index + 1, last_index):
                output_list[i] = number_to_fill

    # 4. Return the modified list
    return output_list