```python
"""
Transforms an input sequence of digits (0, 1, 2) by sorting them according to a specific order: 
all '2's first, followed by all '0's, then all '1's. The counts of each digit are preserved 
from the input to the output.
"""

import collections

def transform(input_str: str) -> str:
    """
    Applies the 2 > 0 > 1 sorting rule to the input digit sequence.

    Args:
        input_str: A string containing space-separated digits (0, 1, or 2).

    Returns:
        A string containing the sorted digits, separated by spaces.
    """
    # 1. Read the input sequence of digits and convert them to integers.
    # Handle potential empty strings or invalid characters gracefully, although examples only show digits.
    try:
        input_digits = [int(digit) for digit in input_str.split()]
    except ValueError:
        # Handle cases where input might not be just digits and spaces
        # For this specific problem based on examples, assume valid input.
        # If needed, add more robust error handling.
        print("Warning: Input string contains non-digit characters.")
        input_digits = [int(digit) for digit in input_str.split() if digit.isdigit()]


    # 2. Determine the total count of '2's, '0's, and '1's.
    counts = collections.Counter(input_digits)
    count_2 = counts.get(2, 0)
    count_0 = counts.get(0, 0)
    count_1 = counts.get(1, 0)

    # 3. Create a new list for the output sequence.
    output_digits = []

    # 4. Append the digit '2' to the output sequence based on its count.
    output_digits.extend([2] * count_2)

    # 5. Append the digit '0' to the output sequence based on its count.
    output_digits.extend([0] * count_0)

    # 6. Append the digit '1' to the output sequence based on its count.
    output_digits.extend([1] * count_1)

    # 7. Format the output sequence with spaces between the digits.
    output_str = " ".join(map(str, output_digits))

    return output_str

```