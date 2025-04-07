```python
"""
Transforms an input grid by identifying pattern components (non-zero, non-8 digits) and template components (digit 8). It maps each template component to the spatially closest pattern component based on the Euclidean distance between their normalized centroids (normalized by overall grid dimensions). The template components in the output grid are then filled with the color of their corresponding mapped pattern component.
"""

import numpy as np
from scipy.ndimage import label, center_of_mass
from scipy.spatial.distance import cdist
import math # Added math import

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
        # Calculate centroids using scipy's center_of_mass for potentially better handling
        # Needs the original grid for color determination if using a generic mask
        # Index needs to be a list or tuple for versions >= 1.9
        component_indices = list(range(1, num_features + 1)) # Ensure it's a list
        
        # Calculate geometric centroids (ignoring grid values for position)
        centroids = center_of_mass(input=binary_mask, labels=labeled_array, index=component_indices)
        
        # If only one component, center_of_mass returns a tuple, not a list of tuples
        if num_features == 1:
             centroids = [centroids] # Make it a list containing the single tuple

        for i, centroid_coords in enumerate(centroids):
            component_label = component_indices[i] # The actual label value (1-based)
            # Get coordinates for the current component
            coords_raw = np.argwhere(labeled_array == component_label)
            if coords_raw.size > 0:
                coords = [tuple(coord) for coord in coords_raw]                
                
                component_info = {
                    'coords': coords,
                    'centroid': centroid_coords, # Use calculated centroid
                }
                # Determine component color
                if target_value is not None:
                   component_info['color'] = target_value
                elif mask is not None: # Assumes single color per component if using mask
                   # Get color from the first coordinate of the component in the original grid
                   first_coord = coords[0] 
                   component_info['color'] = grid[first_coord]
                else: # Should not happen based on initial check
                    component_info['color'] = -1 # Error indicator

                components.append(component_info)
                
    return components


def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies the pattern-template transformation using normalized centroid mapping.

    Args:
        input_grid: A 2D list of integers representing the input grid.

    Returns:
        A 2D list of integers representing the transformed output grid.
    """
    # Convert input to numpy array for efficient processing
    grid = np.array(input_grid, dtype=int)
    output_grid = np.copy(grid)
    rows, cols = grid.shape

    # --- 1. Identify Pattern Components ---
    pattern_components = []
    # Identify unique colors in the potential pattern region (non-zero, not 8)
    unique_colors = np.unique(grid)
    pattern_colors = [c for c in unique_colors if c != 0 and c != 8]

    # Find connected components for each pattern color
    for color in pattern_colors:
        components_for_color = find_connected_components(grid, target_value=color)
        pattern_components.extend(components_for_color)

    # --- 2. Identify Template Components ---
    template_components = find_connected_components(grid, target_value=8)

    # --- 3. Handle edge cases: No pattern or no template ---
    if not pattern_components or not template_components:
        # If either region is missing, no transformation can be applied
        return output_grid.tolist() 

    # --- 4. Calculate Normalized Centroids ---
    # Avoid division by zero if rows or cols is 1 (or 0, though unlikely)
    norm_rows = rows if rows > 0 else 1
    norm_cols = cols if cols > 0 else 1
    
    # Ensure centroids are valid numbers before normalization
    pattern_centroids = np.array([comp['centroid'] for comp in pattern_components if not (math.isnan(comp['centroid'][0]) or math.isnan(comp['centroid'][1]))])
    template_centroids = np.array([comp['centroid'] for comp in template_components if not (math.isnan(comp['centroid'][0]) or math.isnan(comp['centroid'][1]))])

    # Check if filtering removed all components
    if pattern_centroids.shape[0] == 0 or template_centroids.shape[0] == 0:
         print("Warning: Valid centroids not found for all components.")
         return output_grid.tolist() # Cannot proceed without centroids

    # Apply normalization
    pattern_centroids_norm = pattern_centroids / [norm_rows, norm_cols]
    template_centroids_norm = template_centroids / [norm_rows, norm_cols]
    
    # Make sure the number of normalized centroids matches the filtered component lists
    valid_pattern_components = [comp for comp in pattern_components if not (math.isnan(comp['centroid'][0]) or math.isnan(comp['centroid'][1]))]
    valid_template_components = [comp for comp in template_components if not (math.isnan(comp['centroid'][0]) or math.isnan(comp['centroid'][1]))]

    # --- 5. Map Template Components to Pattern Components ---
    # Compute pairwise distances between normalized template and pattern centroids
    # shape: (num_template_components, num_pattern_components)
    distances = cdist(template_centroids_norm, pattern_centroids_norm)

    # Find the index of the closest pattern component for each template component
    # shape: (num_template_components,)
    closest_pattern_indices = np.argmin(distances, axis=1)

    # --- 6. Apply Color Transformation ---
    # Iterate through each *valid* template component and apply the mapped color
    for i, template_comp in enumerate(valid_template_components):
        # Get the index of the closest *valid* pattern component
        pattern_idx = closest_pattern_indices[i]
        # Get the color of that pattern component from the filtered list
        mapped_color = valid_pattern_components[pattern_idx]['color']
        
        # Update the output grid for all coordinates of the current template component
        for r, c in template_comp['coords']:
            # Check bounds just in case, though coords should be valid
            if 0 <= r < rows and 0 <= c < cols:
                output_grid[r, c] = mapped_color

    # Convert the final numpy array back to a list of lists
    return output_grid.tolist()
```