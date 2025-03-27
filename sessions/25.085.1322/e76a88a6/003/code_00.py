import numpy as np

"""
Identifies a "pattern" object (defined by non-white, non-gray pixels) and multiple "marker" objects (contiguous solid rectangular blocks of gray pixels). 
It verifies that the dimensions of the pattern's bounding box exactly match the dimensions of all marker blocks.
If the dimensions match, it creates the output grid by:
1. Copying the input grid.
2. Replacing each gray marker block area with a copy of the pattern object.
The original pattern remains in its position. If dimensions don't match or no pattern/markers are found, the original grid is returned.
"""

def find_pattern_bbox_and_content(grid):
    """
    Finds the bounding box, dimensions, and content of the pattern object.
    The pattern consists of all pixels that are not white (0) or gray (5).
    Returns (bbox, dims, content) or (None, None, None) if no pattern found.
    bbox is (min_r, min_c, max_r, max_c).
    dims is (height, width).
    content is a numpy array of the pattern pixels.
    """
    non_background_pixels = np.argwhere((grid != 0) & (grid != 5))
    if non_background_pixels.size == 0:
        return None, None, None # No pattern found

    min_r = np.min(non_background_pixels[:, 0])
    max_r = np.max(non_background_pixels[:, 0])
    min_c = np.min(non_background_pixels[:, 1])
    max_c = np.max(non_background_pixels[:, 1])

    bbox = (min_r, min_c, max_r, max_c)
    height = max_r - min_r + 1
    width = max_c - min_c + 1
    dims = (height, width)
    # Extract content based on bounding box
    content = grid[min_r:max_r+1, min_c:max_c+1]

    return bbox, dims, content

def find_contiguous_blocks(grid, color):
    """
    Finds all contiguous, solid rectangular blocks of a specific color using BFS.
    Returns a list of dictionaries, each containing 'bbox' (min_r, min_c, max_r, max_c)
    and 'dims' (height, width).
    """
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    blocks = []
    # Using a numpy array as a queue can be efficient for coordinates
    q = np.array([], dtype=np.uint16).reshape(0,2) 

    for r_init in range(rows):
        for c_init in range(cols):
            # Start BFS if we find a pixel of the target color that hasn't been visited
            if grid[r_init, c_init] == color and not visited[r_init, c_init]:
                # Initialize queue and visited status for the new component
                q = np.vstack([q, [r_init, c_init]])
                visited[r_init, c_init] = True
                component_pixels_count = 0
                min_r_block, max_r_block = r_init, r_init
                min_c_block, max_c_block = c_init, c_init

                head = 0
                while head < len(q):
                    r, c = q[head]
                    head += 1
                    component_pixels_count += 1
                    # Update bounding box coordinates
                    min_r_block = min(min_r_block, r)
                    max_r_block = max(max_r_block, r)
                    min_c_block = min(min_c_block, c)
                    max_c_block = max(max_c_block, c)

                    # Check neighbors (4-connectivity)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = r + dr, c + dc
                        # Check bounds, color match, and visited status
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           grid[nr, nc] == color and not visited[nr, nc]:
                            visited[nr, nc] = True
                            # Add valid neighbor to the queue
                            q = np.vstack([q, [nr, nc]])
                
                # Reset queue for the next potential component
                q = np.array([], dtype=np.uint16).reshape(0,2) 

                # Calculate potential dimensions from bounding box
                height = max_r_block - min_r_block + 1
                width = max_c_block - min_c_block + 1

                # Verify if the found component is a solid rectangle
                is_solid_rectangle = True
                # Check 1: Does the number of pixels found match the area of the bounding box?
                if component_pixels_count != height * width:
                     is_solid_rectangle = False
                else:
                    # Check 2: Are all pixels *within* the bounding box of the correct color?
                    # This ensures no holes or intrusions of other colors within the bbox.
                    block_slice = grid[min_r_block:max_r_block + 1, min_c_block:max_c_block + 1]
                    if not np.all(block_slice == color):
                        is_solid_rectangle = False

                # If it's a solid rectangle, add its details to the list
                if is_solid_rectangle:
                    bbox = (min_r_block, min_c_block, max_r_block, max_c_block)
                    dims = (height, width)
                    blocks.append({'bbox': bbox, 'dims': dims})
    return blocks


def transform(input_grid):
    """
    Applies the transformation rule: Copy pattern to gray markers of the same size.
    """
    # Convert input list of lists to numpy array for easier processing
    input_grid_np = np.array(input_grid, dtype=int)
    
    # 1. Identify the pattern object (non-white, non-gray pixels)
    pattern_bbox, pattern_dims, pattern_content = find_pattern_bbox_and_content(input_grid_np)
    
    # If no pattern is found, return the original grid
    if pattern_bbox is None:
        return input_grid 

    # 2. Identify the gray marker blocks (solid gray rectangles)
    marker_color = 5
    markers = find_contiguous_blocks(input_grid_np, marker_color)

    # If no markers are found, return the original grid
    if not markers:
         return input_grid 

    # 3. Check if pattern dimensions match all marker dimensions
    pattern_h, pattern_w = pattern_dims
    all_markers_match = True
    for marker in markers:
        marker_h, marker_w = marker['dims']
        if pattern_h != marker_h or pattern_w != marker_w:
            all_markers_match = False
            break
            
    # If dimensions don't match, return the original grid
    if not all_markers_match:
        return input_grid 

    # 4. Initialize the output grid as a copy of the input grid
    # This preserves the original pattern by default
    output_grid = np.copy(input_grid_np)

    # 5. Replace each marker area with the pattern content
    for marker in markers:
        m_min_r, m_min_c, m_max_r, m_max_c = marker['bbox']
        # Check shape consistency before assignment (should always pass if dim check passed)
        if output_grid[m_min_r:m_max_r+1, m_min_c:m_max_c+1].shape == pattern_content.shape:
             output_grid[m_min_r:m_max_r+1, m_min_c:m_max_c+1] = pattern_content
        else:
            # This case indicates an unexpected issue, log it if necessary
            # print(f"Warning: Shape mismatch during copy despite dimension check. Marker shape: {(m_max_r-m_min_r+1, m_max_c-m_min_c+1)}, Pattern shape: {pattern_content.shape}")
            pass # Continue processing other markers

    # Convert the final numpy array back to a list of lists for the expected output format
    return output_grid.tolist()