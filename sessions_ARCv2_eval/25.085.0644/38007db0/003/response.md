```python
import numpy as np

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Transforms the input grid by extracting the rightmost repeating structural unit.

    1. Identify Separator: Determine the `border_color` from the top-left pixel.
    2. Find Pattern Row: Find the first row (`representative_row`), starting from index 1, containing non-border colors. Fallback to row 0 if necessary.
    3. Measure Pattern Width: In the `representative_row`, find the indices of the `border_color`. Calculate `content_width` as the difference between the second and first index.
    4. Calculate Unit Width: Add 1 to `content_width` to get the full `unit_width` (content + separator). Handle cases with fewer than 2 border occurrences.
    5. Extract Rightmost Unit: Calculate the starting column index and extract the subgrid corresponding to the rightmost unit.
    """

    # Convert input list of lists to a numpy array for easier slicing and analysis
    input_np = np.array(input_grid, dtype=int)
    height, width = input_np.shape

    # 1. Identify Separator: Determine the border_color from the top-left pixel.
    border_color = input_np[0, 0]

    # 2. Find Pattern Row: Find the first row (starting index 1) with non-border colors.
    representative_row_idx = 0 # Default to row 0
    found_representative = False
    if height > 1:
        for r_idx in range(1, height):
            row = input_np[r_idx, :]
            if np.any(row != border_color):
                representative_row_idx = r_idx
                found_representative = True
                break
        # If no representative row found below row 0, and row 0 itself has pattern
        if not found_representative and np.any(input_np[0, :] != border_color):
             representative_row_idx = 0 # Explicitly use row 0 if it works
        # If still no pattern found anywhere (e.g., solid color grid),
        # representative_row_idx remains 0, but calculation below will handle it.

    representative_row = input_np[representative_row_idx, :]

    # 3. Measure Pattern Width & 4. Calculate Unit Width
    unit_width = width # Default to full width if pattern isn't clear
    border_indices = np.where(representative_row == border_color)[0]

    if len(border_indices) >= 2:
        # Calculate width based on the first two border occurrences in the representative row
        content_width = border_indices[1] - border_indices[0]
        calculated_unit_width = content_width + 1
        # Basic sanity check: unit width must be > 0 and <= grid width
        if 0 < calculated_unit_width <= width:
             unit_width = calculated_unit_width
    elif len(border_indices) == 1 and border_indices[0] == 0 and width > 1:
        # Handle cases where the only border is on the left edge.
        # This implies the 'unit' might be the whole grid content.
        # Let unit_width remain the default (full width).
        pass # unit_width already defaults to width

    # 5. Extract Rightmost Unit
    # Calculate the starting column index for the rightmost unit
    start_col = max(0, width - unit_width) # Ensure start_col is not negative

    # Extract the subgrid: all rows, columns from start_col to the end
    output_np = input_np[:, start_col:]

    # Convert the resulting numpy array back to a list of lists
    return output_np.tolist()
```