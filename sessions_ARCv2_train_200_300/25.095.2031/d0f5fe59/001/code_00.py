import numpy as np
from scipy.ndimage import label

"""
Identifies connected components of the digit '8' in the input grid using 8-way connectivity. 
Counts the number of components (N).
Generates an NxN output grid where the main diagonal consists of '8's and all other elements are '0's.
"""

def find_connected_components(grid: np.ndarray, target_value: int) -> int:
    """
    Finds connected components of a specific value in a grid.

    Args:
        grid: The input NumPy array.
        target_value: The value whose components are to be found.

    Returns:
        The number of distinct connected components found.
    """
    # Create a binary mask where target_value is True (1) and others are False (0)
    binary_mask = (grid == target_value)
    
    # Define the structure for 8-way connectivity (including diagonals)
    # [[1,1,1],
    #  [1,1,1],
    #  [1,1,1]] allows connections horizontally, vertically, and diagonally.
    structure = np.ones((3, 3), dtype=int) 
    
    # Label the connected components in the binary mask
    # labeled_array contains the grid with each component marked by a unique integer
    # num_features is the total number of connected components found
    labeled_array, num_features = label(binary_mask, structure=structure)
    
    return num_features

def generate_diagonal_matrix(size: int, diagonal_value: int, off_diagonal_value: int) -> list[list[int]]:
    """
    Generates a square matrix with a specific value on the diagonal and another value elsewhere.

    Args:
        size: The dimension (N) of the square matrix (NxN).
        diagonal_value: The value to place on the main diagonal.
        off_diagonal_value: The value to place in off-diagonal positions.

    Returns:
        A list of lists representing the generated matrix.
    """
    if size == 0:
        return []
    # Create an NxN array filled with the off-diagonal value
    output_np = np.full((size, size), off_diagonal_value, dtype=int)
    # Fill the main diagonal with the diagonal value
    np.fill_diagonal(output_np, diagonal_value)
    # Convert the NumPy array to a list of lists
    return output_np.tolist()

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Transforms the input grid by finding connected components of '8's and 
    generating a diagonal matrix based on the component count.

    Args:
        input_grid: A list of lists representing the input 2D grid.

    Returns:
        A list of lists representing the output diagonal matrix.
    """
    # Convert the input list of lists to a NumPy array for efficient processing
    input_np = np.array(input_grid, dtype=int)

    # Define the target value we are looking for
    target_value = 8

    # Find the number of connected components of the target value
    num_components = find_connected_components(input_np, target_value)

    # Define the values for the output matrix
    diagonal_value = 8
    off_diagonal_value = 0

    # Generate the output grid based on the number of components
    output_grid = generate_diagonal_matrix(num_components, diagonal_value, off_diagonal_value)

    return output_grid
