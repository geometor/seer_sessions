"""
Transforms an input grid by performing the following steps:
1. Examines the input grid row by row, from top to bottom.
2. For each row, determines its "signature": a sequence containing the unique colors present in that row, ordered according to their first appearance from left to right.
3. Collects these row signatures into a list, maintaining the top-to-bottom order.
4. Processes the list of signatures: Initializes a new list with the first signature. Iterates through the remaining signatures, adding a signature to the new list only if it is different from the last signature added.
5. Constructs the output grid by vertically stacking the sequences (rows) from the filtered list of signatures. If the filtered signatures have different lengths, the output grid's width is determined by the maximum length, and shorter rows are padded with 0 (black) on the right.
"""

import numpy as np

def get_row_signature(row):
    """
    Finds the sequence of unique colors in a row, preserving the order of first appearance.

    Args:
        row: A list or 1D numpy array representing a row of the grid.

    Returns:
        A list containing the unique colors in their order of first appearance.
    """
    signature = []
    seen_colors = set()
    for color in row:
        if color not in seen_colors:
            signature.append(color)
            seen_colors.add(color)
    return signature

def filter_consecutive_duplicates(signatures):
    """
    Filters a list of signatures to remove consecutive duplicates.

    Args:
        signatures: A list of lists, where each inner list is a row signature.

    Returns:
        A list of lists containing the filtered signatures.
    """
    if not signatures:
        return []

    filtered_signatures = [signatures[0]]  # Keep the first signature
    # Iterate through the remaining signatures
    for i in range(1, len(signatures)):
        # Compare the current signature with the last added signature in the filtered list
        if signatures[i] != filtered_signatures[-1]:
            filtered_signatures.append(signatures[i])
    return filtered_signatures

def transform(input_grid):
    """
    Applies the described transformation to the input grid.

    Args:
        input_grid: A list of lists or numpy array representing the input grid.

    Returns:
        A numpy array representing the output grid.
    """
    # Ensure input is treated as a list of lists for consistent processing
    if isinstance(input_grid, np.ndarray):
        input_rows = input_grid.tolist()
    else:
        input_rows = input_grid

    # Step 1 & 2: Process each row to get its signature
    all_signatures = []
    for row in input_rows:
        signature = get_row_signature(row)
        all_signatures.append(signature)

    # Step 3 & 4: Filter consecutive duplicate signatures
    filtered_signatures = filter_consecutive_duplicates(all_signatures)

    # Step 5: Construct the output grid
    if not filtered_signatures:
        # Return an empty grid if no signatures remain
        return np.array([], dtype=int).reshape(0,0) # Standard way to represent empty 2D array

    # Determine the dimensions of the output grid
    output_height = len(filtered_signatures)
    # Calculate max width needed, default to 0 if list is empty (though handled above)
    max_width = 0
    if filtered_signatures:
         max_width = max(len(r) for r in filtered_signatures)


    # Initialize the output grid with padding value 0 (black)
    # Ensure integer type for ARC compatibility
    output_grid = np.zeros((output_height, max_width), dtype=int)

    # Fill the output grid with the filtered signatures
    for i, signature in enumerate(filtered_signatures):
        output_grid[i, :len(signature)] = signature # Place signature in the row, padding happens automatically due to np.zeros

    return output_grid