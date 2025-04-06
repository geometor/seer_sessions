```python
"""
Examine the input 3x3 grid of digits. Count the occurrences of each unique digit 
(0 through 9) present in the input grid. Identify the digit that has the highest 
frequency (the mode). Construct a new 3x3 grid where every cell is filled with 
this most frequent digit. Output the newly constructed grid.
"""

from collections import Counter
import itertools

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Transforms an input grid by finding the most frequent digit within it 
    and creating a new grid of the same dimensions filled entirely with that digit.
    """
    
    # Determine the dimensions of the input grid
    rows = len(input_grid)
    if rows == 0:
        return [] # Handle empty input grid
    cols = len(input_grid[0])
    if cols == 0:
        return [[] for _ in range(rows)] # Handle grid with empty rows

    # Flatten the input grid into a single list of numbers
    all_digits = list(itertools.chain.from_iterable(input_grid))

    # Count the frequency of each digit
    digit_counts = Counter(all_digits)

    # Find the digit with the highest frequency (the mode)
    # If there's a tie, most_common(1) picks one of them arbitrarily.
    if not digit_counts:
         # Handle case where grid was non-empty but contained no digits 
         # (e.g., list of empty lists, though input constraints likely prevent this)
         # Or if all cells were non-digits (if input type wasn't guaranteed)
         # For this specific problem (single digits 0-9), this edge case might
         # not occur with valid inputs, but handling it defensively.
         # Let's assume a default or raise an error? Given the problem context,
         # maybe default to 0 or the smallest digit present if any?
         # Sticking to the prompt's logic, find the mode. If no digits, what's the mode?
         # Let's assume valid inputs per problem description, so a mode will exist.
         pass # No need for specific handling if inputs are guaranteed valid

    most_frequent_digit, _ = digit_counts.most_common(1)[0]

    # Initialize the output grid with the determined dimensions
    output_grid = [[0 for _ in range(cols)] for _ in range(rows)]

    # Fill the output grid with the most frequent digit
    for r in range(rows):
        for c in range(cols):
            output_grid[r][c] = most_frequent_digit

    return output_grid

```