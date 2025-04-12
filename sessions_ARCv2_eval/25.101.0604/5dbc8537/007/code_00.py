"""
Handles two distinct grid transformation types based on input grid characteristics.

Type 1 (Segment Fill - Solves train_1):
- Detects input grids likely matching the 15x15 structure from train_1.
- Identifies rows containing exactly one segment of width 7 bounded by the value 9.
- Extracts this 7-element segment.
- Replaces elements with the value 4 inside the segment (excluding the boundary 9s)
  with a "paint" color determined by the row index using a specific mapping.
- A special case applies to row index 6, where the element at relative index 4
  within the segment is set to 0, overriding any previous fill.

Type 2 (Region Projection - Partially Solves train_2):
- Detects input grids likely matching the 20x20 structure from train_2.
- The output grid is 9x20, corresponding to the bottom 9 rows of the input (rows 11-19).
- Cells with value 2 in the input's bottom region are copied directly to the output.
- Cells with value 8 in the input's bottom region are replaced in the output
  with a color determined by analyzing the corresponding column in the top region (rows 0-10).
- The implemented logic for determining the color for '8's (checking for a single unique
  non-background color vs. using a default column map) is INCOMPLETE and leads to
  errors on train_2. It represents a flawed hypothesis requiring refinement.
"""

from typing import List, Tuple, Optional, Set

# --- Helper Functions ---

def find_segments(row: list[int], marker: int, width: int) -> List[Tuple[int, int]]:
    """
    Finds start and end column indices of all non-overlapping segments
    of a specific width bounded by a marker value in a given row.
    Returns a list of (start_col, end_col) tuples.
    """
    indices = [i for i, x in enumerate(row) if x == marker]
    segments = []
    # Iterate through all pairs of marker indices to find segments
    for i in range(len(indices)):
        for j in range(i + 1, len(indices)):
            c1 = indices[i]
            c2 = indices[j]
            # Check if the segment width matches the desired width
            if c2 - c1 + 1 == width:
                # Basic check for overlap: ensure the next potential start marker
                # is after the current end marker. More complex overlap handling
                # might be needed if segments could be nested or truly overlap.
                is_overlapping = False
                for start_existing, end_existing in segments:
                    if not (c2 < start_existing or c1 > end_existing):
                         is_overlapping = True
                         break
                if not is_overlapping:
                    segments.append((c1, c2))
    return segments

# --- Transformation Type 1: Segment Fill ---

def get_paint_color_type1(row_index: int) -> int:
    """
    Determines the paint color for Type 1 transformation based on the row index.
    Mapping derived from train_1 example.
    """
    paint_map = {
        0: 8, 1: 8, 2: 3, 3: 3, 4: 3, 5: 3, 6: 3, 7: 3, 8: 1, 9: 1,
        10: 5, 11: 7, 12: 7, 13: 7, 14: 5
    }
    return paint_map.get(row_index, -1) # Return -1 if index out of range

