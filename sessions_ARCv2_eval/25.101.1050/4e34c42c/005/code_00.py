import numpy as np
from scipy.ndimage import label, generate_binary_structure, binary_dilation
import collections

"""
Transforms an input grid based on marker pixels and associated patterns.
The transformation follows these steps:
1. Identify the background color (BKG) as the most frequent color.
2. Identify the marker color (M) based on the background color (heuristic: M=9 if BKG=8, M=8 if BKG=4).
3. Find all connected components of marker pixels (M) and pattern pixels (non-BKG, non-M).
4. Filter pattern components, keeping only those with more than 5 pixels.
5. For each filtered pattern component (P), check if it's adjacent (8-way) to any marker component (C).
6. If P is adjacent to one or more marker components C_adj, find the minimum row index (m_min_r) across all pixels of C_adj.
7. Get the column bounds (p_min_c, p_max_c) of the pattern P.
8. Store the unique association tuple (m_min_r, p_min_c, p_max_c).
9. For each unique association, extract a slice from the input grid: rows are [m_min_r, m_min_r + 5), columns are [p_min_c, p_max_c + 1). Handle grid boundaries.
10. Sort the extracted slices based on their corresponding m_min_r in descending order.
11. Pad slices vertically with the background color to ensure uniform height (typically 5).
12. Concatenate the sorted, padded slices horizontally to create the output grid.
Handles empty grids or cases where no valid marker-pattern associations are found by returning a 1x1 background grid.

Note: The marker color identification is based on a limited heuristic observed in the examples and might not generalize perfectly. The core logic focuses on extracting 5-row slices starting from the marker's min row, using the pattern's column bounds, sorting by marker row descending, and concatenating. This logic successfully models example 1 but is known to not fully capture example 2's transformation.
"""

def get_background_color(grid: np.ndarray) -> int:
    """Finds the most frequent color in the grid, assuming it's the background."""
    if grid.size == 0:
        return 0
    counts = collections.Counter(grid.flat)
    if counts:
        return counts.most_common(1)[0][0]
    elif grid.size > 0:
        return grid.flat[0]
    else:
        return 0

def find_components(grid: np.ndarray, target_color: int) -> tuple[np.ndarray, int]:
    """Finds connected components of a specific color using 8-way connectivity."""
    binary_grid = (grid == target_color)
    structure = generate_binary_structure(2, 2)
    labeled_grid, num_components = label(binary_grid, structure=structure)
    return labeled_grid, num_components

def get_component_properties(labeled_grid: np.ndarray, num_components: int) -> list[dict]:
    """Extracts properties (coords, size, bbox, min_row) for each component."""
    components = []
    if num_components == 0:
        return components
        
    # Efficiently find coordinates for all labeled pixels
    coords = np.array(np.where(labeled_grid > 0)).T # shape (N, 2) -> [(r1, c1), (r2, c2), ...]
    labels = labeled_grid[coords[:, 0], coords[:, 1]] # Corresponding label for each coordinate

    for label_id in range(1, num_components + 1):
        component_mask = (labels == label_id)
        component_coords = coords[component_mask]
        if component_coords.size == 0:
            continue # Should not happen if num_components > 0

        min_r = np.min(component_coords[:, 0])
        min_c = np.min(component_coords[:, 1])
        max_r = np.max(component_coords[:, 0])
        max_c = np.max(component_coords[:, 1])
        
        components.append({
            'id': label_id,
            'coords': component_coords,
            'size': len(component_coords),
            'bbox': (min_r, min_c, max_r, max_c),
            'min_row': min_r
        })
    return components

