```python
"""
Examine the input 3x3 grid. Select a single digit from the input grid according to the following rule: The most frequent one. If there are more than one, choose the largest number. Create a new 3x3 grid. Fill all cells of the new grid with the selected digit. Output the new grid.
"""

import numpy as np
from collections import Counter

def select_digit(input_grid):
    # Flatten the grid to a list
    flat_list = input_grid.flatten().tolist()
    # Count the occurrences of each digit
    counts = Counter(flat_list)
    # Find the most common digits
    max_count = max(counts.values())
    most_common_digits = [digit for digit, count in counts.items() if count == max_count]
    # If there's a tie, select the largest digit
    selected_digit = max(most_common_digits)
    return selected_digit

def transform(input_grid):
    # Convert input to numpy array
    input_grid = np.array(input_grid)
    
    # Select the digit to use for the output
    selected_digit = select_digit(input_grid)

    # Create a new 3x3 grid filled with the selected digit
    output_grid = np.full((3, 3), selected_digit)

    return output_grid.tolist()
```