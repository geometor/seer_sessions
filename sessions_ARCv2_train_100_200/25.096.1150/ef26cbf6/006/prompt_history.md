
## train_1

**input:**
```
0 0 0 4 1 0 0
0 7 0 4 0 1 1
0 0 0 4 0 1 0
4 4 4 4 4 4 4
0 0 0 4 1 1 0
0 3 0 4 0 1 0
0 0 0 4 1 1 1
4 4 4 4 4 4 4
0 0 0 4 1 1 0
0 8 0 4 0 1 1
0 0 0 4 1 0 1
```


**output:**
```
0 0 0 4 7 0 0
0 7 0 4 0 7 7
0 0 0 4 0 7 0
4 4 4 4 4 4 4
0 0 0 4 3 3 0
0 3 0 4 0 3 0
0 0 0 4 3 3 3
4 4 4 4 4 4 4
0 0 0 4 8 8 0
0 8 0 4 0 8 8
0 0 0 4 8 0 8
```


## train_2

**input:**
```
0 0 0 4 0 0 0 4 0 0 0
0 3 0 4 0 2 0 4 0 6 0
0 0 0 4 0 0 0 4 0 0 0
4 4 4 4 4 4 4 4 4 4 4
1 0 0 4 0 1 0 4 1 0 1
0 1 0 4 1 1 1 4 1 0 1
1 1 1 4 1 0 1 4 0 1 0
```


**output:**
```
0 0 0 4 0 0 0 4 0 0 0
0 3 0 4 0 2 0 4 0 6 0
0 0 0 4 0 0 0 4 0 0 0
4 4 4 4 4 4 4 4 4 4 4
3 0 0 4 0 2 0 4 6 0 6
0 3 0 4 2 2 2 4 6 0 6
3 3 3 4 2 0 2 4 0 6 0
```

Okay, I will analyze the provided task examples to understand the transformation rule.

**Perception of Elements:**

1.  **Grid Structure:** The input and output are 2D grids of single digits.
2.  **Separators:** The digit '4' plays a crucial role as a separator.
    *   **Horizontal Separators:** Rows composed entirely of '4's divide the grid into horizontal segments. These separator rows remain unchanged in the output.
    *   **Vertical Separators:** Columns containing '4's within the horizontal separator rows appear to define vertical regions within the segments. In `train_1`, column 3 acts as a vertical separator. In `train_2`, columns 3 and 8 act as vertical separators.
3.  **Segments and Regions:** The transformation logic operates independently on the horizontal segments, considering the vertical regions within them.
4.  **Key Digits:** Non-zero digits other than '1' seem to act as 'key' digits. Their role depends on the segment context.
5.  **Placeholder Digit:** The digit '1' acts as a placeholder that gets replaced under specific conditions.
6.  **Transformation Logic:** The core transformation involves replacing the placeholder '1's. The value used for replacement depends on the 'key' digits found either within the current segment (for the first segment under certain conditions) or in the corresponding vertical region of the *previous* non-separator segment.

**YAML Fact Document:**


```yaml
task_elements:
  - type: grid
    properties:
      - numeric_cells
      - 2D_structure
objects:
  - object: cell
    properties:
      - value: digit (0-8)
      - position: (row, column)
  - object: horizontal_separator
    properties:
      - type: row
      - composition: all cells contain '4'
      - role: divides grid into segments
      - behavior: remains unchanged
  - object: vertical_separator
    properties:
      - type: column
      - composition: contains '4' at intersection with horizontal_separator rows
      - role: divides segments into regions
  - object: horizontal_segment
    properties:
      - type: set_of_rows
      - location: between horizontal_separators (or grid edge and separator)
      - role: unit of processing
  - object: vertical_region
    properties:
      - type: set_of_columns
      - location: between vertical_separators (or grid edge and separator)
      - role: sub-unit for key association and replacement
  - object: placeholder_digit
    properties:
      - value: 1
      - role: target for replacement
  - object: key_digit
    properties:
      - value: non-zero digit, not '1' (e.g., 2, 3, 5, 6, 7, 8)
      - role: source value for replacement
relationships:
  - relationship: segment_contains_cells
  - relationship: region_contains_cells
  - relationship: cell_has_value
  - relationship: cell_has_position
actions:
  - action: identify_separators
    target: grid
    output: horizontal_separator_rows, vertical_separator_columns
  - action: define_segments
    based_on: horizontal_separator_rows
  - action: define_regions
    based_on: vertical_separator_columns
  - action: find_keys_in_segment
    target: horizontal_segment (input)
    output: map of {region_index: key_digit}
  - action: check_uniqueness_for_first_segment
    target: set of key_digits in the first segment
  - action: replace_placeholders
    target: cells with value '1' in the current segment
    condition: based on segment type (first vs. subsequent) and key availability
    value_source: either a unique internal key (first segment) or keys from the previous segment's regions map
```


