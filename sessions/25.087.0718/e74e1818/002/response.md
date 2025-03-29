Okay, the symmetry hypothesis failed badly. The code execution reveals many mismatches between whether an object *is* vertically symmetric and whether its corresponding rows *are* actually flipped in the expected output.

Let's re-evaluate. The previous code identified *objects* (connected components) and flipped rows based on their vertical extents. The failures indicate this is not the correct approach.

**New Observations & Strategy:**

1.  **Focus on Rows, Not Objects:** The transformation seems to operate on horizontal bands (groups of rows) rather than being determined by individual object properties like symmetry.
2.  **Identify the Bands:** Look at which groups of rows are flipped together.
    *   Example 1: Rows (1, 2, 3) [Red], Rows (4, 5) [Green], Rows (9, 10, 11) [Yellow] are flipped. Rows (6, 7, 8) [Blue] are NOT flipped.
    *   Example 2: Rows (1, 2) [Blue], Rows (4, 5, 6) [Gray], Rows (7, 8) [Red] are flipped. Row 3 [Azure] and Row 9 [Green] are NOT flipped.
    *   Example 3: Rows (1, 2) [Maroon], Rows (4, 5) [Green] are flipped. Row 3 [Yellow] is NOT flipped.
3.  **What defines these bands?**
    *   They seem to correspond to the vertical extent of *something*. Let's reconsider objects.
    *   Maybe it's not individual objects, but *groups* of objects or the *overall pattern* within a certain row range.
    *   In Ex 1, rows 1-3 contain only Red pixels (and background). Rows 4-5 contain only Green. Rows 6-8 contain only Blue. Rows 9-11 contain only Yellow.
    *   In Ex 2, rows 1-2 contain only Blue. Row 3 contains only Azure. Rows 4-6 contain only Gray. Rows 7-8 contain only Red. Row 9 contains only Green.
    *   In Ex 3, rows 1-2 contain only Maroon. Row 3 contains only Yellow. Rows 4-5 contain only Green.
    *   **Hypothesis Refined:** Find maximal vertical bands (contiguous rows) where all non-background pixels within that band belong to the *same color*.
4.  **What determines if a band is flipped?**
    *   Ex 1: Red, Green, Yellow bands flipped. Blue band not flipped.
    *   Ex 2: Blue, Gray, Red bands flipped. Azure, Green bands not flipped.
    *   Ex 3: Maroon, Green bands flipped. Yellow band not flipped.
    *   Let's re-examine the objects *within* these bands and their symmetry.
        *   Ex 1, Blue band (rows 6-8): Contains one object which *is* vertically symmetric. Band NOT flipped.
        *   Ex 1, Red band (rows 1-3): Contains multiple objects. Let's consider the combined pattern in rows 1-3. Is *that* pattern vertically symmetric?
            Input[1:4,:]:
            
```
            [[0,0,0,2,2,2,2,2,2,2,0,0,0],
             [0,0,0,0,2,0,2,0,2,0,0,0,0],
             [0,0,0,0,0,2,0,2,0,0,0,0,0]]
            ```

            Flipud:
            
```
            [[0,0,0,0,0,2,0,2,0,0,0,0,0],
             [0,0,0,0,2,0,2,0,2,0,0,0,0],
             [0,0,0,2,2,2,2,2,2,2,0,0,0]]
            ```

            Not equal. So, the Red band pattern is NOT symmetric. Band IS flipped.
        *   Ex 1, Green band (rows 4-5):
            Input[4:6,:]: `[[0,0,0,3,0,0,3,0,0,3,0,0,0], [0,0,0,0,3,3,3,3,3,0,0,0,0]]`
            Flipud: `[[0,0,0,0,3,3,3,3,3,0,0,0,0], [0,0,0,3,0,0,3,0,0,3,0,0,0]]`
            Not equal. Green band pattern is NOT symmetric. Band IS flipped.
        *   Ex 1, Yellow band (rows 9-11):
            Input[9:12,:]: `[[0,0,0,0,4,4,0,4,4,0,0,0,0], [0,0,0,0,0,0,4,0,0,0,0,0,0], [0,0,0,0,0,0,4,0,0,0,0,0,0]]`
            Flipud: `[[0,0,0,0,0,0,4,0,0,0,0,0,0], [0,0,0,0,0,0,4,0,0,0,0,0,0], [0,0,0,0,4,4,0,4,4,0,0,0,0]]`
            Not equal. Yellow band pattern is NOT symmetric. Band IS flipped.
        *   Ex 2, Azure band (row 3): Single row. Symmetric. Band NOT flipped.
        *   Ex 2, Green band (row 9): Single row. Symmetric. Band NOT flipped.
        *   Ex 3, Yellow band (row 3): Single row. Symmetric. Band NOT flipped.
        *   Check non-symmetric bands from Ex 2/3: Blue (rows 1-2), Gray (4-6), Red (7-8), Maroon (1-2), Green (4-5). All are confirmed non-symmetric when checking the full slice, and all corresponding bands ARE flipped.

