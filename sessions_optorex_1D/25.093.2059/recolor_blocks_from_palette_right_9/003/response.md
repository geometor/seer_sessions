Warning: Response generation stopped. Finish Reason: MAX_TOKENS (2)
Partial text available:
---
```python
import sys
# Add the directory containing helper modules to the Python path
# sys.path.append('/path/to/helper/modules') # Adjust this path as needed

# Assuming helper functions are defined in a module named 'grid_utils' or similar
# If they are simple enough, they can be defined directly within this file.

"""
Transforms a sequence of integers based on the following rules:
1. Identifies all maximal consecutive segments of the digit '5' in the input sequence.
2. Finds the index of the first occurrence of the digit '5'. If '5' is not present, the input is returned unchanged.
3. Extracts all non-zero digits that appear in the input sequence *before* the index of the first '5'. These form an ordered list of 'replacement candidates'.
4. Iterates through the identified segments of '5's (S_1, S_2, ..., S_N) and the replacement candidates (C_1, C_2, ..., C_M).
5. For the k-th segment of '5's (S_k):
   a. If a corresponding k-th replacement candidate (C_k) exists (i.e., k <= M) AND C_k is not equal to 5:
      Replace all digits within segment S_k with the value C_k.
   b. Otherwise (if k > M, or if C_k is equal to 5), leave the segment S_k unchanged.
6. Returns the modified sequence.
"""

def find_segments(data, value):
    """
    Finds the start and end indices of consecutive segments of a specific value.

    Args:
        data (list): The list of items to search within.
        value: The value whose consecutive segments are sought.

    Returns:
        list: A list of tuples, where each tuple is (start_index, end_index)
              for a segment. Returns an empty list if no segments are found.
    """
    segments = []
    in_segment = False
    start_index = -1
    n = len(data)
    for i, item in enumerate(data):
        is_target = (item == value)

        # Start of a new segment
---
