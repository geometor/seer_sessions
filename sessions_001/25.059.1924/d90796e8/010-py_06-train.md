
## example 1
*input:*
```
3 2 0
0 0 0
0 5 0
```
*expected output:*
```
8 0 0
0 0 0
0 5 0
```
*transformed output:*
```
8 0 0
0 0 0
0 5 0
```
size: True
palette: True
color count: True
pixels off: 0
PASSED

## example 2
*input:*
```
5 0 0 0 0 0
0 0 3 2 0 0
0 0 0 0 0 0
0 3 0 0 0 2
0 2 0 0 0 0
5 0 0 3 0 0
0 0 0 0 0 0
```
*expected output:*
```
5 0 0 0 0 0
0 0 8 0 0 0
0 0 0 0 0 0
0 8 0 0 0 2
0 0 0 0 0 0
5 0 0 3 0 0
0 0 0 0 0 0
```
*transformed output:*
```
5 0 0 0 0 0
0 0 8 0 0 0
0 0 0 0 0 0
0 8 0 0 0 0
0 0 0 0 0 0
5 0 0 8 0 0
0 0 0 0 0 0
```
size: True
palette: True
color count: False
pixels off: 2
**FAILED!**

## example 3
*input:*
```
0 0 0 0 0 2 0
3 0 0 0 0 0 3
5 0 2 3 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 2 0
3 2 0 0 0 3 0
0 0 0 5 0 0 0
```
*expected output:*
```
0 0 0 0 0 2 0
3 0 0 0 0 0 3
5 0 0 8 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
8 0 0 0 0 8 0
0 0 0 5 0 0 0
```
*transformed output:*
```
0 0 0 0 0 0 0
8 0 0 0 0 0 8
5 0 0 8 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
8 0 0 0 0 8 0
0 0 0 5 0 0 0
```
size: True
palette: True
color count: False
pixels off: 3
**FAILED!**
