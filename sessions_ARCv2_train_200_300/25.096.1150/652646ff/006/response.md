## General Assessment and Strategy

The previous code correctly identified the concept of a background digit and the need to find specific non-background ("signal" or "foreground") digits to generate 6x6 output patterns. However, the results show consistent failures across all training examples. The key discrepancies are:

1.  **Order of Patterns**: The generated 6x6 blocks are stacked in numerical order of the signal digits (e.g., 1, 4, 8), while the expected outputs show a different order (e.g., 4, 8, 1).
2.  **Structure of Patterns**: The generated patterns in the transformed output do not match the pixel values of the expected output patterns, even though the correct foreground digits seem to be identified (just in the wrong order). This suggests either the assumed 6x6 frame structure is wrong, or the background digit used *within* the generated pattern is incorrect.

**Strategy:**

1.  **Re-evaluate Signal Digit Identification**: Confirm if the self-adjacency rule correctly identifies all necessary digits.
2.  **Determine Correct Ordering**: Analyze the input grids to find the property that dictates the order in which the 6x6 patterns appear in the output. Possibilities include spatial location (top-most, left-most instance of the pattern), frequency, or some other characteristic.
3.  **Verify Pattern Structure**: Explicitly check if the 6x6 patterns in the *expected* outputs always conform to the frame structure assumed previously. Also, confirm if the background digit *within* each 6x6 output block is always the most frequent digit from the *input*.
4.  **Refine the Natural Language Program**: Update the transformation logic based on these findings.

## Metrics Gathering

Let's verify the background digit, the signal digits present in the output, their order, and the pattern structure.


