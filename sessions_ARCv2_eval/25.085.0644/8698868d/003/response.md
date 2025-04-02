```python
import numpy as np
from collections import Counter, defaultdict
import itertools

"""
Natural Language Program:
1.  **Analyze Input:** Scan the input grid to identify the distinct colors present.
2.  **Identify Placeholder Color:** Determine the 'placeholder' color (P). This is the color used for internal frame patterns and often surrounds standalone 'content' shapes. It's frequently the most common color after potential background/border colors, or acts as a separator. Heuristics based on frequency and non-edge location are used.
3.  **Find Objects:** Locate all contiguous regions of non-placeholder colors.
4.  **Categorize Objects:**
    a.  **Frame Objects:** Identify objects that form a rectangular border around an internal area filled entirely with the placeholder color (P). Note their border color (C_frame), bounding box, and the relative coordinates of the internal P pattern.
    b.  **Content Objects:** Identify solid, contiguous objects of a single color (C_content) different from P, typically located within larger areas dominated by P. Note their color (C_content), bounding box, and center coordinates.
5.  **Pair Frame and Content Objects:** Establish a one-to-one mapping between Frame objects and Content objects based primarily on proximity of their centers. Each content object is matched to the closest available frame object.
6.  **Transform Frame Objects:** For each matched pair (Frame, Content):
    a.  Create a new grid representing the transformed frame, using the Frame's original dimensions.
    b.  Fill the border pixels with the Frame's border color (C_frame).
    c.  Fill the interior pixels corresponding to the Frame's original internal P pattern with the Content object's color (C_content).
7.  **Assemble Output:** Arrange the transformed Frame objects in a new grid, maintaining the same relative spatial arrangement they had in the input grid. The output grid's size is determined by the bounding box encompassing all transformed frames, initialized with white (0) and overwritten by the frames.
"""

# ============================================
# Helper Functions: Finding Objects & Properties
# ============================================

def find_contiguous_regions(grid, colors_to_find=None, ignore_colors=None):
    """Finds all contiguous regions for specified colors, ignoring others."""
    height, width = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    regions = defaultdict(list)

    for r in range(height):
        for c in range(width):
            color = grid[r, c]
            if visited[r, c]:
                continue

            valid_color = True
            if colors_to_find is not None and color not in colors_to_find:
                valid_color = False
            if ignore_colors is not None and color in ignore_colors:
                valid_color = False

            if not valid_color:
                visited[r,c] = True # Mark as visited even if ignored/not sought
                continue

            # Found a valid starting point for a region
            region_coords = []
            q = [(r, c)]
            visited[r, c] = True
            region_color = color

            while q:
                row, col = q.pop(0)
                region_coords.append((row, col))

                # Check neighbors (4-connectivity)
                for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                    nr, nc = row + dr, col + dc
                    if 0 <= nr < height and 0 <= nc < width and \
                       not visited[nr, nc] and grid[nr, nc] == region_color:
                        visited[nr, nc] = True
                        q.append((nr, nc))
            
            if region_coords: # Should always be true here
                regions[region_color].append(set(region_coords))

    return regions

def get_bounding_box(coords):
    """Calculates the bounding box (min_r, min_c, max_r, max_c) of a set of coordinates."""
    if not coords:
        return None
    rows = [r for r, c in coords]
    cols = [c for r, c in coords]
    return min(rows), min(cols), max(rows), max(cols)

def get_relative_coords(coords, r_offset, c_offset):
    """Converts absolute coordinates to relative coordinates based on an offset (e.g., top-left corner)."""
    return set((r - r_offset, c - c_offset) for r, c in coords)

# ============================================
# Helper Functions: Analysis & Classification
# ============================================

def determine_placeholder_color(grid, potential_frame_colors, potential_content_colors):
    """Heuristically determines the placeholder color."""
    height, width = grid.shape
    counts = Counter(grid.flatten())
    
    # Exclude colors known *potentially* to be part of frames or content
    exclude_colors = set(potential_frame_colors) | set(potential_content_colors)
    
    sorted_counts = sorted(counts.items(), key=lambda item: item[1], reverse=True)

    # Heuristic 1: Most frequent color that is not a potential frame/content color
    # and forms a reasonably large connected region (suggesting background/filler)
    for color, count in sorted_counts:
        if color not in exclude_colors:
             regions = find_contiguous_regions(grid, colors_to_find=[color])
             if regions[color]:
                 largest_region_size = max(len(r) for r in regions[color])
                 # Check if it forms a significant background/separator region
                 # Thresholds might need tuning based on task examples
                 if largest_region_size > max(5, (height*width) * 0.05): 
                     return color 

    # Heuristic 2: Most frequent color not touching the grid edge (assuming placeholder is internal)
    edge_colors = set(grid[0,:]) | set(grid[-1,:]) | set(grid[:,0]) | set(grid[:,-1])
    for color, count in sorted_counts:
        if color not in exclude_colors and color not in edge_colors:
            return color 

    # Fallback 1: Most frequent color that is not a potential frame/content color (even if small regions/touching edge)
    for color, count in sorted_counts:
         if color not in exclude_colors:
             return color

    # Final Fallback: Most frequent color overall (this is risky but better than failing)
    if sorted_counts:
        return sorted_counts[0][0]
        
    return 0 # Absolute fallback: white

def analyze_objects(grid):
    """Identifies and categorizes frame and content objects, determining the placeholder color."""
    height, width = grid.shape
    
    # Initial pass: find all non-zero regions and tentatively classify
    all_regions = find_contiguous_regions(grid, ignore_colors={0}) # Initially ignore white
    
    potential_frames = []
    potential_contents = []
    potential_frame_colors = set()
    potential_content_colors = set()
    all_objects_found = []
    obj_id_counter = 0

    for color, regions_list in all_regions.items():
        for region_coords in regions_list:
             min_r, min_c, max_r, max_c = get_bounding_box(region_coords)
             obj_height = max_r - min_r + 1
             obj_width = max_c - min_c + 1
             
             is_potential_frame = False
             internal_coords_guess = set() # Store potential internal coordinates
             
             # Check if it looks like a hollow rectangle (potential frame)
             if obj_height > 2 and obj_width > 2:
                 is_hollow = False
                 is_potentially_solid = False # Check if it might just be a solid block
                 internal_non_border_pixels = 0
                 
                 for r in range(min_r + 1, max_r):
                     for c in range(min_c + 1, max_c):
                         if (r, c) not in region_coords:
                             internal_coords_guess.add((r,c))
                             is_hollow = True
                         else:
                             internal_non_border_pixels += 1
                 
                 # Check if the border itself is present and contiguous
                 border_pixels_present = all((r, c) in region_coords for r,c in region_coords if r == min_r or r == max_r or c == min_c or c == max_c)

                 # A potential frame is hollow and has its border pixels
                 if is_hollow and border_pixels_present:
                      is_potential_frame = True
                 # If it's not hollow but has internal pixels of the same color, it's potentially content
                 elif not is_hollow and internal_non_border_pixels > 0:
                     is_potentially_solid = True
                     
             is_solid_content = not is_potential_frame # Tentative: if not a potential frame, assume content

             obj_data = {
                 "id": obj_id_counter,
                 "color": color,
                 "coords": region_coords,
                 "bounds": (min_r, min_c, max_r, max_c),
                 "is_potential_frame": is_potential_frame,
                 "internal_coords_guess": internal_coords_guess if is_potential_frame else None,
             }
             all_objects_found.append(obj_data)
             obj_id_counter += 1
             
             if is_potential_frame:
                 potential_frame_colors.add(color)
             elif is_solid_content: # Only add if it's considered content
                 potential_content_colors.add(color)

    # Determine placeholder color using potential frame/content colors
    placeholder_color = determine_placeholder_color(grid, potential_frame_colors, potential_content_colors)
    
    # Final pass: Categorize using the determined placeholder color
    frames = []
    contents = []
    for obj in all_objects_found:
        is_frame_final = False
        internal_pattern_relative = None
        
        if obj["is_potential_frame"]:
            # Verify internal pattern consists ONLY of the placeholder color
            min_r, min_c, max_r, max_c = obj["bounds"]
            all_internal_are_placeholder = True
            verified_internal_coords = set()
            
            # Check if there's actually an interior space
            has_interior = (max_r - min_r > 1) and (max_c - min_c > 1)
            
            if has_interior:
                for r in range(min_r + 1, max_r):
                    for c in range(min_c + 1, max_c):
                        # Only check pixels *not* part of the object itself
                        if (r,c) not in obj["coords"]: 
                             if grid[r,c] == placeholder_color:
                                 verified_internal_coords.add((r,c))
                             else:
                                 # Found a non-placeholder color inside the potential frame boundary
                                 all_internal_are_placeholder = False
                                 break
                    if not all_internal_are_placeholder: break

                # A frame must have *some* internal placeholder pixels and *only* placeholder pixels
                if all_internal_are_placeholder and verified_internal_coords: 
                    is_frame_final = True
                    internal_pattern_relative = get_relative_coords(verified_internal_coords, min_r, min_c)
            # If it doesn't have an interior space (e.g., 2xN or Nx2 rect), it can't be a frame by this definition
            # else: pass # is_frame_final remains False

        # Decide category
        if is_frame_final:
            frames.append({
                "color": obj["color"],
                "bounds": obj["bounds"],
                "internal_pattern": internal_pattern_relative,
                "height": obj["bounds"][2] - obj["bounds"][0] + 1,
                "width": obj["bounds"][3] - obj["bounds"][1] + 1,
                 # Use center for pairing later if needed
                "center": ((obj["bounds"][0] + obj["bounds"][2]) / 2, (obj["bounds"][1] + obj["bounds"][3]) / 2) 
            })
        elif obj["color"] != placeholder_color: # Avoid classifying placeholder regions as content
            # Add objects that are confirmed *not* frames to contents
            min_r, min_c, max_r, max_c = obj["bounds"]
            center_r = (min_r + max_r) / 2
            center_c = (min_c + max_c) / 2
            contents.append({
                "color": obj["color"],
                "bounds": obj["bounds"],
                "center": (center_r, center_c) # Use center for pairing
            })
            
    return frames, contents, placeholder_color


# ============================================
# Helper Functions: Pairing & Transformation
# ============================================

def pair_frames_contents(frames, contents):
    """Pairs frames and contents based on proximity of their centers."""
    
    if not frames or not contents:
        return {}

    pairing = {}
    # Use sets for efficient removal of used items
    available_contents = { (c['color'], tuple(c['bounds'])): c for c in contents }
    used_content_keys = set()

    # Sort frames to process them in a consistent order (e.g., top-left)
    sorted_frames = sorted(frames, key=lambda f: (f['bounds'][0], f['bounds'][1]))

    for frame in sorted_frames:
        frame_center_r, frame_center_c = frame['center']
        frame_key = (frame['color'], tuple(frame['bounds']))
        
        min_dist = float('inf')
        best_content_key = None
        
        # Find the closest available content object
        for content_key, content_data in available_contents.items():
            if content_key in used_content_keys:
                continue 
                
            content_center_r, content_center_c = content_data['center']
            dist_sq = (frame_center_r - content_center_r)**2 + (frame_center_c - content_center_c)**2
            
            if dist_sq < min_dist:
                min_dist = dist_sq
                best_content_key = content_key
        
        # If a closest content was found, pair them and mark content as used
        if best_content_key:
             pairing[frame_key] = available_contents[best_content_key]
             used_content_keys.add(best_content_key)

    return pairing

def transform_frame(frame_data, content_color):
    """Creates the transformed frame grid."""
    height = frame_data['height']
    width = frame_data['width']
    border_color = frame_data['color']
    internal_pattern = frame_data['internal_pattern'] # Relative coordinates
    
    # Initialize with border color
    transformed = np.full((height, width), border_color, dtype=int)
    
    # Fill internal pattern with content color
    if internal_pattern:
        for r_rel, c_rel in internal_pattern:
             # Ensure relative coords are within bounds (should be by definition if calculated correctly)
             if 0 <= r_rel < height and 0 <= c_rel < width:
                 transformed[r_rel, c_rel] = content_color
                 
    return transformed

# ============================================
# Helper Function: Output Assembly
# ============================================

def assemble_output(transformed_frames_map, original_frames):
    """Assembles the final output grid, placing transformed frames at their original relative positions."""
    if not transformed_frames_map:
        # Return a minimal grid if no frames were transformed
        return np.array([[0]], dtype=int) 

    # Determine the bounding box encompassing all *original* frame positions
    all_min_r, all_min_c = float('inf'), float('inf')
    all_max_r_end, all_max_c_end = float('-inf'), float('-inf') # Track end+1 for size calculation
    
    frame_rel_positions = {} # Store top-left corner relative to overall min_r, min_c
    
    if not original_frames: # Should not happen if transformed_frames_map is populated, but safety check
         return np.array([[0]], dtype=int)

    for frame in original_frames:
        frame_key = (frame['color'], tuple(frame['bounds']))
        # Only consider frames that were actually transformed for layout calculation
        if frame_key in transformed_frames_map:
            min_r, min_c, max_r, max_c = frame['bounds']
            h = max_r - min_r + 1
            w = max_c - min_c + 1
            
            all_min_r = min(all_min_r, min_r)
            all_min_c = min(all_min_c, min_c)
            # Calculate where the bottom-right corner *ends*
            all_max_r_end = max(all_max_r_end, min_r + h) 
            all_max_c_end = max(all_max_c_end, min_c + w)

    # Calculate output dimensions based on the overall span
    # If no frames were found/transformed, handle default case
    if all_min_r == float('inf'):
        return np.array([[0]], dtype=int) 
        
    output_height = all_max_r_end - all_min_r
    output_width = all_max_c_end - all_min_c
    
    # Store relative positions for placement
    for frame in original_frames:
         frame_key = (frame['color'], tuple(frame['bounds']))
         if frame_key in transformed_frames_map:
             rel_r = frame['bounds'][0] - all_min_r
             rel_c = frame['bounds'][1] - all_min_c
             frame_rel_positions[frame_key] = (rel_r, rel_c)


    # Create output grid, initialized with white (0)
    output_grid = np.full((output_height, output_width), 0, dtype=int) 

    # Place transformed frames onto the output grid
    # Sort by original position to handle potential overlaps consistently (top-left first)
    sorted_original_frames = sorted(original_frames, key=lambda f: (f['bounds'][0], f['bounds'][1]))

    for frame in sorted_original_frames:
        frame_key = (frame['color'], tuple(frame['bounds']))
        if frame_key in transformed_frames_map:
            transformed_grid = transformed_frames_map[frame_key]
            h, w = transformed_grid.shape
            # Ensure we have calculated relative position for this frame
            if frame_key in frame_rel_positions:
                rel_r, rel_c = frame_rel_positions[frame_key]
                
                # Ensure placement is within calculated bounds
                if rel_r + h <= output_height and rel_c + w <= output_width:
                     output_grid[rel_r:rel_r+h, rel_c:rel_c+w] = transformed_grid
                else:
                    # This case indicates an issue with layout calculation or frame dimensions
                    print(f"Warning: Frame {frame_key} placement exceeds calculated output bounds.")
                    # Optionally, clip or skip placement
                    end_r = min(rel_r + h, output_height)
                    end_c = min(rel_c + w, output_width)
                    output_grid[rel_r:end_r, rel_c:end_c] = transformed_grid[0:end_r-rel_r, 0:end_c-rel_c]


    return output_grid


# ============================================
# Main Transformation Function
# ============================================

def transform(input_grid):
    """
    Applies the frame-content transformation rule to the input grid.
    """
    # Convert input to numpy array for processing
    input_grid_np = np.array(input_grid, dtype=int)
    
    # Step 1 & 2: Analyze grid to find frames, content objects, and placeholder color
    # analyze_objects handles finding regions, classifying, and determining placeholder
    frames, contents, placeholder_color = analyze_objects(input_grid_np)

    # Handle cases where analysis fails or finds no relevant objects
    if not frames or not contents:
         print(f"Warning: No frames ({len(frames)}) or contents ({len(contents)}) found. Placeholder: {placeholder_color}. Returning default.")
         # Return a minimal default grid (e.g., 1x1 white)
         return np.array([[0]], dtype=int).tolist() 

    # Step 3: Pair frame objects with content objects based on proximity
    pairing = pair_frames_contents(frames, contents)
    
    # Handle cases where pairing fails
    if not pairing:
        print("Warning: Could not pair frames and contents. Returning default.")
        return np.array([[0]], dtype=int).tolist() 

    # Step 4: Transform each frame based on its paired content
    transformed_frames = {}
    # Create a map for easy lookup of original frame data using the key from pairing
    original_frame_map = {(f['color'], tuple(f['bounds'])): f for f in frames}

    for frame_key, content_data in pairing.items():
        # Ensure the frame from the pairing exists in our original frame list
        if frame_key in original_frame_map:
            original_frame_data = original_frame_map[frame_key]
            content_color = content_data['color']
            # Create the new grid for this transformed frame
            transformed_grid = transform_frame(original_frame_data, content_color)
            transformed_frames[frame_key] = transformed_grid
        else:
             # This indicates a mismatch between pairing keys and found frames
             print(f"Warning: Frame key {frame_key} from pairing not found in original frames list.")

    # Step 5: Assemble the final output grid
    # Use the map of transformed grids and the original list of frames (for position info)
    output_grid_np = assemble_output(transformed_frames, frames)

    # Convert final numpy array back to list of lists for the required output format
    return output_grid_np.tolist()

```