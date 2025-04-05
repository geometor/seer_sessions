```python
import numpy as np

"""
Transforms an input sequence (NumPy array) of 12 integers by shifting 
all non-zero elements two positions to the left, with wrap-around. Positions 
not filled by a shifted non-zero element are set to zero.
"""

def calculate_target_index(current_index, shift_amount, sequence_length):
    """Calculates the target index after a circular shift."""
    return (current_index + shift_amount) % sequence_length

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Applies the left shift transformation to the input sequence.

    Args:
        input_grid: A NumPy array of 12 integers representing the input sequence.

    Returns:
        A NumPy array of 12 integers representing the transformed sequence.
    """
    # Define constants for clarity
    sequence_length = len(input_grid)
    shift_amount = -2 # Left shift by 2
    fill_value = 0

    # Initialize output_grid with the fill value (zeros)
    # Ensure the output grid has the same shape and type as the input
    output_grid = np.full_like(input_grid, fill_value)

    # Iterate through the input sequence
    for i in range(sequence_length):
        # Get the value of the current element
        element_value = input_grid[i]

        # Check if the element is non-zero
        if element_value != fill_value:
            # Calculate the target index for the non-zero element
            target_idx = calculate_target_index(i, shift_amount, sequence_length)
            
            # Place the non-zero element into the output grid at the target index
            output_grid[target_idx] = element_value

    # Return the completed output grid
    return output_grid
```