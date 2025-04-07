import numpy as np
from collections import Counter, defaultdict
import itertools

"""
Identifies hollow rectangular frames in the input grid. For each frame, it analyzes the pixels within its bounds but not part of the border itself. It determines a global 'placeholder' color (P) which is common across frame interiors and is replaced in the output. It also identifies a 'content' color (C_content) specific to each frame's interior (the non-P color). The transformation then creates new versions of each frame where the border is preserved, but internal pixels originally colored P are replaced with C_content. Finally, these transformed frames are assembled into an output grid, maintaining their original relative spatial arrangement, on a default white background.
"""

# ============================================
# Helper Functions: Finding Objects & Properties
# ============================================

def find_contiguous_regions(grid, colors_to_find=None, ignore_colors=None):
    """Finds all contiguous regions for specified colors, ignoring others."""
    height, width = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    regions = defaultdict(list) # color -> list of sets of coordinates

    for r in range(height):
        for c in range(width):
            color = grid[r, c]
            if visited[r, c]:
                continue

            # Check if this color should be processed
            valid_start = True
            if ignore_colors is not None and color in ignore_colors:
                valid_start = False
            if colors_to_find is not None and color not in colors_to_find:
                 valid_start = False

            if not valid_start:
                visited[r,c] = True # Mark visited anyway
                continue

            # Start BFS for a new region
            region_coords = set()
            q = [(r, c)]
            visited[r, c] = True
            region_color = color

            while q:
                row, col = q.pop(0)
                region_coords.add((row, col))

                # Check neighbors (4-connectivity)
                for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                    nr, nc = row + dr, col + dc
                    if 0 <= nr < height and 0 <= nc < width and \
                       not visited[nr, nc] and grid[nr, nc] == region_color:
                        visited[nr, nc] = True
                        q.append((nr, nc))

            if region_coords:
                regions[region_color].append(region_coords)

    return regions

def get_bounding_box(coords):
    """Calculates the bounding box (min_r, min_c, max_r, max_c) of a set of coordinates."""
    if not coords:
        return None
    rows = [r for r, c in coords]
    cols = [c for r, c in coords]
    return min(rows), min(cols), max(rows), max(cols)

def is_hollow_rectangle(coords, grid_shape):
    """Checks if a set of coordinates forms a hollow rectangle."""
    if len(coords) < 4: # Need at least 4 points for a minimal 2x2 frame (or 3x3 box)
        return False, None

    min_r, min_c, max_r, max_c = get_bounding_box(coords)
    height = max_r - min_r + 1
    width = max_c - min_c + 1

    # Basic size check (must be at least 3x3 to have a distinct interior)
    if height < 3 or width < 3:
        return False, None

    # Check if all expected border pixels are present
    expected_border_pixels = set()
    for r in range(min_r, max_r + 1):
        if (r, min_c) not in coords: return False, None
        if (r, max_c) not in coords: return False, None
        expected_border_pixels.add((r, min_c))
        expected_border_pixels.add((r, max_c))
    for c in range(min_c + 1, max_c): # Avoid double counting corners
        if (min_r, c) not in coords: return False, None
        if (max_r, c) not in coords: return False, None
        expected_border_pixels.add((min_r, c))
        expected_border_pixels.add((max_r, c))
        
    # Ensure the object *only* consists of border pixels (it shouldn't contain internal pixels of the same color)
    if coords != expected_border_pixels:
        return False, None

    # Check if there's a potential interior (at least one non-border pixel within bounds)
    has_potential_interior = False
    for r in range(min_r + 1, max_r):
        for c in range(min_c + 1, max_c):
            # Check grid bounds just in case, though should be within by definition
            # if 0 <= r < grid_shape[0] and 0 <= c < grid_shape[1]: # Not needed if bounds are correct
            has_potential_interior = True
            break
        if has_potential_interior: break

    if not has_potential_interior:
        return False, None # Not hollow

    return True, (min_r, min_c, max_r, max_c)

# ============================================
# Helper Functions: Analysis
# ============================================

def find_frames(grid):
    """Identifies hollow rectangular frame objects in the grid."""
    frames = []
    # Consider all colors except 0 (white) as potential frame colors initially
    # Background/separator colors will be filtered out if they don't form hollow rectangles
    potential_frame_colors = np.unique(grid[grid != 0])
    if len(potential_frame_colors) == 0:
         return [] # No non-white colors

    all_regions = find_contiguous_regions(grid, colors_to_find=potential_frame_colors)

    obj_id_counter = 0
    for color, regions_list in all_regions.items():
        for region_coords in regions_list:
            is_frame, bounds = is_hollow_rectangle(region_coords, grid.shape)
            if is_frame:
                frames.append({
                    "id": obj_id_counter,
                    "color": color,
                    "coords": region_coords,
                    "bounds": bounds, # (min_r, min_c, max_r, max_c)
                    "height": bounds[2] - bounds[0] + 1,
                    "width": bounds[3] - bounds[1] + 1,
                    "key": (color, bounds) # Unique identifier
                })
                obj_id_counter += 1
    return frames

