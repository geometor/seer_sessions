import numpy as np
from scipy.ndimage import label, binary_fill_holes, generate_binary_structure
from collections import Counter

def analyze_example_fill_small_holes(input_grid_list, output_grid_list):
    input_grid = np.array(input_grid_list)
    output_grid = np.array(output_grid_list)
    height, width = input_grid.shape
    background_color = 0
    
    analysis = {}

    # 1. Find LCC and color C
    non_background_mask = input_grid != background_color
    if not np.any(non_background_mask):
        analysis['status'] = "No non-background pixels."
        analysis['lcc_color'] = background_color
        analysis['potential_holes'] = []
        analysis['small_holes_to_fill'] = []
        analysis['actual_changed_pixels'] = []
        analysis['match'] = np.array_equal(input_grid, output_grid)
        return analysis

    structure = generate_binary_structure(2, 1) # 4-connectivity for shape
    labeled_array, num_features = label(non_background_mask, structure=structure)
    
    if num_features == 0:
        analysis['status'] = "Labeled array found no features."
        analysis['lcc_color'] = background_color
        analysis['potential_holes'] = []
        analysis['small_holes_to_fill'] = []
        analysis['actual_changed_pixels'] = []
        analysis['match'] = np.array_equal(input_grid, output_grid)
        return analysis
        
    component_sizes = np.bincount(labeled_array.ravel())
    if len(component_sizes) > 0:
        component_sizes[0] = 0 # Ignore background label 0
    
    if np.all(component_sizes == 0):
         analysis['status'] = "No non-background components found after filtering label 0."
         analysis['lcc_color'] = background_color
         analysis['potential_holes'] = []
         analysis['small_holes_to_fill'] = []
         analysis['actual_changed_pixels'] = []
         analysis['match'] = np.array_equal(input_grid, output_grid)
         return analysis

    lcc_label = np.argmax(component_sizes)
    lcc_mask = (labeled_array == lcc_label)
    
    # Get LCC color C
    lcc_coords = np.argwhere(lcc_mask)
    if lcc_coords.size == 0:
         analysis['status'] = "LCC found but no coordinates matched the label."
         # This case should ideally not happen if lcc_label came from non-zero counts
         analysis['lcc_color'] = background_color
         analysis['potential_holes'] = []
         analysis['small_holes_to_fill'] = []
         analysis['actual_changed_pixels'] = []
         analysis['match'] = np.array_equal(input_grid, output_grid)
         return analysis
         
    lcc_color = int(input_grid[lcc_coords[0, 0], lcc_coords[0, 1]])
    analysis['lcc_color'] = lcc_color

    # 2. Apply binary_fill_holes
    # The structure for fill_holes defines connectivity of holes, default is 1 (4-way)
    filled_mask = binary_fill_holes(lcc_mask, structure=structure)

    # 3. Identify potential hole pixels P
    potential_hole_pixels_mask = filled_mask & ~lcc_mask
    
    # 4. Label components in P
    hole_structure = generate_binary_structure(2, 1) # 4-connectivity for holes
    labeled_holes, num_hole_features = label(potential_hole_pixels_mask, structure=hole_structure)
    
    analysis['potential_holes'] = []
    if num_hole_features > 0:
        hole_coords = np.argwhere(potential_hole_pixels_mask)
        hole_labels = labeled_holes[potential_hole_pixels_mask]
        component_sizes = Counter(hole_labels)
        
        unique_hole_labels = sorted(component_sizes.keys())

        for h_label in unique_hole_labels:
            coords = tuple(map(tuple, hole_coords[hole_labels == h_label]))
            size = component_sizes[h_label]
            analysis['potential_holes'].append({
                "label": h_label,
                "coords": coords,
                "size": size
            })
            
    # 5. Identify small holes to fill (size <= 2)
    small_holes_to_fill_coords = []
    for hole in analysis['potential_holes']:
        if hole['size'] <= 2:
            small_holes_to_fill_coords.extend(hole['coords'])
    analysis['small_holes_to_fill_coords'] = sorted(small_holes_to_fill_coords) # Sort for comparison

    # 6. Find actual changed pixels
    diff_mask = (input_grid != output_grid) & (input_grid == background_color)
    actual_changed_coords = sorted(tuple(map(tuple, np.argwhere(diff_mask)))) # Sort for comparison
    analysis['actual_changed_pixels'] = actual_changed_coords
    
    # 7. Compare
    analysis['match'] = (analysis['small_holes_to_fill_coords'] == analysis['actual_changed_pixels'])
    analysis['status'] = "Analysis complete."

    return analysis

# Example 1
input1 = [[0,0,0,0,0,0,0,0],[0,1,1,1,1,1,1,0],[0,1,1,1,1,1,1,0],[0,1,1,1,1,1,1,0],[0,1,1,1,1,1,1,0],[0,1,1,1,0,0,1,0],[0,1,1,1,1,1,1,0],[0,0,0,0,0,0,0,0]]
output1 = [[0,0,0,0,0,0,0,0],[0,1,1,1,1,1,1,0],[0,1,1,1,1,1,1,0],[0,1,1,1,1,1,1,0],[0,1,1,1,1,1,1,0],[0,1,1,1,1,1,1,0],[0,1,1,1,1,1,1,0],[0,0,0,0,0,0,0,0]]
print("Example 1 Analysis:")
print(analyze_example_fill_small_holes(input1, output1))

# Example 2
input2 = [[0,0,0,0,0,0,0,0],[0,6,0,0,6,6,6,0],[0,6,0,0,0,0,6,0],[0,6,0,0,0,0,6,0],[0,6,0,0,0,0,6,0],[0,6,0,0,0,0,6,0],[0,6,6,6,6,6,6,0],[0,0,0,0,0,0,0,0]]
output2 = [[0,0,0,0,0,0,0,0],[0,6,6,6,6,6,6,0],[0,6,0,0,0,0,6,0],[0,6,0,0,0,0,6,0],[0,6,0,0,0,0,6,0],[0,6,0,0,0,0,6,0],[0,6,6,6,6,6,6,0],[0,0,0,0,0,0,0,0]]
print("\nExample 2 Analysis:")
print(analyze_example_fill_small_holes(input2, output2))

# Example 3
input3 = [[0,0,0,0,0,0,0,0],[3,3,3,3,3,0,3,3],[3,3,3,3,3,3,0,3],[3,3,0,3,3,3,3,3],[3,3,3,3,3,3,3,3],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0]]
output3 = [[0,0,0,0,0,0,0,0],[3,3,3,3,3,3,3,3],[3,3,3,3,3,3,3,3],[3,3,3,3,3,3,3,3],[3,3,3,3,3,3,3,3],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0]]
print("\nExample 3 Analysis:")
print(analyze_example_fill_small_holes(input3, output3))
