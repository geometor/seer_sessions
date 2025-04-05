Okay, let's analyze the provided examples to understand the transformation task.

**Perception of Elements:**

1.  **Input/Output Format:** Both input and output are sequences of single digits, presented as space-separated strings. They can be interpreted as lists or arrays of integers.
2.  **Key Digit '2':** The digit '2' appears to play a special role. It acts as a boundary or a reference point for the transformation.
3.  **Key Digit '0':** The digit '0' represents empty or fillable space.
4.  **Other Digits (X):** Digits other than '0' and '2' (e.g., 3, 7, 6, 4, 8) seem to be "source" values that can propagate.
5.  **Transformation:** The core transformation involves filling sequences of '0's that are located *between* a non-zero digit `X` (where `X` is not '2') and the digit '2'. The '0's are replaced by the digit `X`.
6.  **Directionality:** The filling action propagates *towards* the '2'.
    *   If the sequence is `... X ... 0 0 0 ... 2 ...`, the '0's are filled with `X` moving rightwards towards '2'. (See train_3, train_6, train_7)
    *   If the sequence is `... 2 ... 0 0 0 ... X ...`, the '0's are filled with `X` moving leftwards towards '2'. (See train_2, train_5)
7.  **No Change Cases:** If there are no zeros between a non-zero digit `X` and the '2', or if the region next to '2' only contains zeros extending to the sequence boundary, no change occurs in that direction. (See train_1, train_4)
8.  **Implicit Assumption:** Based on the examples, there appears to be at most one '2' in any given sequence.

**Facts (YAML):**


```yaml
objects:
  - sequence: a list of single-digit integers.
  - boundary_marker: the integer 2.
  - fillable_space: the integer 0.
  - source_digit: any integer X where X is not 0 and X is not 2.

properties:
  - sequence: has indices and elements.
  - boundary_marker: has a specific index within the sequence.
  - fillable_space: can be replaced by a source_digit.
  - source_digit: determines the value used for filling.

actions:
  - find_boundary: locate the index of the boundary_marker (2).
  - scan_left: search elements to the left of the boundary_marker.
  - scan_right: search elements to the right of the boundary_marker.
  - identify_fill_region: detect consecutive fillable_spaces (0s) adjacent to the boundary_marker.
  - identify_source: find the first source_digit encountered when scanning away from the boundary_marker past a fill_region.
  - fill_region: replace the fillable_spaces (0s) in the identified region with the identified source_digit.

relationships:
  - fillable_space (0) occurs between a source_digit (X) and the boundary_marker (2).
  - filling happens *towards* the boundary_marker (2).
  - source_digit (X) must be the first non-zero digit encountered when moving away from the boundary_marker (2) across a block of zeros.
```


**Natural Language Program:**

1.  Read the input sequence of digits.
2.  Find the index of the digit '2'. If '2' is not present in the sequence, return the original sequence unchanged. Let the index of '2' be `idx_2`.
3.  Create a modifiable copy of the sequence.
4.  **Fill Left:**
    a.  Scan the sequence copy backwards from index `idx_2 - 1` down to index 0.
    b.  Find the first digit `X_left` that is not '0' and not '2'.
    c.  If such a digit `X_left` is found at index `idx_left`:
        i.  Check if all elements between `idx_left + 1` and `idx_2 - 1` (inclusive) are '0'.
        ii. If they are all '0', replace all elements in the sequence copy from `idx_left + 1` to `idx_2 - 1` with `X_left`.
5.  **Fill Right:**
    a.  Scan the sequence copy forwards from index `idx_2 + 1` up to the end of the sequence.
    b.  Find the first digit `X_right` that is not '0' and not '2'.
    c.  If such a digit `X_right` is found at index `idx_right`:
        i.  Check if all elements between `idx_2 + 1` and `idx_right - 1` (inclusive) are '0'.
        ii. If they are all '0', replace all elements in the sequence copy from `idx_2 + 1` to `idx_right - 1` with `X_right`.
6.  Return the modified sequence.