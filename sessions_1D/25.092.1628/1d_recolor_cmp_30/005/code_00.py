"""
Identifies the longest contiguous horizontal sequence(s) of green (3) pixels
in the input grid (assumed to be a single row) and changes their color to 
azure (8). All other pixels remain unchanged. If multiple sequences share the 
maximum length, all of them are changed. If no green sequences exist, the 
grid is returned unchanged.
"""

from typing import List, Dict, Tuple # For type hinting

# Define colors for clarity
GREEN = 3
AZURE = 8
# WHITE = 0 # Included for context, though not directly used in the logic

def find_contiguous_sequences(row: List[int], target_color: int) -> List[Dict]:
    """
    Finds the start index and length of all contiguous sequences 
    of a specific target_color in a 1D list (row).

    Args:
        row: A list of integers representing a row of the grid.
        target_color: The integer value of the color to find sequences of.

    Returns:
        A list of dictionaries, where each dictionary contains the 'start' 
        index and 'length' of a found sequence. Returns an empty list if 
        no sequences are found.
    """
    sequences = []
    current_start = -1
    n = len(row)
    
    # Ensure row elements are standard integers for comparison
    row_int = [int(p) for p in row]
    target_color_int = int(target_color)

    for i, pixel in enumerate(row_int):
        # Check if the current pixel is the target color
        if pixel == target_color_int:
            # If this is the start of a new sequence, record the index
            if current_start == -1:
                current_start = i
        # If the pixel is not the target color
        else:
            # Check if we were just in a sequence
            if current_start != -1:
                # Calculate the length and store the sequence
                length = i - current_start
                sequences.append({'start': current_start, 'length': length})
                # Reset the start index
                current_start = -1
                
    # Handle a sequence that might end at the very end of the row
    if current_start != -1:
        length = n - current_start
        sequences.append({'start': current_start, 'length': length})
        
    return sequences

def transform(input_grid: List[List[int]]) -> List[List[int]]:
    """
    Transforms the input grid based on the described rule.
    """
    # Handle empty or invalid input gracefully
    if not input_grid or not isinstance(input_grid, list) or len(input_grid) == 0:
        return [] 
        
    # Assuming the input grid has only one row based on all examples.
    # Extract the row and ensure it's a list of standard Python integers.
    try:
        input_row = [int(x) for x in input_grid[0]]
    except (IndexError, TypeError, ValueError):
        # If the input isn't structured as expected, return a copy.
        # Create a deep copy to prevent modifying the input.
        return [list(row) for row in input_grid] # Return deep copy

    # Create a mutable copy of the input row for the output.
    output_row = list(input_row) 

    # Step 1: Identify all contiguous horizontal sequences of green (3) pixels.
    green_sequences = find_contiguous_sequences(input_row, GREEN)

    # Step 2: If no green sequences are found, return the grid unchanged.
    if not green_sequences:
        return [output_row] # Return the initial copy

    # Step 3: Find the maximum length among all identified green sequences.
    max_length = 0
    for seq in green_sequences:
        max_length = max(max_length, seq['length'])
            
    # Step 4: Identify all green sequences whose length is equal to this maximum length.
    longest_sequences = [seq for seq in green_sequences if seq['length'] == max_length]

    # Step 5: For each of these longest green sequences, change the color 
    #         of all its constituent pixels from green (3) to azure (8) in the output row.
    for seq in longest_sequences:
        start_index = seq['start']
        seq_length = seq['length']
        for i in range(start_index, start_index + seq_length):
            # Basic bounds check (should be inherently correct from find_sequences logic)
            if 0 <= i < len(output_row):
                output_row[i] = AZURE

    # Step 6: Return the modified grid (single row wrapped in a list).
    return [output_row]