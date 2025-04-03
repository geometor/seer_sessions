```python
"""
Transforms a 1-dimensional input sequence of pixels based on runs of colors.
Iterate through the input sequence, identifying contiguous runs of pixels with the same color.
If a run consists of white pixels (0), keep them white in the output.
If a run consists of maroon pixels (9), change the color based on the parity of the length of the run:
- If the run length is even, change the pixels in the run to blue (1).
- If the run length is odd, change the pixels in the run to azure (8).
The output sequence has the same length as the input sequence.
"""

# No external library imports are needed for this task.

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid: A list or tuple representing the 1D input sequence.

    Returns:
        A list representing the transformed 1D output sequence.
    """
    # Ensure input_grid is treated as a list to allow modification if needed,
    # and create a mutable copy for the output.
    input_sequence = list(input_grid)
    output_grid = list(input_sequence)
    n = len(input_sequence)
    
    # Initialize index to iterate through the sequence
    i = 0
    while i < n:
        # Get the color of the current pixel
        current_color = input_sequence[i]
        
        # Find the end of the current run
        start_index = i
        j = i + 1
        while j < n and input_sequence[j] == current_color:
            j += 1
        
        # Calculate the length of the run
        run_length = j - start_index
        
        # Apply transformation logic if the run color is maroon (9)
        if current_color == 9:
            # Determine the output color based on run length parity
            # Blue (1) for even length, Azure (8) for odd length
            output_color = 1 if run_length % 2 == 0 else 8
            
            # Fill the corresponding segment in the output grid with the new color
            for k in range(start_index, j):
                output_grid[k] = output_color
                
        # If the color is white (0), no action is needed as the output_grid
        # was initialized as a copy of the input.
        
        # Move the index to the start of the next run
        i = j
        
    return output_grid

```