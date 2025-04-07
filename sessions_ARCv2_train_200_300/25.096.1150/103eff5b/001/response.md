```python
"""
Transforms an input grid based on pattern and template regions.

The transformation identifies two distinct regions in the input grid:
1.  Pattern Region: Contains connected components of non-zero digits other than 8.
2.  Template Region: Contains connected components of the digit 8.

The transformation logic is as follows:
1.  Identify all connected components within the pattern region, noting the color (digit) of each component.
2.  Identify all connected components within the template region (all composed of the digit 8).
3.  Calculate a representative point (centroid) for each pattern component and each template component, normalized by the grid dimensions.
4.  For each template component, find the pattern component whose normalized centroid is closest (using Euclidean distance).
5.  Create an output grid by copying the input grid.
6.  For each template component in the output grid, replace its cells (originally 8) with the color of the closest pattern component identified in the previous step.
7.  The pattern region and background (0s) remain unchanged in the output grid.
"""

import numpy as np
from scipy.ndimage import label, center_of_mass
from scipy.spatial.distance import cdist

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
          'color': The integer color/value of the component (if target_value was used).
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
        # Calculate centroids (center_of_mass) for all components at once
        # Note: center_of_mass needs the original grid values if weighting is desired,
        # but here we just need the geometric center of the mask, so input=labeled_array works.
        # However, using binary_mask might be more direct for geometric center.
        # We calculate centroids individually to ensure correct association.
        
        component_indices = np.arange(1, num_features + 1)
        # centroids = center_of_mass(binary_mask, labeled_array, component_indices) # scipy < 1.9
        # centroids = center_of_mass(input=binary_mask, labels=labeled_array, index=component_indices) # scipy >= 1.9

        for i in component_indices:
            coords_raw = np.argwhere(labeled_array == i)
            if coords_raw.size > 0:
                # coords need to be list of tuples for consistency if used elsewhere
                coords = [tuple(coord) for coord in coords_raw]
                
                # Calculate centroid manually for robustness across scipy versions
                centroid = np.mean(coords_raw, axis=0)

                component_info = {
                    'coords': coords,
                    'centroid': tuple(centroid),
                }
                # If finding components of a specific value, store its color
                if target_value is not None:
                   component_info['color'] = target_value
                # If using a mask derived from multiple colors (pattern region),
                # determine color from the first coordinate. Assumes components are single-colored.
                elif mask is not None and target_value is None:
                   first_coord = coords[0]
                   component_info['color'] = grid[first_coord]

                components.append(component_info)
                
    return components


def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies the pattern-template transformation to the input grid.

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

    # --- Handle edge cases: No pattern or no template ---
    if not pattern_components or not template_components:
        # If either region is missing, no transformation can be applied
        return output_grid.tolist() 

    # --- 3. Calculate Normalized Centroids ---
    # Normalize centroids by grid dimensions for relative positioning
    pattern_centroids_norm = np.array([
        (comp['centroid'][0] / rows, comp['centroid'][1] / cols) 
        for comp in pattern_components
    ])
    template_centroids_norm = np.array([
        (comp['centroid'][0] / rows, comp['centroid'][1] / cols) 
        for comp in template_components
    ])

    # --- 4. Map Template Components to Pattern Components ---
    # Compute pairwise distances between normalized template and pattern centroids
    # shape: (num_template_components, num_pattern_components)
    distances = cdist(template_centroids_norm, pattern_centroids_norm)

    # Find the index of the closest pattern component for each template component
    # shape: (num_template_components,)
    closest_pattern_indices = np.argmin(distances, axis=1)

    # --- 5. Apply Color Transformation ---
    # Iterate through each template component and apply the mapped color
    for i, template_comp in enumerate(template_components):
        # Get the index of the closest pattern component
        pattern_idx = closest_pattern_indices[i]
        # Get the color of that pattern component
        mapped_color = pattern_components[pattern_idx]['color']
        
        # Update the output grid for all coordinates of the current template component
        for r, c in template_comp['coords']:
            output_grid[r, c] = mapped_color

    # Convert the final numpy array back to a list of lists
    return output_grid.tolist()
```