
## example 1
*input:*
```
2 0 0
0 2 0
0 0 2
```
*expected output:*
```
2 0 0
0 4 0
0 0 2
```
*transformed output:*
```
2 0 0
0 4 0
0 0 2
```
size: True
palette: True
color count: True
pixels off: 0
PASSED

## example 2
*input:*
```
0 0 9 0 0 0 0 0
0 0 0 9 0 0 0 0
0 0 0 0 9 0 0 0
0 0 0 0 0 9 0 0
9 0 0 0 0 0 9 0
0 9 0 0 0 0 0 9
0 0 9 0 0 0 0 0
0 0 0 9 0 0 0 0
```
*expected output:*
```
0 0 9 0 0 0 0 0
0 0 0 4 0 0 0 0
0 0 0 0 9 0 0 0
0 0 0 0 0 4 0 0
9 0 0 0 0 0 9 0
0 4 0 0 0 0 0 4
0 0 9 0 0 0 0 0
0 0 0 4 0 0 0 0
```
*transformed output:*
```
0 0 9 0 0 0 0 0
0 0 0 4 0 0 0 0
0 0 0 0 9 0 0 0
0 0 0 0 0 4 0 0
4 0 0 0 0 0 9 0
0 4 0 0 0 0 0 4
0 0 4 0 0 0 0 0
0 0 0 4 0 0 0 0
```
size: True
palette: True
color count: False
pixels off: 2
**FAILED!**

## example 3
*input:*
```
0 0 3 0 0 0
0 0 0 3 0 0
0 0 0 0 3 0
3 0 0 0 0 3
0 3 0 0 0 0
0 0 3 0 0 0
```
*expected output:*
```
0 0 3 0 0 0
0 0 0 4 0 0
0 0 0 0 3 0
3 0 0 0 0 4
0 4 0 0 0 0
0 0 3 0 0 0
```
*transformed output:*
```
0 0 3 0 0 0
0 0 0 4 0 0
0 0 0 0 3 0
3 0 0 0 0 4
0 4 0 0 0 0
0 0 3 0 0 0
```
size: True
palette: True
color count: True
pixels off: 0
PASSED
