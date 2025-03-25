"""
1. Identify Active Rows: Examine the input grid and identify all rows containing at least one non-zero pixel.
2. Select Rows: From the active rows, choose up to first three unique rows to include for the output by selecting rows that are unique when comparing leftmost sequence.
3. Extract Sequences: For each selected row:
    *   Find the index of the leftmost non-zero pixel.
    *   Starting from this index, extract pixels up to the third non-zero value.
    *    If the row contains fewer than three, extract until the last non-zero value.
4. Construct Output Grid: Create a new grid with a maximum of three rows. Populate each output row with the corresponding extracted sequence.
"""

import numpy as np

def get_active_rows(grid):
    # returns the indices of rows containing non-zero elements
    rows = []
    for i, row in enumerate(grid):
      if any(val != 0 for val in row):
        rows.append(i)
    return rows

def extract_leftmost_sequence(row):
    # extracts up to the first three non-zero pixels from the row, or fewer if there are less than 3 non-zero pixels
    sequence = []
    non_zero_count = 0
    for pixel in row:
        if pixel != 0:
            sequence.append(pixel)
            non_zero_count += 1
            if non_zero_count == 3:
                break
    return sequence

def select_unique_rows(input_grid, active_rows):
    # select first three unique rows from the list of active rows
    selected_rows = []
    selected_row_indices = []
    
    for row_index in active_rows:
        row = input_grid[row_index]
        sequence = extract_leftmost_sequence(row) #extract sequence for comparing rows
        if sequence not in selected_rows:
            selected_rows.append(sequence)
            selected_row_indices.append(row_index)
            if len(selected_rows) == 3:
                break # Stop after adding 3 rows
                
    return selected_row_indices

def transform(input_grid):
    # convert to numpy array
    input_grid = np.array(input_grid)

    # Identify rows with Non-Zero Pixels
    active_rows = get_active_rows(input_grid)

    # Select first three unique sequences
    selected_row_indices = select_unique_rows(input_grid, active_rows)
    
    # Extract sequences, this time from the original grid using indices
    extracted_sequences = []
    for row_index in selected_row_indices:
       extracted_sequences.append(extract_leftmost_sequence(input_grid[row_index]))
    
    # Determine output grid dimensions
    max_len = 0
    if (len(extracted_sequences) > 0):
        max_len = max(len(seq) for seq in extracted_sequences)
    else:
       return np.array([]) # if no active rows, return an empty numpy array

    num_rows = len(extracted_sequences)
    output_grid = np.zeros((num_rows, max_len), dtype=int)

    # Construct output grid
    for i, seq in enumerate(extracted_sequences):
        output_grid[i, :len(seq)] = seq

    return output_grid