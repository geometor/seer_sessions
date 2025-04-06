import numpy as np
from collections import Counter
# No other standard libraries seem necessary based on the logic

"""
Transform a 9x9 input grid into a 3x3 output grid by analyzing 3x3 subgrids.
For each 3x3 subgrid:
1. Count the frequency of each non-zero digit.
2. Find the non-zero digit(s) with the highest frequency.
3. If the digit '5' is present and its frequency is greater than or equal to the frequency of any other single most frequent non-zero digit, the output for that subgrid is 0.
4. Otherwise, the output is the most frequent non-zero digit. If there's a tie for the most frequent non-zero digit (and '5' doesn't override), the smallest of the tied digits is chosen.
5. If a subgrid contains only zeros, the output is 0.
"""

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Transforms a 9x9 grid to a 3x3 grid based on subgrid analysis.

    Args:
        input_grid: A 9x9 list of lists containing integers (0-9).

    Returns:
        A 3x3 list of lists representing the transformed grid.
    """
    # Convert input list of lists to a NumPy array for efficient slicing
    input_np = np.array(input_grid, dtype=int)
    
    # Initialize the 3x3 output grid with zeros (default value)
    output_grid = np.zeros((3, 3), dtype=int)

    # Iterate through the 3x3 subgrids using block indices
    for R in range(3):  # Block row index (0, 1, 2)
        for C in range(3):  # Block column index (0, 1, 2)
            
            # Extract the corresponding 3x3 subgrid
            # Rows from R*3 to R*3 + 3, Columns from C*3 to C*3 + 3
            subgrid = input_np[R*3:(R+1)*3, C*3:(C+1)*3]
            
            # Flatten the subgrid into a 1D list and filter out zero values
            non_zero_elements = [val for val in subgrid.flatten() if val != 0]

            # --- Determine the output value for the cell (R, C) ---
            
            # Case 1: Subgrid contains only zeros (or is empty)
            if not non_zero_elements:
                output_value = 0 
            else:
                # Case 2: Subgrid contains non-zero elements
                # Count frequencies of each non-zero digit
                counts = Counter(non_zero_elements)
                
                # Get frequency of digit 5 (important for the special rule)
                freq_5 = counts.get(5, 0) # Returns 0 if 5 is not in counts
                
                # Find the maximum frequency among all non-zero digits present
                max_freq = 0
                if counts: # Check if counts is not empty
                   max_freq = max(counts.values())
                   
                # Find all digits that have this maximum frequency
                most_frequent_digits = [digit for digit, freq in counts.items() if freq == max_freq]

                # Apply the transformation rules:
                # Rule A: If 5 is present AND its frequency is >= the max frequency, output is 0
                if freq_5 > 0 and freq_5 >= max_freq:
                    output_value = 0
                # Rule B: Otherwise, output is the smallest of the most frequent digits
                else:
                    # This handles ties by selecting the minimum value digit
                    output_value = min(most_frequent_digits) if most_frequent_digits else 0 # Default to 0 if list somehow empty

            # Assign the calculated value to the corresponding cell in the output grid
            output_grid[R, C] = output_value

    # Convert the NumPy output grid back to a standard list of lists format
    return output_grid.tolist()
