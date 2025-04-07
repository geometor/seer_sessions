import numpy as np
from scipy.ndimage import label
from scipy.spatial.distance import cdist

"""
Transforms an input grid based on pattern and template regions using relative spatial mapping within bounding boxes.

The transformation identifies two distinct regions in the input grid:
1.  Pattern Region: Contains connected components of non-zero digits other than 8.
2.  Template Region: Contains connected components of the digit 8.

The transformation logic is as follows:
1.  Identify all connected components within the pattern region, noting the color (digit) and centroid of each component.
2.  Identify all connected components within the template region (all composed of the digit 8), noting the centroid of each component.
3.  Determine the overall bounding box for the pattern region and the template region.
4.  Normalize the centroid of each pattern component relative to the pattern region's bounding box.
5.  Normalize the centroid of each template component relative to the template region's bounding box.
6.  For each template component, find the pattern component whose normalized centroid (within its respective bounding box) is closest (using Euclidean distance).
7.  Create an output grid by copying the input grid.
8.  For each template component in the output grid, replace its cells (originally 8) with the color of the closest pattern component identified in the previous step.
9.  The pattern region and background (0s) remain unchanged in the output grid.
"""

def find_connected_components(grid: np.ndarray, target_value: int = None, mask: np.ndarray = None) -> list[dict]:
    """
    Finds connected components in a grid for a specific value or based on a mask.
    Uses 8-connectivity.

    Args:
        grid: The input NumPy array.
        target_value: The integer value to find components of. If None, use mask.
        mask: A boolean mask where True indicates cells belonging to potential components. If None, use target_value.

    Returns:
        A list of dictionaries, each representing a component with:
          'coords': list of (row, col) tuples.
          'centroid': (row, col) tuple for the component's center of mass.
          'color': The integer color/value of the component.
    """
    if mask is None and target_value is not None:
        binary_mask = (grid == target_value)
    elif mask is not None:
        binary_mask = mask
    else:
        raise ValueError("Either target_value or mask must be provided.")

    # Define 8-connectivity structure
    structure = np.ones((3, 3), dtype=bool)
    
    # Label connected components
    labeled_array, num_features = label(binary_mask, structure=structure)
    
    components = []
    if num_features > 0:
        component_indices = np.arange(1, num_features + 1)
        for i in component_indices:
            # Get coordinates for the current component
            coords_raw = np.argwhere(labeled_array == i)
            if coords_raw.size > 0:
                coords = [tuple(coord) for coord in coords_raw]
                # Calculate centroid (center of mass)
                centroid = tuple(np.mean(coords_raw, axis=0))
                
                component_info = {
                    'coords': coords,
                    'centroid': centroid,
                }
                # Determine component color
                if target_value is not None:
                   component_info['color'] = target_value
                elif mask is not None: # Assumes single color per component if using mask
                   first_coord = coords[0]
                   component_info['color'] = grid[first_coord]
                else: # Should not happen based on initial check
                    component_info['color'] = -1 # Error indicator

                components.append(component_info)
                
    return components

def get_bounding_box(coords_list: list[tuple]) -> tuple | None:
    """Calculates the bounding box (min_r, min_c, max_r, max_c) for a list of coordinates."""
    if not coords_list:
        return None
    rows, cols = zip(*coords_list)
    min_r, max_r = min(rows), max(rows)
    min_c, max_c = min(cols), max(cols)
    return min_r, min_c, max_r, max_c

def normalize_centroid(centroid: tuple, bbox: tuple) -> tuple | None:
    """Normalizes a centroid relative to a bounding box."""
    min_r, min_c, max_r, max_c = bbox
    centroid_r, centroid_c = centroid
    
    height = max_r - min_r
    width = max_c - min_c
    
    # Handle cases where bounding box has zero height or width
    norm_r = 0.5 if height == 0 else (centroid_r - min_r) / height
    norm_c = 0.5 if width == 0 else (centroid_c - min_c) / width
    
    # Clamp values between 0 and 1 just in case centroid is exactly on min/max boundary
    # Although division handles this, explicit clamp adds robustness.
    norm_r = max(0.0, min(1.0, norm_r))
    norm_c = max(0.0, min(1.0, norm_c))

    return norm_r, norm_c


