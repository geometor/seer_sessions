```python
import copy

"""
Transforms a 1D sequence of colors based on the following rule:
1. Identify the single non-white (non-zero) color present in the input sequence ('active_color').
2. Initialize the output sequence as a copy of the input sequence.
3. Iterate through the input sequence. For each pixel that matches the 'active_color':
    a. Check if this pixel is 'isolated', meaning its immediate left neighbor (if it exists) is white (0) AND its immediate right neighbor (if it exists) is white (0). Boundary pixels only need their single neighbor to be white.
    b. If the pixel is isolated:
        i. If its left neighbor exists and is white in the original input, change the color of the left neighbor in the output sequence to 'active_color'.
        ii. If its right neighbor exists and is white in the original input, change the color of the right neighbor in the output sequence to 'active_color'.
4. Return the modified output sequence. If no active_color is found, return the original input.
"""

def find_active_color(input_sequence):
    """Finds the unique non-zero color in the sequence."""
    active_color = 0
    for pixel in input_sequence:
        if pixel != 0:
            active_color = pixel
            break # Assume only one active color as per examples
    return active_color

def transform(input_sequence):
    """
    Applies the transformation rule to the input sequence.
    """
    # Find the active color
    active_color = find_active_color(input_sequence)
    if active_color == 0:
        # No transformation needed if no active color
        return copy.deepcopy(input_sequence)

    # Initialize output_sequence as a copy of the input
    output_sequence = copy.deepcopy(input_sequence)
    n = len(input_sequence)

    # Iterate through the input sequence to find isolated active pixels
    for i in range(n):
        # Check if the current pixel has the active color
        if input_sequence[i] == active_color:
            # Determine if the left side is isolated (white neighbor or boundary)
            is_left_isolated = (i == 0) or (input_sequence[i-1] == 0)

            # Determine if the right side is isolated (white neighbor or boundary)
            is_right_isolated = (i == n - 1) or (input_sequence[i+1] == 0)

            # If the pixel is isolated (both sides are white or boundary)
            if is_left_isolated and is_right_isolated:
                # Color the left neighbor in the output if it exists and was white
                if i > 0 and input_sequence[i-1] == 0:
                    output_sequence[i-1] = active_color
                # Color the right neighbor in the output if it exists and was white
                if i < n - 1 and input_sequence[i+1] == 0:
                    output_sequence[i+1] = active_color

    # Return the modified output sequence
    return output_sequence
```