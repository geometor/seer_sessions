
## example 1
*input:*
```
0 0 0 0 0
0 2 0 0 0
0 0 0 0 0
```
*expected output:*
```
3 0 6 0 0
0 0 0 0 0
8 0 7 0 0
```
*transformed output:*
```
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
```
size: True
palette: True
color count: False
pixels off: 4
**FAILED!**

## example 2
*input:*
```
0 0 0 0 0
0 0 0 0 0
0 0 0 0 2
```
*expected output:*
```
0 0 0 0 0
0 0 0 3 0
0 0 0 0 0
```
*transformed output:*
```
0 0 0 0 0
0 0 0 3 0
0 0 0 0 0
```
size: True
palette: True
color count: True
pixels off: 0
PASSED

## example 3
*input:*
```
0 0 2 0 0
0 0 0 0 0
0 0 0 0 0
```
*expected output:*
```
0 0 0 0 0
0 8 0 7 0
0 0 0 0 0
```
*transformed output:*
```
0 0 0 0 0
0 8 0 7 0
0 0 0 0 0
```
size: True
palette: True
color count: True
pixels off: 0
PASSED

## example 4
*input:*
```
0 0 0 0 0
0 0 0 2 0
0 0 0 0 0
```
*expected output:*
```
0 0 3 0 6
0 0 0 0 0
0 0 8 0 7
```
*transformed output:*
```
0 0 3 0 6
0 0 0 0 0
0 0 8 0 7
```
size: True
palette: True
color count: True
pixels off: 0
PASSED
