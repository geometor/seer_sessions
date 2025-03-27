import numpy as np

"""
Identify all possible 3x3 subgrids within the input grid.
Calculate the density (count of non-white pixels) for each 3x3 subgrid.
Return the 3x3 subgrid with the highest density.
If multiple subgrids share the maximum density, the one encountered first
in a top-to-bottom, left-to-right scan is returned.
"""

def find_dense_subgrid(grid, subgrid_size=(3, 3)):
    """
    Finds the subgrid of a specific size with the maximum number of non-zero pixels.

    Args:
        grid (np.array): The input grid.
        subgrid_size (tuple): The (height, width) of the subgrid to search for.

    Returns:
        tuple: A tuple containing the subgrid (np.array) with the highest density
               and its density (int). Returns (None, -1) if no such subgrid can be formed.
    """
    grid_height, grid_width = grid.shape
    sub_height, sub_width = subgrid_size

    max_density = -1
    best_subgrid = None

    # Check if the grid is large enough to contain the specified subgrid size
    if grid_height < sub_height or grid_width < sub_width:
        return best_subgrid, max_density

    # Iterate through all possible top-left corners (r, c) of the subgrid
    for r in range(grid_height - sub_height + 1):
        for c in range(grid_width - sub_width + 1):
            # Extract the subgrid
            subgrid = grid[r:r+sub_height, c:c+sub_width]

            # Calculate the density (count of non-white/non-zero pixels)
            density = np.count_nonzero(subgrid)

            # Update if this subgrid has a strictly higher density
            # This ensures the first one found in scan order is kept in case of ties
            if density > max_density:
                max_density = density
                # Store a copy
                best_subgrid = subgrid.copy()

    return best_subgrid, max_density


def transform(input_grid):
    """
    Transforms the input grid by finding the 3x3 subgrid with the most
    non-white pixels and returning it.

    Args:
        input_grid (list of lists): The input grid represented as a list of lists.

    Returns:
        list of lists: The 3x3 subgrid with the maximum density of non-white pixels.
                       Returns a 3x3 grid of zeros if the input is smaller than 3x3
                       or if no non-zero pixels are found in any 3x3 subgrid.
    """
    # Convert input to numpy array for easier slicing and calculations
    grid_np = np.array(input_grid, dtype=int)

    # Define the target subgrid size
    subgrid_size = (3, 3)

    # Find the subgrid with the highest density
    selected_subgrid, max_density = find_dense_subgrid(grid_np, subgrid_size)

    # Handle cases where no valid subgrid was found or the max density was 0
    if selected_subgrid is None:
        # Return a default 3x3 grid of zeros
        output_grid = np.zeros(subgrid_size, dtype=int)
    else:
        output_grid = selected_subgrid

    # Convert the resulting numpy array back to a list of lists for the expected output format
    return output_grid.tolist()