import numpy as np

"""
Identify magenta (6) lines (rows or columns) that act as separators in the input grid.
Determine the layout of segments (subgrids between separators) based on whether separators are rows, columns, or both.
Extract these segments.
Rearrange the segments into a new grid based on the identified layout:
- If the input layout was a 2x2 grid (row and column separators), stack segments vertically in the order: top-left, bottom-right, top-right, bottom-left, separated by magenta rows.
- If the input layout was a vertical stack (row separators), arrange segments horizontally in reverse order (bottom to top becomes left to right), separated by magenta columns.
- If the input layout was a horizontal row (column separators), stack segments vertically in the original order (left to right becomes top to bottom), separated by magenta rows.
"""

# Define color constants
SEPARATOR_COLOR = 6
BACKGROUND_COLOR = 7 # Not strictly needed for logic but good for context

def find_separators(grid):
    """Finds the indices of complete rows and columns made of SEPARATOR_COLOR."""
    rows, cols = grid.shape
    separator_rows = [r for r in range(rows) if np.all(grid[r, :] == SEPARATOR_COLOR)]
    separator_cols = [c for c in range(cols) if np.all(grid[:, c] == SEPARATOR_COLOR)]
    return separator_rows, separator_cols

def determine_layout(separator_rows, separator_cols):
    """Determines the layout based on the presence of row and/or column separators."""
    has_row_sep = len(separator_rows) > 0
    has_col_sep = len(separator_cols) > 0
    
    if has_row_sep and has_col_sep:
        return '2x2 grid'
    elif has_row_sep:
        return 'vertical stack'
    elif has_col_sep:
        return 'horizontal row'
    else:
        # Should not happen based on examples, but handle defensively
        return 'unknown' 

def extract_segments(grid, separator_rows, separator_cols, layout):
    """Extracts segments (subgrids) based on separator locations and layout."""
    segments = []
    rows, cols = grid.shape

    # Define potential segment boundaries
    row_boundaries = [-1] + separator_rows + [rows]
    col_boundaries = [-1] + separator_cols + [cols]

    # Iterate through potential segment areas defined by boundaries
    for r_idx in range(len(row_boundaries) - 1):
        r_start = row_boundaries[r_idx] + 1
        r_end = row_boundaries[r_idx + 1]
        
        # Skip if the segment height is zero (adjacent separators)
        if r_start >= r_end:
            continue

        for c_idx in range(len(col_boundaries) - 1):
            c_start = col_boundaries[c_idx] + 1
            c_end = col_boundaries[c_idx + 1]

            # Skip if the segment width is zero
            if c_start >= c_end:
                continue
            
            segment = grid[r_start:r_end, c_start:c_end]
            # Store segment along with its original top-left corner for ordering later if needed
            segments.append({'grid': segment, 'pos': (r_start, c_start)})

    # Sort segments based on reading order (top-to-bottom, left-to-right) for consistency
    segments.sort(key=lambda s: (s['pos'][0], s['pos'][1]))
    
    return [s['grid'] for s in segments]


def transform(input_grid):
    """
    Transforms the input grid by identifying segments separated by magenta lines,
    determining the layout, extracting segments, and rearranging them according
    to specific rules based on the layout.
    """
    input_np = np.array(input_grid, dtype=int)
    
    # 1. Identify Separators
    separator_rows, separator_cols = find_separators(input_np)

    # 2. Determine Input Layout
    layout = determine_layout(separator_rows, separator_cols)

    # 3. Extract Segments
    # Ensure segments are extracted in a consistent order (e.g., reading order)
    segments = extract_segments(input_np, separator_rows, separator_cols, layout)

    if not segments:
        # Handle cases where no segments are found (e.g., input is just separators or empty)
        # Based on examples, this shouldn't happen with valid inputs.
        # Returning an empty grid or the input might be options, but let's assume valid input.
        return np.array([[]]) 

    segment_h, segment_w = segments[0].shape
    num_segments = len(segments)
    separator_thickness = 1 # Assuming single line separators

    # 4. Rearrange Segments based on layout
    if layout == '2x2 grid':
        # Expecting 4 segments for a 2x2 layout
        if num_segments != 4:
             raise ValueError(f"Expected 4 segments for 2x2 layout, found {num_segments}")
        # Order: top-left (0), bottom-right (3), top-right (1), bottom-left (2)
        ordered_segments = [segments[0], segments[3], segments[1], segments[2]]
        
        # Arrangement: vertical stack
        output_h = num_segments * segment_h + (num_segments - 1) * separator_thickness
        output_w = segment_w
        output_grid = np.full((output_h, output_w), BACKGROUND_COLOR, dtype=int) # Fill with background initially
        
        current_row = 0
        for i, seg in enumerate(ordered_segments):
            output_grid[current_row : current_row + segment_h, :] = seg
            current_row += segment_h
            if i < num_segments - 1:
                output_grid[current_row : current_row + separator_thickness, :] = SEPARATOR_COLOR
                current_row += separator_thickness

    elif layout == 'vertical stack':
        # Order: reversed input order (bottom to top becomes left to right)
        ordered_segments = segments[::-1] 
        
        # Arrangement: horizontal row
        output_h = segment_h
        output_w = num_segments * segment_w + (num_segments - 1) * separator_thickness
        output_grid = np.full((output_h, output_w), BACKGROUND_COLOR, dtype=int) # Fill with background initially
        
        current_col = 0
        for i, seg in enumerate(ordered_segments):
            output_grid[:, current_col : current_col + segment_w] = seg
            current_col += segment_w
            if i < num_segments - 1:
                output_grid[:, current_col : current_col + separator_thickness] = SEPARATOR_COLOR
                current_col += separator_thickness
                
    elif layout == 'horizontal row':
        # Order: same as input order (left to right becomes top to bottom)
        ordered_segments = segments 
        
        # Arrangement: vertical stack
        output_h = num_segments * segment_h + (num_segments - 1) * separator_thickness
        output_w = segment_w
        output_grid = np.full((output_h, output_w), BACKGROUND_COLOR, dtype=int) # Fill with background initially
        
        current_row = 0
        for i, seg in enumerate(ordered_segments):
            output_grid[current_row : current_row + segment_h, :] = seg
            current_row += segment_h
            if i < num_segments - 1:
                output_grid[current_row : current_row + separator_thickness, :] = SEPARATOR_COLOR
                current_row += separator_thickness

    else: # Unknown layout or error
        # Fallback or error handling - perhaps return input or empty
        # Based on problem constraints, this path shouldn't be hit for valid test cases.
        # Returning input grid as a safe default if logic fails.
        print(f"Warning: Unknown or unhandled layout '{layout}'. Returning original grid.")
        return input_np

    # 5. Return Output Grid
    return output_grid.tolist() # Convert back to list of lists for ARC standard output
