import numpy as np
from collections import Counter

"""
Transforms an input grid based on identifying signal digits, locating specific 
6x6 patterns associated with them in the input, determining the order based on 
these locations, and generating corresponding standard output patterns.

1. Determine the background digit (most frequent).
2. Identify signal digits: non-background digits with at least one adjacent 
   (including diagonal) neighbor of the same digit.
3. Define the standard 6x6 pattern structure: a fixed frame of 8 foreground 
   cells against the background digit. The foreground coordinates are:
   (0,2), (0,3), (1,1), (1,4), (2,0), (2,5), (3,0), (3,5), (4,1), (4,4), (5,2), (5,3).
4. Locate all occurrences of this standard 6x6 pattern within the input grid 
   for each identified signal digit. Record the top-left corner (row, col) and 
   the signal digit for each match.
5. Determine the output order: Sort the found pattern occurrences primarily by 
   row, secondarily by column. Extract the unique signal digits based on this 
   sorted order, taking the first occurrence of each digit.
6. Construct the output grid: For each signal digit in the determined order, 
   create the standard 6x6 pattern using that digit as foreground and the 
   background digit. Stack these patterns vertically.
7. Return the resulting stacked grid. If no signal digits are found or no 
   pattern instances are located, return an empty grid.
"""

def _get_background_digit(grid: np.ndarray) -> int:
    """Finds the most frequent digit in the grid."""
    if grid.size == 0:
        raise ValueError("Input grid cannot be empty") 
    counts = Counter(grid.flatten())
    background_digit = counts.most_common(1)[0][0]
    return int(background_digit) 

def _find_signal_digits(grid: np.ndarray, background_digit: int) -> list[int]:
    """Identifies signal digits based on self-adjacency (including diagonals)."""
    rows, cols = grid.shape
    unique_digits = np.unique(grid)
    candidate_digits = [int(d) for d in unique_digits if d != background_digit] 
    signal_digits = set()
    neighbors = [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]

    for digit in candidate_digits:
        locations = np.argwhere(grid == digit)
        is_signal = False
        for r, c in locations:
            for dr, dc in neighbors:
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols and grid[nr, nc] == digit:
                    signal_digits.add(digit)
                    is_signal = True; break
            if is_signal: break
    # Return sorted list - although order will be determined later, 
    # returning sorted list is consistent
    return sorted(list(signal_digits))

def _create_pattern_grid(foreground_digit: int, background_digit: int) -> np.ndarray:
    """Creates the standard 6x6 grid with the specified foreground/background pattern."""
    pattern = np.full((6, 6), background_digit, dtype=int)
    # Define the coordinates for the foreground digit (the frame)
    # using the CORRECTED coordinates based on analysis
    fg_rows = [0, 0, 1, 1, 2, 2, 3, 3, 4, 4, 5, 5]
    fg_cols = [2, 3, 1, 4, 0, 5, 0, 5, 1, 4, 2, 3]
    pattern[fg_rows, fg_cols] = foreground_digit
    return pattern

def _find_pattern_occurrences(grid: np.ndarray, signal_digits: list[int], background_digit: int) -> list[tuple[int, int, int]]:
    """
    Scans the input grid for all occurrences of the standard 6x6 pattern for any signal digit.
    Returns a list of tuples: (row, column, signal_digit) for each match.
    """
    rows, cols = grid.shape
    occurrences = []
    if not signal_digits:
        return [] # No signal digits, no patterns to find

    # Pre-generate target patterns for efficiency
    target_patterns = {
        sig_digit: _create_pattern_grid(sig_digit, background_digit)
        for sig_digit in signal_digits
    }

    # Scan through all possible 6x6 top-left corners
    for r in range(rows - 5):
        for c in range(cols - 5):
            subgrid = grid[r:r+6, c:c+6]
            
            # Check if this subgrid matches any of the target patterns
            for sig_digit, target_pattern in target_patterns.items():
                if np.array_equal(subgrid, target_pattern):
                    occurrences.append((r, c, sig_digit))
                    # Assuming a subgrid matches only one pattern type, break inner loop
                    break 
                    
    return occurrences

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies the transformation rule to the input grid.
    """
    # Convert input list of lists to a numpy array for efficient processing
    input_array = np.array(input_grid, dtype=int)

    # Handle empty input grid case
    if input_array.size == 0:
        return [] 

    # Step 1: Identify the background digit (most frequent)
    background_digit = _get_background_digit(input_array)

    # Step 2: Identify signal digits (non-background, self-adjacent)
    signal_digits = _find_signal_digits(input_array, background_digit)
    if not signal_digits:
        return [] # No signal digits found

    # Step 4: Locate all occurrences of the standard pattern in the input grid
    pattern_occurrences = _find_pattern_occurrences(input_array, signal_digits, background_digit)
    if not pattern_occurrences:
         return [] # No patterns found in the input

    # Step 5: Determine the output order based on occurrence location
    # Sort occurrences first by row, then by column
    pattern_occurrences.sort(key=lambda x: (x[0], x[1]))

    # Extract the unique signal digits in the determined order
    ordered_signal_digits = []
    seen_digits = set()
    for r, c, sig_digit in pattern_occurrences:
        if sig_digit not in seen_digits:
            ordered_signal_digits.append(sig_digit)
            seen_digits.add(sig_digit)
            
    # Step 6 & 7: Construct the output grid by stacking patterns in order
    output_patterns = []
    for fg_digit in ordered_signal_digits:
        # Create the standard 6x6 pattern for the current signal digit
        pattern_grid = _create_pattern_grid(fg_digit, background_digit)
        output_patterns.append(pattern_grid)

    # Stack the generated patterns vertically
    # vstack requires at least one array, handled by checks above
    output_grid_np = np.vstack(output_patterns)

    # Convert the final numpy array back to a list of lists
    return output_grid_np.tolist()