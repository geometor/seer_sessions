
## example 1
*input:*
```
9 0 0
9 9 9
9 9 9
```
*expected output:*
```
0 9 9
0 9 9
9 9 9
```
*transformed output:*
```
9 9 9
9 0 0
9 9 9
```
size: True
palette: True
color count: True
pixels off: 4
**FAILED!**

## example 2
*input:*
```
6 6 6
0 0 0
6 6 0
```
*expected output:*
```
6 0 0
6 0 6
6 0 6
```
*transformed output:*
```
6 6 0
6 6 6
0 0 0
```
size: True
palette: True
color count: True
pixels off: 4
**FAILED!**

## example 3
*input:*
```
0 0 9
0 0 9
9 9 9
```
*expected output:*
```
9 9 9
0 0 9
0 0 9
```
*transformed output:*
```
9 9 9
0 0 9
0 0 9
```
size: True
palette: True
color count: True
pixels off: 0
PASSED

## example 4
*input:*
```
2 0 2
0 0 2
0 2 2
```
*expected output:*
```
2 2 2
0 0 2
2 0 0
```
*transformed output:*
```
0 2 2
2 0 2
0 0 2
```
size: True
palette: True
color count: True
pixels off: 4
**FAILED!**