*   **Final Hypothesis:**
    1.  Identify maximal vertical bands (contiguous sets of rows) such that all non-background pixels within the band share the same color.
    2.  For each such band, extract the corresponding slice from the input grid.
    3.  Check if this extracted slice is vertically symmetrical (i.e., `np.array_equal(slice, np.flipud(slice))`).
    4.  If the slice is NOT vertically symmetrical, replace that slice in the output grid with the vertically flipped version of the slice.
    5.  If the slice IS vertically symmetrical, copy the original slice to the output grid (or leave it unchanged if starting with a copy).

This hypothesis seems to cover all examples correctly.

**Strategy Re-Cap:** The initial code's failure was applying the flip based on individual object extents and potentially incorrect symmetry checks. The refined strategy identifies monolithic color bands, checks the vertical symmetry of the *entire band's pattern*, and flips the band *only* if it's not symmetric.

## General Assessment

The provided code correctly identified objects but failed because its core logic (flipping rows based on individual object extents) did not match the underlying task rule. The failures on Examples 1 and 3, and the specific analysis of which rows were flipped vs. not flipped in the expected outputs, revealed that the transformation operates on larger vertical "bands" defined by color, and the decision to flip depends on the vertical symmetry of the *entire pattern within that band*. The previous code's symmetry check (if it existed implicitly or explicitly) was likely applied incorrectly or at the wrong level (individual objects vs. full bands). The new strategy involves identifying these color-based row bands and checking the symmetry of the pixel pattern within each band to decide whether to apply a vertical flip to those rows.

## Metrics Gathering

Based on the code execution and manual analysis:

| Example | Input Shape | Output Shape | Bands (Color: Rows)                | Flipped Bands (Expected) | Symmetric Bands (Pattern) | Non-Symmetric Bands (Pattern) |
| :------ | :---------- | :----------- | :--------------------------------- | :----------------------- | :------------------------ | :---------------------------- |
| 1       | (13, 13)    | (13, 13)     | Red: 1-3, Green: 4-5, Blue: 6-8, Yellow: 9-11 | Red, Green, Yellow       | Blue                      | Red, Green, Yellow            |
| 2       | (11, 11)    | (11, 11)     | Blue: 1-2, Azure: 3, Gray: 4-6, Red: 7-8, Green: 9 | Blue, Gray, Red          | Azure, Green              | Blue, Gray, Red               |
| 3       | (7, 7)      | (7, 7)       | Maroon: 1-2, Yellow: 3, Green: 4-5 | Maroon, Green            | Yellow                    | Maroon, Green                 |

*   **Observation:** A band of rows is flipped if and only if the pattern of pixels within that band (across the full grid width) is NOT vertically symmetric. Single-row bands are always vertically symmetric and are never flipped.

## Facts (YAML)


