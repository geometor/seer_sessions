```python
import collections

"""
Transforms an input sequence of 12 integers (0, 1, or 2) by rearranging 
them such that all '2's appear first, followed by the necessary number of '0's
to maintain a total length of 12, and finally all '1's appear last. 
The counts of '1's and '2's from the input are preserved in the output.
"""

def transform(input_str: str) -> str:
    """
    Applies the transformation rule to the input string.

    Args:
        input_str: A string containing 12 space-separated integers (0, 1, or 2).

    Returns:
        A string containing 12 space-separated integers representing the transformed sequence.
    """
    # Parse the input string into a list of integers
    input_list = [int(x) for x in input_str.split()]
    total_length = 12 # The required length of the sequence

    # Count the occurrences of '2' and '1' in the input list
    counts = collections.Counter(input_list)
    num_twos = counts.get(2, 0)
    num_ones = counts.get(1, 0)

    # Calculate the number of '0's needed for the output list
    # The total length must be maintained
    num_zeros = total_length - num_twos - num_ones

    # Construct the output list
    # Place all '2's first
    output_list = [2] * num_twos
    # Then place the calculated number of '0's
    output_list.extend([0] * num_zeros)
    # Finally, place all '1's
    output_list.extend([1] * num_ones)

    # Convert the output list back to a space-separated string
    output_str = " ".join(map(str, output_list))

    return output_str

```