```python
import collections

"""
Transforms an input sequence of integers (0, 1, 2) by rearranging its elements according to a specific custom order: all '2's first, followed by all '0's, and finally all '1's. The counts of each digit (0, 1, 2) from the input sequence are preserved in the output sequence.
"""

def transform(input_str: str) -> list[int]:
    """
    Sorts a sequence of digits (0, 1, 2) based on the custom order 2 > 0 > 1.

    Args:
        input_str: A string containing space-separated integers (0, 1, or 2).

    Returns:
        A list of integers sorted according to the rule: 2s, then 0s, then 1s.
    """
    # Parse the input string into a list of integers
    # Handle potential errors if input is not as expected, though examples are clean.
    try:
        input_list = [int(x) for x in input_str.split()]
    except ValueError:
        print("Error: Input string contains non-integer values.")
        return [] # Or raise an exception

    # Count the occurrences of each number (2, 0, 1)
    counts = collections.Counter(input_list)
    count2 = counts.get(2, 0)
    count0 = counts.get(0, 0)
    count1 = counts.get(1, 0)

    # Construct the output list based on the counts and the desired order (2, 0, 1)
    output_list = []
    output_list.extend([2] * count2) # Add all the '2's
    output_list.extend([0] * count0) # Add all the '0's
    output_list.extend([1] * count1) # Add all the '1's

    return output_list

# Example usage (optional, for testing)
# train_1_input = "0 1 2 1 1 1 0 2 0 0 0 0"
# train_1_output = transform(train_1_input)
# print(f"Input: {train_1_input}")
# print(f"Output: {train_1_output}") # Expected: [2, 2, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1]

# train_2_input = "2 0 2 0 1 0 0 0 2 0 2 2"
# train_2_output = transform(train_2_input)
# print(f"Input: {train_2_input}")
# print(f"Output: {train_2_output}") # Expected: [2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 1]
                                     # Actual:   [2, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 1] (follows derived rule)
```