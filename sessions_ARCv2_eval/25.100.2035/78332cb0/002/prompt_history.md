
## train_1

**input:**
```
7 7 7 7 7 6 7 4 7 7 7
7 7 7 7 7 6 7 4 4 4 7
7 7 7 7 7 6 7 7 7 4 7
7 2 2 2 7 6 7 7 7 4 7
7 7 2 7 7 6 7 7 7 4 7
6 6 6 6 6 6 6 6 6 6 6
7 7 7 1 7 6 7 7 3 7 7
7 1 1 1 7 6 7 3 3 7 7
7 1 1 1 7 6 7 3 7 7 7
7 1 1 1 7 6 7 3 7 7 7
7 7 7 7 7 6 7 3 7 7 7
```


**output:**
```
7 7 7 7 7
7 7 7 7 7
7 7 7 7 7
7 2 2 2 7
7 7 2 7 7
6 6 6 6 6
7 7 3 7 7
7 3 3 7 7
7 3 7 7 7
7 3 7 7 7
7 3 7 7 7
6 6 6 6 6
7 4 7 7 7
7 4 4 4 7
7 7 7 4 7
7 7 7 4 7
7 7 7 4 7
6 6 6 6 6
7 7 7 1 7
7 1 1 1 7
7 1 1 1 7
7 1 1 1 7
7 7 7 7 7
```


## train_2

**input:**
```
7 7 7 7 7
7 7 8 8 7
7 7 8 8 7
8 8 8 7 7
7 7 7 7 7
6 6 6 6 6
7 7 7 7 7
2 2 2 7 7
7 7 2 2 7
7 7 7 2 2
7 7 7 7 7
6 6 6 6 6
7 7 7 7 7
7 9 7 9 9
7 9 9 9 7
7 9 7 7 7
7 7 7 7 7
```


**output:**
```
7 7 7 7 7 6 7 7 7 7 7 6 7 7 7 7 7
7 9 7 9 9 6 2 2 2 7 7 6 7 7 8 8 7
7 9 9 9 7 6 7 7 2 2 7 6 7 7 8 8 7
7 9 7 7 7 6 7 7 7 2 2 6 8 8 8 7 7
7 7 7 7 7 6 7 7 7 7 7 6 7 7 7 7 7
```


## train_3

**input:**
```
7 7 7 7 7 6 7 7 1 7 7 6 7 7 9 7 7
7 8 8 8 7 6 7 7 1 7 7 6 7 9 9 9 7
7 7 8 7 7 6 7 7 1 7 7 6 7 7 7 7 7
7 7 8 7 7 6 7 7 1 7 7 6 7 7 7 7 7
7 7 8 7 7 6 7 7 1 7 7 6 7 7 7 7 7
```


**output:**
```
7 7 7 7 7
7 8 8 8 7
7 7 8 7 7
7 7 8 7 7
7 7 8 7 7
6 6 6 6 6
7 7 1 7 7
7 7 1 7 7
7 7 1 7 7
7 7 1 7 7
7 7 1 7 7
6 6 6 6 6
7 7 9 7 7
7 9 9 9 7
7 7 7 7 7
7 7 7 7 7
7 7 7 7 7
```

Okay, let's break down the transformation logic.

**Perception of Elements:**

1.  **Grids:** The inputs and outputs are numerical grids.
2.  **Numbers/Colors:** The grids use digits, likely representing different colors or object types. '7' appears to be a background color. '6' acts as a separator element. Digits like '1', '2', '3', '4', '8', '9' represent distinct patterns or objects embedded within the background.
3.  **Separators (6s):** Lines composed entirely of '6's appear either horizontally (spanning the grid width) or vertically (spanning the grid height). These lines function to divide the grid or delineate sections.
4.  **Pattern Regions:** Connected areas of digits other than '6' or '7' form distinct regions or patterns.
5.  **Subgrids/Panels:** The transformation involves either splitting the main grid into subgrids based on separators or extracting pattern regions into standardized panels (like 5x5).
6.  **Orientation & Arrangement:** The transformation changes the orientation and arrangement of these patterns/subgrids. Sometimes they are stacked vertically, sometimes arranged horizontally. The separators ('6's) are also used in the output, potentially changing orientation (horizontal input separators leading to vertical output separators, and vice versa).
7.  **Ordering:** The order in which patterns/subgrids appear in the output depends on their original position in the input and the type of separation (horizontal vs. vertical).

**YAML Facts:**