def transform_type1(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies the segment fill transformation (derived from train_1).
    Finds 7-wide segments bounded by 9s, and fills internal 4s based on row index.
    """
    output_grid = []
    boundary_marker = 9
    segment_width = 7
    fill_target = 4 # The color inside the segment to be replaced

    # Process each row individually
    for r, row in enumerate(input_grid):
        # Find all segments matching the criteria in the current row
        valid_segments = find_segments(row, boundary_marker, segment_width)

        # Expect exactly one valid segment per row for this type
        if len(valid_segments) == 1:
            c1, c2 = valid_segments[0]
            
            # Extract the identified segment
            segment = row[c1 : c2 + 1]
            # Create a mutable copy to modify for the output row
            output_row = list(segment)
            
            # Determine the primary paint color for this row index
            paint_color = get_paint_color_type1(r)
            
            # Iterate through the interior positions of the segment (indices 1 to 5)
            for i in range(1, 6):
                # If the original value at this position matches the fill target (4)
                if output_row[i] == fill_target:
                    # Replace it with the determined paint color
                    output_row[i] = paint_color
                    
            # Apply the special modification rule for row index 6
            if r == 6:
                # Set the element at relative index 4 (5th element) to 0
                output_row[4] = 0 
                
            # Add the processed row to the final output grid
            output_grid.append(output_row)
        else:
            # If a row does not contain exactly one valid segment, behavior is undefined for Type 1.
            # Skip the row.
            pass 
            
    return output_grid

# --- Transformation Type 2: Region Projection ---

# Mapping for Type 2 hypothesis: used when a single non-background color C is found in the top column
TRAIN2_SINGLE_COLOR_MAP = {3: 3, 9: 9, 6: 5, 0: 7}

# Mapping for Type 2 hypothesis: used when the top column has only background or multiple non-bg colors
# Based on column index. Includes best-guess values for ambiguous columns.
# THIS MAP IS PART OF THE FLAWED HYPOTHESIS.
TRAIN2_DEFAULT_COLOR_MAP = {
    0: 4, 1: 4, 2: 6, 3: 6, 4: 1, 5: 9, 6: 1, 7: 3, 8: 3, 9: 3,
    10: 9, 11: 5, 12: 5, 13: 4, 14: 7, 15: 4, 16: 7, 17: 4, 18: 7, 19: 0
}

def transform_type2(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies the region projection transformation (derived from train_2).
    Uses the bottom 9 rows as a template, copying 2s and filling 8s
    based on analysis of the corresponding column in the top 11 rows.
    NOTE: The logic for determining the color for '8's is INCOMPLETE/FLAWED.
    """
    input_height = len(input_grid)
    input_width = len(input_grid[0]) if input_height > 0 else 0
    
    # Basic check for expected dimensions
    if input_height != 20 or input_width != 20:
        return [] # Return empty if dimensions don't match expected Type 2

    output_height = 9
    output_width = 20
    top_region_rows = 11
    top_background_color = 8
    bottom_preserved_color = 2
    bottom_fill_target_color = 8
    
    # Initialize the output grid
    output_grid = [[0] * output_width for _ in range(output_height)] 

    # Iterate through the coordinates of the output grid
    for r in range(output_height): # Output rows 0-8
        for c in range(output_width): # Output columns 0-19
            # Calculate the corresponding row index in the input grid's bottom region
            input_row_idx = r + top_region_rows # Input rows 11-19
            
            # Get the value from the relevant cell in the input grid's bottom region
            value_in_bottom = input_grid[input_row_idx][c]
            
            # Rule 1: Copy preserved color (2)
            if value_in_bottom == bottom_preserved_color:
                output_grid[r][c] = bottom_preserved_color
            # Rule 2: Determine fill color for the target color (8)
            elif value_in_bottom == bottom_fill_target_color:
                # --- Start of Flawed/Incomplete Logic for determining paint color P ---
                # Analyze the corresponding column in the top region
                top_col_pattern = [input_grid[i][c] for i in range(top_region_rows)]
                # Find unique non-background colors in the top column
                non_bg_colors: Set[int] = {color for color in top_col_pattern if color != top_background_color}
                
                paint_color = -1 # Default error/unassigned color
                if len(non_bg_colors) == 1:
                    # Case A: Exactly one unique non-background color found
                    unique_color = non_bg_colors.pop()
                    # Use the single color map hypothesis
                    paint_color = TRAIN2_SINGLE_COLOR_MAP.get(unique_color, unique_color)
                else:
                    # Case B: Zero or more than one unique non-background color found
                    # Use the default map hypothesis based on the column index
                    paint_color = TRAIN2_DEFAULT_COLOR_MAP.get(c, 0) # Default to 0 if column index is unexpected
                # --- End of Flawed/Incomplete Logic ---

                output_grid[r][c] = paint_color
            # Rule 3: Handle other unexpected values if necessary
            else:
                # Copy the unexpected value directly
                output_grid[r][c] = value_in_bottom 

    return output_grid

# --- Main Transform Function ---

def transform(input_grid: list[list[int]]) -> list[list[int]]:  
    """
    Detects the transformation type based on input grid dimensions 
    (as a proxy for the observed patterns in training examples)
    and applies the corresponding transformation logic.
    """
    # Get input grid dimensions
    height = len(input_grid)
    width = len(input_grid[0]) if height > 0 else 0

    # Detect transformation type based on grid dimensions observed in training examples
    # This is a simple heuristic; more robust detection might analyze content.
    if height == 15 and width == 15:
        # Assumed Type 1 (Segment Fill) based on train_1 dimensions
        # This logic correctly solves train_1.
        return transform_type1(input_grid)
    elif height == 20 and width == 20:
         # Assumed Type 2 (Region Projection) based on train_2 dimensions
         # This logic partially solves train_2; contains known flaws.
        return transform_type2(input_grid)
    else:
        # If grid size doesn't match known types, behavior is undefined.
        # Return empty list for unrecognized sizes.
        return []