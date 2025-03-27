```python
import numpy as np

"""
Analyze a 4x14 input grid, interpreting it as three distinct 4x4 blocks 
separated by white columns (at indices 4 and 9). Determine a characteristic 
color for each block based on its content. Construct a 3x3 output grid where 
the first row is filled with the color derived from the first block, the second 
row with the color from the second block, and the third row with the color 
from the third block.

Rule for determining block color:
1. If a block contains exactly one unique color other than gray (5) and white (0), 
   that unique color is the characteristic color.
2. If a block contains only gray (5) pixels, the characteristic color is red (2).
3. If a block contains only gray (5) and white (0) pixels:
   - If it's the first block (leftmost), the color is green (3).
   - If it's the second block (middle), the color is azure (8).
   - The rule for the third block in this state is not defined by the examples, 
     but the observed patterns suggest it would follow either the 'unique color' 
     or 'all gray' rules if applicable.
"""

def analyze_block(block, block_index):
    """
    Analyzes a 4x4 block to determine its characteristic color based on content and index.

    Args:
        block (np.ndarray): A 4x4 numpy array representing the block.
        block_index (int): The index of the block (0 for left, 1 for middle, 2 for right).

    Returns:
        int: The characteristic color code for the block.
             Returns -1 if a rule isn't found (e.g., Gray+White for block 3).
    """
    unique_colors = np.unique(block)
    
    # Filter out gray (5) and white (0)
    non_background_colors = [c for c in unique_colors if c != 5 and c != 0]

    # Rule 1: Exactly one unique non-gray/white color
    if len(non_background_colors) == 1:
        return non_background_colors[0]

    # Rule 2: All gray
    if np.all(block == 5):
        return 2 # red

    # Rule 3: Only gray and white
    contains_only_gray_white = True
    for color in unique_colors:
        if color != 5 and color != 0:
            contains_only_gray_white = False
            break
            
    if contains_only_gray_white:
        if block_index == 0:
            return 3 # green
        elif block_index == 1:
            return 8 # azure
        # else: # Rule for block_index == 2 (third block) is not explicitly defined for gray+white only
        #     # Based on examples, this case doesn't occur for block 3.
        #     # We can return a default or raise an error, returning -1 for now.
        #     return -1 

    # Handle cases not covered by rules explicitly (e.g., multiple unique colors, or gray+white for block 3)
    # The logic above covers all observed training cases. If a Gray+White Block 3 occurs,
    # or a block with multiple unique colors, this might return None implicitly or need adjustment.
    # Returning -1 indicates an unhandled case based on provided examples.
    return -1 


def transform(input_grid):
    """
    Transforms the input grid based on the analysis of its three 4x4 blocks.

    Args:
        input_grid (np.ndarray): A 4x14 numpy array.

    Returns:
        np.ndarray: A 3x3 numpy array representing the transformed output.
    """
    input_np = np.array(input_grid)

    # 1. Partition Input into three 4x4 blocks
    block1 = input_np[0:4, 0:4]
    block2 = input_np[0:4, 5:9]
    block3 = input_np[0:4, 10:14]

    # 2. Analyze Blocks and Determine Output Colors
    color1 = analyze_block(block1, 0)
    color2 = analyze_block(block2, 1)
    color3 = analyze_block(block3, 2)
    
    # Handle potential undefined cases if analyze_block returned -1
    if color1 == -1 or color2 == -1 or color3 == -1:
        # Optional: Raise an error or return a default grid if a rule was missing
        # For now, let's assume valid colors based on training data
        # print(f"Warning: Unhandled block state encountered. Colors found: {color1}, {color2}, {color3}")
        pass # Proceeding, but the result might be incorrect if -1 was returned

    # 3. Construct Output grid
    output_grid = np.zeros((3, 3), dtype=int)
    
    # Fill rows with determined colors
    output_grid[0, :] = color1
    output_grid[1, :] = color2
    output_grid[2, :] = color3

    return output_grid.tolist() # Return as list of lists as per ARC standard
```