```yaml
task_description: Reorganize pattern blocks extracted from an input grid, using '6' as a separator and '7' as background. The reorganization method (splitting vs. extracting) and output arrangement (horizontal/vertical stacking, ordering) depend on the configuration of the '6' separators in the input.

elements:
  - id: grid
    description: A 2D array of integers.
  - id: background_digit
    value: 7
    description: Represents empty space or background.
  - id: separator_digit
    value: 6
    description: Used to form lines that separate regions or subgrids.
  - id: pattern_digits
    value: [1, 2, 3, 4, 8, 9] # Digits observed in patterns
    description: Digits representing the core patterns/objects.
  - id: separator_line
    description: A horizontal or vertical line composed entirely of separator_digits (6).
  - id: pattern_region
    description: A connected component of pattern_digits within the grid, not crossing separator_lines.
  - id: subgrid
    description: A rectangular section of the input grid obtained by splitting along separator_lines.
  - id: panel
    description: A standardized grid (e.g., 5x5) used in the output to display an extracted pattern_region, padded with background_digit (7).

relationships_and_actions:
  - action: identify_separators
    input: grid
    output: list of horizontal_separator_lines, list of vertical_separator_lines
    description: Locates complete rows or columns filled only with the separator_digit (6).
  - action: determine_mode
    input: grid, separator_lines
    output: mode ('split' or 'extract'), separator_type ('horizontal' or 'vertical')
    description: >
      Checks if separators fully partition the grid into rectangular blocks each containing one pattern (Mode 'split').
      If horizontal separators partition -> separator_type = 'horizontal'.
      If vertical separators partition -> separator_type = 'vertical'.
      Otherwise, assume Mode 'extract' (like train_1). In train_1, the separator is horizontal.
  - action: split_grid
    condition: mode == 'split'
    input: grid, separator_lines, separator_type
    output: list of subgrids, order ('original' or 'reverse')
    description: >
      Splits the grid along the separators.
      If separator_type is 'horizontal', order is 'reverse' (bottom-to-top).
      If separator_type is 'vertical', order is 'original' (left-to-right).
  - action: extract_regions
    condition: mode == 'extract'
    input: grid
    output: list of panels, order ('relative_position')
    description: >
      Finds connected pattern_regions. Creates a 5x5 panel for each, placing the pattern inside padded with background_digit (7).
      Determines order based on region position relative to the main separator (e.g., Above-Left, Below-Right, Above-Right, Below-Left for a horizontal separator).
  - action: construct_output
    input: subgrids or panels, order, separator_type (from mode determination)
    output: output_grid
    description: >
      Arranges the subgrids/panels according to the determined order.
      If input separators were horizontal (split mode) or if mode was extract: arrange items HORIZONTALLY/VERTICALLY?? -> Recheck logic.
      - If Mode 'split' with HORIZONTAL separators: Arrange subgrids HORIZONTALLY in REVERSE order, separated by VERTICAL 6s lines.
      - If Mode 'split' with VERTICAL separators: Arrange subgrids VERTICALLY in ORIGINAL order, separated by HORIZONTAL 6s lines.
      - If Mode 'extract' (like train_1, horizontal separator): Arrange panels VERTICALLY in relative_position order (AL, BR, AR, BL), separated by HORIZONTAL 6s lines.

```

**Natural Language Program:**

1.  **Identify Separators:** Scan the input grid to find all complete horizontal rows and complete vertical columns consisting solely of the digit '6'.
2.  **Determine Operating Mode:**
    *   **Check for Grid Split Mode:** If the identified '6' separators perfectly divide the input grid into distinct rectangular subgrids such that each subgrid contains exactly one connected region of pattern digits (non-'6', non-'7'), then activate "Grid Split Mode". Note whether the partitioning separators were horizontal or vertical.
    *   **Default to Region Extract Mode:** If Grid Split Mode does not apply (e.g., only one separator line exists, or multiple pattern regions exist within the areas defined by separators), activate "Region Extract Mode". Assume the primary separator is the single horizontal line of '6's if present (as in train_1).
