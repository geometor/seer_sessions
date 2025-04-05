```python
import numpy as np

"""
Transforms an input NumPy grid (potentially multi-dimensional) containing 0s and 3s 
into an output grid of the same shape containing 0s, 1s, and 2s.

The transformation operates on the flattened sequence of the grid:
1.  Each 0 in the flattened sequence maps to a 0 in the output.
2.  Contiguous blocks (runs) of 3s in the flattened sequence are mapped to either 1s or 2s.
3.  The mapping rule for blocks of 3s depends on the very first element of the flattened sequence:
    - If the first element is 0: The first block of 3s maps to 2s, and all subsequent blocks map to 1s.
    - If the first element is 3: The first block of 3s maps to 1s, and all subsequent blocks map to 2s.
The final output grid has the same shape as the input grid.
"""

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Applies the transformation rule to the input NumPy grid.

    Args:
        input_grid: A NumPy array (potentially multi-dimensional) containing integers (0s and 3s).

    Returns:
        A NumPy array of the same shape containing the transformed sequence (0s, 1s, 2s).
    """
    
    # Store the original shape of the input grid
    original_shape = input_grid.shape
    
    # Flatten the input grid to process it as a 1D sequence
    flattened_input = input_grid.flatten()
    n = flattened_input.shape[0]

    # Handle empty input
    if n == 0:
        # Return an empty array with the original shape (which might be (0,) or (0, 0), etc.)
        return np.array([], dtype=int).reshape(original_shape)

    # Initialize a flattened output array with zeros
    flattened_output = np.zeros(n, dtype=int)

    # Determine the mapping rule based on the very first element of the flattened input
    first_block_map_value = 0
    subsequent_block_map_value = 0
    
    # Check if the flattened array has at least one element before accessing index 0
    if n > 0:
        if flattened_input[0] == 0:
            first_block_map_value = 2
            subsequent_block_map_value = 1
        elif flattened_input[0] == 3:
            first_block_map_value = 1
            subsequent_block_map_value = 2
        # Assuming input only contains 0 or 3

    # Initialize block tracking variables
    block_count = 0
    current_map_value = 0 # Stores the value to map the current block of 3s to

    # Iterate through the flattened input sequence
    for i in range(n):
        input_val = flattened_input[i]

        # Handle 0s: output is already 0, so just assign and continue
        if input_val == 0:
            flattened_output[i] = 0
            continue # Skip the rest of the loop for 0s

        # Handle 3s
        elif input_val == 3:
            # Check if this is the start of a new block of 3s in the flattened sequence
            # A new block starts at index 0 if the value is 3,
            # or if the current value is 3 and the previous was 0.
            is_new_block_start = (i == 0) or (flattened_input[i-1] == 0)

            if is_new_block_start:
                # Increment block counter
                block_count += 1
                # Determine the mapping value for this new block
                if block_count == 1:
                    current_map_value = first_block_map_value
                else:
                    current_map_value = subsequent_block_map_value

            # Set the output value using the mapping value for the current block
            flattened_output[i] = current_map_value
            
        # Optional: Handle unexpected input values if necessary
        # else:
        #     pass # Or raise an error, or assign a default

    # Reshape the flattened output array back to the original input grid shape
    output_grid = flattened_output.reshape(original_shape)

    return output_grid
```