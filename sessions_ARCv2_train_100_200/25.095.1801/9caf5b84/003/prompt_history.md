
## train_1

**input:**
```
1 2 5 5 0 3
3 0 2 3 1 3
1 5 3 5 2 1
2 3 5 1 1 5
3 3 0 1 2 0
3 1 5 1 3 1
```


**output:**
```
1 7 7 7 7 3
3 7 7 3 1 3
1 7 3 7 7 1
7 3 7 1 1 7
3 3 7 1 7 7
3 1 7 1 3 1
```


## train_2

**input:**
```
0 9 5 9
9 2 5 2
0 2 5 1
1 2 9 2
```


**output:**
```
7 9 7 9
9 2 7 2
7 2 7 7
7 2 9 2
```


## train_3

**input:**
```
9 1 2 1 1 2
1 1 2 6 3 6
6 1 6 6 9 6
6 2 9 6 9 3
1 2 6 2 6 1
1 6 3 3 2 3
```


**output:**
```
7 1 7 1 1 7
1 1 7 6 7 6
6 1 6 6 7 6
6 7 7 6 7 7
1 7 6 7 6 1
1 6 7 7 7 7
```


## train_4

**input:**
```
1 2 1 0 0 0
0 6 1 0 1 0
0 4 1 0 2 6
4 1 2 1 1 1
```


**output:**
```
1 7 1 0 0 0
0 7 1 0 1 0
0 7 1 0 7 7
7 1 7 1 1 1
```

## Perception of Elements

The task involves transforming a 2D grid of single digits into another grid of the same dimensions. The transformation rule appears to be consistent across all examples but depends on the statistical properties (specifically, digit frequencies) of the *entire* input grid. Each cell's transformation is determined by whether its digit belongs to a dynamically calculated "stable set". All digits not in the stable set are replaced by a constant digit, 7.

## Documented Facts


```yaml
task_elements:
  - name: input_grid
    type: 2D array of integers (0-9)
  - name: output_grid
    type: 2D array of integers (0-9)
    description: Same dimensions as input_grid.
  - name: transformation_rule
    type: conditional replacement
    description: Replaces certain digits based on global grid statistics.
  - name: stable_set
    type: set of integers
    description: Digits that remain unchanged during transformation. Determined by frequency analysis.
  - name: replacement_value
    type: integer
    value: 7
    description: The constant digit used to replace non-stable digits.

relationships:
  - type: determination
    source: input_grid
    target: stable_set
    details: The stable_set is determined by the frequency distribution of digits within the input_grid.
  - type: transformation
    input: input_grid cell value
    condition: cell value NOT IN stable_set
    output: replacement_value (7)
  - type: transformation
    input: input_grid cell value
    condition: cell value IN stable_set
    output: input_grid cell value (no change)

stable_set_determination:
  - step: Calculate frequency of each digit (0-9) in the input_grid.
  - step: Identify M, the smallest digit with the highest frequency.
  - step: Identify D2, the smallest digit with the second highest frequency.
  - step: Initialize stable_set S = {1}.
  - step: If M is not 1, add M to S.
  - step: Add D2 to S.
```


## Natural Language Program

1.  Analyze the input grid to count the frequency of each digit from 0 to 9.
2.  Determine the digit `M` that occurs most frequently. If multiple digits share the highest frequency, choose the smallest among them.
3.  Determine the digit `D2` that occurs second most frequently. If multiple digits share the second highest frequency, choose the smallest among them.
4.  Define a set of "stable" digits, `S`. Start by adding the digit `1` to `S`.
5.  If the most frequent digit `M` is different from `1`, add `M` to the stable set `S`.
6.  Add the second most frequent digit `D2` to the stable set `S`. (Note: `S` automatically handles duplicates if `D2` is already present).
7.  Construct the output grid by examining each digit in the input grid:
    *   If the input digit is present in the stable set `S`, keep the digit unchanged in the corresponding position in the output grid.
    *   If the input digit is *not* present in the stable set `S`, place the digit `7` in the corresponding position in the output grid.
