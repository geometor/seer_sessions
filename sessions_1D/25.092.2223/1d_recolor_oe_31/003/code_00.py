import numpy as np

# Define color constants for clarity
GRAY = 5
YELLOW = 4
ORANGE = 7
WHITE = 0 # Although not explicitly used in replacement logic, good for context

def transform(input_grid):
    """
    Transforms the input grid by recoloring contiguous horizontal segments of gray pixels.
    Gray segments with odd length are replaced with yellow pixels.
    Gray segments with even length are replaced with orange pixels.
    All other pixels (e.g., white) remain unchanged.
    The transformation is applied independently to each row.
    """
    # Convert the input list of lists to a NumPy array for efficient processing
    input_np = np.array(input_grid, dtype=int)
    # Create a copy of the input array to store the output, ensuring non-gray pixels are preserved
    output_np = np.copy(input_np)
    # Get the dimensions of the grid
    rows, cols = input_np.shape

    # Iterate through each row of the grid
    for r in range(rows):
        in_segment = False  # Flag to track if we are currently inside a gray segment
        start_col = -1      # Variable to store the starting column index of the current segment

        # Iterate through each column in the current row
        for c in range(cols):
            pixel = input_np[r, c]

            # Check if the current pixel is gray
            if pixel == GRAY:
                if not in_segment:
                    # Found the start of a new gray segment
                    in_segment = True
                    start_col = c
            # Check if we were previously in a gray segment and it has now ended
            elif in_segment:
                # The segment ended because the current pixel is not gray
                in_segment = False
                end_col = c - 1  # The segment ended at the previous column
                length = end_col - start_col + 1 # Calculate the length of the segment

                # Determine the replacement color based on the parity of the segment length
                replacement_color = YELLOW if length % 2 != 0 else ORANGE # Odd -> Yellow (4), Even -> Orange (7)

                # Apply the replacement color to the corresponding segment in the output grid
                # Uses NumPy slicing for efficient assignment: output_np[row, start_col:end_col+1]
                output_np[r, start_col : end_col + 1] = replacement_color

                start_col = -1 # Reset the start column index

        # After iterating through all columns, check if a segment was ongoing and ended at the last column
        if in_segment:
            # The segment extended to the end of the row
            end_col = cols - 1 # The last column index
            length = end_col - start_col + 1 # Calculate the length

            # Determine the replacement color based on parity
            replacement_color = YELLOW if length % 2 != 0 else ORANGE

            # Apply the replacement color to the segment in the output grid
            output_np[r, start_col : end_col + 1] = replacement_color

    # Convert the resulting NumPy array back to a list of lists, the standard ARC format
    return output_np.tolist()