import numpy as np
from collections import Counter, defaultdict
import itertools

"""
Natural Language Program:
1.  **Analyze Input:** Scan the input grid to identify the distinct colors present.
2.  **Identify Placeholder Color:** Determine the 'placeholder' color (P). This is the color used for internal frame patterns and often surrounds standalone 'content' shapes. It's frequently the most common color after potential background/border colors, or acts as a separator.
3.  **Find Objects:** Locate all contiguous regions of non-placeholder colors.
4.  **Categorize Objects:**
    a.  **Frame Objects:** Identify objects that form a rectangular border around an internal area filled entirely with the placeholder color (P). Note their border color (C_frame), bounding box, and the relative coordinates of the internal P pattern.
    b.  **Content Objects:** Identify solid, contiguous objects of a single color (C_content) different from P, typically located within larger areas dominated by P. Note their color (C_content) and approximate location/region.
5.  **Pair Frame and Content Objects:** Establish a one-to-one mapping between Frame objects and Content objects based on their relative spatial positions or the locations of the regions they occupy (e.g., horizontal alignment, quadrant mapping).
6.  **Transform Frame Objects:** For each matched pair (Frame, Content):
    a.  Create a new grid representing the transformed frame, using the Frame's original dimensions.
    b.  Fill the border pixels with the Frame's border color (C_frame).
    c.  Fill the interior pixels corresponding to the Frame's original internal P pattern with the Content object's color (C_content).
7.  **Assemble Output:** Arrange the transformed Frame objects in a new grid, maintaining the same relative spatial arrangement they had in the input grid. The output grid's size is determined by the bounding box encompassing all transformed frames.
"""

def find_contiguous_regions(grid, colors_to_find=None, ignore_colors=None):
    """Finds all contiguous regions for specified colors."""
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

            region_coords = []
            q = [(r, c)]
            visited[r, c] = True
            region_color = color

            while q:
                row, col = q.pop(0)
                region_coords.append((row, col))

                for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                    nr, nc = row + dr, col + dc
                    if 0 <= nr < height and 0 <= nc < width and \
                       not visited[nr, nc] and grid[nr, nc] == region_color:
                        visited[nr, nc] = True
                        q.append((nr, nc))
            
            regions[region_color].append(set(region_coords))

    return regions

def get_bounding_box(coords):
    """Calculates the bounding box of a set of coordinates."""
    if not coords:
        return None
    rows = [r for r, c in coords]
    cols = [c for r, c in coords]
    return min(rows), min(cols), max(rows), max(cols)

def get_relative_coords(coords, r_offset, c_offset):
    """Converts absolute coordinates to relative coordinates."""
    return set((r - r_offset, c - c_offset) for r, c in coords)

def determine_placeholder_color(grid, potential_frame_colors, potential_content_colors):
    """Heuristic to determine the placeholder color."""
    height, width = grid.shape
    counts = Counter(grid.flatten())
    
    # Exclude colors known to be part of frames or content
    exclude_colors = set(potential_frame_colors) | set(potential_content_colors)
    
    # Often the placeholder separates things, look for colors with high counts that aren't frames/content
    most_common_non_object = None
    max_count = -1
    
    sorted_counts = sorted(counts.items(), key=lambda item: item[1], reverse=True)

    for color, count in sorted_counts:
        if color not in exclude_colors:
             # Simple heuristic: highest count non-object color
             # More advanced: color that forms large connected regions separating objects
             # For now, let's try the most frequent non-frame/content color
             # Let's refine: often it's the background separating frames, or the internal fill.
             # Let's check if this color forms the largest connected region.
             regions = find_contiguous_regions(grid, colors_to_find=[color])
             if regions[color]:
                 largest_region_size = max(len(r) for r in regions[color])
                 # If it forms a significant background/separator region
                 if largest_region_size > (height*width) * 0.1 or largest_region_size > 10: # Adjust threshold needed
                     return color # Assume this is the placeholder


    # Fallback if the above fails (e.g., small examples)
    if sorted_counts:
        for color, count in sorted_counts:
             if color not in exclude_colors:
                 return color # Take the most frequent non-frame/content

    # If all colors are frame/content (unlikely), maybe return most frequent overall? Risky.
    # Let's specifically check the fill color of potential frames identified earlier.
    # This requires finding frames first, which needs the placeholder. Circular dependency.
    
    # Let's try another heuristic: color that is NOT on the edge of the grid
    # This assumes placeholder isn't the absolute background touching edges.
    
    edge_colors = set(grid[0,:]) | set(grid[-1,:]) | set(grid[:,0]) | set(grid[:,-1])
    
    for color, count in sorted_counts:
        if color not in exclude_colors and color not in edge_colors:
            return color # Most frequent non-frame/content color that doesn't touch the edge

    # Final desperate fallback: most frequent color overall.
    if sorted_counts:
        return sorted_counts[0][0]
        
    return 0 # Default to white if grid is empty or uniform?


