import numpy as np
from collections import Counter

def get_majority_color(elements):
    """
    Finds the most frequent element (color) in a list or array.
    If there's a tie, it returns the one that appears first among the most frequent.
    """
    if not elements:
        return None # Or a default color like 0 if appropriate for the context
    count = Counter(elements)
    # Find the maximum count
    max_count = 0
    for element in count:
        if count[element] > max_count:
            max_count = count[element]
    
    # Find elements with the maximum count
    majority_elements = [element for element, freq in count.items() if freq == max_count]
    
    # If there's only one majority element, return it
    if len(majority_elements) == 1:
        return majority_elements[0]
    else:
        # Tie-breaking: return the one that appeared first in the original list
        # This requires iterating through the original list to find the first occurrence
        # of any element present in majority_elements
        for elem in elements:
            if elem in majority_elements:
                return elem
        # Fallback (shouldn't be reached if elements is not empty)
        return majority_elements[0]


def transform(input_grid):
    """
    Determines if the grid has a dominant row or column pattern based on color homogeneity.
    Identifies 'noise' pixels (those not matching the majority color of their row/column)
    and replaces them with the majority color of that row/column.

    1. Calculate row and column homogeneity scores.
    2. Determine orientation (row or column) based on scores.
    3. Iterate through rows/columns based on orientation.
    4. For each row/column, find the majority color.
    5. Replace pixels in that row/column that don't match the majority color.
    """
    input_np = np.array(input_grid, dtype=int)
    rows, cols = input_np.shape
    output_grid = np.copy(input_np)

    # 1. Calculate homogeneity scores
    row_homogeneity_score = 0
    for r in range(rows):
        row_elements = list(input_np[r, :])
        if row_elements:
            count = Counter(row_elements)
            row_homogeneity_score += max(count.values()) if count else 0

    col_homogeneity_score = 0
    for c in range(cols):
        col_elements = list(input_np[:, c])
        if col_elements:
            count = Counter(col_elements)
            col_homogeneity_score += max(count.values()) if count else 0

    # 2. Determine orientation
    # If scores are equal, default to row-based processing (as seen in test case logic)
    # Although the description said row >= col, let's refine: row > col -> row, col > row -> col. If equal?
    # Let's stick to the description: row >= col is 'row' orientation.
    orientation = 'row' if row_homogeneity_score >= col_homogeneity_score else 'column'

    # 3. & 4. & 5. Iterate and replace based on orientation
    if orientation == 'row':
        # Process row by row
        for r in range(rows):
            row_elements = list(input_np[r, :])
            if not row_elements: continue # Skip empty rows if they could exist
            
            majority_color = get_majority_color(row_elements)
            if majority_color is None: continue # Skip if row has no majority (e.g., empty or all unique)

            for c in range(cols):
                if input_np[r, c] != majority_color:
                    output_grid[r, c] = majority_color
    else: # orientation == 'column'
        # Process column by column
        for c in range(cols):
            col_elements = list(input_np[:, c])
            if not col_elements: continue # Skip empty columns if they could exist
            
            majority_color = get_majority_color(col_elements)
            if majority_color is None: continue # Skip if column has no majority

            for r in range(rows):
                if input_np[r, c] != majority_color:
                    output_grid[r, c] = majority_color

    return output_grid.tolist()