``` python
import numpy as np
from collections import Counter

def _get_background_digit(grid: np.ndarray) -> int:
    """Finds the most frequent digit in the grid."""
    if grid.size == 0:
        return -1 # Or raise error
    counts = Counter(grid.flatten())
    return int(counts.most_common(1)[0][0])

def analyze_example(input_grid_list: list[list[int]], output_grid_list: list[list[int]]):
    """Analyzes input and output for background, foreground digits, and order."""
    input_grid = np.array(input_grid_list, dtype=int)
    output_grid = np.array(output_grid_list, dtype=int)

    bg_digit_input = _get_background_digit(input_grid)

    # Determine foreground digits and their order from the output
    foreground_digits_ordered = []
    if output_grid.size > 0 and output_grid.shape[0] % 6 == 0 and output_grid.shape[1] == 6:
        num_patterns = output_grid.shape[0] // 6
        for i in range(num_patterns):
            pattern = output_grid[i*6 : (i+1)*6, :]
            unique_in_pattern = np.unique(pattern)
            if len(unique_in_pattern) == 2:
                fg = unique_in_pattern[0] if unique_in_pattern[1] == bg_digit_input else unique_in_pattern[1]
                if fg != bg_digit_input: # Ensure we identified a non-background digit
                     foreground_digits_ordered.append(int(fg))
                else: # Handle case where pattern might only contain background? Unlikely based on examples.
                     foreground_digits_ordered.append(None) # Mark as problematic
            elif len(unique_in_pattern) == 1 and unique_in_pattern[0] == bg_digit_input:
                 # This case might occur if a pattern only had the background digit, ignore
                 pass
            else:
                 # More than 2 digits or only one non-background digit? Problem.
                 foreground_digits_ordered.append(None) # Mark as problematic


    # Find signal digits using the adjacency rule from previous code
    signal_digits_adjacency = set()
    rows, cols = input_grid.shape
    unique_digits_input = np.unique(input_grid)
    candidate_digits = [int(d) for d in unique_digits_input if d != bg_digit_input]
    neighbors = [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]
    for digit in candidate_digits:
        locations = np.argwhere(input_grid == digit)
        is_signal = False
        for r, c in locations:
            for dr, dc in neighbors:
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols and input_grid[nr, nc] == digit:
                    signal_digits_adjacency.add(digit)
                    is_signal = True; break
            if is_signal: break
    sorted_signal_digits_adjacency = sorted(list(signal_digits_adjacency))


    # Check pattern structure (using the first pattern in output as example)
    pattern_structure_match = True
    if len(foreground_digits_ordered) > 0 and foreground_digits_ordered[0] is not None:
        first_pattern = output_grid[0:6, 0:6]
        fg_digit = foreground_digits_ordered[0]
        bg_digit = bg_digit_input # Assume background is consistent

        # Expected coordinates for foreground digit
        expected_fg_coords = set([
            (0,0), (0,2), (0,3), (0,5),
            (1,0), (1,1), (1,4), (1,5),
            (2,0), (2,5),
            (3,0), (3,5),
            (4,0), (4,1), (4,4), (4,5),
            (5,0), (5,2), (5,3), (5,5)
        ])
        actual_fg_coords = set(tuple(coord) for coord in np.argwhere(first_pattern == fg_digit))

        if expected_fg_coords != actual_fg_coords:
            pattern_structure_match = False
        # Also check background positions implicitly - are all other cells the bg_digit?
        elif np.count_nonzero(first_pattern == bg_digit) != (36 - len(expected_fg_coords)):
             pattern_structure_match = False


    return {
        "input_shape": input_grid.shape,
        "output_shape": output_grid.shape,
        "input_bg_digit": bg_digit_input,
        "output_foreground_digits_ordered": foreground_digits_ordered,
        "adjacency_signal_digits_sorted": sorted_signal_digits_adjacency,
        "first_pattern_structure_matches_assumed": pattern_structure_match
    }

# --- Data ---
train_inputs = [
    [[2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2], [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2], [2, 2, 2, 5, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 5, 2, 2], [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2], [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2], [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2], [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2], [2, 2, 2, 4, 4, 2, 2, 2, 8, 8, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2], [2, 2, 4, 2, 2, 4, 2, 8, 2, 2, 8, 2, 3, 3, 2, 2, 2, 2, 2, 2], [2, 4, 2, 2, 2, 2, 4, 5, 2, 2, 2, 8, 2, 2, 3, 2, 2, 2, 2, 2], [2, 4, 2, 9, 2, 2, 4, 2, 2, 2, 3, 8, 2, 9, 2, 3, 2, 2, 2, 2], [2, 2, 4, 2, 2, 4, 2, 8, 2, 2, 8, 2, 2, 2, 2, 3, 2, 2, 2, 2], [2, 2, 2, 4, 4, 2, 2, 2, 8, 8, 2, 3, 2, 2, 3, 2, 2, 2, 2, 2], [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 2, 2, 2, 2, 2, 2], [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2], [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2], [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 5, 2, 2, 2, 2, 2, 2, 2, 2, 2], [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2], [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2], [5, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]],
    [[3, 3, 3, 3, 3, 3, 3, 3, 3, 3], [5, 3, 3, 4, 4, 3, 3, 3, 3, 3], [3, 3, 4, 3, 8, 4, 3, 3, 3, 3], [3, 4, 3, 8, 3, 3, 4, 3, 3, 3], [3, 4, 8, 1, 3, 3, 4, 8, 3, 3], [3, 1, 4, 3, 1, 4, 3, 8, 3, 3], [1, 3, 3, 4, 4, 1, 8, 3, 3, 3], [1, 3, 5, 3, 8, 8, 3, 3, 3, 3], [3, 1, 3, 3, 1, 3, 3, 3, 3, 3], [3, 3, 1, 1, 3, 3, 5, 3, 3, 3]],
    [[4, 4, 4, 4, 4, 5, 4, 4, 4, 4, 4, 4, 4], [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 7, 4], [4, 4, 2, 2, 4, 4, 4, 4, 4, 4, 4, 4, 4], [4, 2, 4, 4, 2, 4, 4, 4, 4, 4, 4, 4, 4], [2, 4, 4, 7, 4, 2, 4, 4, 4, 4, 4, 4, 4], [2, 4, 4, 4, 4, 8, 8, 4, 4, 5, 4, 4, 4], [4, 2, 4, 4, 8, 4, 4, 8, 4, 4, 4, 4, 4], [4, 4, 2, 8, 4, 4, 4, 4, 8, 4, 4, 4, 4], [4, 4, 4, 8, 4, 4, 4, 4, 3, 3, 4, 4, 4], [4, 4, 4, 4, 8, 4, 4, 3, 4, 4, 3, 4, 4], [4, 5, 4, 4, 4, 8, 3, 4, 4, 4, 4, 3, 4], [4, 4, 7, 4, 4, 4, 3, 4, 4, 5, 4, 3, 4], [4, 4, 4, 4, 4, 4, 4, 3, 4, 4, 3, 4, 4]],
    [[8, 8, 8, 8, 8, 8, 8, 8, 5, 8], [8, 8, 8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 4, 4, 8, 3, 3, 8, 8], [8, 8, 4, 8, 8, 4, 8, 8, 3, 8], [8, 4, 2, 8, 3, 8, 4, 8, 8, 3], [8, 4, 8, 8, 3, 8, 4, 8, 8, 3], [8, 8, 4, 8, 8, 4, 8, 8, 3, 8], [8, 8, 8, 4, 4, 8, 3, 3, 8, 8], [8, 5, 8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8, 2, 8, 8]]
]

train_outputs = [
    [[2, 2, 4, 4, 2, 2], [2, 4, 2, 2, 4, 2], [4, 2, 2, 2, 2, 4], [4, 2, 2, 2, 2, 4], [2, 4, 2, 2, 4, 2], [2, 2, 4, 4, 2, 2], [2, 2, 8, 8, 2, 2], [2, 8, 2, 2, 8, 2], [8, 2, 2, 2, 2, 8], [8, 2, 2, 2, 2, 8], [2, 8, 2, 2, 8, 2], [2, 2, 8, 8, 2, 2], [2, 2, 3, 3, 2, 2], [2, 3, 2, 2, 3, 2], [3, 2, 2, 2, 2, 3], [3, 2, 2, 2, 2, 3], [2, 3, 2, 2, 3, 2], [2, 2, 3, 3, 2, 2]],
    [[3, 3, 4, 4, 3, 3], [3, 4, 3, 3, 4, 3], [4, 3, 3, 3, 3, 4], [4, 3, 3, 3, 3, 4], [3, 4, 3, 3, 4, 3], [3, 3, 4, 4, 3, 3], [3, 3, 8, 8, 3, 3], [3, 8, 3, 3, 8, 3], [8, 3, 3, 3, 3, 8], [8, 3, 3, 3, 3, 8], [3, 8, 3, 3, 8, 3], [3, 3, 8, 8, 3, 3], [3, 3, 1, 1, 3, 3], [3, 1, 3, 3, 1, 3], [1, 3, 3, 3, 3, 1], [1, 3, 3, 3, 3, 1], [3, 1, 3, 3, 1, 3], [3, 3, 1, 1, 3, 3]],
    [[4, 4, 3, 3, 4, 4], [4, 3, 4, 4, 3, 4], [3, 4, 4, 4, 4, 3], [3, 4, 4, 4, 4, 3], [4, 3, 4, 4, 3, 4], [4, 4, 3, 3, 4, 4], [4, 4, 8, 8, 4, 4], [4, 8, 4, 4, 8, 4], [8, 4, 4, 4, 4, 8], [8, 4, 4, 4, 4, 8], [4, 8, 4, 4, 8, 4], [4, 4, 8, 8, 4, 4], [4, 4, 2, 2, 4, 4], [4, 2, 4, 4, 2, 4], [2, 4, 4, 4, 4, 2], [2, 4, 4, 4, 4, 2], [4, 2, 4, 4, 2, 4], [4, 4, 2, 2, 4, 4]],
    [[8, 8, 4, 4, 8, 8], [8, 4, 8, 8, 4, 8], [4, 8, 8, 8, 8, 4], [4, 8, 8, 8, 8, 4], [8, 4, 8, 8, 4, 8], [8, 8, 4, 4, 8, 8], [8, 8, 3, 3, 8, 8], [8, 3, 8, 8, 3, 8], [3, 8, 8, 8, 8, 3], [3, 8, 8, 8, 8, 3], [8, 3, 8, 8, 3, 8], [8, 8, 3, 3, 8, 8]]
]

results = []
for i in range(len(train_inputs)):
    print(f"--- Analyzing Example {i+1} ---")
    analysis = analyze_example(train_inputs[i], train_outputs[i])
    results.append(analysis)
    print(analysis)

# Check if pattern structure is consistent across all examples where it was checked
consistent_structure = all(r['first_pattern_structure_matches_assumed'] for r in results if r['output_foreground_digits_ordered'])
print(f"\nPattern structure consistently matches assumed frame: {consistent_structure}")

# Compare adjacency-based sorting vs output order
print("\nComparison of Adjacency Signal Digits (Sorted) vs Actual Output Order:")
for i, r in enumerate(results):
    print(f"Example {i+1}:")
    print(f"  Adjacency (sorted): {r['adjacency_signal_digits_sorted']}")
    print(f"  Actual Output Order: {r['output_foreground_digits_ordered']}")
    print(f"  Match: {r['adjacency_signal_digits_sorted'] == r['output_foreground_digits_ordered']}")

print(f"\nBackground digits: {[r['input_bg_digit'] for r in results]}")

# Identify digits filtered out by adjacency rule
print("\nDigits in input vs. Adjacency Signal Digits:")
for i, r in enumerate(results):
    input_grid = np.array(train_inputs[i])
    all_non_bg = sorted([int(d) for d in np.unique(input_grid) if d != r['input_bg_digit']])
    signal = r['adjacency_signal_digits_sorted']
    missed_or_noise = [d for d in all_non_bg if d not in signal]
    print(f"Example {i+1} (BG={r['input_bg_digit']}):")
    print(f"  All non-BG digits in input: {all_non_bg}")
    print(f"  Signal digits (adjacency):  {signal}")
    print(f"  Non-signal/Noise digits:  {missed_or_noise}")



```
```
--- Analyzing Example 1 ---
{'input_shape': (20, 20), 'output_shape': (18, 6), 'input_bg_digit': 2, 'output_foreground_digits_ordered': [4, 8, 3], 'adjacency_signal_digits_sorted': [3, 4, 8], 'first_pattern_structure_matches_assumed': False}
--- Analyzing Example 2 ---
{'input_shape': (10, 10), 'output_shape': (18, 6), 'input_bg_digit': 3, 'output_foreground_digits_ordered': [4, 8, 1], 'adjacency_signal_digits_sorted': [1, 4, 8], 'first_pattern_structure_matches_assumed': False}
--- Analyzing Example 3 ---
{'input_shape': (13, 13), 'output_shape': (18, 6), 'input_bg_digit': 4, 'output_foreground_digits_ordered': [3, 8, 2], 'adjacency_signal_digits_sorted': [2, 3, 8], 'first_pattern_structure_matches_assumed': False}
--- Analyzing Example 4 ---
{'input_shape': (10, 10), 'output_shape': (12, 6), 'input_bg_digit': 8, 'output_foreground_digits_ordered': [4, 3], 'adjacency_signal_digits_sorted': [3, 4], 'first_pattern_structure_matches_assumed': False}

Pattern structure consistently matches assumed frame: False

Comparison of Adjacency Signal Digits (Sorted) vs Actual Output Order:
Example 1:
  Adjacency (sorted): [3, 4, 8]
  Actual Output Order: [4, 8, 3]
  Match: False
Example 2:
  Adjacency (sorted): [1, 4, 8]
  Actual Output Order: [4, 8, 1]
  Match: False
Example 3:
  Adjacency (sorted): [2, 3, 8]
  Actual Output Order: [3, 8, 2]
  Match: False
Example 4:
  Adjacency (sorted): [3, 4]
  Actual Output Order: [4, 3]
  Match: False

Background digits: [2, 3, 4, 8]

Digits in input vs. Adjacency Signal Digits:
Example 1 (BG=2):
  All non-BG digits in input: [3, 4, 5, 8, 9]
  Signal digits (adjacency):  [3, 4, 8]
  Non-signal/Noise digits:  [5, 9]
Example 2 (BG=3):
  All non-BG digits in input: [1, 4, 5, 8]
  Signal digits (adjacency):  [1, 4, 8]
  Non-signal/Noise digits:  [5]
Example 3 (BG=4):
  All non-BG digits in input: [2, 3, 5, 7, 8]
  Signal digits (adjacency):  [2, 3, 8]
  Non-signal/Noise digits:  [5, 7]
Example 4 (BG=8):
  All non-BG digits in input: [2, 3, 4, 5]
  Signal digits (adjacency):  [3, 4]
  Non-signal/Noise digits:  [2, 5]

```
## Analysis of Metrics