def analyze_objects(grid, placeholder_color):
    """Identifies and categorizes frame and content objects."""
    height, width = grid.shape
    all_regions = find_contiguous_regions(grid, ignore_colors={placeholder_color})
    
    frames = []
    contents = []
    potential_frame_colors = set()
    potential_content_colors = set()

    # First pass to identify potential types and colors
    obj_id_counter = 0
    all_objects_found = []
    for color, regions_list in all_regions.items():
        for region_coords in regions_list:
             min_r, min_c, max_r, max_c = get_bounding_box(region_coords)
             obj_height = max_r - min_r + 1
             obj_width = max_c - min_c + 1
             
             is_potential_frame = False
             internal_pattern_coords = set()
             # Check if it forms a border around a placeholder region
             if obj_height > 2 and obj_width > 2:
                 is_border = True
                 has_internal_placeholder = False
                 for r in range(min_r + 1, max_r):
                     for c in range(min_c + 1, max_c):
                         coord = (r, c)
                         if coord not in region_coords:
                             if grid[r,c] == placeholder_color:
                                 has_internal_placeholder = True
                                 internal_pattern_coords.add(coord)
                             else: # Internal pixel is neither border nor placeholder
                                 is_border = False
                                 break
                     if not is_border: break
                 
                 # Check if border pixels are present
                 border_present = False
                 for r, c in region_coords:
                     if r == min_r or r == max_r or c == min_c or c == max_c:
                         border_present = True
                         break
                 
                 if is_border and has_internal_placeholder and border_present:
                     is_potential_frame = True

             obj_data = {
                 "id": obj_id_counter,
                 "color": color,
                 "coords": region_coords,
                 "bounds": (min_r, min_c, max_r, max_c),
                 "is_potential_frame": is_potential_frame,
                 "internal_placeholder_coords": internal_pattern_coords if is_potential_frame else None,
             }
             all_objects_found.append(obj_data)
             obj_id_counter += 1
             
             if is_potential_frame:
                 potential_frame_colors.add(color)
             else:
                 # Assume non-frames are content for now
                 potential_content_colors.add(color)

    # Refine placeholder using identified potential frame/content colors
    actual_placeholder_color = determine_placeholder_color(grid, potential_frame_colors, potential_content_colors)
    
    # Second pass to finalize categorization using the refined placeholder color
    frames = []
    contents = []
    for obj in all_objects_found:
        is_frame_final = False
        internal_pattern_relative = None
        
        if obj["is_potential_frame"]:
            # Re-verify internal pattern with the actual placeholder color
            min_r, min_c, max_r, max_c = obj["bounds"]
            all_internal_are_placeholder = True
            verified_internal_coords = set()
            if min_r+1 <= max_r-1 and min_c+1 <= max_c-1: # Check if there's an interior
                for r in range(min_r + 1, max_r):
                    for c in range(min_c + 1, max_c):
                        if (r,c) not in obj["coords"]: # If it's an internal pixel
                             if grid[r,c] == actual_placeholder_color:
                                 verified_internal_coords.add((r,c))
                             else:
                                 all_internal_are_placeholder = False
                                 break
                    if not all_internal_are_placeholder: break
                
                if all_internal_are_placeholder and verified_internal_coords: # Must have some placeholder inside
                    is_frame_final = True
                    internal_pattern_relative = get_relative_coords(verified_internal_coords, min_r, min_c)

        if is_frame_final:
            frames.append({
                "color": obj["color"],
                "bounds": obj["bounds"],
                "internal_pattern": internal_pattern_relative,
                "height": obj["bounds"][2] - obj["bounds"][0] + 1,
                "width": obj["bounds"][3] - obj["bounds"][1] + 1,
            })
        else:
            # Add objects that are confirmed *not* frames (using the final placeholder) to contents
             min_r, min_c, max_r, max_c = obj["bounds"]
             center_r = (min_r + max_r) / 2
             center_c = (min_c + max_c) / 2
             contents.append({
                "color": obj["color"],
                "bounds": obj["bounds"],
                "center": (center_r, center_c) # Use center for pairing
            })
            
    return frames, contents, actual_placeholder_color