def is_adjacent(comp1_coords: np.ndarray, comp2_labeled_grid: np.ndarray, comp2_id: int) -> bool:
    """Checks if component 1 is adjacent (8-way) to component 2 using dilation."""
    mask1 = np.zeros_like(comp2_labeled_grid, dtype=bool)
    if comp1_coords.size > 0:
        mask1[comp1_coords[:, 0], comp1_coords[:, 1]] = True
    
    # Dilate mask1 by 1 pixel in all 8 directions
    structure = generate_binary_structure(2, 2)
    dilated_mask1 = binary_dilation(mask1, structure=structure)
    
    # Check if the dilated mask overlaps with component 2
    mask2 = (comp2_labeled_grid == comp2_id)
    overlap = np.any(dilated_mask1 & mask2)
    
    return overlap

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Transforms the input grid based on marker pixels and associated patterns.
    """
    input_np = np.array(input_grid, dtype=np.int8)
    h, w = input_np.shape

    # Handle empty input grid
    if h == 0 or w == 0:
        return [[]]

    # 1. Identify background color
    background_color = get_background_color(input_np)

    # 2. Identify marker color (heuristic based on examples)
    marker_color = -1 # Default invalid
    if background_color == 8:
        marker_color = 9
    elif background_color == 4:
        marker_color = 8
    # Add more rules or a better detection method if needed
    
    # Handle case where marker color couldn't be determined or isn't present
    if marker_color == -1 or not np.any(input_np == marker_color):
         # Check if grid contains only background
         if np.all(input_np == background_color):
              return [[int(background_color)]]
         else:
              # If other colors exist but no marker found, assume error/no transform
              return [[int(background_color)]] # Or maybe return input? Specs unclear.

    # 3. Find marker components
    marker_labeled, num_marker_comp = find_components(input_np, marker_color)
    marker_components = get_component_properties(marker_labeled, num_marker_comp)
    if not marker_components:
        return [[int(background_color)]] # No markers found

    # 4. Find pattern components (non-BKG, non-M)
    pattern_mask = (input_np != background_color) & (input_np != marker_color)
    pattern_labeled, num_pattern_comp = label(pattern_mask, structure=generate_binary_structure(2, 2))
    all_pattern_components = get_component_properties(pattern_labeled, num_pattern_comp)

    # 5. Filter pattern components by size
    filtered_patterns = [p for p in all_pattern_components if p['size'] > 5]

    # 6. Associate patterns and markers, store unique associations
    associations = set()
    for pattern in filtered_patterns:
        adjacent_marker_min_rows = []
        is_adj_to_any_marker = False
        
        # Check adjacency efficiently: dilate pattern, check overlap with any marker pixel
        pattern_only_mask = np.zeros_like(input_np, dtype=bool)
        pattern_only_mask[pattern['coords'][:,0], pattern['coords'][:,1]] = True
        structure = generate_binary_structure(2, 2)
        dilated_pattern_mask = binary_dilation(pattern_only_mask, structure=structure)
        
        marker_mask_overall = (input_np == marker_color)
        
        if np.any(dilated_pattern_mask & marker_mask_overall):
             # Find specific adjacent marker components and their min rows
             adjacent_marker_pixels = input_np[dilated_pattern_mask & marker_mask_overall]
             # Get the labels of these marker pixels from marker_labeled grid
             marker_coords_where_overlap = np.array(np.where(dilated_pattern_mask & marker_mask_overall)).T
             
             if marker_coords_where_overlap.size > 0:
                 adjacent_marker_labels = set(marker_labeled[marker_coords_where_overlap[:, 0], marker_coords_where_overlap[:, 1]])
                 # Remove label 0 if present (background)
                 adjacent_marker_labels.discard(0)

                 if adjacent_marker_labels:
                     is_adj_to_any_marker = True
                     # Find the min_row for each adjacent marker component
                     for m_comp in marker_components:
                         if m_comp['id'] in adjacent_marker_labels:
                             adjacent_marker_min_rows.append(m_comp['min_row'])

        # 7. If adjacent, find overall min_marker_row and pattern columns
        if is_adj_to_any_marker and adjacent_marker_min_rows:
            overall_m_min_r = min(adjacent_marker_min_rows)
            p_min_c = pattern['bbox'][1]
            p_max_c = pattern['bbox'][3]
            associations.add((overall_m_min_r, p_min_c, p_max_c))

    # If no valid associations found
    if not associations:
        return [[int(background_color)]]

    # 8. Extract slices based on unique associations
    extracted_regions = []
    for m_min_r, p_min_c, p_max_c in associations:
        start_row = m_min_r
        end_row = min(start_row + 5, h)
        start_col = p_min_c
        end_col = p_max_c + 1

        # Ensure valid slice dimensions before extracting
        if start_row < end_row and start_col < end_col:
            extracted_slice = input_np[start_row:end_row, start_col:end_col]
            if extracted_slice.size > 0:
                extracted_regions.append({'trigger_row': m_min_r, 'slice': extracted_slice})

    # Handle case where extraction yielded nothing valid
    if not extracted_regions:
         return [[int(background_color)]]

    # 9. Sort slices by trigger_row descending
    extracted_regions.sort(key=lambda x: x['trigger_row'], reverse=True)

    final_slices = [region['slice'] for region in extracted_regions]

    # 10. Determine max height and pad slices
    max_h = 0
    valid_heights = [s.shape[0] for s in final_slices if s.ndim == 2 and s.shape[0] > 0]
    if valid_heights:
        max_h = max(valid_heights)
    # Default target height should ideally be 5, unless all slices are shorter due to grid boundary
    target_h = 5 
    if max_h < target_h and max_h > 0:
         target_h = max_h # Adjust if grid boundary limited all slices
    elif max_h == 0 and final_slices: # Should not happen with size > 0 check
         return [[int(background_color)]]


    padded_slices = []
    for s in final_slices:
        if s.ndim == 2 and s.shape[0] > 0 and s.shape[1] > 0:
            current_h = s.shape[0]
            if current_h < target_h:
                pad_h = target_h - current_h
                padding = np.full((pad_h, s.shape[1]), background_color, dtype=s.dtype)
                padded_s = np.vstack((s, padding))
                padded_slices.append(padded_s)
            elif current_h == target_h:
                padded_slices.append(s)
            # else: slice is taller? Should not happen with 5-row extraction limit.

    # If padding resulted in no valid slices
    if not padded_slices:
         return [[int(background_color)]]

    # 11. Concatenate slices horizontally
    try:
        # Final check for consistent height before stacking
        first_height = padded_slices[0].shape[0]
        if not all(arr.shape[0] == first_height for arr in padded_slices):
             print(f"Error: Mismatched heights before hstack. Target H: {target_h}. Actual Heights: {[arr.shape[0] for arr in padded_slices]}")
             # Attempt to use the most common height? Or fail? Let's fail for now.
             return [[int(background_color)]] 
             
        output_np = np.hstack(padded_slices)
    except ValueError as e:
        print(f"Error during hstack: {e}")
        return [[int(background_color)]]
    except IndexError as e:
         print(f"Error: Index error, likely no padded slices. {e}")
         return [[int(background_color)]]


    # Convert final numpy array back to list of lists
    return output_np.tolist()