def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies the pattern-template transformation to the input grid using
    bounding box normalization for spatial mapping.
    """
    # Convert input to numpy array for efficient processing
    grid = np.array(input_grid, dtype=int)
    output_grid = np.copy(grid)
    rows, cols = grid.shape

    # --- 1. Identify Pattern Components ---
    pattern_components = []
    all_pattern_coords = []
    unique_colors = np.unique(grid)
    pattern_colors = [c for c in unique_colors if c != 0 and c != 8]

    for color in pattern_colors:
        components_for_color = find_connected_components(grid, target_value=color)
        pattern_components.extend(components_for_color)
        for comp in components_for_color:
            all_pattern_coords.extend(comp['coords'])

    # --- 2. Identify Template Components ---
    template_components = find_connected_components(grid, target_value=8)
    all_template_coords = []
    for comp in template_components:
        all_template_coords.extend(comp['coords'])

    # --- Handle edge cases: No pattern or no template ---
    if not pattern_components or not template_components:
        return output_grid.tolist() 

    # --- 3. Calculate Bounding Boxes ---
    pattern_bbox = get_bounding_box(all_pattern_coords)
    template_bbox = get_bounding_box(all_template_coords)

    # --- Handle edge case: Bounding box calculation failed (empty regions) ---
    # This check is somewhat redundant due to the component check above, but safe.
    if pattern_bbox is None or template_bbox is None:
         return output_grid.tolist()

    # --- 4 & 5. Calculate and Normalize Centroids within Bounding Boxes ---
    pattern_centroids_norm = []
    for comp in pattern_components:
        norm_centroid = normalize_centroid(comp['centroid'], pattern_bbox)
        if norm_centroid: # Ensure normalization succeeded
             pattern_centroids_norm.append(norm_centroid)
        else: # Should not happen if components exist
            return output_grid.tolist() # Or handle error appropriately
            
    template_centroids_norm = []
    for comp in template_components:
        norm_centroid = normalize_centroid(comp['centroid'], template_bbox)
        if norm_centroid: # Ensure normalization succeeded
            template_centroids_norm.append(norm_centroid)
        else: # Should not happen if components exist
             return output_grid.tolist() # Or handle error appropriately

    # Convert lists of normalized centroids to NumPy arrays for cdist
    pattern_centroids_norm_np = np.array(pattern_centroids_norm)
    template_centroids_norm_np = np.array(template_centroids_norm)
    
    # Ensure we have the same number of normalized centroids as components
    if len(pattern_centroids_norm_np) != len(pattern_components) or \
       len(template_centroids_norm_np) != len(template_components):
        # This indicates an issue during normalization, potentially zero-sized bbox for a component?
        # Though handled in normalize_centroid, add a safety return.
        print("Warning: Mismatch between components and normalized centroids.") 
        return output_grid.tolist()


    # --- 6. Map Template Components to Pattern Components ---
    # Compute pairwise distances between normalized template and pattern centroids
    distances = cdist(template_centroids_norm_np, pattern_centroids_norm_np)

    # Find the index of the closest pattern component for each template component
    closest_pattern_indices = np.argmin(distances, axis=1)

    # --- 7. Apply Color Transformation ---
    # Iterate through each template component and apply the mapped color
    for i, template_comp in enumerate(template_components):
        # Get the index of the closest pattern component
        pattern_idx = closest_pattern_indices[i]
        # Get the color of that pattern component
        mapped_color = pattern_components[pattern_idx]['color']
        
        # Update the output grid for all coordinates of the current template component
        for r, c in template_comp['coords']:
            output_grid[r, c] = mapped_color

    # --- 8. Finalize ---
    # Convert the final numpy array back to a list of lists
    return output_grid.tolist()