1.  **Background Digit**: Correctly identified as the most frequent digit in all examples (2, 3, 4, 8 respectively).
2.  **Signal Digits (Adjacency Rule)**: The adjacency rule successfully identifies the digits that *are* used in the output (e.g., finds [3, 4, 8] for Ex 1 where output uses 4, 8, 3). It also correctly filters out the 'noise' digits (e.g., 5, 9 in Ex 1; 5 in Ex 2; 5, 7 in Ex 3; 2, 5 in Ex 4).
3.  **Order of Digits**: The crucial finding is that the **actual order** of foreground digits in the output (`output_foreground_digits_ordered`) is **different** from the numerically sorted order of signal digits found by adjacency (`adjacency_signal_digits_sorted`). This confirms Hypothesis H1: the sorting criteria is not simple numerical order. The specific order needs to be determined.
4.  **Pattern Structure**: The analysis (`first_pattern_structure_matches_assumed`: False) indicates that the 6x6 patterns in the **expected output** do **not** match the fixed frame structure assumed previously. This invalidates Hypothesis H3 and the `_create_pattern_grid` function used before. The actual structure of the 6x6 blocks needs to be extracted directly from the input.

**New Hypothesis for Ordering**: The order might be determined by the location of the *first* instance of a pattern matching the *actual* structure in the input grid (e.g., scan top-to-bottom, left-to-right).

