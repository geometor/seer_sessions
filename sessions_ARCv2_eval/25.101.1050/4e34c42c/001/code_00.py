import numpy as np
from scipy.ndimage import label, generate_binary_structure
import collections

"""
Processes an input grid based on marker pixels (color 9). It identifies connected 
components of marker pixels. For each unique minimum row (`m_min_r`) associated 
with any marker component, it defines a potential 5-row high region starting 
from `m_min_r`. It then finds the horizontal bounding box of all non-background, 
non-marker pixels within those 5 rows (or fewer if near the grid bottom). 
This rectangular slice is extracted. 

These extracted slices are collected, ensuring duplicate regions (defined by 
start row and column bounds) are not added multiple times. The collected slices 
are then sorted based on the minimum row (`m_min_r`) of the marker component(s) 
that triggered their generation, in descending order. Finally, the sorted slices 
are padded (if necessary) to have the same height and concatenated horizontally 
to form the output grid. Handles edge cases like empty grids, grid boundaries, 
and missing markers or associated patterns.
"""

def get_background_color(grid: np.ndarray) -> int:
    """Finds the most frequent color in the grid, returning 0 as default."""
    if grid.size == 0:
        return 0 # Default background if grid is empty
    # Use collections.Counter for potentially faster counting on typical grids
    counts = collections.Counter(grid.flat)
    if counts:
         # most_common(1) returns list of tuples [(value, count)]
         return counts.most_common(1)[0][0]
    elif grid.size > 0:
         # Fallback if counter is empty but grid has elements (shouldn't happen)
         return grid.flat[0] 
    else:
         return 0 # Default

def find_components_and_min_rows(grid: np.ndarray, condition_func) -> list[int]:
    """
    Finds connected components satisfying a condition function and returns a list 
    of the minimum row index for each distinct component found.
    """
    binary_grid = condition_func(grid)
    # Use 8-way connectivity (diagnals included)
    structure = generate_binary_structure(2, 2) 
    labeled_grid, num_components = label(binary_grid, structure=structure)
    
    components_min_rows = []
    if num_components > 0:
        min_rows_per_label = {}
        # Iterate through the grid to find the minimum row for each label
        # This avoids finding all coordinates if only min_row is needed
        for r in range(labeled_grid.shape[0]):
            for c in range(labeled_grid.shape[1]):
                label_id = labeled_grid[r, c]
                if label_id > 0:
                    if label_id not in min_rows_per_label:
                        min_rows_per_label[label_id] = r
                    # Optimization: if we found the first row instance, 
                    # no need to update further for this label_id's min row.
                    # However, simpler just to let it find all first occurrences.
        
        components_min_rows = list(min_rows_per_label.values())
                 
    return components_min_rows # Returns a list of min_rows, one for each component

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Transforms the input grid based on marker pixels (color 9).
    Extracts 5-row high slices associated with marker components, sorts them 
    by the marker's minimum row (descending), and concatenates horizontally.
    """
    input_np = np.array(input_grid, dtype=np.int8)
    h, w = input_np.shape

    # Handle empty input grid
    if h == 0 or w == 0:
        return [[]]

    # Identify marker color (fixed at 9) and background color
    marker_color = 9
    background_color = get_background_color(input_np)

    # Find the minimum row for each marker component
    marker_component_min_rows = find_components_and_min_rows(input_np, lambda g: g == marker_color)
    
    # If no markers found, return a 1x1 background grid as per interpretation
    if not marker_component_min_rows:
         return [[int(background_color)]] 

    extracted_regions = []
    # Track processed regions defined by (start_row, col_min, col_max) to avoid duplicates
    processed_regions = set() 

    # Use unique min_rows associated with markers to define potential slice start rows
    unique_min_rows = sorted(list(set(marker_component_min_rows)))

    for m_min_r in unique_min_rows:
        
        # Define the row slice range (max 5 rows, respecting grid height)
        start_row = m_min_r
        end_row = min(start_row + 5, h) 
        
        # Consider only rows that actually exist in the grid
        if start_row >= h:
             continue
        
        # Get the data for the rows [start_row, end_row) across the full width
        row_slice_data = input_np[start_row:end_row, :]
        
        # Create a mask for non-background, non-marker pixels within this row slice
        pattern_mask = (row_slice_data != background_color) & (row_slice_data != marker_color)
        
        # Find the column indices where such pattern pixels exist
        pattern_cols_in_slice = np.where(pattern_mask)[1] # We only need column indices
        
        # If no pattern pixels found in these rows, this marker row doesn't yield a slice
        if pattern_cols_in_slice.size == 0:
            continue 
            
        # Determine the horizontal extent (min/max columns) of the pattern in this slice
        p_min_c = np.min(pattern_cols_in_slice)
        p_max_c = np.max(pattern_cols_in_slice)
        
        # Define the region identifier to check if we already extracted this exact slice
        region_id = (start_row, p_min_c, p_max_c)
        if region_id in processed_regions:
            continue # Skip duplicate region
        processed_regions.add(region_id)

        # Extract the final slice using defined rows and calculated pattern columns
        extracted_slice = input_np[start_row:end_row, p_min_c : p_max_c + 1]

        # Store the slice along with the marker row that triggered it (for sorting)
        # Ensure the slice is not empty before storing
        if extracted_slice.size > 0:
             extracted_regions.append({'trigger_row': m_min_r, 'slice': extracted_slice})

    # Sort the collected regions based on the marker row that triggered them, descending order
    extracted_regions.sort(key=lambda x: x['trigger_row'], reverse=True)

    # If no valid regions were extracted, return background grid
    if not extracted_regions:
         return [[int(background_color)]] 

    final_slices = [region['slice'] for region in extracted_regions]
    
    # Determine the target height (max height found among slices) for padding
    max_h = 0
    if final_slices:
        heights = [s.shape[0] for s in final_slices if s.ndim == 2] # Check shape exists
        if heights:
             max_h = max(heights)
        
    # Pad slices shorter than max_h at the bottom with the background color
    padded_slices = []
    for s in final_slices:
         # Ensure it's a valid 2D array before padding
        if s.ndim == 2 and s.shape[0] > 0 and s.shape[1] > 0:
            if s.shape[0] < max_h:
                pad_h = max_h - s.shape[0]
                # Create padding array
                padding = np.full((pad_h, s.shape[1]), background_color, dtype=s.dtype)
                # Stack original slice on top of padding
                padded_s = np.vstack((s, padding))
                padded_slices.append(padded_s)
            else:
                # Slice already has max height
                padded_slices.append(s)
        # Optionally handle cases where a slice might be empty or 1D? 
        # The extraction logic should prevent this if size > 0 check works.

    # If after padding, no valid slices remain, return background
    if not padded_slices:
         return [[int(background_color)]] 

    # Perform horizontal stacking (concatenation)
    try:
        output_np = np.hstack(padded_slices)
    except ValueError as e:
        # Catch potential errors during hstack (e.g., if somehow heights mismatch despite padding)
        print(f"Error during hstack: {e}")
        # Return a default error indicator or background grid
        return [[int(background_color)]]


    # Convert final numpy array back to list of lists
    return output_np.tolist()