```python
import collections
import itertools

"""
Transforms the input grid based on digit frequencies.

1. Calculate the frequency of each digit (0-9) across the entire input grid.
2. Identify 'M', the smallest digit with the highest frequency.
3. Identify 'D2', the smallest digit with the second highest frequency.
4. Create a "stable set" containing only M and D2.
5. Iterate through the input grid:
   - If a digit is in the stable set, keep it.
   - Otherwise, replace it with 7.
"""

def _find_m_d2(input_grid: list[list[int]]) -> tuple[int, int | None]:
    """
    Finds M (smallest digit with highest frequency) and 
    D2 (smallest digit with second highest frequency).

    Args:
        input_grid: The 2D list of integers.

    Returns:
        A tuple (m, d2), where m is the most frequent digit (smallest tie-breaker)
        and d2 is the second most frequent digit (smallest tie-breaker).
        Returns (m, None) if there is only one frequency level.
    """
    # Flatten the grid and count digit frequencies
    all_digits = list(itertools.chain.from_iterable(input_grid))
    if not all_digits:
        return (None, None) # Handle empty grid case
        
    counts = collections.Counter(all_digits)
    
    # Group digits by frequency
    grouped_by_freq = collections.defaultdict(list)
    for digit, freq in counts.items():
        grouped_by_freq[freq].append(digit)
        
    # Sort frequencies in descending order
    sorted_freqs = sorted(grouped_by_freq.keys(), reverse=True)
    
    # Determine M (smallest digit with the highest frequency)
    highest_freq = sorted_freqs[0]
    m = min(grouped_by_freq[highest_freq])
    
    # Determine D2 (smallest digit with the second highest frequency)
    d2 = None
    if len(sorted_freqs) > 1:
        second_highest_freq = sorted_freqs[1]
        d2 = min(grouped_by_freq[second_highest_freq])
        
    # Handle edge case where M might be the only digit type
    # If d2 wasn't found because only one frequency level exists,
    # the logic implicitly handles this as d2 remains None.
    # If the problem guarantees at least two frequency levels or digits,
    # this check might be redundant, but it's safer.
        
    return m, d2


def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies the transformation rule based on digit frequencies.

    Args:
        input_grid: A list of lists representing the input grid of digits.

    Returns:
        A list of lists representing the transformed output grid.
    """
    
    # Handle empty input grid
    if not input_grid or not input_grid[0]:
        return []

    rows = len(input_grid)
    cols = len(input_grid[0])
    
    # initialize output_grid with the same dimensions
    output_grid = [[0 for _ in range(cols)] for _ in range(rows)]

    # 1-3. Determine M (most frequent) and D2 (second most frequent) digits
    m, d2 = _find_m_d2(input_grid)
    
    # Handle case where grid might be too small or uniform to find M and D2
    if m is None: 
         # If no digits, return empty or copy? Let's return a grid of 7s of same size.
         # Or maybe copy input? Based on rule, if stable set is empty, all become 7.
         return [[7 for _ in range(cols)] for _ in range(rows)]

    # 4. Create the stable set containing M and D2
    stable_set = set()
    stable_set.add(m)
    if d2 is not None:
        stable_set.add(d2)
        
    replacement_value = 7

    # 5. Perform transformations
    for r in range(rows):
        for c in range(cols):
            digit = input_grid[r][c]
            # If the digit is in the stable set, keep it
            if digit in stable_set:
                output_grid[r][c] = digit
            # Otherwise, replace it with 7
            else:
                output_grid[r][c] = replacement_value

    return output_grid
```

