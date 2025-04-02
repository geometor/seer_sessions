import numpy as np

"""
Identifies non-white contiguous objects ("patterns") in the input grid. For each 
pattern, it determines its bounding box, dimensions (Height H, Width W), and 
column span (C_start, C_end). It then searches the grid *below* the pattern's 
bounding box, within the same column span, for the topmost rectangular area of 
the exact same dimensions (H x W) that consists entirely of white pixels (0) 
("canvas"). If such a canvas is found, the pixel data from the pattern's 
bounding box is copied onto the canvas location in the output grid. 
The rest of the grid remains unchanged.
"""

def get_non_white_objects(grid_np):
    """
    Finds contiguous non-white objects and their properties using numpy and loops.
    
    Args:
        grid_np (np.array): The input grid as a numpy array.

    Returns:
        list: A list of dictionaries, each representing a non-white object 
              with its properties (color, bbox, height, width, data, etc.).
    """
    objects = []
    visited = np.zeros_like(grid_np, dtype=bool)
    rows, cols = grid_np.shape

    for r in range(rows):
        for c in range(cols):
            # Process only non-white pixels that haven't been visited
            if not visited[r, c] and grid_np[r, c] != 0:
                color = grid_np[r, c]
                q = [(r, c)] # Use list as queue for BFS
                visited[r, c] = True
                component_pixels = [(r, c)]
                min_r, max_r, min_c, max_c = r, r, c, c

                head = 0
                while head < len(q):
                    row, col = q[head]
                    head += 1

                    # Update bounding box
                    min_r = min(min_r, row)
                    max_r = max(max_r, row)
                    min_c = min(min_c, col)
                    max_c = max(max_c, col)

                    # Check 4 neighbors (non-diagonal adjacency)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        # Check bounds, visited status, and same color
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           not visited[nr, nc] and grid_np[nr, nc] == color:
                            visited[nr, nc] = True
                            q.append((nr, nc))
                            component_pixels.append((nr, nc))

                # Calculate properties of the found object
                height = max_r - min_r + 1
                width = max_c - min_c + 1
                bbox = (min_r, min_c, max_r, max_c)
                # Extract object data from its bounding box in the original grid
                obj_data = grid_np[min_r:max_r+1, min_c:max_c+1]

                objects.append({
                    'color': color, # The specific color of this object
                    'bbox': bbox,
                    'height': height,
                    'width': width,
                    'data': obj_data, # Pixel data within the bounding box
                    'num_pixels': len(component_pixels)
                })
                
    # Sort objects primarily by starting row, then by starting column for deterministic processing
    objects.sort(key=lambda obj: (obj['bbox'][0], obj['bbox'][1]))
    return objects

def transform(input_grid):
    """
    Transforms the input grid by copying non-white pattern bounding boxes onto 
    corresponding white canvas areas located below them.

    Args:
        input_grid (list of lists): The input grid represented as a 2D list of integers.

    Returns:
        list of lists: The transformed grid.
    """
    input_np = np.array(input_grid, dtype=int)
    output_np = input_np.copy()
    rows, cols = input_np.shape
    
    # Find all non-white "pattern" objects
    pattern_objects = get_non_white_objects(input_np)
    
    # Keep track of canvas areas that have been filled to avoid overwriting
    # Store the tuple (r_start, c_start, r_end, c_end) of the canvas bbox
    filled_canvas_bboxes = set() 

    # Iterate through each found pattern object
    for pattern in pattern_objects:
        pr_s, pc_s, pr_e, pc_e = pattern['bbox']
        H = pattern['height']
        W = pattern['width']
        pattern_data = pattern['data'] # Data within the pattern's bbox
        
        # Search for the topmost matching white canvas below the pattern
        found_canvas = False
        for cr_s in range(pr_e + 1, rows - H + 1): # Start search below pattern end row
            # Canvas column span must match pattern's column span
            cc_s = pc_s 
            cr_e = cr_s + H - 1
            ce_e = cc_s + W - 1

            # Ensure the potential canvas location is within grid bounds (width check)
            if ce_e >= cols:
                continue # Cannot fit width-wise

            # Define the potential canvas bounding box
            canvas_bbox = (cr_s, cc_s, cr_e, ce_e)

            # Check if this potential canvas area has already been filled
            if canvas_bbox in filled_canvas_bboxes:
                continue

            # Extract the subgrid for the potential canvas area
            potential_canvas_area = input_np[cr_s:cr_e+1, cc_s:ce_e+1]

            # Check if the area is entirely white (all zeros)
            if np.all(potential_canvas_area == 0):
                # Found the topmost matching canvas for this pattern
                
                # Perform the replacement in the output grid
                output_np[cr_s:cr_e+1, cc_s:ce_e+1] = pattern_data
                
                # Mark this canvas area as filled
                filled_canvas_bboxes.add(canvas_bbox)
                
                # Stop searching for canvases for this pattern, move to the next pattern
                found_canvas = True
                break 
                
        # If no canvas was found for this pattern, continue to the next pattern object

    # Convert the final numpy array back to a list of lists
    return output_np.tolist()