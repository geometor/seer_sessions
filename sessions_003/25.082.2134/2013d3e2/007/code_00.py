"""
1.  **Identify Active Rows:** Examine the input grid to identify rows that contain at least one non-zero pixel. These are the "active rows."

2.  **Select Rows by Leftmost Sequence:**
     *   Iterate through the active rows.
     * For each row, find the index of the *leftmost* non-zero pixel.
     *   Extract the sequence starting at that index, including up to the first three non-zero pixels.
     *   select up to 3 rows that have unique leftmost non-zero sequences.

3.  **Construct Output Grid:**
    *   Create a new output grid. The number of rows in the output grid will be the number of selected active rows (up to 3).
    *   Populate each row of the output grid with the extracted sequence from the corresponding selected row. If a sequence has fewer than three pixels, the remaining cells in the output row should remain 0.
    *   The output grid will have at most 3 rows, if no active rows or no unique rows, the grid will be empty.
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
    # extracts up to the first three non-zero pixels from the row, starting from the leftmost non-zero pixel
    sequence = []
    non_zero_count = 0
    start_index = -1

    # Find the index of the leftmost non-zero pixel
    for i, pixel in enumerate(row):
        if pixel != 0:
            start_index = i
            break

    # If no non-zero pixel is found, return an empty sequence
    if start_index == -1:
        return sequence

    # Extract the sequence
    for i in range(start_index, len(row)):
        if row[i] != 0:
            sequence.append(row[i])
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