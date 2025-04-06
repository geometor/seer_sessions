import numpy as np

"""
The transformation operates on a square numerical grid. It first identifies the main diagonal (top-left to bottom-right) and the anti-diagonal (top-right to bottom-left). It calculates the sum of elements along each of these diagonals. 

The diagonal with the larger sum is selected. If the sums are equal, the main diagonal is chosen by default (although this specific case isn't demonstrated in the examples, it's a reasonable tie-breaker).

The selected diagonal's elements are then transferred to the corresponding positions in an output grid of the same size, initialized with zeros. However, one element from the selected diagonal is *excluded* (i.e., its corresponding position in the output grid remains zero).

The index of the element to exclude depends on the value of the input grid element at position [1][0] (second row, first column) and whether the main or anti-diagonal was selected:

1.  **If the main diagonal was selected:**
    *   If `input_grid[1][0]` is 0, exclude the first element (index 0) of the main diagonal (`input_grid[0][0]`).
    *   If `input_grid[1][0]` is not 0, exclude the last element (index n-1) of the main diagonal (`input_grid[n-1][n-1]`).

2.  **If the anti-diagonal was selected:**
    *   If `input_grid[1][0]` is 0, exclude the last element (index n-1) of the anti-diagonal (`input_grid[n-1][0]`).
    *   If `input_grid[1][0]` is not 0, exclude the first element (index 0) of the anti-diagonal (`input_grid[0][n-1]`).

All other positions in the output grid remain zero.
"""

def transform(input_grid):
    """
    Transforms the input grid based on diagonal sums and a specific exclusion rule.

    Args:
        input_grid: A list of lists representing the input square grid.

    Returns:
        A list of lists representing the transformed output grid.
    """
    n = len(input_grid)
    output_grid = [[0 for _ in range(n)] for _ in range(n)]
    
    # Convert to numpy array for easier diagonal access if needed, or use list comprehensions
    # input_np = np.array(input_grid) # Optional, can do without numpy

    # --- Extract Diagonals ---
    main_diag = [input_grid[i][i] for i in range(n)]
    anti_diag = [input_grid[i][n - 1 - i] for i in range(n)]

    # --- Calculate Sums ---
    main_diag_sum = sum(main_diag)
    anti_diag_sum = sum(anti_diag)

    # --- Determine Chosen Diagonal and Exclusion Index ---
    exclude_value_source = input_grid[1][0]
    exclude_index = -1 # Initialize with an invalid index

    if main_diag_sum >= anti_diag_sum:
        # Main diagonal is chosen (or tie)
        chosen_diag = main_diag
        is_main_diag = True
        if exclude_value_source == 0:
            exclude_index = 0 # Exclude first element
        else:
            exclude_index = n - 1 # Exclude last element
    else:
        # Anti-diagonal is chosen
        chosen_diag = anti_diag
        is_main_diag = False
        if exclude_value_source == 0:
            exclude_index = n - 1 # Exclude last element (from anti-diag perspective)
        else:
            exclude_index = 0 # Exclude first element (from anti-diag perspective)

    # --- Populate Output Grid ---
    for i in range(n):
        if i != exclude_index: # Check if this index should be excluded
            if is_main_diag:
                # Place element on the main diagonal of the output
                output_grid[i][i] = input_grid[i][i] 
            else:
                # Place element on the anti-diagonal of the output
                output_grid[i][n - 1 - i] = input_grid[i][n - 1 - i]

    return output_grid