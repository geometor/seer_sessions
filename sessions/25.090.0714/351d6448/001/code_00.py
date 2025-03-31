import numpy as np
from typing import List, Tuple, Optional, Dict, Any

"""
Transformation Rule:

1.  Identify horizontal separator lines made of gray pixels (color 5) in the input grid. These lines divide the grid into sequential stages.
2.  Within each stage (the rows above a separator line, or the top rows if no separator is above), locate the row containing a colored object pattern (non-white, non-gray pixels).
3.  Extract the object pattern (sequence of colors) and its starting column index for each stage.
4.  Analyze the sequence of these objects to determine the rule of progression from one stage to the next. This rule could involve a change in horizontal position (shift) or a change in size (growth).
5.  Apply this progression rule one more time to the last observed object in the sequence to predict the pattern and position of the next object.
6.  Create a 3-row output grid with the same width as the input grid, initialized with white pixels (color 0).
7.  Place the predicted next object pattern into the middle row (row index 1) of the output grid at its predicted starting column index.
"""

def find_separator_rows(grid: np.ndarray) -> List[int]:
    """Finds the row indices of horizontal lines composed entirely of gray pixels (5)."""
    separator_rows = []
    gray_color = 5
    for r in range(grid.shape[0]):
        if np.all(grid[r, :] == gray_color):
            separator_rows.append(r)
    return separator_rows

def find_object_in_row(row: np.ndarray) -> Optional[Tuple[List[int], int]]:
    """
    Finds the first contiguous sequence of non-white (0), non-gray (5) pixels in a row.
    Returns the pattern (list of colors) and the starting column index.
    Returns None if no such object is found.
    """
    pattern = []
    start_col = -1
    in_object = False
    for c in range(row.shape[0]):
        pixel = row[c]
        if pixel != 0 and pixel != 5:
            if not in_object:
                start_col = c
                in_object = True
            pattern.append(pixel)
        elif in_object:
            # Found the end of the object
            break
    if pattern:
        return pattern, start_col
    else:
        return None

def extract_object_sequence(grid: np.ndarray, separator_rows: List[int]) -> List[Tuple[List[int], int]]:
    """
    Extracts the sequence of objects from the stages defined by separator rows.
    Each object is represented as (pattern, start_col).
    """
    objects = []
    start_row = 0
    stage_rows = []

    # Define search ranges for each stage
    search_ranges = []
    last_separator = -1
    for sep_row in separator_rows:
        search_ranges.append((last_separator + 1, sep_row))
        last_separator = sep_row
    search_ranges.append((last_separator + 1, grid.shape[0])) # Last stage

    # Find object in each stage
    for r_start, r_end in search_ranges:
        found_in_stage = False
        for r in range(r_start, r_end):
            obj_info = find_object_in_row(grid[r, :])
            if obj_info:
                objects.append(obj_info)
                found_in_stage = True
                break # Assume only one object row per stage based on examples
        # Optional: Add error handling if no object found in a stage where expected

    return objects

def analyze_progression(objects: List[Tuple[List[int], int]]) -> Dict[str, Any]:
    """
    Analyzes the sequence of objects to determine the progression rule.
    Detects either a constant shift in position or growth in length.
    """
    if len(objects) < 2:
        # Cannot determine progression with fewer than 2 objects
        # Defaulting to no change might be an option, but let's indicate failure
        return {"type": "unknown"}

    patterns = [obj[0] for obj in objects]
    positions = [obj[1] for obj in objects]
    lengths = [len(p) for p in patterns]

    # Check for position shift (pattern and length constant)
    pos_diffs = np.diff(positions)
    if len(set(str(p) for p in patterns)) == 1 and len(set(lengths)) == 1 and len(set(pos_diffs)) == 1:
         return {"type": "shift", "amount": pos_diffs[0]}

    # Check for length growth (pattern base constant, position constant)
    # For growth, the pattern usually extends the same color
    len_diffs = np.diff(lengths)
    if len(set(positions)) == 1 and len(set(len_diffs)) == 1:
        # Check if the pattern is consistent (e.g., always the same color added)
        consistent_growth = True
        base_color = patterns[0][0] # Assume growth adds the same color
        for i in range(len(patterns)):
             if not all(p == base_color for p in patterns[i]):
                 consistent_growth = False
                 break
        if consistent_growth:
             return {"type": "grow", "amount": len_diffs[0]}

    # If neither fits, return unknown
    return {"type": "unknown"}


def predict_next_object(last_object: Tuple[List[int], int], progression_rule: Dict[str, Any]) -> Tuple[List[int], int]:
    """Predicts the next object based on the last one and the progression rule."""
    last_pattern, last_pos = last_object
    rule_type = progression_rule.get("type")
    amount = progression_rule.get("amount")

    if rule_type == "shift":
        next_pos = last_pos + amount
        next_pattern = last_pattern # Pattern stays the same
        return next_pattern, next_pos
    elif rule_type == "grow":
        next_pos = last_pos # Position stays the same
        growth_amount = amount
        # Assume growth adds the first color of the pattern
        grow_color = last_pattern[0]
        next_pattern = last_pattern + [grow_color] * growth_amount
        return next_pattern, next_pos
    else:
        # Default: return the last object if rule is unknown or no change
        return last_pattern, last_pos


def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Applies the transformation rule to the input grid.
    Finds object sequence, determines progression, predicts next state,
    and places it in the center row of a 3-row output grid.
    """
    # 1. Find separator rows
    separator_rows = find_separator_rows(input_grid)

    # 2. Extract the sequence of objects
    object_sequence = extract_object_sequence(input_grid, separator_rows)

    if not object_sequence:
        # Handle cases where no objects are found (e.g., return empty grid or input?)
        # For now, return a default 3xWidth white grid
        height, width = input_grid.shape
        return np.zeros((3, width), dtype=int)

    # 3. Analyze the progression
    progression_rule = analyze_progression(object_sequence)

    # 4. Get the last object
    last_object = object_sequence[-1]

    # 5. Predict the next object state
    next_pattern, next_pos = predict_next_object(last_object, progression_rule)

    # 6. Create the output grid (3 rows, same width, filled with white)
    height, width = input_grid.shape
    output_grid = np.zeros((3, width), dtype=int)

    # 7. Place the predicted object in the middle row (row 1)
    # Ensure the object fits within the grid boundaries
    start_col = next_pos
    end_col = start_col + len(next_pattern)

    # Clip placement if object goes out of bounds
    place_start_col = max(0, start_col)
    place_end_col = min(width, end_col)
    pattern_start_idx = max(0, -start_col)
    pattern_end_idx = pattern_start_idx + (place_end_col - place_start_col)

    if place_start_col < place_end_col: # Check if there is anything to place
        output_grid[1, place_start_col:place_end_col] = next_pattern[pattern_start_idx:pattern_end_idx]

    return output_grid