**New Hypothesis for Pattern Structure**: The required 6x6 patterns *are* present in the input grid. Instead of generating a fixed pattern, the task is likely to *find* these specific 6x6 patterns in the input and extract them. The adjacency rule might just be a way to identify *which* digits form these patterns, but the patterns themselves must be located and copied.

Let's re-examine the input/output of Example 1. BG=2. Output order is 4, 8, 3.
Input contains clumps of 4s, 8s, and 3s. We need to find the 6x6 block corresponding to '4', the 6x6 block for '8', and the 6x6 block for '3' *within* the input grid that match the respective blocks in the output.

Example 1 Output blocks:
Block 1 (Digit 4):

```
2 2 4 4 2 2
2 4 2 2 4 2
4 2 2 2 2 4
4 2 2 2 2 4
2 4 2 2 4 2
2 2 4 4 2 2
```

Block 2 (Digit 8):

```
2 2 8 8 2 2
2 8 2 2 8 2
8 2 2 2 2 8
8 2 2 2 2 8
2 8 2 2 8 2
2 2 8 8 2 2
```

Block 3 (Digit 3):

```
2 2 3 3 2 2
2 3 2 2 3 2
3 2 2 2 2 3
3 2 2 2 2 3
2 3 2 2 3 2
2 2 3 3 2 2
```