```yaml
task_description: Vertically flip horizontal bands of the grid based on color and symmetry.
definitions:
  band: A maximal contiguous set of rows where all non-background pixels share the same color.
  vertical_symmetry: A grid slice is vertically symmetric if it is identical to itself when flipped top-to-bottom.
processing_steps:
  - step: Identify all maximal vertical bands based on uniform non-background color.
    details: Iterate through rows, grouping consecutive rows that contain only pixels of background (0) or a single specific color (1-9).
  - step: For each identified band:
    - sub_step: Extract the grid slice corresponding to the band's rows.
    - sub_step: Check if the extracted slice is vertically symmetric.
    - sub_step: If the slice is NOT vertically symmetric, perform a vertical flip (top-to-bottom reversal) on the rows of this slice.
    - sub_step: If the slice IS vertically symmetric, leave the rows unchanged.
  - step: Construct the output grid by applying the flips (or lack thereof) to the corresponding row bands from the input grid.
examples_analysis:
  - example: 1
    bands:
      - color: Red, rows: [1, 2, 3], symmetric: false, action: flip
      - color: Green, rows: [4, 5], symmetric: false, action: flip
      - color: Blue, rows: [6, 7, 8], symmetric: true, action: keep
      - color: Yellow, rows: [9, 10, 11], symmetric: false, action: flip
  - example: 2
    bands:
      - color: Blue, rows: [1, 2], symmetric: false, action: flip
      - color: Azure, rows: [3], symmetric: true, action: keep
      - color: Gray, rows: [4, 5, 6], symmetric: false, action: flip
      - color: Red, rows: [7, 8], symmetric: false, action: flip
      - color: Green, rows: [9], symmetric: true, action: keep
  - example: 3
    bands:
      - color: Maroon, rows: [1, 2], symmetric: false, action: flip
      - color: Yellow, rows: [3], symmetric: true, action: keep
      - color: Green, rows: [4, 5], symmetric: false, action: flip

```


## Natural Language Program

1.  Initialize the output grid as a copy of the input grid.
2.  Iterate through the rows of the input grid to identify maximal contiguous vertical "bands". A band is defined as a sequence of one or more rows where all non-background (non-zero) pixels within those rows have the *same* color. Bands are separated by rows containing only background pixels or rows where the non-background color changes.
3.  For each identified band:
    a.  Determine the start row (`min_row`) and end row (`max_row`) of the band.
    b.  Extract the rectangular slice of the input grid corresponding to this band (from `min_row` to `max_row`, covering all columns).
    c.  Check if this extracted slice is vertically symmetrical. This means checking if the slice is identical to the result of flipping the slice vertically (top-to-bottom).
    d.  If the slice is **not** vertically symmetrical, then vertically flip the extracted slice and place this flipped version into the output grid at the corresponding rows (`min_row` to `max_row`).
    e.  If the slice **is** vertically symmetrical, do nothing (the output grid already contains the original, unflipped rows from the initial copy).
4.  Return the modified output grid.## General Assessment

The initial code attempted to solve the task by identifying individual connected objects and flipping the rows spanning their vertical extent. This approach failed on two out of three training examples. The analysis of the failed examples, compared with the successful one, revealed that the transformation is not determined by individual objects but by larger horizontal "bands" defined by color. The key determining factor for whether a band's rows are flipped is the vertical symmetry of the *entire pattern* within that band, not the symmetry of individual objects it might contain. The previous code applied flips based on object extents, leading to incorrect results when a band contained multiple objects or when a symmetric object existed within a band that should not have been flipped (like the blue object in Example 1 or the yellow object in Example 3).

The strategy moving forward is to:
1.  Identify maximal contiguous vertical bands where all non-background pixels share the same color.
2.  For each band, check if the pattern within the full grid slice corresponding to those rows is vertically symmetric.
3.  Flip the rows of the band in the output grid *only if* the band's pattern is *not* vertically symmetric.

## Metrics Gathering

