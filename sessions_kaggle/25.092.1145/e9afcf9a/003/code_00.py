import numpy as np

"""
Transforms a 2xN input NumPy array containing two distinct repeating numbers 
into a 2xN output NumPy array.
The first output row alternates between the number from the first input row (num1) 
and the number from the second input row (num2), starting with num1.
The second output row alternates between num2 and num1, starting with num2.
"""

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Applies the alternating transformation rule to the input NumPy array.

    Args:
        input_grid: A 2xN NumPy array where the first row contains repetitions 
                    of one number (num1) and the second row contains repetitions 
                    of another number (num2).

    Returns:
        A 2xN NumPy array with alternating patterns based on num1 and num2.
    """
    # Validate input shape
    if input_grid.ndim != 2 or input_grid.shape[0] != 2:
        raise ValueError("Input grid must be a 2D array with 2 rows.")
    
    # Extract numbers and dimensions
    num1 = input_grid[0, 0] # Get the number from the first row
    num2 = input_grid[1, 0] # Get the number from the second row
    num_rows, num_cols = input_grid.shape # Get shape (should be 2, N)
    
    # Initialize the output grid with the same shape and dtype as the input
    output_grid = np.zeros_like(input_grid)

    # Generate the first output row (starts with num1)
    for j in range(num_cols):
        if j % 2 == 0: # Even indices (0, 2, 4...)
            output_grid[0, j] = num1
        else: # Odd indices (1, 3, 5...)
            output_grid[0, j] = num2
            
    # Generate the second output row (starts with num2)
    for j in range(num_cols):
        if j % 2 == 0: # Even indices (0, 2, 4...)
            output_grid[1, j] = num2
        else: # Odd indices (1, 3, 5...)
            output_grid[1, j] = num1

    return output_grid
