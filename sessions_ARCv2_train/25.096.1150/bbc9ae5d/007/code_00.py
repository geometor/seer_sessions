"""
Transforms an input list of integers according to the following rule:
1. The first line of the output represents the initial input list, formatted as a space-separated string.
2. Subsequent lines are generated iteratively by replacing the leftmost '0' in the current list state with the value of the first element of the original input list.
3. The number of replacement steps (R) performed is calculated as R = (L + 2) // 3 (integer division, equivalent to ceil(L / 3)), where L is the length of the input list.
4. The total number of output lines is R + 1. The process stops after R replacements or when no more zeros are found.
5. The final output is a single string containing all generated sequence states, each on a new line.
"""

from typing import List, Optional

# Helper function to format a list into a space-separated string
def format_list_to_string(int_list: List[int]) -> str:
  """Formats a list of integers into a space-separated string."""
  return " ".join(map(str, int_list))

# Helper function to find the index of the first zero
def find_first_zero_index(int_list: List[int]) -> Optional[int]:
  """Finds the index of the first zero in the list. Returns None if not found."""
  try:
    return int_list.index(0)
  except ValueError:
    return None

def transform(input_sequence: List[int]) -> str:
    """
    Applies the iterative zero-replacement transformation to the input list.

    Args:
      input_sequence: A list of integers.

    Returns:
      A string containing the initial state and subsequent states after each
      replacement step, separated by newlines.
    """

    # 1. Determine the total length L
    L = len(input_sequence)
    if L == 0:
        return "" # Handle empty input case

    # 2. Calculate the number of replacement steps R
    R = (L + 2) // 3 # Integer division equivalent to ceil(L/3)

    # 3. Identify the fill_digit (first element)
    fill_digit = input_sequence[0]

    # 4. Initialize a list to store the output sequences (as lists of integers)
    output_states = []

    # 5. Create a working copy of the initial sequence
    current_sequence = list(input_sequence)

    # 6. Add the initial sequence state to the output list (store a copy)
    output_states.append(list(current_sequence))

    # 7. Repeat the replacement R times
    for _ in range(R):
        # a. Find the index of the first occurrence of 0
        index_zero = find_first_zero_index(current_sequence)

        # b. If a 0 is found
        if index_zero is not None:
            # i. Update the element at index_zero *in the current working list*
            current_sequence[index_zero] = fill_digit
            # ii. Add a *copy* of the modified sequence state to the output list
            output_states.append(list(current_sequence))
        else:
            # c. If no 0 is found, stop the loop (all fillable zeros filled)
            break

    # 8. Convert each sequence list in the output list into a space-separated string
    output_lines = [format_list_to_string(seq) for seq in output_states]

    # 9. Join these formatted strings with newline characters
    output_string = "\n".join(output_lines)

    # 10. Return the final output string
    return output_string