Previous Code:
```python
import collections
import itertools

"""
Transforms the input grid based on digit frequencies.

1. Calculate the frequency of each digit (0-9) across the entire input grid.
2. Identify 'M', the smallest digit with the highest frequency.
3. Identify 'D2', the smallest digit with the second highest frequency.
4. Create a "stable set" containing only M and D2.
5. Iterate through the input grid:
   - If a digit is in the stable set, keep it.
   - Otherwise, replace it with 7.
"""

def _find_m_d2(input_grid: list[list[int]]) -> tuple[int, int | None]:
    """
    Finds M (smallest digit with highest frequency) and 
    D2 (smallest digit with second highest frequency).

    Args:
        input_grid: The 2D list of integers.

    Returns:
        A tuple (m, d2), where m is the most frequent digit (smallest tie-breaker)
        and d2 is the second most frequent digit (smallest tie-breaker).
        Returns (m, None) if there is only one frequency level.
    """
    # Flatten the grid and count digit frequencies
    all_digits = list(itertools.chain.from_iterable(input_grid))
    if not all_digits:
        return (None, None) # Handle empty grid case
        
    counts = collections.Counter(all_digits)
    
    # Group digits by frequency
    grouped_by_freq = collections.defaultdict(list)
    for digit, freq in counts.items():
        grouped_by_freq[freq].append(digit)
        
    # Sort frequencies in descending order
    sorted_freqs = sorted(grouped_by_freq.keys(), reverse=True)
    
    # Determine M (smallest digit with the highest frequency)
    highest_freq = sorted_freqs[0]
    m = min(grouped_by_freq[highest_freq])
    
    # Determine D2 (smallest digit with the second highest frequency)
    d2 = None
    if len(sorted_freqs) > 1:
        second_highest_freq = sorted_freqs[1]
        d2 = min(grouped_by_freq[second_highest_freq])
        
    # Handle edge case where M might be the only digit type
    # If d2 wasn't found because only one frequency level exists,
    # the logic implicitly handles this as d2 remains None.
    # If the problem guarantees at least two frequency levels or digits,
    # this check might be redundant, but it's safer.
        
    return m, d2


def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies the transformation rule based on digit frequencies.

    Args:
        input_grid: A list of lists representing the input grid of digits.

    Returns:
        A list of lists representing the transformed output grid.
    """
    
    # Handle empty input grid
    if not input_grid or not input_grid[0]:
        return []

    rows = len(input_grid)
    cols = len(input_grid[0])
    
    # initialize output_grid with the same dimensions
    output_grid = [[0 for _ in range(cols)] for _ in range(rows)]

    # 1-3. Determine M (most frequent) and D2 (second most frequent) digits
    m, d2 = _find_m_d2(input_grid)
    
    # Handle case where grid might be too small or uniform to find M and D2
    if m is None: 
         # If no digits, return empty or copy? Let's return a grid of 7s of same size.
         # Or maybe copy input? Based on rule, if stable set is empty, all become 7.
         return [[7 for _ in range(cols)] for _ in range(rows)]

    # 4. Create the stable set containing M and D2
    stable_set = set()
    stable_set.add(m)
    if d2 is not None:
        stable_set.add(d2)
        
    replacement_value = 7

    # 5. Perform transformations
    for r in range(rows):
        for c in range(cols):
            digit = input_grid[r][c]
            # If the digit is in the stable set, keep it
            if digit in stable_set:
                output_grid[r][c] = digit
            # Otherwise, replace it with 7
            else:
                output_grid[r][c] = replacement_value

    return output_grid
```
Results for code_00.py:

Train Set Results:

## Example 1:
Input:
```
1 2 5 5 0 3
3 0 2 3 1 3
1 5 3 5 2 1
2 3 5 1 1 5
3 3 0 1 2 0
3 1 5 1 3 1
```
Expected Output:
```
1 7 7 7 7 3
3 7 7 3 1 3
1 7 3 7 7 1
7 3 7 1 1 7
3 3 7 1 7 7
3 1 7 1 3 1
```
Transformed Output:
```
1 7 5 5 7 7
7 7 7 7 1 7
1 5 7 5 7 1
7 7 5 1 1 5
7 7 7 1 7 7
7 1 5 1 7 1
```
Match: False
Pixels Off: 17
Size Correct: True
Color Palette Correct: False
Color Count Correct: False
Score: 188.88888888888889

## Example 2:
Input:
```
0 9 5 9
9 2 5 2
0 2 5 1
1 2 9 2
```
Expected Output:
```
7 9 7 9
9 2 7 2
7 2 7 7
7 2 9 2
```
Transformed Output:
```
7 9 7 9
9 2 7 2
7 2 7 7
7 2 9 2
```
Match: True
Pixels Off: 0
Size Correct: True
Color Palette Correct: True
Color Count Correct: True
Score: 0.0

## Example 3:
Input:
```
9 1 2 1 1 2
1 1 2 6 3 6
6 1 6 6 9 6
6 2 9 6 9 3
1 2 6 2 6 1
1 6 3 3 2 3
```
Expected Output:
```
7 1 7 1 1 7
1 1 7 6 7 6
6 1 6 6 7 6
6 7 7 6 7 7
1 7 6 7 6 1
1 6 7 7 7 7
```
Transformed Output:
```
7 1 7 1 1 7
1 1 7 6 7 6
6 1 6 6 7 6
6 7 7 6 7 7
1 7 6 7 6 1
1 6 7 7 7 7
```
Match: True
Pixels Off: 0
Size Correct: True
Color Palette Correct: True
Color Count Correct: True
Score: 0.0

