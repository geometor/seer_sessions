import numpy as np

def find_stripe_boundaries(grid):
    """
    Identifies the column indices that mark the start of new vertical stripes.
    Assumes boundaries are defined by color changes in the first row.

    Args:
        grid (np.array): The input grid.

    Returns:
        list: A list of column indices where stripes begin. Includes 0 for the first stripe.
    """
    boundaries = [0]  # The first stripe always starts at column 0
    first_row = grid[0]
    for col in range(1, len(first_row)):
        if first_row[col] != first_row[col - 1]:
            boundaries.append(col)
    return boundaries

def extract_stripes(grid, boundaries):
    """
    Extracts the sub-grids corresponding to each vertical stripe.

    Args:
        grid (np.array): The input grid.
        boundaries (list): List of starting column indices for each stripe.

    Returns:
        list: A list of np.arrays, each representing a stripe's content.
    """
    stripes = []
    num_cols = grid.shape[1]
    for i in range(len(boundaries)):
        start_col = boundaries[i]
        # Determine the end column for the current stripe
        if i + 1 < len(boundaries):
            end_col = boundaries[i+1]
        else:
            # Last stripe goes to the end of the grid
            end_col = num_cols
        # Extract the stripe using numpy slicing
        stripe_content = grid[:, start_col:end_col]
        stripes.append(stripe_content)
    return stripes

def transform(input_grid):
    """
    Reverses the order of vertical stripes identified within the input grid.

    The function identifies vertical stripes based on color changes in the
    first row. It then extracts these stripes, reverses their order, and
    concatenates them horizontally to form the output grid. The internal
    content and structure of each stripe are preserved.
    """
    # Convert input list of lists to a numpy array for efficient slicing
    input_np = np.array(input_grid, dtype=int)

    # 1. Identify the distinct vertical stripes based on the first row
    stripe_boundaries = find_stripe_boundaries(input_np)

    # 2. Extract the content of each stripe
    stripes = extract_stripes(input_np, stripe_boundaries)

    # 3. Reverse the order of the extracted stripes
    reversed_stripes = stripes[::-1] # Use slicing to reverse the list

    # 4. Reconstruct the grid by horizontally stacking the reversed stripes
    if not reversed_stripes: # Handle empty input case
         output_np = np.array([[] for _ in range(input_np.shape[0])]) # empty grid with correct height
    else:
         output_np = np.hstack(reversed_stripes)

    # Convert the resulting numpy array back to a list of lists
    output_grid = output_np.tolist()

    return output_grid