**Natural Language Program:**

1.  Initialize the `output_grid` as a direct copy of the `input_grid`.
2.  Identify the row indices of all `horizontal_separator_rows` (rows containing only the digit 4).
3.  Identify the column indices of all `vertical_separator_columns` (columns containing a 4 in at least one `horizontal_separator_row`).
4.  Define the `horizontal_segments` based on the row indices between the `horizontal_separator_rows` (and grid edges).
5.  Define the `vertical_regions` based on the column indices between the `vertical_separator_columns` (and grid edges). Map each column index to its corresponding `vertical_region_index`.
6.  Initialize an empty map called `previous_segment_region_keys` to store the key digit associated with each vertical region from the previously processed segment.
7.  Iterate through the `horizontal_segments` from top to bottom. Let the current segment span rows `r_start` to `r_end`.
8.  Create a temporary map `current_segment_region_keys`. Iterate through all cells `(r, c)` where `r` is between `r_start` and `r_end`. If the `input_grid[r][c]` is a non-zero digit other than 1, find its `vertical_region_index` (`v_idx`). If `v_idx` is not already a key in `current_segment_region_keys`, add the mapping `v_idx: input_grid[r][c]`.
9.  Collect all unique non-zero digits (excluding 1) found within the current segment from the `input_grid`. Let this be `unique_keys_in_segment`.
10. **Determine Replacement Rule:**
    a.  **If `previous_segment_region_keys` is empty (this is the first segment being processed):**
        i.  Check if `unique_keys_in_segment` contains exactly one digit. Let this be `segment_key`.
        ii. If yes, iterate through cells `(r, c)` in the current segment. If `input_grid[r][c]` is 1, set `output_grid[r][c] = segment_key`.
    b.  **Else (this is a subsequent segment):**
        i.  Iterate through cells `(r, c)` in the current segment.
        ii. If `input_grid[r][c]` is 1:
            1.  Find the `vertical_region_index` (`v_idx`) for column `c`.
            2.  If `v_idx` exists as a key in `previous_segment_region_keys`, set `output_grid[r][c] = previous_segment_region_keys[v_idx]`.