## Example 4:
Input:
```
1 2 1 0 0 0
0 6 1 0 1 0
0 4 1 0 2 6
4 1 2 1 1 1
```
Expected Output:
```
1 7 1 0 0 0
0 7 1 0 1 0
0 7 1 0 7 7
7 1 7 1 1 1
```
Transformed Output:
```
1 7 1 0 0 0
0 7 1 0 1 0
0 7 1 0 7 7
7 1 7 1 1 1
```
Match: True
Pixels Off: 0
Size Correct: True
Color Palette Correct: True
Color Count Correct: True
Score: 0.0
## General Assessment and Strategy

The initial code, based on keeping the smallest most frequent digit (M) and the smallest second most frequent digit (D2), successfully transformed examples 2, 3, and 4 but failed on example 1. This indicates the core logic of using digit frequency is likely correct, but the specific rule for constructing the "stable set" (digits to keep) was inaccurate.

Analysis of example 1 revealed that the actual stable digits ({1, 3}) were precisely those tied for the highest frequency. In contrast, examples 2, 3, and 4 (where the code worked) either had no tie for the highest frequency (Examples 2 and 3) or the tied digits happened to be M and D2 (Example 4, where 0 and 1 had the same highest frequency, M=0, and the next frequency belonged to digit 2, making D2=2, but the code's stable set {M, D2} = {0, 1} still matched the output).

This suggests a revised rule:
*   If there's a tie for the highest frequency, the stable set includes *all* digits sharing that highest frequency.
*   If there's a unique digit with the highest frequency (M), the stable set includes M and the smallest digit with the second highest frequency (D2).

**Strategy:**
1.  Verify this revised hypothesis by recalculating frequencies and applying the new rule to all examples using `tool_code`.
2.  Update the `Documented Facts` to reflect this conditional rule for the stable set.
3.  Refine the `Natural Language Program` to clearly describe this two-part logic.

## Metrics Gathering

The following metrics were calculated to verify the revised hypothesis.



*code_execution:*
```python
import collections
import itertools

def analyze_grid(grid_id, input_grid):
    all_digits = list(itertools.chain.from_iterable(input_grid))
    if not all_digits:
        print(f"{grid_id}: Empty grid")
        return {}

    counts = collections.Counter(all_digits)
    print(f"{grid_id} Counts: {dict(sorted(counts.items()))}")

    grouped_by_freq = collections.defaultdict(list)
    for digit, freq in counts.items():
        grouped_by_freq[freq].append(digit)

    sorted_freqs = sorted(grouped_by_freq.keys(), reverse=True)

    highest_freq = sorted_freqs[0]
    highest_freq_digits = sorted(grouped_by_freq[highest_freq])
    m = highest_freq_digits[0]
    print(f"{grid_id}: Highest Freq={highest_freq}, Digits H={highest_freq_digits}, M={m}")

    d2 = None
    second_highest_freq = None
    second_highest_freq_digits = []
    if len(sorted_freqs) > 1:
        second_highest_freq = sorted_freqs[1]
        second_highest_freq_digits = sorted(grouped_by_freq[second_highest_freq])
        d2 = second_highest_freq_digits[0]
        print(f"{grid_id}: Second Highest Freq={second_highest_freq}, Digits={second_highest_freq_digits}, D2={d2}")
    else:
        print(f"{grid_id}: Only one frequency level.")

    # Determine Stable Set based on Hypothesis 3
    stable_set = set()
    if len(highest_freq_digits) > 1:
        stable_set = set(highest_freq_digits)
        print(f"{grid_id}: Tie for highest freq. Calculated Stable Set = H = {sorted(list(stable_set))}")
    elif d2 is not None:
        stable_set = {m, d2}
        print(f"{grid_id}: No tie for highest freq. Calculated Stable Set = {{M, D2}} = {sorted(list(stable_set))}")
    else: # Only one frequency level, M exists but D2 does not
        stable_set = {m}
        print(f"{grid_id}: Only one frequency level. Calculated Stable Set = {{M}} = {sorted(list(stable_set))}")

    return {
        "counts": dict(sorted(counts.items())),
        "highest_freq": highest_freq,
        "highest_freq_digits": highest_freq_digits,
        "M": m,
        "second_highest_freq": second_highest_freq,
        "second_highest_freq_digits": second_highest_freq_digits,
        "D2": d2,
        "calculated_stable_set": sorted(list(stable_set))
    }

# Example 1 Data
input_1 = [
    [1, 2, 5, 5, 0, 3], [3, 0, 2, 3, 1, 3], [1, 5, 3, 5, 2, 1],
    [2, 3, 5, 1, 1, 5], [3, 3, 0, 1, 2, 0], [3, 1, 5, 1, 3, 1]
]
output_1 = [
    [1, 7, 7, 7, 7, 3], [3, 7, 7, 3, 1, 3], [1, 7, 3, 7, 7, 1],
    [7, 3, 7, 1, 1, 7], [3, 3, 7, 1, 7, 7], [3, 1, 7, 1, 3, 1]
]
metrics_1 = analyze_grid("Example 1", input_1)
observed_stable_1 = sorted(list(set(d for r in output_1 for d in r if d != 7)))
print(f"Example 1: Observed Stable Set = {observed_stable_1}")
print(f"Example 1: Match = {metrics_1['calculated_stable_set'] == observed_stable_1}")
print("-" * 20)

# Example 2 Data
input_2 = [
    [0, 9, 5, 9], [9, 2, 5, 2], [0, 2, 5, 1], [1, 2, 9, 2]
]
output_2 = [
    [7, 9, 7, 9], [9, 2, 7, 2], [7, 2, 7, 7], [7, 2, 9, 2]
]
metrics_2 = analyze_grid("Example 2", input_2)
observed_stable_2 = sorted(list(set(d for r in output_2 for d in r if d != 7)))
print(f"Example 2: Observed Stable Set = {observed_stable_2}")
print(f"Example 2: Match = {metrics_2['calculated_stable_set'] == observed_stable_2}")
print("-" * 20)

# Example 3 Data
input_3 = [
    [9, 1, 2, 1, 1, 2], [1, 1, 2, 6, 3, 6], [6, 1, 6, 6, 9, 6],
    [6, 2, 9, 6, 9, 3], [1, 2, 6, 2, 6, 1], [1, 6, 3, 3, 2, 3]
]
output_3 = [
    [7, 1, 7, 1, 1, 7], [1, 1, 7, 6, 7, 6], [6, 1, 6, 6, 7, 6],
    [6, 7, 7, 6, 7, 7], [1, 7, 6, 7, 6, 1], [1, 6, 7, 7, 7, 7]
]
metrics_3 = analyze_grid("Example 3", input_3)
observed_stable_3 = sorted(list(set(d for r in output_3 for d in r if d != 7)))
print(f"Example 3: Observed Stable Set = {observed_stable_3}")
print(f"Example 3: Match = {metrics_3['calculated_stable_set'] == observed_stable_3}")
print("-" * 20)

# Example 4 Data
input_4 = [
    [1, 2, 1, 0, 0, 0], [0, 6, 1, 0, 1, 0], [0, 4, 1, 0, 2, 6],
    [4, 1, 2, 1, 1, 1]
]
output_4 = [
    [1, 7, 1, 0, 0, 0], [0, 7, 1, 0, 1, 0], [0, 7, 1, 0, 7, 7],
    [7, 1, 7, 1, 1, 1]
]
metrics_4 = analyze_grid("Example 4", input_4)
observed_stable_4 = sorted(list(set(d for r in output_4 for d in r if d != 7)))
print(f"Example 4: Observed Stable Set = {observed_stable_4}")
print(f"Example 4: Match = {metrics_4['calculated_stable_set'] == observed_stable_4}")
print("-" * 20)
```

*code_execution_result:*
outcome: OUTCOME_OK
```
Example 1 Counts: {0: 4, 1: 10, 2: 5, 3: 10, 5: 7}
Example 1: Highest Freq=10, Digits H=[1, 3], M=1
Example 1: Second Highest Freq=7, Digits=[5], D2=5
Example 1: Tie for highest freq. Calculated Stable Set = H = [1, 3]
Example 1: Observed Stable Set = [1, 3]
Example 1: Match = True
--------------------
Example 2 Counts: {0: 2, 1: 2, 2: 5, 5: 3, 9: 4}
Example 2: Highest Freq=5, Digits H=[2], M=2
Example 2: Second Highest Freq=4, Digits=[9], D2=9
Example 2: No tie for highest freq. Calculated Stable Set = {M, D2} = [2, 9]
Example 2: Observed Stable Set = [2, 9]
Example 2: Match = True
--------------------
Example 3 Counts: {1: 9, 2: 7, 3: 5, 6: 11, 9: 4}
Example 3: Highest Freq=11, Digits H=[6], M=6
Example 3: Second Highest Freq=9, Digits=[1], D2=1
Example 3: No tie for highest freq. Calculated Stable Set = {M, D2} = [1, 6]
Example 3: Observed Stable Set = [1, 6]
Example 3: Match = True
--------------------
Example 4 Counts: {0: 8, 1: 9, 2: 3, 4: 2, 6: 2}
Example 4: Highest Freq=9, Digits H=[1], M=1
Example 4: Second Highest Freq=8, Digits=[0], D2=0
Example 4: No tie for highest freq. Calculated Stable Set = {M, D2} = [0, 1]
Example 4: Observed Stable Set = [0, 1]
Example 4: Match = True
--------------------

```
## Documented Facts


```yaml
task_elements:
  - name: input_grid
    type: 2D array of integers (0-9)
  - name: output_grid
    type: 2D array of integers (0-9)
    description: Same dimensions as input_grid.
  - name: transformation_rule
    type: conditional replacement
    description: Replaces certain digits based on global grid frequency statistics.
  - name: stable_set
    type: set of integers
    description: Digits that remain unchanged during transformation. Determined by frequency analysis and tie-breaking rules.
  - name: replacement_value
    type: integer
    value: 7
    description: The constant digit used to replace non-stable digits.

frequency_analysis:
  - name: digit_counts
    type: map (digit -> count)
    description: Frequency of each digit (0-9) in the input_grid.
  - name: grouped_by_frequency
    type: map (frequency -> list_of_digits)
    description: Digits grouped by their frequency count.
  - name: highest_frequency
    type: integer
    description: The maximum frequency found among all digits.
  - name: highest_frequency_digits
    type: list of integers
    description: Sorted list of all digits that occur with the highest_frequency.
  - name: M
    type: integer
    description: The smallest digit among highest_frequency_digits. (min(highest_frequency_digits)).
  - name: second_highest_frequency
    type: integer or None
    description: The second highest frequency count found. None if only one frequency level exists.
  - name: second_highest_frequency_digits
    type: list of integers or None
    description: Sorted list of digits occurring with the second_highest_frequency. None if fewer than two frequency levels exist.
  - name: D2
    type: integer or None
    description: The smallest digit among second_highest_frequency_digits. (min(second_highest_frequency_digits)). None if fewer than two frequency levels exist.

stable_set_determination:
  - step: Calculate digit_counts for the input_grid.
  - step: Determine highest_frequency and highest_frequency_digits.
  - step: Check if len(highest_frequency_digits) > 1 (tie for highest frequency).
  - step: >
      If tie exists: stable_set = set(highest_frequency_digits).
  - step: >
      If no tie exists:
        - Identify M (min(highest_frequency_digits)).
        - Determine second_highest_frequency and D2 (min digit with that frequency).
        - If D2 exists: stable_set = {M, D2}.
        - If D2 does not exist (only one frequency level): stable_set = {M}.

grid_transformation:
  - input: input_grid cell value (digit)
  - condition: digit IS IN stable_set
  - output: digit (no change)
  - condition: digit IS NOT IN stable_set
  - output: replacement_value (7)
```


## Natural Language Program

1.  **Analyze Frequencies:** Scan the entire input grid and count the occurrences of each digit (0 through 9).
2.  **Identify Highest Frequency Digits:** Determine the highest frequency achieved by any digit. Create a list, `H`, containing all digits that occur with this highest frequency.
3.  **Check for Ties:** Examine the list `H`.
    *   **Case 1: Tie for Highest Frequency** (List `H` contains more than one digit): Define the "stable set" `S` as the set containing all digits in `H`.
    *   **Case 2: No Tie for Highest Frequency** (List `H` contains only one digit, `M`):
        *   Find the second highest frequency present in the grid.
        *   Identify `D2`, the *smallest* digit that occurs with this second highest frequency.
        *   Define the "stable set" `S` as the set containing `M` and `D2`. (If there is no second highest frequency, meaning all digits present have the same frequency, the stable set `S` contains only `M`).
4.  **Transform Grid:** Create the output grid with the same dimensions as the input grid. Iterate through each cell of the input grid:
    *   If the digit in the input cell is present in the stable set `S`, copy that digit to the corresponding cell in the output grid.
    *   If the digit in the input cell is *not* present in the stable set `S`, place the digit `7` in the corresponding cell in the output grid.
5.  **Output:** Return the completed output grid.
