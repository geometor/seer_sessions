"""
1.  **Identify** all connected regions of blue (1) pixels and yellow (4) pixels in the input grid. Consider pixels connected if they are orthogonally or diagonally adjacent.
2.  **Iterate** through each identified yellow region.
3.  **Check** if the yellow region is adjacent to *any* blue region. Adjacency includes orthogonal and diagonal neighbors.
4.  If a yellow region is adjacent to *any* blue region, change *all* pixels within that yellow region to blue (1).
5.  If a yellow region is *not* adjacent to any blue region, it remains unchanged.
"""

import numpy as np
from scipy.ndimage import label, find_objects

def get_regions(grid, color):
    """Finds connected regions of a specific color."""
    colored_grid = (grid == color).astype(int)
    labeled_grid, num_labels = label(colored_grid)
    regions = find_objects(labeled_grid)
    return regions, labeled_grid, num_labels

def is_adjacent(region1_slice, labeled_grid1, region2_slice, labeled_grid2):
    """Checks if two regions are adjacent (orthogonal or diagonal)."""
    if region1_slice is None or region2_slice is None:
        return False

    # Expand region1_slice by 1 pixel in all directions
    expanded_slice = (
        slice(max(0, region1_slice[0].start - 1), min(labeled_grid1.shape[0], region1_slice[0].stop + 1)),
        slice(max(0, region1_slice[1].start - 1), min(labeled_grid1.shape[1], region1_slice[1].stop + 1))
    )

    # Get the expanded region from labeled_grid1
    expanded_region = labeled_grid1[expanded_slice]

    # Find unique labels in region2 that intersect with the expanded region1
    region1_label = labeled_grid1[region1_slice][0,0] #get label for region1
    region2_labels_in_expanded_region = np.unique(labeled_grid2[expanded_slice])
    
    # Exclude 0 (background) and the label of region1_slice itself
    region2_labels_in_expanded_region = region2_labels_in_expanded_region[region2_labels_in_expanded_region != 0]
    region2_labels_in_expanded_region = region2_labels_in_expanded_region[region2_labels_in_expanded_region != region1_label]

    return len(region2_labels_in_expanded_region) > 0

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)

    # 1. Identify connected regions of blue and yellow
    yellow_regions, yellow_labeled_grid, num_yellow_regions = get_regions(input_grid, 4)
    blue_regions, blue_labeled_grid, num_blue_regions = get_regions(input_grid, 1)

    # 2. Iterate through each yellow region
    for yr_slice in yellow_regions:
        if yr_slice is None:  # Handle potentially empty slices. find_objects can contain None.
          continue

        is_adj = False # adjacent to any blue region

        # 3. Check adjacency to *any* blue region
        for br_slice in blue_regions:
            if is_adjacent(yr_slice, yellow_labeled_grid, br_slice, blue_labeled_grid):
                is_adj = True
                break  # No need to check other blue regions if one adjacency is found
        
        # 4. Transform the yellow region if adjacent
        if is_adj:
            yellow_label = yellow_labeled_grid[yr_slice][0,0]
            output_grid[yellow_labeled_grid == yellow_label] = 1

    # 5. Yellow regions not adjacent to blue remain unchanged (implicit in the logic)
    return output_grid