All these blocks share the *same structure*, just with a different foreground digit (4, 8, or 3) and the background digit (2). This structure *is* the one assumed previously. The metric check failed because the tool code `analyze_example` used hardcoded coordinates which seem to be incorrect based on the actual output data provided in the problem description. Let's re-verify the pattern coordinates against the expected output:

Pattern:

```
B B F F B B  (Row 0: F at index 2, 3) <- My previous analysis was wrong
B F B B F B  (Row 1: F at index 1, 4) <- My previous analysis was wrong
F B B B B F  (Row 2: F at index 0, 5) <- Correct
F B B B B F  (Row 3: F at index 0, 5) <- Correct
B F B B F B  (Row 4: F at index 1, 4) <- My previous analysis was wrong
B B F F B B  (Row 5: F at index 2, 3) <- My previous analysis was wrong
```

This *is* a consistent frame structure, just different from the one I derived initially. The tool code check needs correction.

**Revised Understanding:**
1. Find Background Digit (BG).
2. Find Signal Digits (non-BG, self-adjacent).
3. Find all occurrences of 6x6 subgrids in the input that match the *correct* frame pattern (verified above) for *each* signal digit.
4. Determine the order: It's likely based on the top-most, then left-most occurrence of *any* valid 6x6 pattern found in step 3. Collect the signal digits in this order.
5. Construct the output: For each signal digit *in the determined order*, create the standard 6x6 pattern using that digit and the BG digit. Stack these patterns vertically.

## YAML Facts


