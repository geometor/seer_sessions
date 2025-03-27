```python
import numpy as np

def transform(input_grid):
    """
    Scales an input grid based on the count of its non-white pixels.

    1. Counts the total number of non-white (value > 0) pixels in the input 
       grid to determine the scaling factor `N`.
    2. Calculates the dimensions of the output grid as `H_out = H_in * N` and 
       `W_out = W_in * N`, where `H_in` and `W_in` are the height and width 
       of the input grid.
    3. Creates a new output grid initialized with white (0).
    4. Iterates through each pixel `(r, c)` of the input grid.
    5. For each input pixel with color `V`, it fills an `N x N` block in the 
       output grid starting at `(r * N, c * N)` with the color `V`. If `V` is 
       white (0), the corresponding `N x N` block in the output grid remains 
       white.
    6. Returns the generated output grid.
    """

    # Convert input list of lists to a numpy array for easier processing
    input_np = np.array(input_grid, dtype=int)
    
    # Get input dimensions
    H_in, W_in = input_np.shape

    # Count non-white (non-zero) pixels to determine the scale factor N
    N = np.count_nonzero(input_np)

    # Handle edge case where there are no non-white pixels (though not in examples)
    # If N is 0, perhaps return the original grid or an empty one.
    # Based on examples, N is expected to be > 0. Let's assume N > 0.
    # If N was 0, H_out and W_out would be 0, which might cause issues.
    # For robustness, if N=0, maybe return the input grid? Let's stick to the observed pattern.
    if N == 0:
        # Or potentially return an empty grid: np.array([[]], dtype=int).tolist()
        # Based on the examples, N is always > 0, so this might not be necessary for ARC.
        # Let's proceed assuming N > 0 as per the derived rule.
        # If this assumption breaks, we can revisit.
        pass # Continue assuming N > 0

    # Calculate output dimensions
    H_out = H_in * N
    W_out = W_in * N

    # Create the output grid, initialized with white (0)
    output_np = np.zeros((H_out, W_out), dtype=int)

    # Iterate through each pixel of the input grid
    for r in range(H_in):
        for c in range(W_in):
            # Get the color of the current input pixel
            color = input_np[r, c]
            
            # If the color is not white (0)
            if color != 0:
                # Calculate the top-left coordinates for the block in the output grid
                start_row = r * N
                start_col = c * N
                
                # Fill the N x N block in the output grid with the color
                # Slicing: [start_row : end_row, start_col : end_col]
                # end_row = start_row + N
                # end_col = start_col + N
                output_np[start_row : start_row + N, start_col : start_col + N] = color

    # Convert the output numpy array back to a list of lists for the expected format
    output_grid = output_np.tolist()

    return output_grid
```