def analyze_interiors_and_find_placeholder(grid, frames):
    """Analyzes pixels inside frames to find placeholder and content colors."""
    internal_colors_by_frame = {} # frame_key -> set of internal colors
    all_internal_colors_counts = Counter()
    internal_pixels_by_frame = {} # frame_key -> set of internal coords

    if not frames:
        return -1, {}, {} # Return default placeholder (-1), empty dicts

    for frame in frames:
        frame_key = frame["key"]
        min_r, min_c, max_r, max_c = frame["bounds"]
        frame_coords = frame["coords"]
        internal_colors = set()
        internal_pixels = set()

        for r in range(min_r + 1, max_r):
            for c in range(min_c + 1, max_c):
                # Check if the pixel is inside bounds but NOT part of the frame border itself
                # The is_hollow_rectangle check already ensures frame_coords only contains the border
                coord = (r, c)
                # Double check it's not part of frame coords (shouldn't be necessary with correct is_hollow_rectangle)
                if coord not in frame_coords:
                    color = grid[r, c]
                    internal_colors.add(color)
                    all_internal_colors_counts[color] += 1
                    internal_pixels.add(coord)


        internal_colors_by_frame[frame_key] = internal_colors
        internal_pixels_by_frame[frame_key] = internal_pixels

    # Determine placeholder color (P)
    # Heuristic: Most frequent color found across all internal areas.
    placeholder_color = -1 # Default
    if all_internal_colors_counts:
        # Sort by count (desc) then by color (asc) for determinism
        sorted_internal_colors = sorted(all_internal_colors_counts.items(), key=lambda item: (-item[1], item[0]))
        placeholder_color = sorted_internal_colors[0][0]

    return placeholder_color, internal_colors_by_frame, internal_pixels_by_frame


def find_content_colors(internal_colors_by_frame, placeholder_color):
    """Determines the content color for each frame."""
    content_colors = {} # frame_key -> content_color

    for frame_key, colors_in_interior in internal_colors_by_frame.items():
        possible_content_colors = colors_in_interior - {placeholder_color}
        
        if len(possible_content_colors) == 1:
            content_colors[frame_key] = list(possible_content_colors)[0]
        elif len(possible_content_colors) == 0:
             # If only placeholder color is inside, maybe content color is same as frame color?
             # Or maybe the frame should be filled entirely with frame color?
             # Let's assume content color = frame color in this case.
             frame_color = frame_key[0] # Get color from frame_key (color, bounds)
             content_colors[frame_key] = frame_color
             # print(f"Warning: Frame {frame_key} interior only contains placeholder. Assuming content color = frame color ({frame_color}).")
        else:
            # Multiple non-placeholder colors found. This case is ambiguous based on examples.
            # Let's pick the most frequent one *within this specific frame* as a guess.
            # Or maybe the least frequent? Or rely on order? Default to first found.
            # This needs refinement if such cases occur.
            # print(f"Warning: Frame {frame_key} interior has multiple non-placeholder colors: {possible_content_colors}. Picking first one.")
            content_colors[frame_key] = sorted(list(possible_content_colors))[0]

    return content_colors

# ============================================
# Helper Functions: Transformation & Assembly
# ============================================

def transform_single_frame(grid, frame_data, internal_pixels, placeholder_color, content_color):
    """Creates the transformed grid for a single frame."""
    height = frame_data['height']
    width = frame_data['width']
    frame_color = frame_data['color']
    min_r, min_c, _, _ = frame_data['bounds']

    # Initialize the new frame grid - start with content color, then draw border? Or vice versa?
    # Let's initialize with a temp value (-1) then fill border and interior.
    transformed_grid = np.full((height, width), -1, dtype=int)

    # Iterate through the relative coordinates of the new grid
    for r_rel in range(height):
        for c_rel in range(width):
            orig_r, orig_c = min_r + r_rel, min_c + c_rel
            coord = (orig_r, orig_c)

            if coord in frame_data['coords']: # Is it a border pixel?
                transformed_grid[r_rel, c_rel] = frame_color
            elif coord in internal_pixels: # Is it an internal pixel?
                original_color = grid[orig_r, orig_c]
                if original_color == placeholder_color:
                    transformed_grid[r_rel, c_rel] = content_color
                else:
                    # Assume it was already the content color or another color to preserve
                    # Based on the logic, it *should* be the content color if not placeholder
                    transformed_grid[r_rel, c_rel] = original_color
            else:
                # Should not happen if internal_pixels covers all non-border pixels within bounds
                # If it does, maybe fill with default background (0)? Or leave as -1 for debugging?
                # Let's fill with white (0) as a safe default for unexpected spots inside bounds.
                transformed_grid[r_rel, c_rel] = 0
                # print(f"Warning: Coordinate {coord} is within bounds but neither border nor identified internal pixel for frame {frame_data['key']}. Filling with 0.")


    # Check for any remaining -1s (indicates logic error)
    if np.any(transformed_grid == -1):
         print(f"Error: Untouched pixels (-1) remaining in transformed frame {frame_data['key']}. Filling with 0.")
         transformed_grid[transformed_grid == -1] = 0


    return transformed_grid


