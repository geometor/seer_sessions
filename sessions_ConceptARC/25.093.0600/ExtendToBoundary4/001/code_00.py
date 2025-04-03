import numpy as np
import copy

"""
Identifies maximal continuous horizontal or vertical line segments of identical non-zero numbers in the input grid.
For each segment, it checks the path extending outwards from both endpoints along the segment's axis.
If such a path consists of one or more zeros and terminates immediately before another non-zero number (before hitting the grid boundary), 
then all the zeros along that path are filled with the segment's number in the output grid. 
This process is applied cumulatively for all identified segments and their qualifying extensions.
"""

def _identify_segments(grid):
    """
    Identifies all maximal horizontal and vertical segments of identical non-zero numbers.
    Returns a list of segments, where each segment is represented as:
    (value, orientation, list_of_coordinates)
    orientation is 'h' for horizontal, 'v' for vertical.
    """
    height, width = grid.shape
    segments = []
    visited = np.zeros_like(grid, dtype=bool) # Keep track of cells already part of a found segment

    for r in range(height):
        for c in range(width):
            if grid[r, c] != 0 and not visited[r, c]:
                val = grid[r, c]

                # Check horizontal segment
                h_coords = []
                cc = c
                while cc < width and grid[r, cc] == val:
                    h_coords.append((r, cc))
                    cc += 1
                if len(h_coords) > 1: # Only consider segments of length 2 or more
                    segments.append((val, 'h', h_coords))
                    for rr, cc_seg in h_coords:
                        visited[rr, cc_seg] = True
                # Reset visited status if only length 1 horizontal segment found here,
                # so it can potentially be part of a vertical segment.
                elif len(h_coords) == 1 and not visited[r,c]: 
                    pass # Keep visited[r,c] False for now

                # Check vertical segment only if not part of a horizontal segment found *starting* here
                # or if it's a single cell (which could start a vertical segment)
                # We also need to re-check visited status in case it was part of a horizontal segment
                # that started earlier on the same row.
                if not visited[r,c]:
                    v_coords = []
                    rr = r
                    while rr < height and grid[rr, c] == val:
                        v_coords.append((rr, c))
                        rr += 1
                    if len(v_coords) > 1: # Only consider segments of length 2 or more
                         # Check if any part of this overlaps with an already added horizontal segment cell
                         is_new_vertical = True
                         for rr_seg, cc_seg in v_coords:
                             if visited[rr_seg, cc_seg]: # If any cell was visited (part of horizontal)
                                 is_new_vertical = False
                                 break
                         if is_new_vertical:
                            segments.append((val, 'v', v_coords))
                            for rr_seg, cc_seg in v_coords:
                                visited[rr_seg, cc_seg] = True # Mark as visited
                    # If only a single cell was found vertically (and horizontally), mark it visited
                    # to prevent re-processing
                    elif len(h_coords) <=1 and len(v_coords) == 1:
                         visited[r,c] = True
                         
    # Correction: The above logic might miss segments if a cell is part of both H and V segments.
    # A better approach: find all H segments, then all V segments independently, mark visited separately?
    # Let's refine: find H first, mark visited. Then find V, only adding if *not* fully contained in visited H. No, simpler: find all possible starts.
    
    # Re-try identification logic: Simpler, find all H segments, then all V segments.
    segments = []
    visited_h = np.zeros_like(grid, dtype=bool)
    visited_v = np.zeros_like(grid, dtype=bool)

    # Find horizontal segments
    for r in range(height):
        c = 0
        while c < width:
            if grid[r, c] != 0:
                val = grid[r, c]
                start_c = c
                while c < width and grid[r, c] == val:
                    c += 1
                end_c = c - 1
                if end_c > start_c: # Length >= 2
                    coords = [(r, cc) for cc in range(start_c, end_c + 1)]
                    segments.append({'value': val, 'orientation': 'h', 'coords': coords})
            else:
                c += 1

    # Find vertical segments
    for c in range(width):
        r = 0
        while r < height:
            if grid[r, c] != 0:
                val = grid[r, c]
                start_r = r
                while r < height and grid[r, c] == val:
                    r += 1
                end_r = r - 1
                if end_r > start_r: # Length >= 2
                    coords = [(rr, c) for rr in range(start_r, end_r + 1)]
                    segments.append({'value': val, 'orientation': 'v', 'coords': coords})
            else:
                r += 1
                
    # Handle single non-zero cells - they can also extend if conditions met
    # No, the examples show extension only from segments of length > 1. train_4: 8 is length 3, 9 is length 3. train_1: 1 is length 5, 2 is length 3. train_2: 6 is length 2, 3 is length 5. train_3: 4 is length 3, 7 is length 2.
    # So, the length >= 2 logic seems correct based on examples.

    return segments


def transform(input_grid):
    """
    Transforms the input grid based on extending line segments.
    """
    # Convert to numpy array for easier manipulation
    grid_np = np.array(input_grid, dtype=int)
    output_grid = copy.deepcopy(grid_np)
    height, width = grid_np.shape

    # Identify all maximal horizontal and vertical segments of length >= 2
    segments = _identify_segments(grid_np)

    # Iterate through each segment and check for extensions from its endpoints
    for segment in segments:
        value = segment['value']
        orientation = segment['orientation']
        coords = segment['coords']
        
        # Sort coordinates to easily find endpoints
        coords.sort()
        start_coord = coords[0]
        end_coord = coords[-1]

        # Check extension from the 'start' endpoint (left for 'h', top for 'v')
        zeros_path_start = []
        blocked_start = False
        if orientation == 'h':
            r, c = start_coord
            next_c = c - 1
            while next_c >= 0 and output_grid[r, next_c] == 0: # Check output grid for zeros
                zeros_path_start.append((r, next_c))
                next_c -= 1
            if next_c >= 0 and output_grid[r, next_c] != 0: # Check for blocking non-zero in output grid
                blocked_start = True
        else: # orientation == 'v'
            r, c = start_coord
            next_r = r - 1
            while next_r >= 0 and output_grid[next_r, c] == 0:
                zeros_path_start.append((next_r, c))
                next_r -= 1
            if next_r >= 0 and output_grid[next_r, c] != 0:
                blocked_start = True

        # Fill path if blocked
        if blocked_start and zeros_path_start:
             # Fill in reverse order of finding to apply correctly if segments cross paths
            for rz, cz in reversed(zeros_path_start):
                 output_grid[rz, cz] = value

        # Check extension from the 'end' endpoint (right for 'h', bottom for 'v')
        zeros_path_end = []
        blocked_end = False
        if orientation == 'h':
            r, c = end_coord
            next_c = c + 1
            while next_c < width and output_grid[r, next_c] == 0:
                zeros_path_end.append((r, next_c))
                next_c += 1
            if next_c < width and output_grid[r, next_c] != 0:
                blocked_end = True
        else: # orientation == 'v'
            r, c = end_coord
            next_r = r + 1
            while next_r < height and output_grid[next_r, c] == 0:
                zeros_path_end.append((next_r, c))
                next_r += 1
            if next_r < height and output_grid[next_r, c] != 0:
                blocked_end = True
                
        # Fill path if blocked
        if blocked_end and zeros_path_end:
            for rz, cz in zeros_path_end: # Fill in order found
                 output_grid[rz, cz] = value

    # Convert back to list of lists for the expected output format
    return output_grid.tolist()