```python
"""
Takes an input string of space-separated digits (0, 1, or 2), 
parses these digits, sorts them in descending order (2s, then 1s, then 0s), 
and returns the sorted digits as a new space-separated string.
"""

# No external libraries are needed for this simple sorting task.

def transform(input_str: str) -> str:
    """
    Sorts the digits in the input string in descending order.

    Args:
        input_str: A string containing space-separated digits (0, 1, or 2).

    Returns:
        A string containing the same digits sorted in descending order, 
        separated by spaces.
    """
    # 1. Split the input string into individual digit strings
    digit_strings = input_str.split()

    # 2. Convert the digit strings into a list of integers
    #    (Using integers makes sorting straightforward)
    digits = [int(d) for d in digit_strings]

    # 3. Sort the list of digits in descending order
    #    The 'reverse=True' argument achieves descending sort.
    digits.sort(reverse=True)

    # 4. Convert the sorted integers back into strings
    sorted_digit_strings = [str(d) for d in digits]

    # 5. Join the sorted digit strings back into a single space-separated string
    output_str = " ".join(sorted_digit_strings)

    # 6. Return the result
    return output_str

```