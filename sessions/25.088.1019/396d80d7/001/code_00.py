import numpy as np
from collections import Counter

"""
Transformation Rule:

1.  Identify the background color (most frequent color).
2.  Identify the two non-background colors present in the central pattern.
3.  Determine which of these two colors is the 'frame' color (adjacent to the background) and which is the 'fill' color (the other one).
4.  Create an output grid initialized as a copy of the input grid.
5.  Iterate through each pixel of the input grid.
6.  If a pixel is the background color and has at least one direct neighbor (up, down, left, right) with the 'frame' color, change this pixel's color in the output grid to the 'fill' color.
7.  Otherwise, the pixel retains its original color in the output grid.
"""

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.
    """
    # Convert input list of lists to a numpy array for easier manipulation
    input_array = np.array(input_grid, dtype=int)
    output_array = np.copy(input_array)
    rows, cols = input_array.shape

    # 1. Identify background color (most frequent)
    colors, counts = np.unique(input_array, return_counts=True)
    background_color = colors[np.argmax(counts)]

    # 2. Identify the two non-background colors
    non_background_colors = [c for c in colors if c != background_color]
    
    # Check if we have exactly two non-background colors as expected
    if len(non_background_colors) != 2:
        # Handle unexpected case, maybe return input or raise error
        # For now, assume the pattern holds based on examples
        print(f"Warning: Expected 2 non-background colors, found {len(non_background_colors)}. Proceeding with available colors.")
        if not non_background_colors: return input_grid # Cannot proceed
        # If only one, logic below might need adjustment, but let's try
        
    frame_color = -1 # Initialize with invalid value
    fill_color = -1  # Initialize with invalid value

    # 3. Determine frame and fill colors
    possible_frame_colors = set()
    for r in range(rows):
        for c in range(cols):
            color = input_array[r, c]
            if color in non_background_colors:
                # Check neighbors for background color
                for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                    nr, nc = r + dr, c + dc
                    # Check boundaries
                    if 0 <= nr < rows and 0 <= nc < cols:
                        if input_array[nr, nc] == background_color:
                            possible_frame_colors.add(color)
                            break # Found adjacent background, no need to check other neighbors for this cell

    # Based on examples, only one non-background color should be adjacent to background
    if len(possible_frame_colors) == 1:
         frame_color = list(possible_frame_colors)[0]
         # Fill color is the other non-background color
         for c in non_background_colors:
             if c != frame_color:
                 fill_color = c
                 break
    elif len(possible_frame_colors) == 2 and len(non_background_colors) == 2:
         # This case is ambiguous based on the rule description, but unlikely given examples.
         # If it occurs, we might need a more specific rule (e.g., which color appears more on the border?)
         # Let's arbitrarily pick one based on value, though this is a guess.
         print("Warning: Ambiguous frame/fill colors. Both touch background.")
         frame_color = min(non_background_colors) # Arbitrary choice
         fill_color = max(non_background_colors) # Arbitrary choice
    elif len(possible_frame_colors) == 0 and len(non_background_colors) > 0:
         # None touch background? Maybe the pattern is fully enclosed.
         # This violates the premise, but let's handle it. Assign arbitrarily.
         print("Warning: No non-background color touches background.")
         if len(non_background_colors) >= 1: frame_color = non_background_colors[0]
         if len(non_background_colors) >= 2: fill_color = non_background_colors[1]
         else: fill_color = frame_color # If only one non-bg color, it's both?
    elif not non_background_colors:
        print("Warning: No non-background colors found.")
        return input_grid # Nothing to transform
    else: # If only one non_bg color was found initially, and it touched background
        frame_color = list(possible_frame_colors)[0]
        fill_color = frame_color # Use the same color? The rule needs clarification here. Let's assume this for now.


    # Check if frame and fill colors were successfully assigned
    if frame_color == -1 or fill_color == -1:
        print("Error: Could not determine frame or fill color reliably.")
        return input_grid # Return original if colors couldn't be determined


    # 4. & 5. Iterate through grid and apply transformation
    for r in range(rows):
        for c in range(cols):
            # 6. Check if the current pixel is background
            if input_array[r, c] == background_color:
                # Check direct neighbors (up, down, left, right)
                has_frame_neighbor = False
                for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                    nr, nc = r + dr, c + dc
                    # Check boundaries
                    if 0 <= nr < rows and 0 <= nc < cols:
                        # Check if neighbor is the frame color
                        if input_array[nr, nc] == frame_color:
                            has_frame_neighbor = True
                            break # Found one, no need to check others
                
                # If it has a frame color neighbor, change the output pixel to fill color
                if has_frame_neighbor:
                    output_array[r, c] = fill_color
            # 7. Otherwise (pixel is not background, or is background but no frame neighbor), 
            # the output_array already has the correct original color from the copy.

    # Convert the result back to a list of lists
    return output_array.tolist()