def pair_frames_contents(frames, contents, grid_shape):
    """Pairs frames and contents based on spatial relationship."""
    
    if not frames or not contents:
        return {}

    # Simple case: if equal number, try pairing by order (e.g., top-to-bottom, left-to-right)
    if len(frames) == len(contents):
        # Sort frames and contents based on position (e.g., top-left corner)
        sorted_frames = sorted(frames, key=lambda f: (f['bounds'][0], f['bounds'][1]))
        sorted_contents = sorted(contents, key=lambda c: (c['bounds'][0], c['bounds'][1]))
        
        # Check if simple horizontal pairing works (like Ex1)
        # Requires frames and contents to be roughly horizontally aligned in pairs
        # This is too specific, let's try a more general region approach inspired by Ex2

    # Region-based pairing (inspired by Ex2)
    height, width = grid_shape
    mid_r, mid_c = height // 2, width // 2

    def get_region(bounds):
        min_r, min_c, max_r, max_c = bounds
        center_r = (min_r + max_r) / 2
        center_c = (min_c + max_c) / 2
        
        if center_r < mid_r and center_c < mid_c: return "TL"
        if center_r < mid_r and center_c >= mid_c: return "TR"
        if center_r >= mid_r and center_c < mid_c: return "BL"
        if center_r >= mid_r and center_c >= mid_c: return "BR"
        # Add center/middle if needed, but quadrant might be enough

    frame_regions = {get_region(f['bounds']): f for f in frames}
    content_regions = {get_region(c['bounds']): c for c in contents}

    pairing = {}

    # Define the mapping based on example 2: Content Region -> Frame Region
    region_map = {
        "TR": "TL", # Content in TR maps to Frame in TL
        "BR": "TR", # Content in BR maps to Frame in TR
        "BL": "ML", # Content in BL maps to Frame in ML (Need to adjust region definition if ML needed)
        "MR": "MR"  # Content in MR maps to Frame in MR (Need to adjust region definition if MR needed)
    }
    
    # Let's reconsider Ex1: Left Frame (Blue), Left Content (Red). Right Frame (Yellow), Right Content (Green).
    # If we use regions:
    # Ex1: Blue Frame ~TL, Red Content ~BL. Yellow Frame ~TR, Green Content ~BR.
    # Mapping: Content BL -> Frame TL, Content BR -> Frame TR.
    
    # Combined Hypothesis: Content location determines target Frame location.
    mapping_rule = {}
    if len(frames) == 2 and len(contents) == 2: # Likely Ex1 structure
        # Assuming frames are roughly T/B or L/R aligned, and contents are too.
        f_sorted = sorted(frames, key=lambda f: (f['bounds'][1], f['bounds'][0])) # Sort Left-to-Right
        c_sorted = sorted(contents, key=lambda c: (c['bounds'][1], c['bounds'][0])) # Sort Left-to-Right
        if len(f_sorted) == len(c_sorted): # Should be true here
             for i in range(len(f_sorted)):
                 pairing[f_sorted[i]['color'], tuple(f_sorted[i]['bounds'])] = c_sorted[i] # Pair frame with content at same index
             return pairing

    elif len(frames) > 0 and len(contents) > 0: # Try quadrant mapping (like Ex2 structure)
        # Redefine regions more carefully if needed, e.g., 3x3 grid instead of 2x2
        # For now, stick to 4 quadrants TL, TR, BL, BR
        # Define the mapping based on observations (Ex1 & Ex2 combined logic attempt)
        # Content Region -> Target Frame Region
        region_map = { 
             "BL": "TL", # Ex1 Red -> Blue
             "BR": "TR", # Ex1 Green -> Yellow & Ex2 Orange -> Green
             "TR": "TL", # Ex2 Maroon -> Yellow (This contradicts Ex1 TR->TR!)
             # Let's assume Ex2 mapping is dominant if > 2 pairs
             # Ex2: Content TR -> Frame TL; Content BR -> Frame TR; Content BL -> Frame ML; Content MR -> Frame MR
             # The regions ML and MR need better definition. Maybe relative to placeholder areas?
             # This pairing logic is complex and task-specific.
             # Let's use a simple proximity pairing for now as a fallback/alternative.
             
        # Proximity pairing: find the closest content for each frame
        paired_contents = set()
        for frame in frames:
            frame_center_r = (frame['bounds'][0] + frame['bounds'][2]) / 2
            frame_center_c = (frame['bounds'][1] + frame['bounds'][3]) / 2
            
            min_dist = float('inf')
            best_content = None
            
            for content in contents:
                content_id = (content['color'], tuple(content['bounds']))
                if content_id in paired_contents:
                    continue # Skip already paired content
                    
                dist = ((frame_center_r - content['center'][0])**2 + 
                        (frame_center_c - content['center'][1])**2)**0.5
                
                if dist < min_dist:
                    min_dist = dist
                    best_content = content
            
            if best_content:
                 pairing[(frame['color'], tuple(frame['bounds']))] = best_content
                 paired_contents.add((best_content['color'], tuple(best_content['bounds'])))

        return pairing
        
    return {} # No pairing possible


def transform_frame(frame_data, content_color):
    """Creates the transformed frame grid."""
    height = frame_data['height']
    width = frame_data['width']
    border_color = frame_data['color']
    internal_pattern = frame_data['internal_pattern']
    
    # Initialize with border color
    transformed = np.full((height, width), border_color, dtype=int)
    
    # Fill internal pattern with content color
    if internal_pattern:
        for r_rel, c_rel in internal_pattern:
             # Ensure relative coords are within bounds (should be by definition)
             if 0 <= r_rel < height and 0 <= c_rel < width:
                 transformed[r_rel, c_rel] = content_color
                 
    return transformed

def assemble_output(transformed_frames_map, original_frames):
    """Assembles the final output grid."""
    if not transformed_frames_map:
        # Handle cases where no frames were found or transformed
        # Maybe return an empty grid or based on task specifics?
        # Let's assume at least one frame is expected if the input has them.
        # If input truly had no frames, maybe return empty 1x1 grid?
        return np.array([[0]], dtype=int) # Default fallback

    # Find overall bounding box of original frames to determine layout
    all_min_r, all_min_c = float('inf'), float('inf')
    all_max_r, all_max_c = float('-inf'), float('-inf')
    
    for frame in original_frames:
        min_r, min_c, max_r, max_c = frame['bounds']
        all_min_r = min(all_min_r, min_r)
        all_min_c = min(all_min_c, min_c)
        all_max_r = max(all_max_r, max_r)
        all_max_c = max(all_max_c, max_c)
        
    # Calculate output dimensions based on relative positions
    output_height = 0
    output_width = 0
    frame_rel_positions = {}

    for frame in original_frames:
        frame_key = (frame['color'], tuple(frame['bounds']))
        if frame_key in transformed_frames_map:
            transformed_grid = transformed_frames_map[frame_key]
            h, w = transformed_grid.shape
            rel_r = frame['bounds'][0] - all_min_r
            rel_c = frame['bounds'][1] - all_min_c
            frame_rel_positions[frame_key] = (rel_r, rel_c)
            output_height = max(output_height, rel_r + h)
            output_width = max(output_width, rel_c + w)

    # Create output grid (use a common background color? Example 1 output uses frame colors, Example 2 too)
    # It seems the output grid contains *only* the transformed frames.
    # Initialize with a color not present? Or determine dominant background if frames overlap?
    # Let's initialize with 0 (white) and overwrite. If frames overlap, the later one wins.
    output_grid = np.full((output_height, output_width), 0, dtype=int) # Use 0 as default background

    # Place transformed frames (sort by original position to handle potential overlaps consistently?)
    sorted_original_frames = sorted(original_frames, key=lambda f: (f['bounds'][0], f['bounds'][1]))

    for frame in sorted_original_frames:
        frame_key = (frame['color'], tuple(frame['bounds']))
        if frame_key in transformed_frames_map:
            transformed_grid = transformed_frames_map[frame_key]
            h, w = transformed_grid.shape
            rel_r, rel_c = frame_rel_positions[frame_key]
            output_grid[rel_r:rel_r+h, rel_c:rel_c+w] = transformed_grid

    return output_grid


def transform(input_grid):
    """
    Transforms the input grid by identifying 'frame' objects and 'content' objects.
    The internal pattern of each frame (made of a placeholder color) is replaced 
    by the color of a corresponding content object, based on their spatial relationship.
    The transformed frames are then assembled into the output grid, maintaining their
    relative positions.
    """
    input_grid = np.array(input_grid, dtype=int)
    height, width = input_grid.shape

    # 1. Analyze objects to find frames, contents, and placeholder color
    frames, contents, placeholder_color = analyze_objects(input_grid, None) # Pass None first, placeholder determined inside

    if not frames or not contents:
         # If no frames or no contents found, the transformation likely doesn't apply
         # Return maybe an empty grid or the input? Task description unclear.
         # Based on examples, output is derived from frames. No frames -> empty output?
         print("Warning: No frames or contents found.")
         # Let's try returning a 1x1 black grid as a default signal
         return np.array([[0]], dtype=int) 

    # 2. Pair frames with contents
    pairing = pair_frames_contents(frames, contents, input_grid.shape)
    
    if not pairing:
        print("Warning: Could not pair frames and contents.")
        return np.array([[0]], dtype=int) 


    # 3. Transform each frame based on its paired content
    transformed_frames = {}
    original_frame_map = {(f['color'], tuple(f['bounds'])): f for f in frames}

    for frame_key, content_data in pairing.items():
        if frame_key in original_frame_map:
            original_frame_data = original_frame_map[frame_key]
            content_color = content_data['color']
            transformed_grid = transform_frame(original_frame_data, content_color)
            transformed_frames[frame_key] = transformed_grid
        else:
             print(f"Warning: Frame key {frame_key} from pairing not found in original frames.")


    # 4. Assemble the output grid
    output_grid = assemble_output(transformed_frames, frames)

    return output_grid.tolist() # Return as list of lists per requirement

