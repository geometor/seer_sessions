"""
The transformation extracts a sequence of non-zero pixels from each row of the input grid, starting from the leftmost non-zero pixel and continuing until a zero pixel or the end of the row is reached. The output grid's dimensions are determined by the number of active rows and the length of the longest extracted sequence. Shorter rows are padded with zeros.
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
    # extracts the sequence of non-zero pixels starting from the leftmost non-zero pixel
    sequence = []
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
        else:
            break  # Stop when a zero pixel is encountered

    return sequence

def transform(input_grid):
    # convert to numpy array
    input_grid = np.array(input_grid)

    # Identify rows with Non-Zero Pixels
    active_rows = get_active_rows(input_grid)

    # Extract sequences
    extracted_sequences = []
    for row_index in active_rows:
        row = input_grid[row_index]
        sequence = extract_leftmost_sequence(row)
        extracted_sequences.append(sequence)

    # Determine output grid dimensions
    max_len = 0
    if (len(extracted_sequences) > 0):
        max_len = max(len(seq) for seq in extracted_sequences)
    else:
       return np.array([]) # if no active rows, return an empty numpy array
      
    num_rows = len(extracted_sequences)
    output_grid = np.zeros((num_rows, max_len), dtype=int)

    # Construct output grid, padding shorter sequences with zeros
    for i, seq in enumerate(extracted_sequences):
        output_grid[i, :len(seq)] = seq

    return output_grid