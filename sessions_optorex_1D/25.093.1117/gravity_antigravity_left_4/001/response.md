```python
import collections

def transform(input_sequence_str):
    """
    Sorts the input sequence of digits based on the custom order: 2 comes first, then 0, then 1.

    Args:
        input_sequence_str: A string representing the input sequence of digits separated by spaces.

    Returns:
        A string representing the sorted sequence of digits separated by spaces.
    """
    # Parse the input string into a list of integers
    input_sequence = [int(digit) for digit in input_sequence_str.split()]

    # Count the occurrences of each digit (0, 1, 2)
    counts = collections.Counter(input_sequence)
    count_0 = counts.get(0, 0)
    count_1 = counts.get(1, 0)
    count_2 = counts.get(2, 0)

    # Initialize an empty list for the output sequence
    output_sequence = []

    # Append '2's to the output sequence based on their count
    output_sequence.extend([2] * count_2)

    # Append '0's to the output sequence based on their count
    output_sequence.extend([0] * count_0)

    # Append '1's to the output sequence based on their count
    output_sequence.extend([1] * count_1)

    # Convert the output list back to a space-separated string
    output_sequence_str = " ".join(map(str, output_sequence))

    return output_sequence_str
```