"""
The output is the digit that appears most frequently as the *first* digit across all *rows*. 
If two digits appear the first number of times in different rows with the equal amount, 
examine the second digits across all rows and output the most frequent digit. 
If a tie remains, move to check the third digits, and so on.
"""

from collections import Counter

def transform(input_grid):
    # initialize output
    output = None

    # Iterate through column indices
    for col_index in range(len(input_grid[0])):
        # Get the digits at the current column index for each row
        first_digits = [row[col_index] for row in input_grid]

        # Count the occurrences of each digit
        digit_counts = Counter(first_digits)

        # Find the most frequent digit(s)
        max_count = max(digit_counts.values())
        most_frequent_digits = [digit for digit, count in digit_counts.items() if count == max_count]

        # If only one most frequent, that's our output
        if len(most_frequent_digits) == 1:
            output = most_frequent_digits[0]
            break  # Exit the loop as we found the output
        else:
            # If equal counts for multiple digits and this is the last index we will return the first one
            if col_index == len(input_grid[0])-1:
              output = most_frequent_digits[0]

    return output