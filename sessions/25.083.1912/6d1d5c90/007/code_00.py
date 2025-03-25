"""
Transforms an input grid by removing rows starting with 2, processing rows starting with 6, 
reconstructing the first row from the removed row, truncating all rows to length 6, and sorting.
"""

import numpy as np

def transform(input_grid):
    # Convert input_grid to a list of lists for easier manipulation.
    rows = [list(row) for row in input_grid]
    
    # 1. Removal: Identify and remove any row that begins with the digit '2'.
    #    Store the removed row for later use.
    removed_row = None
    rows_to_process = []
    for row in rows:
        if row[0] == 2:
            removed_row = row
        else:
            rows_to_process.append(row)
    
    # 2. Process '6' Rows: Identify rows that begin with the digit '6'.
    #    Remove the leading '6' from these rows.
    processed_six_rows = []
    other_rows = []
    for row in rows_to_process:
        if row[0] == 6:
            processed_six_rows.append(row[1:])  # Remove the leading '6'
        else:
            other_rows.append(row)

    # 3. Reconstruct First Row: Use the removed row.
    reconstructed_row = []
    if removed_row:
      reconstructed_row = removed_row

    # 4. Truncate all rows to length 6
    truncated_reconstructed_row = reconstructed_row[:6] if reconstructed_row else []
    truncated_six_rows = [row[:6] for row in processed_six_rows]
    truncated_other_rows = [row[:6] for row in other_rows]

    # 5. Sort: Sort lexicographically.
    
    all_rows = []
    if (truncated_reconstructed_row):
        all_rows.append(truncated_reconstructed_row)
    all_rows.extend(truncated_other_rows)
    all_rows.extend(truncated_six_rows)
    
    sorted_rows = sorted(all_rows)


    # 6. Combine for output:
    output_rows = sorted_rows

    # Convert back to numpy array
    output_grid = np.array(output_rows)

    return output_grid