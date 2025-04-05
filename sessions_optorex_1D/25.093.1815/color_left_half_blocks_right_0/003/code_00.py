import math # Included for potential future use, though not strictly needed for this logic.

"""
Transforms an input list of 0s and 2s into an output list of 0s, 2s, and 8s.
Zeros remain unchanged.
Groups of consecutive 2s are transformed based on their length:
- The first 2 of any group becomes 8.
- The second 2 becomes 8 only if the group length is 4 or more; otherwise, it remains 2.
- All subsequent 2s (third, fourth, etc.) in the group remain 2.
"""

def find_group_end(input_list, start_index):
    """
    Finds the index immediately after the end of a consecutive group of 2s
    starting at start_index.

    Args:
        input_list: The list being scanned.
        start_index: The index where the group of 2s begins.

    Returns:
        The index immediately following the last 2 in the consecutive group.
    """
    current_index = start_index
    while current_index < len(input_list) and input_list[current_index] == 2:
        current_index += 1
    return current_index

def transform(input_list):
    """
    Applies the transformation rule to the input list.

    Args:
        input_list: A list of integers containing only 0s and 2s.

    Returns:
        A new list of integers containing 0s, 2s, and 8s based on the transformation rules.
    """
    # Initialize the output list
    output_list = []
    i = 0
    n = len(input_list)

    # Iterate through the input list
    while i < n:
        current_element = input_list[i]

        # Handle 0s: they remain unchanged
        if current_element == 0:
            output_list.append(0)
            i += 1 # Move to the next element

        # Handle 2s: identify the group and apply transformation rules
        elif current_element == 2:
            # Record the start index of the group
            group_start_index = i
            # Find the end index (exclusive) and calculate the length of the group
            group_end_index = find_group_end(input_list, i)
            group_length = group_end_index - group_start_index

            # Process the first element of the group (always becomes 8)
            output_list.append(8)

            # Process the second element of the group (if it exists)
            if group_length >= 2:
                # Apply the rule: second element is 8 only if group length is >= 4
                if group_length >= 4:
                    output_list.append(8)
                else:
                    output_list.append(2)

            # Process the remaining elements of the group (third onwards, always remain 2)
            # Start loop from k=2 because the first two elements (k=0 and k=1 relative to group start) are handled
            for k in range(2, group_length):
                output_list.append(2)

            # Move the main index past the processed group
            i = group_end_index

        # Optional: Handle unexpected values if the input contract (only 0s and 2s) might be violated
        # else:
        #     output_list.append(current_element) # Or raise an error
        #     i += 1

    # Return the fully transformed list
    return output_list