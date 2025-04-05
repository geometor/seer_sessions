import typing
from typing import List, Dict, Union, Optional

"""
Transforms a sequence of 0s and 3s based on contiguous groups of 3s, according to the following rules:

1.  Identifies contiguous groups of the number 3 in the input sequence. 0s act as separators and remain unchanged.
2.  Determines an initial transformation value (1 or 2) for the first group of 3s (G1).
    - If only one group exists, the value is 1.
    - If the first group (G1) is strictly longer than the second group (G2), the value is 1.
    - Otherwise (G1 is shorter or equal in length to G2), the value is 2.
3.  Assigns transformation values (1 or 2) to subsequent groups by strictly alternating from the initial value (1 becomes 2, 2 becomes 1).
4.  Constructs the output sequence by replacing the 3s within each identified group with its assigned transformation value, while keeping the original 0s.
"""

# Helper function to find groups of 3s
def find_groups_of_3(numbers: List[int]) -> List[Dict[str, int]]:
    """
    Finds contiguous groups of the number 3 in a list of numbers.

    Args:
        numbers: A list of integers (0s and 3s).

    Returns:
        A list of dictionaries, where each dictionary represents a group
        and contains 'start' (start index), 'end' (end index), and 'length'. 
        Returns an empty list if no groups of 3 are found.
    """
    groups = []
    in_group = False
    start_index = -1
    for i, num in enumerate(numbers):
        if num == 3 and not in_group:
            # Start of a new group
            in_group = True
            start_index = i
        elif num != 3 and in_group:
            # End of the current group
            groups.append({'start': start_index, 'end': i - 1, 'length': i - start_index})
            in_group = False
            start_index = -1
    # Handle case where the last group extends to the end of the list
    if in_group:
        groups.append({'start': start_index, 'end': len(numbers) - 1, 'length': len(numbers) - start_index})
    return groups

def transform(input_sequence: List[int]) -> List[int]:
    """
    Applies the transformation rule to the input sequence.

    Args:
        input_sequence: A list of integers containing only 0s and 3s.

    Returns:
        A list of integers containing the transformed sequence (0s, 1s, and 2s).
    """
    # 1. Initialize output sequence as a copy of the input sequence.
    output_sequence = list(input_sequence)

    # 2. Scan the input sequence to identify all contiguous groups of 3s.
    groups = find_groups_of_3(input_sequence)

    # 3. If no groups of 3s are found, return the original sequence.
    if not groups:
        return output_sequence

    # 4. Determine the initial transformation value (P1) for the first group (G1).
    initial_value = 1  # Default if only one group exists (Rule 4a)
    if len(groups) >= 2:
        # Compare lengths of the first (G1) and second (G2) groups (Rule 4b)
        if groups[0]['length'] <= groups[1]['length']:
             # If G1 is shorter or equal to G2, initial value is 2 (Rule 4b.iii)
            initial_value = 2
        # else: G1 is strictly longer than G2, initial value remains 1 (Rule 4b.ii)

    # 5. & 6. Assign alternating values and modify the output sequence.
    current_value = initial_value
    for group in groups:
        # 6b. Replace 3s in the output list within the group's range with the assigned value.
        for i in range(group['start'], group['end'] + 1):
            if output_sequence[i] == 3: # Ensure we only replace 3s
                 output_sequence[i] = current_value
        # 5. Alternate the value for the next group.
        current_value = 3 - current_value # Switches between 1 and 2 (3-1=2, 3-2=1)

    # 7. Return the modified output sequence.
    return output_sequence
