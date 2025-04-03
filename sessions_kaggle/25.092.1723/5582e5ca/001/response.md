```python
import collections

"""
Transforms a 3x3 input grid of digits into a 3x3 output grid where every cell 
is filled with the digit that appears most frequently (the mode) in the input grid.
"""

def transform(input_grid):
    """
    Args:
        input_grid (list[list[int]]): A 3x3 grid represented as a list of lists 
                                       containing single-digit integers (0-9).

    Returns:
        list[list[int]]: A 3x3 grid where all cells contain the most frequent 
                         digit from the input grid.
    """
    
    # Flatten the input grid into a single list of digits
    all_digits = [digit for row in input_grid for digit in row]
    
    # Calculate the frequency of each digit (0-9)
    # Using collections.Counter is efficient for this
    digit_counts = collections.Counter(all_digits)
    
    # Find the digit with the highest frequency (the mode)
    # The most_common(1) method returns a list with one tuple: [(mode, count)]
    # Handle the case where the input grid might be empty or have no mode (though unlikely for 3x3)
    if not digit_counts:
        # Decide on default behavior, e.g., return a grid of 0s or raise error
        # For this task structure, assume valid input, but conceptually:
        most_frequent_digit = 0 # Or some other default
    else:
        # Find the mode. If there are ties, most_common might return any one of them.
        # To handle ties deterministically (e.g., pick smallest digit), more logic would be needed.
        # Based on examples, assuming a unique mode or any mode is acceptable.
        most_frequent_digit = digit_counts.most_common(1)[0][0]

    # Get the dimensions of the input grid (assuming it's always 3x3 as per examples)
    rows = len(input_grid)
    cols = len(input_grid[0]) if rows > 0 else 0
    
    # Initialize the output grid
    output_grid = [[0 for _ in range(cols)] for _ in range(rows)]

    # Fill the output grid with the most frequent digit
    for r in range(rows):
        for c in range(cols):
            output_grid[r][c] = most_frequent_digit

    return output_grid

```