``` python
import numpy as np

def get_bands(grid):
    """Identifies maximal vertical bands of uniform color."""
    rows, cols = grid.shape
    bands = []
    current_band_color = -1 # -1 indicates no active band color
    start_row = 0
    
    for r in range(rows):
        unique_colors = np.unique(grid[r, :])
        non_background_colors = unique_colors[unique_colors != 0]
        
        current_row_color = -1 # Default: background only or mixed colors
        if len(non_background_colors) == 1:
            current_row_color = non_background_colors[0]
        elif len(non_background_colors) == 0:
             current_row_color = 0 # Pure background row
        # else: mixed colors or error, treat as band break
             
        if r == 0:
            # First row
            if current_row_color > 0: # Start band if non-background
                 current_band_color = current_row_color
                 start_row = r
            # If background/mixed, remain -1
        else:
            if current_band_color > 0: # Currently in a band
                if current_row_color != current_band_color: # Band breaks
                    # Finalize previous band
                    bands.append({"color": current_band_color, "rows": list(range(start_row, r))})
                    # Start new band?
                    if current_row_color > 0:
                         current_band_color = current_row_color
                         start_row = r
                    else: # Background or mixed row, end band
                         current_band_color = -1
                # else: Same color, continue band
            else: # Not currently in a band
                 if current_row_color > 0: # Start a new band
                      current_band_color = current_row_color
                      start_row = r
                 # else: Still background/mixed, do nothing

    # Add the last band if it extends to the end
    if current_band_color > 0:
        bands.append({"color": current_band_color, "rows": list(range(start_row, rows))})
        
    return bands

def check_band_symmetry_and_flip(grid, bands, expected_output):
    """Checks symmetry for each band and compares required flip with expected."""
    results = []
    output_copy = np.copy(grid) # Simulate transformation
    
    for band in bands:
        min_row = band["rows"][0]
        max_row = band["rows"][-1]
        color = band["color"]
        
        band_slice = grid[min_row : max_row + 1, :]
        is_symmetric = np.array_equal(band_slice, np.flipud(band_slice))
        
        # Determine if the expected output shows this band flipped
        expected_slice = expected_output[min_row : max_row + 1, :]
        is_actually_flipped = False
        if not is_symmetric: # Only non-symmetric can be flipped
             if np.array_equal(np.flipud(band_slice), expected_slice):
                 is_actually_flipped = True
        elif np.array_equal(band_slice, expected_slice): # Symmetric band should match input
             is_actually_flipped = False # Consistent with not being flipped
        else:
             # Symmetric band but output doesn't match input - error in logic or data
             pass 
             
        # Simulate the transform based on symmetry rule
        should_flip = not is_symmetric
        if should_flip:
             output_copy[min_row : max_row + 1, :] = np.flipud(band_slice)
             
        results.append({
            "color": color,
            "rows": band["rows"],
            "is_symmetric": is_symmetric,
            "should_flip": should_flip,
            "is_actually_flipped": is_actually_flipped,
            "match": should_flip == is_actually_flipped
        })
        
    final_match = np.array_equal(output_copy, expected_output)
    
    return results, final_match


# --- Example 1 Data ---
input_grid_1 = np.array([
    [0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,2,2,2,2,2,2,2,0,0,0],
    [0,0,0,0,2,0,2,0,2,0,0,0,0],
    [0,0,0,0,0,2,0,2,0,0,0,0,0],
    [0,0,0,3,0,0,3,0,0,3,0,0,0],
    [0,0,0,0,3,3,3,3,3,0,0,0,0],
    [0,0,0,0,1,1,1,1,1,0,0,0,0],
    [0,0,0,0,1,0,0,0,1,0,0,0,0],
    [0,0,0,0,1,1,1,1,1,0,0,0,0],
    [0,0,0,0,4,4,0,4,4,0,0,0,0],
    [0,0,0,0,0,0,4,0,0,0,0,0,0],
    [0,0,0,0,0,0,4,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0]
])
expected_output_1_prompt = np.array([
    [0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,2,0,2,0,0,0,0,0], # row 3 input
    [0,0,0,0,2,0,2,0,2,0,0,0,0], # row 2 input
    [0,0,0,2,2,2,2,2,2,2,0,0,0], # row 1 input -> Red flipped
    [0,0,0,0,3,3,3,3,3,0,0,0,0], # row 5 input
    [0,0,0,3,0,0,3,0,0,3,0,0,0], # row 4 input -> Green flipped
    [0,0,0,0,1,1,1,1,1,0,0,0,0], # row 6 input
    [0,0,0,0,1,0,0,0,1,0,0,0,0], # row 7 input
    [0,0,0,0,1,1,1,1,1,0,0,0,0], # row 8 input -> Blue NOT flipped
    [0,0,0,0,0,0,4,0,0,0,0,0,0], # row 11 input
    [0,0,0,0,0,0,4,0,0,0,0,0,0], # row 10 input
    [0,0,0,0,4,4,0,4,4,0,0,0,0], # row 9 input -> Yellow flipped
    [0,0,0,0,0,0,0,0,0,0,0,0,0]
])

# --- Example 2 Data ---
input_grid_2 = np.array([
    [0,0,0,0,0,0,0,0,0,0,0],
    [0,0,1,1,1,1,1,1,1,0,0],
    [0,0,0,1,1,0,1,1,0,0,0],
    [0,0,0,8,8,8,8,8,0,0,0],
    [0,0,0,5,0,5,0,5,0,0,0],
    [0,0,0,5,0,0,0,5,0,0,0],
    [0,0,0,5,5,5,5,5,0,0,0],
    [0,0,0,0,2,2,2,0,0,0,0],
    [0,0,0,0,0,2,0,0,0,0,0],
    [0,0,0,3,3,3,3,3,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0]
])
expected_output_2 = np.array([
    [0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,1,1,0,1,1,0,0,0], # Flipped Blue
    [0,0,1,1,1,1,1,1,1,0,0], # Flipped Blue
    [0,0,0,8,8,8,8,8,0,0,0], # Original Azure
    [0,0,0,5,5,5,5,5,0,0,0], # Flipped Gray
    [0,0,0,5,0,0,0,5,0,0,0], # Flipped Gray
    [0,0,0,5,0,5,0,5,0,0,0], # Flipped Gray
    [0,0,0,0,0,2,0,0,0,0,0], # Flipped Red
    [0,0,0,0,2,2,2,0,0,0,0], # Flipped Red
    [0,0,0,3,3,3,3,3,0,0,0], # Original Green
    [0,0,0,0,0,0,0,0,0,0,0]
])

# --- Example 3 Data ---
input_grid_3 = np.array([
    [0,0,0,0,0,0,0],
    [0,0,9,9,9,0,0],
    [0,9,0,9,0,9,0],
    [0,0,4,4,4,0,0],
    [0,3,3,3,3,3,0],
    [0,0,0,3,0,0,0],
    [0,0,0,0,0,0,0]
])
expected_output_3 = np.array([
    [0,0,0,0,0,0,0],
    [0,9,0,9,0,9,0], # Flipped Maroon
    [0,0,9,9,9,0,0], # Flipped Maroon
    [0,0,4,4,4,0,0], # Original Yellow
    [0,0,0,3,0,0,0], # Flipped Green
    [0,3,3,3,3,3,0], # Flipped Green
    [0,0,0,0,0,0,0]
])

all_grids = {
    "ex1": {"input": input_grid_1, "expected": expected_output_1_prompt},
    "ex2": {"input": input_grid_2, "expected": expected_output_2},
    "ex3": {"input": input_grid_3, "expected": expected_output_3},
}

full_results = {}
for name, grids in all_grids.items():
    print(f"--- Analyzing {name} ---")
    inp = grids["input"]
    exp = grids["expected"]
    bands = get_bands(inp)
    print(f"Bands found: {bands}")
    band_results, final_match = check_band_symmetry_and_flip(inp, bands, exp)
    print("Band Analysis:")
    for res in band_results:
        print(f"  Color {res['color']}, Rows {res['rows']}: Symmetric={res['is_symmetric']}, ShouldFlip={res['should_flip']}, ActuallyFlipped={res['is_actually_flipped']}, Match={res['match']}")
    print(f"Overall Match based on Symmetry Rule: {final_match}")
    full_results[name] = {
         "bands": bands,
         "analysis": band_results,
         "overall_match": final_match
    }

print("\n--- Summary Table ---")
print("| Example | Input Shape | Output Shape | Bands (Color: Rows)                | Flipped Bands (Expected) | Symmetric Bands (Pattern) | Non-Symmetric Bands (Pattern) | Rule Match |")
print("| :------ | :---------- | :----------- | :--------------------------------- | :----------------------- | :------------------------ | :---------------------------- | :--------- |")

for name, res in full_results.items():
    inp = all_grids[name]['input']
    in_shape = inp.shape
    out_shape = all_grids[name]['expected'].shape
    band_strs = []
    flipped_bands_exp = []
    sym_bands = []
    non_sym_bands = []
    for b_res in res['analysis']:
        color_map = {2:"Red", 3:"Green", 1:"Blue", 4:"Yellow", 8:"Azure", 5:"Gray", 9:"Maroon"}
        color_name = color_map.get(b_res['color'], str(b_res['color']))
        rows_str = f"{b_res['rows'][0]}-{b_res['rows'][-1]}" if len(b_res['rows']) > 1 else str(b_res['rows'][0])
        band_strs.append(f"{color_name}: {rows_str}")
        if b_res['is_actually_flipped']:
             flipped_bands_exp.append(color_name)
        if b_res['is_symmetric']:
             sym_bands.append(color_name)
        else:
             non_sym_bands.append(color_name)

    print(f"| {name.replace('ex','')}       | {in_shape}    | {out_shape}    | {', '.join(band_strs)} | {', '.join(flipped_bands_exp)}       | {', '.join(sym_bands)}                      | {', '.join(non_sym_bands)}            | {res['overall_match']}     |")


```
```
--- Analyzing ex1 ---
Bands found: [{'color': np.int64(2), 'rows': [1, 2, 3]}, {'color': np.int64(3), 'rows': [4, 5]}, {'color': np.int64(1), 'rows': [6, 7, 8]}, {'color': np.int64(4), 'rows': [9, 10, 11]}]
Band Analysis:
  Color 2, Rows [1, 2, 3]: Symmetric=False, ShouldFlip=True, ActuallyFlipped=True, Match=True
  Color 3, Rows [4, 5]: Symmetric=False, ShouldFlip=True, ActuallyFlipped=True, Match=True
  Color 1, Rows [6, 7, 8]: Symmetric=True, ShouldFlip=False, ActuallyFlipped=False, Match=True
  Color 4, Rows [9, 10, 11]: Symmetric=False, ShouldFlip=True, ActuallyFlipped=True, Match=True
Overall Match based on Symmetry Rule: True
--- Analyzing ex2 ---
Bands found: [{'color': np.int64(1), 'rows': [1, 2]}, {'color': np.int64(8), 'rows': [3]}, {'color': np.int64(5), 'rows': [4, 5, 6]}, {'color': np.int64(2), 'rows': [7, 8]}, {'color': np.int64(3), 'rows': [9]}]
Band Analysis:
  Color 1, Rows [1, 2]: Symmetric=False, ShouldFlip=True, ActuallyFlipped=True, Match=True
  Color 8, Rows [3]: Symmetric=True, ShouldFlip=False, ActuallyFlipped=False, Match=True
  Color 5, Rows [4, 5, 6]: Symmetric=False, ShouldFlip=True, ActuallyFlipped=True, Match=True
  Color 2, Rows [7, 8]: Symmetric=False, ShouldFlip=True, ActuallyFlipped=True, Match=True
  Color 3, Rows [9]: Symmetric=True, ShouldFlip=False, ActuallyFlipped=False, Match=True
Overall Match based on Symmetry Rule: True
--- Analyzing ex3 ---
Bands found: [{'color': np.int64(9), 'rows': [1, 2]}, {'color': np.int64(4), 'rows': [3]}, {'color': np.int64(3), 'rows': [4, 5]}]
Band Analysis:
  Color 9, Rows [1, 2]: Symmetric=False, ShouldFlip=True, ActuallyFlipped=True, Match=True
  Color 4, Rows [3]: Symmetric=True, ShouldFlip=False, ActuallyFlipped=False, Match=True
  Color 3, Rows [4, 5]: Symmetric=False, ShouldFlip=True, ActuallyFlipped=True, Match=True
Overall Match based on Symmetry Rule: True

--- Summary Table ---
| Example | Input Shape | Output Shape | Bands (Color: Rows)                | Flipped Bands (Expected) | Symmetric Bands (Pattern) | Non-Symmetric Bands (Pattern) | Rule Match |
| :------ | :---------- | :----------- | :--------------------------------- | :----------------------- | :------------------------ | :---------------------------- | :--------- |
| 1       | (13, 13)    | (13, 13)    | Red: 1-3, Green: 4-5, Blue: 6-8, Yellow: 9-11 | Red, Green, Yellow       | Blue                      | Red, Green, Yellow            | True     |
| 2       | (11, 11)    | (11, 11)    | Blue: 1-2, Azure: 3, Gray: 4-6, Red: 7-8, Green: 9 | Blue, Gray, Red       | Azure, Green                      | Blue, Gray, Red            | True     |
| 3       | (7, 7)    | (7, 7)    | Maroon: 1-2, Yellow: 3, Green: 4-5 | Maroon, Green       | Yellow                      | Maroon, Green            | True     |

```
The metrics gathered using the `get_bands` and `check_band_symmetry_and_flip` functions confirm the refined hypothesis. The rule based on flipping non-symmetric color bands correctly predicts the output for all three training examples.