11. **Prepare for Next Segment:** Update `previous_segment_region_keys` by assigning it the contents of `current_segment_region_keys`.
12. After iterating through all segments, return the final `output_grid`.
```python
"""
The transformation rule operates on a 2D grid of digits. It identifies horizontal separator rows (all 4s) and vertical separator columns (containing 4s in horizontal separator rows). These separators define segments and regions within the grid.

The core logic involves replacing placeholder digits '1' with 'key' digits (non-zero, not 1). The replacement value depends on the segment:

1.  For the first segment (before the first horizontal separator), if there's exactly one unique key digit within that segment, all '1's in that segment are replaced by that unique key digit.
2.  For subsequent segments, each '1' is replaced by the key digit found in the *corresponding vertical region* of the *immediately preceding non-separator segment*.

Key digits within a segment are associated with the vertical region they reside in. The first key digit encountered when scanning a region (top-to-bottom, left-to-right within rows) is typically used. Horizontal separator rows remain unchanged.
"""

import copy
import numpy as np # Using numpy for easier grid manipulation

def _find_horizontal_separators(grid: np.ndarray) -> list[int]:
    """Finds the indices of rows that consist entirely of the separator digit (4)."""
    separator_rows = []
    separator_value = 4
    for r_idx, row in enumerate(grid):
        if np.all(row == separator_value):
            separator_rows.append(r_idx)
    return separator_rows

def _find_vertical_separators(grid: np.ndarray, horizontal_separator_rows: list[int]) -> list[int]:
    """Finds the indices of columns that contain the separator digit (4) in at least one horizontal separator row."""
    separator_cols = []
    separator_value = 4
    if not horizontal_separator_rows: # No horizontal separators, thus no vertical separators defined by them
        return []
        
    num_cols = grid.shape[1]
    for c_idx in range(num_cols):
        is_separator = False
        for r_idx in horizontal_separator_rows:
            if grid[r_idx, c_idx] == separator_value:
                is_separator = True
                break
        if is_separator:
            separator_cols.append(c_idx)
    return sorted(list(set(separator_cols))) # Ensure uniqueness and order

def _get_vertical_region_index(col: int, vertical_separator_cols: list[int]) -> int:
    """Determines the vertical region index for a given column index."""
    region_index = 0
    for sep_col in vertical_separator_cols:
        if col < sep_col:
            return region_index
        region_index += 1
    return region_index # Column is in the last region (or the only region if no separators)

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies the transformation rule to the input grid.
    Identifies segments and regions based on separators (digit 4).
    Replaces placeholder '1's based on key digits from the current segment (if first)
    or the corresponding region in the previous segment.
    """
    # Convert to numpy array for easier slicing and manipulation
    grid_np = np.array(input_grid, dtype=int)
    output_grid_np = grid_np.copy() # Initialize output_grid
    
    num_rows, num_cols = grid_np.shape

    # 1. Identify separators
    horizontal_separator_rows = _find_horizontal_separators(grid_np)
    vertical_separator_cols = _find_vertical_separators(grid_np, horizontal_separator_rows)

    # 6. Initialize storage for keys from the previous segment
    previous_segment_region_keys = {}

    # 7. Iterate through horizontal segments
    segment_starts = [0] + [r + 1 for r in horizontal_separator_rows]
    segment_ends = [r for r in horizontal_separator_rows] + [num_rows]

    for i in range(len(segment_starts)):
        r_start = segment_starts[i]
        r_end = segment_ends[i]

        # Skip empty segments or separator rows themselves
        if r_start >= r_end:
            # If this was a separator row, reset previous keys if needed, 
            # or just continue if it's an empty segment gap
            if r_start in horizontal_separator_rows:
                # Separator rows act as dividers, clear the memory of the previous segment's keys
                 # However, the logic dictates using the *last non-separator segment's* keys.
                 # So, we don't necessarily clear `previous_segment_region_keys` here unless
                 # we want to enforce strict separation (revisit if examples contradict).
                 # For now, let's assume keys persist across single separator rows.
                 pass
            continue

        # 8. Find keys in the current segment and associate them with regions
        current_segment_region_keys = {}
        unique_keys_in_segment = set()
        
        for r in range(r_start, r_end):
            for c in range(num_cols):
                val = grid_np[r, c]
                if val != 0 and val != 1 and val != 4: # It's a key digit
                    unique_keys_in_segment.add(val)
                    v_idx = _get_vertical_region_index(c, vertical_separator_cols)
                    # Store the first key found in each region within this segment
                    if v_idx not in current_segment_region_keys:
                        current_segment_region_keys[v_idx] = val

        # 10. Determine Replacement Rule and Apply
        is_first_segment = not bool(previous_segment_region_keys) # Check if previous keys map is empty

        if is_first_segment:
             # Rule 10.a: First segment logic
             # Check if only one unique key exists IN THE ORIGINAL INPUT for this segment
             segment_keys_from_input = set()
             for r in range(r_start, r_end):
                 for c in range(num_cols):
                     val = grid_np[r, c]
                     if val != 0 and val != 1 and val != 4:
                        segment_keys_from_input.add(val)

             if len(segment_keys_from_input) == 1:
                 segment_key = list(segment_keys_from_input)[0]
                 # Replace 1s in the output grid for this segment
                 for r in range(r_start, r_end):
                     for c in range(num_cols):
                         if grid_np[r, c] == 1:
                             output_grid_np[r, c] = segment_key
        else:
            # Rule 10.b: Subsequent segment logic
            for r in range(r_start, r_end):
                for c in range(num_cols):
                    if grid_np[r, c] == 1: # Found a placeholder
                        v_idx = _get_vertical_region_index(c, vertical_separator_cols)
                        # Replace with the key from the corresponding region in the *previous* segment
                        if v_idx in previous_segment_region_keys:
                            output_grid_np[r, c] = previous_segment_region_keys[v_idx]

        # 11. Prepare for Next Segment: Update previous keys with the current segment's keys
        # Only update if the current segment actually contained keys.
        # Check this based on the keys found in the *original input* for this segment
        # This prevents overwriting the previous keys if the current segment was all 0s/1s/4s
        
        # Re-find keys specifically for passing to the *next* segment
        keys_to_pass = {}
        for r in range(r_start, r_end):
            for c in range(num_cols):
                val = grid_np[r, c]
                if val != 0 and val != 1 and val != 4: # It's a key digit
                    v_idx = _get_vertical_region_index(c, vertical_separator_cols)
                    if v_idx not in keys_to_pass: # Store first key per region
                       keys_to_pass[v_idx] = val
                       
        # Update previous_segment_region_keys only if the current segment wasn't just a separator
        # and actually contained some keys to pass on.
        if keys_to_pass: # If keys were found in this segment
             previous_segment_region_keys = keys_to_pass.copy()
        # If no keys were found, the previous_segment_region_keys remain unchanged from the segment before this one.

    # Convert back to list of lists for the final output
    return output_grid_np.tolist()
```
```python
"""
The transformation rule operates on a 2D grid of digits. It identifies horizontal
separator rows (all 4s) and vertical separator columns (containing 4s in horizontal
separator rows). These separators define horizontal segments and vertical regions
within the grid.

The core logic involves replacing placeholder digits '1' with 'key' digits
(non-zero, non-1, non-4, i.e., 2, 3, 5, 6, 7, 8). The replacement rule depends
on the number of unique key digits found within each horizontal segment:

1.  **One Unique Key:** If a segment contains exactly one unique key digit, all
    '1's within that segment are replaced by that single key digit.
2.  **Zero Unique Keys:** If a segment contains no key digits (only 0s, 1s, and 4s),
    each '1' within that segment is replaced by the key digit associated with its
    corresponding vertical region in the *most recently processed segment that
    contained keys*.
3.  **Multiple Unique Keys:** If a segment contains more than one unique key digit,
    the '1's within that segment remain unchanged.

Key digits within a segment are associated with the vertical region they reside in.
The first key digit encountered when scanning a region (top-to-bottom,
left-to-right within rows) is typically used to define the region's key for
that segment. This region-to-key mapping is stored and potentially used by
subsequent segments that lack their own keys. Horizontal separator rows remain
unchanged in the output.
"""

import numpy as np
import copy

def _find_horizontal_separators(grid: np.ndarray) -> list[int]:
    """Finds the indices of rows that consist entirely of the separator digit (4)."""
    separator_rows = []
    separator_value = 4
    for r_idx, row in enumerate(grid):
        if np.all(row == separator_value):
            separator_rows.append(r_idx)
    return separator_rows

def _find_vertical_separators(grid: np.ndarray, horizontal_separator_rows: list[int]) -> list[int]:
    """Finds the indices of columns that contain the separator digit (4) in at least one horizontal separator row."""
    separator_cols = set() # Use a set to automatically handle duplicates
    separator_value = 4
    if not horizontal_separator_rows: # No horizontal separators, thus no vertical separators defined by them
        return []

    num_cols = grid.shape[1]
    for c_idx in range(num_cols):
        is_separator = False
        for r_idx in horizontal_separator_rows:
             # Ensure r_idx is within grid bounds (should always be true if horizontal_separator_rows is correct)
            if 0 <= r_idx < grid.shape[0] and grid[r_idx, c_idx] == separator_value:
                is_separator = True
                break
        if is_separator:
            separator_cols.add(c_idx)
    return sorted(list(separator_cols)) # Return sorted list

def _get_vertical_region_index(col: int, vertical_separator_cols: list[int]) -> int:
    """Determines the vertical region index for a given column index."""
    region_index = 0
    for sep_col in vertical_separator_cols:
        if col < sep_col:
            return region_index
        region_index += 1
    # Column is in the last region (or the only region if no separators)
    return region_index

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies the transformation rule to the input grid.
    """
    # Convert input to numpy array for easier handling
    grid_np = np.array(input_grid, dtype=int)
    # Initialize output grid as a copy of the input
    output_grid_np = grid_np.copy()
    num_rows, num_cols = grid_np.shape

    # Identify horizontal and vertical separators
    horizontal_separator_rows = _find_horizontal_separators(grid_np)
    vertical_separator_cols = _find_vertical_separators(grid_np, horizontal_separator_rows)

    # Initialize the memory for the region-key mapping from the last valid segment
    previous_segment_valid_region_keys = {}

    # Define segment boundaries
    segment_starts = [0] + [r + 1 for r in horizontal_separator_rows]
    segment_ends = [r for r in horizontal_separator_rows] + [num_rows]

    # Iterate through horizontal segments
    for i in range(len(segment_starts)):
        r_start = segment_starts[i]
        r_end = segment_ends[i]

        # Skip empty segments or separator rows themselves
        if r_start >= r_end or r_start in horizontal_separator_rows:
            continue # Separator rows are already copied, and empty segments need no processing

        # Analyze the current segment (from input grid)
        unique_keys_in_segment = set()
        current_segment_region_keys = {}
        key_digits = {2, 3, 5, 6, 7, 8} # Define key digits (non-0, non-1, non-4)

        for r in range(r_start, r_end):
            for c in range(num_cols):
                val = grid_np[r, c]
                if val in key_digits:
                    # Found a key digit
                    unique_keys_in_segment.add(val)
                    v_idx = _get_vertical_region_index(c, vertical_separator_cols)
                    # Store the first key found for each region within this segment
                    if v_idx not in current_segment_region_keys:
                        current_segment_region_keys[v_idx] = val

        # Apply replacement rules based on the number of unique keys found
        num_unique_keys = len(unique_keys_in_segment)

        if num_unique_keys == 1:
            # Rule 1: Single unique key -> replace all 1s with this key
            segment_key = list(unique_keys_in_segment)[0]
            for r in range(r_start, r_end):
                for c in range(num_cols):
                    if grid_np[r, c] == 1:
                        output_grid_np[r, c] = segment_key
        elif num_unique_keys == 0:
            # Rule 2: No unique keys -> replace 1s using previous segment's keys based on region
            if previous_segment_valid_region_keys: # Only replace if we have previous keys
                for r in range(r_start, r_end):
                    for c in range(num_cols):
                        if grid_np[r, c] == 1:
                            v_idx = _get_vertical_region_index(c, vertical_separator_cols)
                            if v_idx in previous_segment_valid_region_keys:
                                output_grid_np[r, c] = previous_segment_valid_region_keys[v_idx]
        # else num_unique_keys > 1:
            # Rule 3: Multiple unique keys -> do nothing, 1s remain unchanged (already copied)

        # Update the memory for the *next* segment if the current segment contained keys
        if current_segment_region_keys: # Check if the map is non-empty
            previous_segment_valid_region_keys = current_segment_region_keys.copy()
            # No need to explicitly copy, assignment creates a new reference,
            # but copy() is safer if modifying the dict later, though not strictly needed here.

    # Convert the final numpy array back to a list of lists
    return output_grid_np.tolist()
```
```python
import numpy as np
import copy

"""
The transformation rule operates on a 2D grid of digits. It identifies horizontal
separator rows (all 4s) and vertical separator columns (containing 4s in horizontal
separator rows). These separators define horizontal segments and vertical regions
within the grid.

The core logic involves replacing placeholder digits '1' with 'key' digits
(non-zero, non-1, non-4, i.e., 2, 3, 5, 6, 7, 8). The replacement rule depends
on the number of unique key digits found within each horizontal segment:

1.  **One Unique Key:** If a segment contains exactly one unique key digit, all
    '1's within that segment are replaced by that single key digit.
2.  **Zero Unique Keys:** If a segment contains no key digits (only 0s, 1s, and 4s),
    each '1' within that segment is replaced by the key digit associated with its
    corresponding vertical region in the *most recently processed segment that
    contained keys*.
3.  **Multiple Unique Keys:** If a segment contains more than one unique key digit,
    the '1's within that segment remain unchanged.

Key digits within a segment are associated with the vertical region they reside in.
The first key digit encountered when scanning a region (top-to-bottom,
left-to-right within rows) is typically used to define the region's key for
that segment. This region-to-key mapping is stored (in key_memory) and potentially
used by subsequent segments that lack their own keys. Horizontal separator rows
remain unchanged in the output.
"""


def _find_horizontal_separators(grid: np.ndarray) -> list[int]:
    """Finds the indices of rows that consist entirely of the separator digit (4)."""
    separator_rows = []
    separator_value = 4
    for r_idx, row in enumerate(grid):
        if np.all(row == separator_value):
            separator_rows.append(r_idx)
    return separator_rows

def _find_vertical_separators(grid: np.ndarray, horizontal_separator_rows: list[int]) -> list[int]:
    """Finds the indices of columns that contain the separator digit (4) in at least one horizontal separator row."""
    separator_cols = set() # Use a set to automatically handle duplicates
    separator_value = 4
    if not horizontal_separator_rows: # No horizontal separators, thus no vertical separators defined by them
        return []

    num_cols = grid.shape[1]
    for c_idx in range(num_cols):
        is_separator = False
        for r_idx in horizontal_separator_rows:
             # Ensure r_idx is within grid bounds
            if 0 <= r_idx < grid.shape[0] and grid[r_idx, c_idx] == separator_value:
                is_separator = True
                break
        if is_separator:
            separator_cols.add(c_idx)
    return sorted(list(separator_cols)) # Return sorted list

def _get_vertical_region_index(col: int, vertical_separator_cols: list[int]) -> int:
    """Determines the vertical region index for a given column index."""
    region_index = 0
    for sep_col in vertical_separator_cols:
        if col < sep_col:
            return region_index
        region_index += 1
    # Column is in the last region (or the only region if no separators)
    return region_index

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies the transformation rule to the input grid.
    """
    # Convert input to numpy array for easier handling
    grid_np = np.array(input_grid, dtype=int)
    # Initialize output grid as a copy of the input
    output_grid_np = grid_np.copy()
    num_rows, num_cols = grid_np.shape

    # Identify horizontal and vertical separators
    horizontal_separator_rows = _find_horizontal_separators(grid_np)
    vertical_separator_cols = _find_vertical_separators(grid_np, horizontal_separator_rows)

    # Initialize the memory for the region-key mapping from the last valid segment
    key_memory = {}

    # Define segment boundaries
    segment_starts = [0] + [r + 1 for r in horizontal_separator_rows]
    segment_ends = [r for r in horizontal_separator_rows] + [num_rows]

    # Define the set of possible key digits
    key_digits = {2, 3, 5, 6, 7, 8} # Digits that act as keys

    # Iterate through horizontal segments
    for i in range(len(segment_starts)):
        r_start = segment_starts[i]
        r_end = segment_ends[i]

        # Skip empty segments or separator rows themselves
        if r_start >= r_end or r_start in horizontal_separator_rows:
            continue # Separator rows are already copied, and empty segments need no processing

        # Analyze the current segment (from the original input grid)
        unique_keys_in_segment = set()
        current_segment_region_keys = {}

        # Find all keys and their region mapping within the current segment
        for r in range(r_start, r_end):
            for c in range(num_cols):
                val = grid_np[r, c]
                if val in key_digits:
                    # Found a key digit
                    unique_keys_in_segment.add(val)
                    v_idx = _get_vertical_region_index(c, vertical_separator_cols)
                    # Store the first key found for each region within this segment
                    if v_idx not in current_segment_region_keys:
                        current_segment_region_keys[v_idx] = val

        # Apply replacement rules based on the number of unique keys found in this segment
        num_unique_keys = len(unique_keys_in_segment)

        if num_unique_keys == 1:
            # Rule 1: Single unique key -> replace all 1s in the output grid with this key
            segment_key = list(unique_keys_in_segment)[0]
            for r in range(r_start, r_end):
                for c in range(num_cols):
                    if grid_np[r, c] == 1: # Check original grid for placeholder
                        output_grid_np[r, c] = segment_key # Modify output grid
        elif num_unique_keys == 0:
            # Rule 2: No unique keys -> replace 1s using memory from previous segments
            if key_memory: # Only replace if we have memory
                for r in range(r_start, r_end):
                    for c in range(num_cols):
                        if grid_np[r, c] == 1: # Check original grid for placeholder
                            v_idx = _get_vertical_region_index(c, vertical_separator_cols)
                            if v_idx in key_memory:
                                output_grid_np[r, c] = key_memory[v_idx] # Modify output grid
        # else num_unique_keys > 1:
            # Rule 3: Multiple unique keys -> do nothing to 1s in this segment
            # The output grid already has the copied 1s, so no action needed.
            pass

        # Update the key memory *if* keys were found in the current segment
        if current_segment_region_keys: # Check if the map is non-empty
            key_memory = current_segment_region_keys.copy()
            # Use copy() to ensure the memory is not just a reference that might change later

    # Convert the final numpy array back to a list of lists
    return output_grid_np.tolist()
```
