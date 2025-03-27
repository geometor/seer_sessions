```python
"""
The transformation takes an input grid and produces an output grid that is twice the height and twice the width of the input.
The output grid is composed of four quadrants, each the size of the input grid.
1. The Top-Left (TL) quadrant is identical to the input grid.
2. The Top-Right (TR) quadrant is the input grid rotated 90 degrees clockwise.
3. The Bottom-Left (BL) quadrant is the input grid rotated 90 degrees counter-clockwise.
4. The Bottom-Right (BR) quadrant is the input grid rotated 180 degrees.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by creating a 2x2 arrangement of rotated versions of the input.
    - TL: 0 degrees rotation
    - TR: 90 degrees clockwise rotation
    - BL: 90 degrees counter-clockwise rotation
    - BR: 180 degrees rotation

    Args:
        input_grid (list of list of int): The input grid.

    Returns:
        list of list of int: The transformed output grid.
    """
    # Convert input list of lists to a numpy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)
    
    # Get dimensions of the input grid
    input_height, input_width = input_np.shape
    
    # Calculate dimensions of the output grid
    output_height = input_height * 2
    output_width = input_width * 2
    
    # Initialize the output grid with zeros (or any placeholder)
    # Using the same dtype as input is good practice
    output_np = np.zeros((output_height, output_width), dtype=input_np.dtype)
    
    # --- Calculate the four quadrants ---
    
    # Top-Left (TL): 0 degrees rotation (original input)
    q_tl = input_np 
    
    # Top-Right (TR): 90 degrees clockwise rotation
    # np.rot90 rotates counter-clockwise by default, so k=-1 for clockwise
    q_tr = np.rot90(input_np, k=-1) 
    
    # Bottom-Left (BL): 90 degrees counter-clockwise rotation
    q_bl = np.rot90(input_np, k=1) 
    
    # Bottom-Right (BR): 180 degrees rotation
    q_br = np.rot90(input_np, k=2) 
    
    # --- Place the quadrants into the output grid ---
    
    # Place TL quadrant
    output_np[0:input_height, 0:input_width] = q_tl
    
    # Place TR quadrant
    output_np[0:input_height, input_width:output_width] = q_tr
    
    # Place BL quadrant
    output_np[input_height:output_height, 0:input_width] = q_bl
    
    # Place BR quadrant
    output_np[input_height:output_height, input_width:output_width] = q_br
    
    # Convert the final numpy array back to a list of lists
    output_grid = output_np.tolist()
    
    return output_grid

```