## Facts (YAML)


```yaml
task_description: Vertically flip horizontal bands of the grid based on color and symmetry.
definitions:
  band: A maximal contiguous set of one or more rows where all non-background pixels share the same single color. Bands are separated by rows containing only background pixels (0) or rows containing pixels of multiple different non-background colors.
  vertical_symmetry: A grid slice (representing a band) is vertically symmetric if it is identical to itself when its rows are flipped top-to-bottom using `numpy.flipud`.
processing_steps:
  - step: Identify all maximal vertical color bands in the input grid.
    details: Iterate through rows from top to bottom. Group consecutive rows `r_start` to `r_end` if all non-zero pixels within `grid[r_start:r_end+1, :]` have the exact same color value.
  - step: Initialize the output grid as a copy of the input grid.
  - step: For each identified band:
    - sub_step: Define the row range `min_row` to `max_row`.
    - sub_step: Extract the grid slice `input_slice = input_grid[min_row : max_row + 1, :]`.
    - sub_step: Check if `input_slice` is vertically symmetric by comparing `input_slice` with `numpy.flipud(input_slice)`.
    - sub_step: If the slice is NOT vertically symmetric:
        action: Compute the flipped slice `flipped_slice = numpy.flipud(input_slice)`.
        action: Update the output grid `output_grid[min_row : max_row + 1, :] = flipped_slice`.
    - sub_step: If the slice IS vertically symmetric:
        action: No change is needed for this band in the output grid (it retains the values from the initial copy).
  - step: Return the final output grid.
examples_analysis:
  - example: 1
    bands:
      - color: Red, rows: [1, 2, 3], symmetric: false, action: flip
      - color: Green, rows: [4, 5], symmetric: false, action: flip
      - color: Blue, rows: [6, 7, 8], symmetric: true, action: keep
      - color: Yellow, rows: [9, 10, 11], symmetric: false, action: flip
    result: Rule matches expected output.
  - example: 2
    bands:
      - color: Blue, rows: [1, 2], symmetric: false, action: flip
      - color: Azure, rows: [3], symmetric: true, action: keep
      - color: Gray, rows: [4, 5, 6], symmetric: false, action: flip
      - color: Red, rows: [7, 8], symmetric: false, action: flip
      - color: Green, rows: [9], symmetric: true, action: keep
    result: Rule matches expected output.
  - example: 3
    bands:
      - color: Maroon, rows: [1, 2], symmetric: false, action: flip
      - color: Yellow, rows: [3], symmetric: true, action: keep
      - color: Green, rows: [4, 5], symmetric: false, action: flip
    result: Rule matches expected output.

```


## Natural Language Program

1.  Create the output grid as an identical copy of the input grid.
2.  Scan the input grid row by row to identify continuous vertical bands. A band consists of one or more consecutive rows where every non-background pixel shares the same color. A band ends when a row with only background pixels, a row with multiple different non-background colors, or a row with a different single non-background color is encountered.
3.  For each identified band, defined by its start row (`min_row`) and end row (`max_row`):
    a.  Extract the rectangular portion (slice) of the input grid corresponding to these rows (`input_grid[min_row : max_row + 1, :]`).
    b.  Determine if this extracted slice is vertically symmetrical by checking if the slice is equal to itself flipped vertically (top-to-bottom).
    c.  If the slice is **not** vertically symmetrical, replace the corresponding rows in the output grid with the vertically flipped version of the slice.
    d.  If the slice **is** vertically symmetrical, make no changes to the corresponding rows in the output grid.
4.  Return the final output grid.