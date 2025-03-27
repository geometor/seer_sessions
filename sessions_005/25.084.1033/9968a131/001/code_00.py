import numpy as np

"""
Transforms the input grid based on the following rules:
1. Iterate through each row of the input grid.
2. If the row index is even, the row remains unchanged in the output.
3. If the row index is odd:
    a. Find the smallest index k (k >= 1) where the color at input[row][k] has appeared before in that row (at index j < k).
    b. If no such k exists, the row remains unchanged.
    c. If k is found:
        i. If the repeating color input[row][k] is the same as the first color input[row][0], the segment from index 1 to k (inclusive) undergoes a right circular shift by one position. The rest of the row remains unchanged.
        ii. If the repeating color input[row][k] is different from the first color input[row][0], the segment from index 0 to k-1 (inclusive) undergoes a right circular shift by one position. The rest of the row remains unchanged.
"""

def transform(input_grid):
    """
    Applies the described transformation rule to the input grid.

    Args:
        input_grid (list[list[int]]): A 2D list representing the input grid.

    Returns:
        list[list[int]]: A 2D list representing the transformed output grid.
    """
    # Convert input to a NumPy array for easier slicing and manipulation
    input_np = np.array(input_grid, dtype=int)
    # Create a copy to modify, ensuring the original input is untouched
    output_grid = input_np.copy()
    height, width = input_np.shape

    # Iterate through each row with its index
    for r in range(height):
        # Only process odd-indexed rows (1, 3, 5, ...)
        if r % 2 == 1:
            first_repeat_k = -1 # Initialize index of first repeat
            # Search for the first index k >= 1 where the color repeats
            # Check input_np[r, k] against the slice input_np[r, 0:k]
            for k in range(1, width):
                current_val = input_np[r, k]
                # Check if the current value exists in the preceding part of the row
                if current_val in input_np[r, 0:k]:
                    first_repeat_k = k
                    break # Stop at the first occurrence

            # If a repeating element was found (first_repeat_k is not -1)
            if first_repeat_k != -1:
                k = first_repeat_k
                
                # Case 1: The repeating color is the same as the first color in the row
                if input_np[r, k] == input_np[r, 0]:
                    # Define the segment from index 1 to k (inclusive)
                    # Ensure k >= 1 to have a valid segment [1:k+1]
                    if k >= 1:
                        segment = input_np[r, 1 : k + 1]
                        # Perform right circular shift only if segment has elements
                        if segment.size > 0:
                            # Move last element to the first position
                            shifted_segment = np.concatenate(([segment[-1]], segment[:-1]))
                            # Update the output grid with the shifted segment
                            output_grid[r, 1 : k + 1] = shifted_segment
                            
                # Case 2: The repeating color is different from the first color
                else:
                    # Define the segment from index 0 to k-1 (inclusive)
                    segment = input_np[r, 0 : k]
                    # Perform right circular shift only if segment has elements
                    if segment.size > 0:
                        # Move last element to the first position
                        shifted_segment = np.concatenate(([segment[-1]], segment[:-1]))
                        # Update the output grid with the shifted segment
                        output_grid[r, 0 : k] = shifted_segment
                        
        # Even rows (r % 2 == 0) or rows with no relevant repeat remain unchanged
        # as output_grid started as a copy of input_np.

    # Convert the final NumPy array back to a list of lists for the expected output format
    return output_grid.tolist()