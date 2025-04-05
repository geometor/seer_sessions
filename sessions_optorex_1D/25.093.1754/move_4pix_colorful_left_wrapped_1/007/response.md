```python
"""
Transforms an input sequence of 12 integers by dividing it into three 
consecutive chunks of 4 integers each. The output sequence is constructed by 
rearranging these chunks in the order: second chunk, third chunk, first chunk.
"""

import numpy as np

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Rearranges chunks of a 12-integer NumPy array.

    Args:
        input_grid: A 1D NumPy array containing 12 integers.

    Returns:
        A 1D NumPy array containing the rearranged 12 integers.
    """

    # Ensure the input is a 1D array of size 12 
    # (assuming valid input as per problem constraints)
    # if input_grid.shape != (12,):
    #     raise ValueError("Input grid must be a 1D array with 12 elements.")

    # Define the size of each chunk
    chunk_size = 4
    
    # Calculate the start indices for each chunk
    start_idx_chunk1 = 0
    start_idx_chunk2 = chunk_size
    start_idx_chunk3 = 2 * chunk_size

    # Extract the three chunks using array slicing
    # Chunk 1: Elements from index 0 up to (but not including) index 4
    chunk_1 = input_grid[start_idx_chunk1 : start_idx_chunk2] 
    # Chunk 2: Elements from index 4 up to (but not including) index 8
    chunk_2 = input_grid[start_idx_chunk2 : start_idx_chunk3]
    # Chunk 3: Elements from index 8 up to the end of the array (index 12)
    chunk_3 = input_grid[start_idx_chunk3 : ] 

    # Construct the output grid by concatenating the chunks in the desired order:
    # second chunk (indices 4-7), then third chunk (indices 8-11), 
    # then first chunk (indices 0-3).
    output_grid = np.concatenate((chunk_2, chunk_3, chunk_1))

    # Return the newly constructed array
    return output_grid
```