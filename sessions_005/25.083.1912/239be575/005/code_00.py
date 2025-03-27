"""
1.  **Identify Leading Digits:** For each row in the input grid, identify the first digit (the leading digit).

2.  **Count Row Leaders:** Count the number of rows for which each digit is the leading digit.

3.  **Find Maximum Row Leaders:** Determine the digit(s) that appear as the leading digit in the maximum number of rows.

4.  **Tie-breaker:**
    *   If only one digit leads the most rows, that digit is the output.
    *   If multiple digits are tied for leading the most rows, a tie-breaker rule must be applied.  The current hypothesis is to examine subsequent digits in *all* rows, not just tied ones, and select the most frequent one. If ties persist, continue to the next digit, and so on.  If all columns are exhausted, return the first tied leader encountered.

5.  **Return Output:** The digit determined from steps 3 and 4 will be output.
"""

from collections import Counter

def get_row_leaders(input_grid):
    """Counts how many times each digit appears as the leading digit in a row."""
    row_leaders = {}
    for row in input_grid:
        first_digit = row[0]
        if first_digit not in row_leaders:
            row_leaders[first_digit] = 0
        row_leaders[first_digit] += 1
    return row_leaders

def find_max_leaders(row_leaders):
    """Identifies the digit(s) that lead the most rows."""
    max_count = max(row_leaders.values())
    max_leaders = [digit for digit, count in row_leaders.items() if count == max_count]
    return max_leaders

def tie_breaker(input_grid, max_leaders):
    """Breaks ties among leading digits using subsequent digits in *all* rows."""

    if not input_grid:
        return max_leaders[0]
    
    for col_index in range(1, len(input_grid[0])): # start on second digit
        digit_counts = Counter()
        
        for row in input_grid:
          if col_index < len(row): # make sure there *is* a digit to check
            digit_counts[row[col_index]] += 1

        if digit_counts:  # if any digits, process
          max_count = max(digit_counts.values())
          most_frequent = [digit for digit, count in digit_counts.items() if count == max_count]
          if len(most_frequent) == 1: # if single most frequent, return it
            return most_frequent[0]
          # otherwise, it stays tied, proceed to next digit
          
    # If all digits checked and tie still remains, return the *first* leader
    return max_leaders[0]

def transform(input_grid):
    # Count how many times each digit is a row leader
    row_leaders = get_row_leaders(input_grid)

    # Determine the digits that are maximum row leaders
    max_leaders = find_max_leaders(row_leaders)

    # If there's a tie, use tie-breaker logic
    if len(max_leaders) > 1:
        output = tie_breaker(input_grid, max_leaders)
    else:
        # If there's only one leader, return it
        output = max_leaders[0]

    return output