def assemble_output(transformed_frames_map, original_frames):
    """Assembles the final output grid."""
    if not transformed_frames_map or not original_frames:
        return np.array([[0]], dtype=int) # Default minimal grid

    # Find overall bounding box of original frames
    all_min_r, all_min_c = float('inf'), float('inf')
    all_max_r, all_max_c = float('-inf'), float('-inf')

    original_frame_data_map = {f['key']: f for f in original_frames}

    # Use keys present in transformed_frames_map for bounds calculation
    relevant_keys = transformed_frames_map.keys()
    if not relevant_keys:
        return np.array([[0]], dtype=int)

    for frame_key in relevant_keys:
        if frame_key in original_frame_data_map:
            min_r, min_c, max_r, max_c = original_frame_data_map[frame_key]['bounds']
            all_min_r = min(all_min_r, min_r)
            all_min_c = min(all_min_c, min_c)
            all_max_r = max(all_max_r, max_r)
            all_max_c = max(all_max_c, max_c)
        else:
            # This indicates a key mismatch, should not happen
            print(f"Warning: Key {frame_key} from transformed map not found in original frames for bounds calculation.")


    if all_min_r == float('inf'): # No valid frames found/matched
        return np.array([[0]], dtype=int)

    output_height = all_max_r - all_min_r + 1
    output_width = all_max_c - all_min_c + 1

    # Create output grid, initialized with white (0)
    output_grid = np.full((output_height, output_width), 0, dtype=int)

    # Sort original frames by top-left corner for consistent placement order
    sorted_original_frames = sorted(original_frames, key=lambda f: (f['bounds'][0], f['bounds'][1]))

    # Place transformed frames
    for frame_data in sorted_original_frames:
        frame_key = frame_data['key']
        if frame_key in transformed_frames_map:
            transformed_grid = transformed_frames_map[frame_key]
            h, w = transformed_grid.shape
            
            # Calculate relative position in the output grid
            orig_min_r, orig_min_c, _, _ = frame_data['bounds']
            rel_r = orig_min_r - all_min_r
            rel_c = orig_min_c - all_min_c

            # Place the transformed grid
            if rel_r >= 0 and rel_c >= 0 and rel_r + h <= output_height and rel_c + w <= output_width:
                output_grid[rel_r:rel_r + h, rel_c:rel_c + w] = transformed_grid
            else:
                 # This suggests an issue with overall bounds calculation or frame size mismatch
                 print(f"Warning: Frame {frame_key} placement [{rel_r}:{rel_r+h}, {rel_c}:{rel_c+w}] out of bounds for output grid size ({output_height}, {output_width}). Clipping.")
                 # Attempt to clip placement
                 paste_h = min(h, output_height - rel_r)
                 paste_w = min(w, output_width - rel_c)
                 if paste_h > 0 and paste_w > 0 and rel_r>=0 and rel_c>=0:
                     output_grid[rel_r:rel_r + paste_h, rel_c:rel_c + paste_w] = transformed_grid[:paste_h, :paste_w]


    return output_grid


# ============================================
# Main Transformation Function
# ============================================

def transform(input_grid):
    """
    Applies the frame interior transformation rule to the input grid.
    """
    # Convert input to numpy array for processing
    input_grid_np = np.array(input_grid, dtype=int)

    # Step 1: Identify Frame Objects
    frames = find_frames(input_grid_np)
    if not frames:
        # print("No frames identified. Returning default grid.")
        return np.array([[0]], dtype=int).tolist()

    # Step 2 & 3: Analyze Frame Interiors & Determine Placeholder Color (P)
    placeholder_color, internal_colors_by_frame, internal_pixels_by_frame = analyze_interiors_and_find_placeholder(input_grid_np, frames)
    if placeholder_color == -1:
        # print("Could not determine placeholder color. Returning default grid.")
        # This might happen if frames have no interior pixels
        return np.array([[0]], dtype=int).tolist()

    # Step 4: Identify Frame-Specific Content Color (C_content)
    content_colors = find_content_colors(internal_colors_by_frame, placeholder_color)
    if not content_colors:
         # This might happen if internal_colors_by_frame was empty etc.
         # print("Could not determine content colors. Returning default grid.")
         return np.array([[0]], dtype=int).tolist()

    # Step 5: Transform Frames
    transformed_frames_map = {} # frame_key -> transformed_grid
    for frame_data in frames:
        frame_key = frame_data['key']
        if frame_key in content_colors and frame_key in internal_pixels_by_frame:
            content_color = content_colors[frame_key]
            internal_pixels = internal_pixels_by_frame[frame_key]
            transformed_grid = transform_single_frame(input_grid_np, frame_data, internal_pixels, placeholder_color, content_color)
            transformed_frames_map[frame_key] = transformed_grid
        else:
            # print(f"Warning: Missing content color or internal pixels for frame {frame_key}. Skipping transformation.")
             pass


    # Step 6: Assemble Output Grid
    output_grid_np = assemble_output(transformed_frames_map, frames)

    # Convert final numpy array back to list of lists for the required output format
    return output_grid_np.tolist()