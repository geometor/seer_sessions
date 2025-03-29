```python
import copy
import numpy as np
from scipy.ndimage import label, find_objects

def transform(input_grid):
    """
    Transforms the input grid based on the following rules:
    1. All Gray (5) pixels in the input change to Yellow (4) in the output.
    2. Identify connected components of Orange (7) pixels in the input using orthogonal adjacency.
    3. For each Orange component, check if any of its pixels are orthogonally adjacent to any pixel that was originally Gray (5).
    4. If an Orange component is adjacent to an original Gray pixel, change all pixels belonging to that component to Gray (5) in the output.
    5. Orange components not adjacent to any original Gray pixel remain Orange (7).
    6. All other pixels remain unchanged.
    The transformation checks neighbors and connectivity based on the *original* input grid.
    """

    # Convert input list of lists to numpy array for easier processing
    input_np = np.array(input_grid, dtype=int)
    height, width = input_np.shape

    # Create a deep copy to modify; convert this copy to numpy for modification
    # Using deepcopy first ensures the original list structure if needed later,
    # though we'll return a list derived from output_np.
    output_grid_list = copy.deepcopy(input_grid)
    output_np = np.array(output_grid_list, dtype=int)

    # --- Step 1 & Identify Original Gray Locations ---
    # Find coordinates of all original Gray pixels
    original_gray_coords = set()
    for r in range(height):
        for c in range(width):
            if input_np[r, c] == 5:
                # Rule 1: Change Gray to Yellow in the output
                output_np[r, c] = 4
                # Store the location for adjacency checks later
                original_gray_coords.add((r, c))

    # --- Step 2: Identify Orange Components ---
    # Create a mask for Orange pixels
    orange_mask = (input_np == 7)
    
    # Define connectivity structure (orthogonal only)
    structure = np.array([[0, 1, 0],
                          [1, 1, 1],
                          [0, 1, 0]], dtype=bool)
                          
    # Label connected components of Orange pixels
    # labeled_components will have 0 for background, and >0 integer labels for components
    labeled_components, num_components = label(orange_mask, structure=structure)

    # --- Step 3 & 4: Check Adjacency and Transform Orange Components ---
    # Get coordinates for each labeled component
    # find_objects returns slices, but we need actual coordinates per component
    component_coords = {}
    for r in range(height):
        for c in range(width):
            label_id = labeled_components[r, c]
            if label_id > 0: # Exclude background label 0
                if label_id not in component_coords:
                    component_coords[label_id] = []
                component_coords[label_id].append((r, c))

    # Iterate through each found Orange component
    for label_id in range(1, num_components + 1):
        component_pixels = component_coords.get(label_id, [])
        is_adjacent_to_original_gray = False
        
        # Check adjacency for this component
        for r, c in component_pixels:
            # Check orthogonal neighbors (Up, Down, Left, Right)
            for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                nr, nc = r + dr, c + dc
                # Check if neighbor is within bounds and was originally Gray
                if 0 <= nr < height and 0 <= nc < width:
                    if (nr, nc) in original_gray_coords:
                        is_adjacent_to_original_gray = True
                        break # Found adjacency for this pixel, no need to check other neighbors
            if is_adjacent_to_original_gray:
                break # Found adjacency for this component, no need to check other pixels in component

        # If the component is adjacent to an original Gray pixel, transform all its pixels
        if is_adjacent_to_original_gray:
            for r, c in component_pixels:
                output_np[r, c] = 5 # Change Orange to Gray

    # --- Step 5 & 6 ---
    # Pixels not matching Rule 1 or Rule 4 remain as they were in the initial deep copy.
    # This includes non-adjacent Orange components and all other colors (like White/0, Yellow/4 etc. from input).

    # Convert the final numpy array back to a list of lists
    output_grid = output_np.tolist()

    return output_grid
```