```yaml
objects:
  - name: input_grid
    type: 2D list of integers
    properties:
      - rows: integer
      - columns: integer
      - cells: containing single digits
      - background_digit: integer (most frequent digit)
      - signal_digits: list of integers (non-background, self-adjacent)
      - noise_digits: list of integers (non-background, not self-adjacent)
      - embedded_patterns: 6x6 subgrids matching a specific structure

  - name: output_grid
    type: 2D list of integers
    properties:
      - rows: multiple of 6
      - columns: 6
      - composed_of: vertically stacked 6x6 patterns

  - name: pattern
    type: 6x6 2D list of integers
    properties:
      - structure: fixed frame shape (8 foreground cells, 28 background cells)
      - foreground_digit: a signal digit from the input
      - background_digit: the background digit from the input

actions:
  - name: identify_background_digit
    input: input_grid
    output: background_digit
    description: Find the most frequent digit in the input grid.

  - name: identify_signal_digits
    input: input_grid, background_digit
    output: list of signal_digits
    description: Find all unique non-background digits where at least one instance is adjacent (horizontally, vertically, or diagonally) to another instance of the same digit.

  - name: find_pattern_occurrences
    input: input_grid, background_digit, list of signal_digits
    output: list of tuples (row, column, signal_digit)
    description: Scan the input grid for all 6x6 subgrids matching the defined pattern structure for any signal digit. Record the top-left corner (row, col) and the signal digit for each match.

  - name: determine_output_order
    input: list of pattern occurrences (row, column, signal_digit)
    output: ordered list of unique signal_digits
    description: Sort the found pattern occurrences primarily by row, secondarily by column. Extract the unique signal digits based on this sorted order.

  - name: construct_pattern
    input: foreground_digit, background_digit
    output: pattern (6x6 grid)
    description: Create a 6x6 grid using the background digit, filling the 8 specific frame cells with the foreground digit. The frame coordinates are: (0,2), (0,3), (1,1), (1,4), (2,0), (2,5), (3,0), (3,5), (4,1), (4,4), (5,2), (5,3).

  - name: construct_output_grid
    input: ordered list of signal_digits, background_digit
    output: output_grid
    description: For each signal digit in the determined order, construct its corresponding 6x6 pattern. Stack these patterns vertically.

```


## Natural Language Program

1.  **Analyze Input**: Given an input grid of digits.
2.  **Find Background**: Determine the background digit (BG) by finding the most frequent digit in the entire input grid.
3.  **Identify Potential Signal Digits**: Identify all unique digits in the input grid that are not the background digit (BG).
4.  **Filter for Actual Signal Digits**: For each potential signal digit, check if any instance of it in the input grid is adjacent (horizontally, vertically, or diagonally) to another instance of the *same* digit. Keep only those digits that satisfy this condition; these are the actual signal digits.
5.  **Define Target Pattern Structure**: Define the required 6x6 pattern structure: it consists of the background digit (BG) filling most cells, and a specific foreground digit (FG) filling 8 cells in a fixed frame shape. The coordinates for the foreground digit (FG) relative to the top-left corner (0,0) of the 6x6 pattern are: (0,2), (0,3), (1,1), (1,4), (2,0), (2,5), (3,0), (3,5), (4,1), (4,4), (5,2), (5,3).
6.  **Locate Pattern Instances**: Scan the input grid (e.g., row by row, then column by column) for all occurrences of 6x6 subgrids. For each 6x6 subgrid, check if it perfectly matches the target pattern structure defined in step 5, using the input grid's background digit (BG) and one of the actual signal digits (found in step 4) as the foreground digit (FG). Record the top-left row index, top-left column index, and the signal digit (FG) for every match found.
7.  **Determine Output Order**: Create a list of the matches found in step 6. Sort this list primarily by row index (ascending) and secondarily by column index (ascending). Iterate through the sorted list and collect the signal digits encountered, ensuring each signal digit is added only the *first* time it appears in the sorted list. This creates the final ordered list of signal digits for the output.
8.  **Construct Output**: Initialize an empty output grid. For each signal digit in the final ordered list obtained in step 7:
    a.  Create the standard 6x6 pattern grid using the current signal digit as the foreground (FG) and the input grid's background digit (BG), following the structure defined in step 5.
    b.  Append this 6x6 pattern grid vertically to the bottom of the output grid being built.
9.  **Finalize**: Return the constructed output grid. If no signal digits are found or no pattern instances are located, return an empty grid.