3.  **Process Based on Mode:**
    *   **If Grid Split Mode:**
        *   Remove the separator lines to get a list of subgrids.
        *   If the original separators were **horizontal**: Arrange the subgrids **horizontally** in the output. Order them based on their original vertical position, starting from the **bottom** subgrid and moving upwards (reverse order). Separate adjacent subgrids in the output with a single **vertical** column of '6's.
        *   If the original separators were **vertical**: Arrange the subgrids **vertically** in the output. Order them based on their original horizontal position, starting from the **leftmost** subgrid and moving rightwards (original order). Separate adjacent subgrids in the output with a single **horizontal** row of '6's.
    *   **If Region Extract Mode (based on train_1):**
        *   Identify all connected regions of pattern digits (not '6' or '7').
        *   For each region, determine its bounding box.
        *   Create a 5x5 output panel for each region, filled initially with the background digit '7'. Copy the pattern from the region's bounding box into this 5x5 panel (preserving its internal structure, specific alignment within the 5x5 needs careful implementation, potentially based on examples).
        *   Determine the position of each region relative to the primary horizontal separator line (e.g., Above/Below) and its horizontal position (e.g., Left/Right relative to the grid's center or start
```python
import numpy as np
from scipy.ndimage import label, find_objects

"""
Transforms an input grid based on the arrangement of '6' separators.

The transformation operates in one of two modes: 'split' or 'extract'.

1.  **Identify Separators:** Find all complete rows and columns consisting only of the digit 6.

2.  **Determine Mode:**
    *   **Split Mode:** Activated if separators perfectly partition the grid into rectangular subgrids (typically 5x5 in examples), each containing a single non-background pattern.
        *   If partitioning is done by HORIZONTAL separators (like train_2): The subgrids are extracted, ordered from BOTTOM to TOP, and arranged HORIZONTALLY in the output, separated by VERTICAL lines of 6s.
        *   If partitioning is done by VERTICAL separators (like train_3): The subgrids are extracted, ordered from LEFT to RIGHT, and arranged VERTICALLY in the output, separated by HORIZONTAL lines of 6s.
    *   **Extract Mode:** Activated if the grid isn't perfectly partitioned by separators (e.g., a single separator line exists like train_1).
        *   Identify connected regions of digits other than 6 (separator) and 7 (background).
        *   For each region, create a 5x5 'panel' initialized with 7s.
        *   Copy the pattern from the region's bounding box into the top-left of its panel.
        *   Determine the region's position relative to the main separator (e.g., Above/Below, Left/Right).
        *   Order the panels based on a specific positional sequence (derived from train_1: Top-Right, Bottom-Right, Top-Left, Bottom-Left - corresponding to digits 4, 3, 2, 1 in that example). Note: The digit values (1,2,3,4) themselves are patterns, not positional indices. The order is derived from observing train_1's input/output mapping. Let's refine this: the order seems to be Top-Left, Bottom-Right, Top-Right, Bottom-Left relative to the separator. Re-checking train_1 output: Panel1(2), Panel2(3), Panel3(4), Panel4(1). Original positions: 2(Top-Left), 3(Bottom-Right), 4(Top-Right), 1(Bottom-Left). So the output order is Top-Left, Bottom-Right, Top-Right, Bottom-Left.
        *   Arrange the ordered panels VERTICALLY, separated by HORIZONTAL lines of 6s.

3.  **Construct Output:** Assemble the subgrids or panels with their respective separators according to the determined mode and ordering.
"""

def find_horizontal_separators(grid_np):
    """Finds indices of rows composed entirely of 6."""
    rows, cols = grid_np.shape
    separator_indices = []
    for r in range(rows):
        if np.all(grid_np[r, :] == 6):
            separator_indices.append(r)
    return separator_indices

def find_vertical_separators(grid_np):
    """Finds indices of columns composed entirely of 6."""
    rows, cols = grid_np.shape
    separator_indices = []
    for c in range(cols):
        if np.all(grid_np[:, c] == 6):
            separator_indices.append(c)
    return separator_indices

def get_subgrids(grid_np, separator_indices, axis):
    """Extracts subgrids based on separator indices along a given axis."""
    subgrids = []
    start = 0
    for idx in separator_indices:
        if axis == 0: # Horizontal separators -> split rows
            subgrid = grid_np[start:idx, :]
        else: # Vertical separators -> split columns
            subgrid = grid_np[:, start:idx]
        if subgrid.size > 0: # Avoid empty subgrids
            subgrids.append(subgrid)
        start = idx + 1
    # Add the last subgrid
    if axis == 0:
        subgrid = grid_np[start:, :]
    else:
        subgrid = grid_np[:, start:]
    if subgrid.size > 0:
        subgrids.append(subgrid)
    return subgrids

def create_panel(region_slice):
    """Creates a 5x5 panel and places the region slice in the top-left."""
    panel = np.full((5, 5), 7, dtype=int) # Fill with background
    h, w = region_slice.shape
    # Ensure the slice fits within the 5x5 panel
    copy_h = min(h, 5)
    copy_w = min(w, 5)
    panel[0:copy_h, 0:copy_w] = region_slice[0:copy_h, 0:copy_w]
    return panel

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Transforms the input grid based on separator lines (6) and pattern regions.
    """
    if not input_grid or not input_grid[0]:
        return []

    grid_np = np.array(input_grid, dtype=int)
    rows, cols = grid_np.shape
    background_digit = 7
    separator_digit = 6

    # --- Identify Separators ---
    h_separators = find_horizontal_separators(grid_np)
    v_separators = find_vertical_separators(grid_np)

    # --- Determine Mode and Process ---
    output_grid_np = None

    # Mode 1: Split by Vertical Separators (like train_3)
    # Assumes only vertical separators exist and partition the grid
    if v_separators and not h_separators:
        subgrids = get_subgrids(grid_np, v_separators, axis=1)
        # Keep original left-to-right order
        # Arrange vertically, separated by horizontal 6s lines
        output_parts = []
        separator_row = np.full((1, subgrids[0].shape[1]), separator_digit, dtype=int)
        for i, subgrid in enumerate(subgrids):
            output_parts.append(subgrid)
            if i < len(subgrids) - 1:
                output_parts.append(separator_row)
        output_grid_np = np.vstack(output_parts)

    # Mode 2: Split by Horizontal Separators (like train_2)
    # Assumes only horizontal separators exist and partition the grid
    elif h_separators and not v_separators and len(h_separators) > 1: # Need more than one separator to define distinct subgrids clearly for this mode
        subgrids = get_subgrids(grid_np, h_separators, axis=0)
        # Reverse order (bottom-to-top)
        subgrids.reverse()
        # Arrange horizontally, separated by vertical 6s lines
        output_parts = []
        separator_col = np.full((subgrids[0].shape[0], 1), separator_digit, dtype=int)
        for i, subgrid in enumerate(subgrids):
            output_parts.append(subgrid)
            if i < len(subgrids) - 1:
                output_parts.append(separator_col)
        output_grid_np = np.hstack(output_parts)

    # Mode 3: Extract Regions (like train_1)
    # Assumes a single horizontal separator and requires region extraction
    elif len(h_separators) == 1 and not v_separators:
        separator_row_idx = h_separators[0]
        # Find connected components (patterns) excluding background and separators
        mask = (grid_np != background_digit) & (grid_np != separator_digit)
        labeled_array, num_features = label(mask)
        objects_slices = find_objects(labeled_array)

        regions = []
        for i, slc in enumerate(objects_slices):
            # Get the slice corresponding to the object's bounding box
            region_slice = grid_np[slc]
            # Get the pattern itself (exclude background within the bounding box)
            pattern_mask_in_slice = (labeled_array[slc] == (i + 1))
            # Use the original digits from grid_np where the mask is true
            pattern_data = grid_np[slc][pattern_mask_in_slice]
            
            # Create the 5x5 panel - extract the bounding box content directly
            panel = create_panel(grid_np[slc])

            # Determine position relative to the separator
            center_y = slc[0].start + (slc[0].stop - slc[0].start) / 2
            center_x = slc[1].start + (slc[1].stop - slc[1].start) / 2
            
            is_above = center_y < separator_row_idx
            # Using middle column as reference for left/right
            is_left = center_x < cols / 2 

            pos_key = ""
            if is_above:
                pos_key += "T"
            else:
                pos_key += "B"
            if is_left:
                pos_key += "L"
            else:
                pos_key += "R"
                
            regions.append({'panel': panel, 'pos': pos_key})

        # Sort regions based on the observed order: TL, BR, TR, BL
        sort_order = {'TL': 0, 'BR': 1, 'TR': 2, 'BL': 3}
        regions.sort(key=lambda r: sort_order.get(r['pos'], 99)) # Sort by key, default to end if pos not found

        # Assemble panels vertically with horizontal separators
        output_parts = []
        panel_width = 5 # Assuming 5x5 panels
        separator_row = np.full((1, panel_width), separator_digit, dtype=int)
        for i, region in enumerate(regions):
            output_parts.append(region['panel'])
            if i < len(regions) - 1:
                output_parts.append(separator_row)
        
        if output_parts: # Check if any regions were found
             output_grid_np = np.vstack(output_parts)
        else: # Handle case with no patterns found
             output_grid_np = np.array([[]])


    # Fallback or Unhandled Case: Return input or empty
    else:
        # This case isn't covered by the examples (e.g., both H and V separators, no separators, etc.)
        # Returning the input as a default might be reasonable for debugging.
        # Or return empty if transformation is undefined.
        # For now, let's return empty for unhandled cases.
         return [] # Or return input_grid if that's preferred

    # --- Convert final numpy array back to list of lists ---
    if output_grid_np is None or output_grid_np.size == 0:
        return []
        
    return output_grid_np.tolist()

```
