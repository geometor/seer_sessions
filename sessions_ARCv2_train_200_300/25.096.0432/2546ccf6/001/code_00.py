import numpy as np
import copy

"""
The transformation identifies horizontal and vertical grid lines composed of a single, repeating non-zero integer (G). These lines partition the grid into sections. 
It then iterates through vertically adjacent sections. 
If a section contains only zeros (is 'empty') and its immediate vertical neighbor (above or below) contains a pattern (non-zero values other than G), the pattern from the neighbor is copied into the empty section, but flipped vertically. 
Grid lines and sections that do not meet these conditions remain unchanged.
"""

def _find_grid_lines(grid_np: np.ndarray) -> tuple[list[int], list[int], int | None]:
    """
    Finds the indices of horizontal and vertical grid lines and the separator value.
    Assumes lines are solid runs of the same non-zero digit.
    """
    rows, cols = grid_np.shape
    h_lines = []
    v_lines = []
    separator_val = None

    # Find potential separator value (look for solid non-zero rows/cols)
    potential_sep_vals = set()
    for r in range(rows):
        unique_vals = np.unique(grid_np[r, :])
        if len(unique_vals) == 1 and unique_vals[0] != 0:
            potential_sep_vals.add(unique_vals[0])
            break # Assume first found is the one
    if not potential_sep_vals:
         for c in range(cols):
            unique_vals = np.unique(grid_np[:, c])
            if len(unique_vals) == 1 and unique_vals[0] != 0:
                potential_sep_vals.add(unique_vals[0])
                break # Assume first found is the one

    if not potential_sep_vals:
        # Fallback: Check a few specific points if no solid lines found initially
        # This might be brittle but covers the example structure
        candidates = [grid_np[0, 4], grid_np[4, 0], grid_np[0, 9], grid_np[9,0]] # Example locations
        non_zero_candidates = [c for c in candidates if c != 0]
        if non_zero_candidates:
             separator_val = non_zero_candidates[0] # Take the first one
        else: # No clear separator found
             return [], [], None
    else:
        separator_val = potential_sep_vals.pop()

    # Find horizontal lines
    for r in range(rows):
        if np.all(grid_np[r, :] == separator_val):
            h_lines.append(r)

    # Find vertical lines
    for c in range(cols):
         if np.all(grid_np[:, c] == separator_val):
            v_lines.append(c)

    return h_lines, v_lines, separator_val


def _get_section_coords(rows: int, cols: int, h_lines: list[int], v_lines: list[int]) -> list[tuple[int, int, int, int]]:
    """
    Determines the content coordinates (excluding boundary lines) of each section.
    Returns list of tuples: (row_start, row_end, col_start, col_end)
    """
    sections = []
    row_boundaries = [-1] + h_lines + [rows]
    col_boundaries = [-1] + v_lines + [cols]

    for i in range(len(row_boundaries) - 1):
        r_start = row_boundaries[i] + 1
        r_end = row_boundaries[i+1]
        if r_start >= r_end: continue # Skip if section has zero height

        for j in range(len(col_boundaries) - 1):
            c_start = col_boundaries[j] + 1
            c_end = col_boundaries[j+1]
            if c_start >= c_end: continue # Skip if section has zero width

            sections.append((r_start, r_end, c_start, c_end))

    return sections

def _get_section_content(grid_np: np.ndarray, coords: tuple[int, int, int, int]) -> np.ndarray:
    """Extracts the content of a section given its coordinates."""
    r_start, r_end, c_start, c_end = coords
    return grid_np[r_start:r_end, c_start:c_end]

def _is_section_empty(content: np.ndarray) -> bool:
    """Checks if a section's content is all zeros."""
    return np.all(content == 0)

def _has_pattern(content: np.ndarray, separator_val: int) -> bool:
    """Checks if a section's content has any non-zero values other than the separator."""
    # Check if any element is not 0 AND not the separator value
    return np.any((content != 0) & (content != separator_val))


def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Identifies grid sections separated by lines of a single non-zero digit 'G'.
    If a section contains only zeros and is vertically adjacent to a section
    containing a pattern (non-zero, non-G values), the pattern is copied
    into the zero section, flipped vertically.
    """
    # Convert to numpy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)
    output_np = input_np.copy() # Start with a copy
    rows, cols = input_np.shape

    # Find grid lines and the separator value
    h_lines, v_lines, separator_val = _find_grid_lines(input_np)

    # If no separator found, return input as is (or handle error)
    if separator_val is None:
        print("Warning: Could not determine grid separator value.")
        return input_grid # Or raise an error

    # Define the sections based on the grid lines
    section_coords = _get_section_coords(rows, cols, h_lines, v_lines)

    # Create a mapping from starting row/col to section index for easier lookup
    coord_map = {(r_start, c_start): i for i, (r_start, r_end, c_start, c_end) in enumerate(section_coords)}

    # Iterate through sections to find vertically adjacent pairs
    for i, (r_start1, r_end1, c_start1, c_end1) in enumerate(section_coords):
        # Look for a section directly below (starts where current section ends + 1 for the line)
        lower_neighbor_coord_key = (r_end1 + 1, c_start1)
        if lower_neighbor_coord_key in coord_map:
            j = coord_map[lower_neighbor_coord_key]
            r_start2, r_end2, c_start2, c_end2 = section_coords[j]

            # Ensure columns align (should be guaranteed by grid structure)
            if c_start1 == c_start2 and c_end1 == c_end2:
                # Section 1 is upper, Section 2 is lower
                upper_coords = (r_start1, r_end1, c_start1, c_end1)
                lower_coords = (r_start2, r_end2, c_start2, c_end2)

                # Get content from the ORIGINAL input grid
                upper_content = _get_section_content(input_np, upper_coords)
                lower_content = _get_section_content(input_np, lower_coords)

                # Check conditions and apply transformation to output_np

                # Case 1: Upper is empty, Lower has pattern
                if _is_section_empty(upper_content) and _has_pattern(lower_content, separator_val):
                    # Ensure dimensions match before copying
                    if upper_content.shape == lower_content.shape:
                        flipped_pattern = np.flipud(lower_content)
                        output_np[r_start1:r_end1, c_start1:c_end1] = flipped_pattern
                    # else: print warning or handle mismatch

                # Case 2: Lower is empty, Upper has pattern
                elif _is_section_empty(lower_content) and _has_pattern(upper_content, separator_val):
                     # Ensure dimensions match before copying
                    if upper_content.shape == lower_content.shape:
                        flipped_pattern = np.flipud(upper_content)
                        output_np[r_start2:r_end2, c_start2:c_end2] = flipped_pattern
                    # else: print warning or handle mismatch


    # Convert back to list of lists for the final output
    output_grid = output_np.tolist()
    return output_grid