"""
1.  **Identify Azure Regions:** Locate all contiguous regions of color 8 (azure) within the input grid.
2.  **Horizontal Span Calculation:** For each azure region, and for regions that are horizontally adjacent, calculate the combined horizontal span.
3. **Conditional Replacement:** For any combined azure region:
    *   If the horizontal span is less than 5, no replacement occurs.
    *   If the horizontal span is 5 or greater, examine each pixel:
        1.  Check for a pixel directly above.
        2.  If a pixel exists directly above, replace the azure pixel with the color of the pixel above.
        3.  If there's no pixel directly above, retain the original azure color (8).
4. For other colours, no action.
"""

import numpy as np

def find_contiguous_regions(grid, color):
    """Finds contiguous regions of a specific color in the grid."""
    regions = []
    visited = np.zeros_like(grid, dtype=bool)

    def dfs(row, col, current_region):
        """Depth-first search to find contiguous region."""
        if (row < 0 or row >= grid.shape[0] or col < 0 or col >= grid.shape[1] or
                visited[row, col] or grid[row, col] != color):
            return
        visited[row, col] = True
        current_region.append((row, col))
        dfs(row + 1, col, current_region)
        dfs(row - 1, col, current_region)
        dfs(row, col + 1, current_region)
        dfs(row, col - 1, current_region)

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if grid[row, col] == color and not visited[row, col]:
                current_region = []
                dfs(row, col, current_region)
                regions.append(current_region)
    return regions

def get_horizontal_span(region):
    """Calculates the horizontal span of a region, assuming region is sorted."""
    if not region:
        return 0
    
    # Group cells by row
    rows = {}
    for r, c in region:
        if r not in rows:
            rows[r] = []
        rows[r].append((r,c))

    total_span = 0
    for row, cells in rows.items():
        total_span += len(cells)
    
    return total_span

def combine_horizontally_adjacent_regions(regions):
    """Combines horizontally adjacent regions."""
    combined_regions = []
    processed = [False] * len(regions)

    for i in range(len(regions)):
        if processed[i]:
            continue

        current_combined_region = list(regions[i])  # Start with the current region
        processed[i] = True

        for j in range(i + 1, len(regions)):
             if processed[j]:
                continue
             #get rows for region i
             rows_i = set()
             for r, c in regions[i]:
                rows_i.add(r)
            #get rows for region j
             rows_j = set()
             for r, c in regions[j]:
                rows_j.add(r)

             if rows_i.intersection(rows_j): #check if regions on same row
                #sort by row, col
                regions[i].sort(key=lambda x: (x[0], x[1]))
                regions[j].sort(key=lambda x: (x[0], x[1]))

                #get last col of region i, and first col of region j on any common row
                last_col_i = {}
                for r,c in regions[i]:
                    if r in rows_i.intersection(rows_j):
                        last_col_i[r] = c
                
                first_col_j = {}
                for r,c in regions[j]:
                    if r in rows_i.intersection(rows_j):
                        first_col_j[r] = c
                
                adjacent = False
                for r in rows_i.intersection(rows_j):
                    if first_col_j[r] - last_col_i[r] == 1:
                        adjacent = True

                if adjacent:
                    current_combined_region.extend(regions[j])
                    processed[j] = True

        combined_regions.append(current_combined_region)

    #add any regions that were not processed (ie not horizontally adjacent to any other)
    for i in range(len(regions)):
        if not processed[i]:
            combined_regions.append(regions[i])
    
    return combined_regions

def transform(input_grid):
    """Transforms the input grid according to the specified rule."""
    output_grid = np.copy(input_grid)
    azure_regions = find_contiguous_regions(input_grid, 8)

    # Combine horizontally adjacent regions
    combined_regions = combine_horizontally_adjacent_regions(azure_regions)

    for region in combined_regions:
        # Sort by row and then by column
        region.sort(key=lambda x: (x[0], x[1]))
        span = get_horizontal_span(region)

        if span >= 5:
            for r, c in region:
                if r > 0:  # Check if there's a pixel above
                    output_grid[r, c] = input_grid[r - 1, c]

    return output_grid