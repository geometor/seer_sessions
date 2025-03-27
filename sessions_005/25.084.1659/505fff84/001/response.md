```python
import numpy as np

def transform(input_grid):
    """
    Extracts horizontal segments from rows containing both a blue (1) and an azure (8) pixel.
    The segment consists of the pixels strictly between the first blue and first azure pixels found in that row.
    The extracted segments are stacked vertically in the order of their original rows to form the output grid.
    If no such rows are found, an empty grid is returned.
    """
    # Convert input list of lists to a NumPy array for efficient processing
    input_grid_np = np.array(input_grid, dtype=int)
    height, width = input_grid_np.shape
    
    # List to store the segments extracted from each relevant row
    extracted_segments = []

    # Iterate through each row of the input grid
    for r in range(height):
        row = input_grid_np[r, :]

        # Find the column indices of all blue (1) pixels in the current row
        blue_indices = np.where(row == 1)[0]
        # Find the column indices of all azure (8) pixels in the current row
        azure_indices = np.where(row == 8)[0]

        # Proceed only if both a blue and an azure pixel exist in this row
        if len(blue_indices) > 0 and len(azure_indices) > 0:
            # Get the column index of the *first* blue pixel
            blue_col = blue_indices[0]
            # Get the column index of the *first* azure pixel
            azure_col = azure_indices[0]

            # Determine the start and end columns for the segment extraction
            # The segment includes pixels *between* the markers, exclusive of markers
            start_col = min(blue_col, azure_col) + 1
            end_col = max(blue_col, azure_col)

            # Ensure there are actually pixels between the markers
            if start_col < end_col:
                # Extract the segment from the row
                segment = row[start_col:end_col]
                # Add the extracted segment to our list
                extracted_segments.append(segment)

    # If no segments were extracted across all rows, return an empty grid represented by an empty list
    if not extracted_segments:
        return []

    # Check if all extracted segments have the same length. This is assumed based on examples.
    # If they didn't, np.vstack would raise an error.
    
    # Stack the collected segments vertically to form the output grid
    output_grid_np = np.vstack(extracted_segments)

    # Convert the resulting NumPy array back to a standard Python list of lists format
    output_grid = output_grid_np.tolist()

    return output_grid
```