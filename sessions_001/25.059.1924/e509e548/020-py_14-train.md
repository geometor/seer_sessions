
## example 1
*input:*
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 3 3 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 3 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 3 0 0
0 0 0 3 0 0 3 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 3 3 3 3 0 0 0 0 0 3 3 3 0 0 0 0 0 0
0 0 0 3 0 0 0 0 0 0 0 0 3 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 3 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 3 3 3 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 3 3 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 3 0 0 0 0 0 0 0 0 0 0 0 0 0 0 3 3 0 0 0
0 3 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 3 0 0 0
0 3 0 0 0 0 0 0 0 0 0 0 0 0 0 0 3 3 0 0 0
3 3 3 3 0 0 3 3 3 3 3 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 3 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 3 0 0 0 0 0 0 0 0 3 3 3 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 3 0 3 0 0 0
0 0 3 0 0 0 0 0 0 0 0 0 0 0 0 3 0 3 0 0 0
0 3 3 0 0 0 0 0 0 0 0 0 0 0 0 0 0 3 0 0 0
```
*expected output:*
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 1 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0
0 0 0 2 0 0 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 2 2 2 2 0 0 0 0 0 6 6 6 0 0 0 0 0 0
0 0 0 2 0 0 0 0 0 0 0 0 6 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 6 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 6 6 6 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 6 6 0 0 0
0 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 6 0 0 0
0 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 6 6 0 0 0
2 2 2 2 0 0 1 1 1 1 1 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 6 6 6 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 6 0 6 0 0 0
0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 6 0 6 0 0 0
0 1 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 6 0 0 0
```
*transformed output:*
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 1 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0
0 0 0 6 0 0 6 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 6 6 6 6 0 0 0 0 0 1 1 1 0 0 0 0 0 0
0 0 0 6 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 1 1 1 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 6 6 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 2 2 0 0 0
0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 2 0 0 0
0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 2 2 0 0 0
1 1 1 1 0 0 1 1 1 1 2 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 2 2 2 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 2 0 2 0 0 0
0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 2 0 2 0 0 0
0 1 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 2 0 0 0
```
size: True
palette: True
color count: False
pixels off: 38
**FAILED!**

## example 2
*input:*
```
3 3 3 0 0 0 0 0 0 0 0
0 0 3 0 0 0 3 3 3 3 0
0 0 3 0 0 0 3 0 0 3 0
0 0 0 0 0 0 3 0 0 3 0
0 0 0 0 0 0 3 0 0 3 0
0 0 0 0 0 0 0 0 0 0 0
3 3 3 3 3 0 0 0 0 0 0
0 0 3 0 0 0 0 0 0 0 0
0 0 3 0 0 0 0 0 0 0 0
0 0 3 3 3 0 0 0 0 0 0
```
*expected output:*
```
1 1 1 0 0 0 0 0 0 0 0
0 0 1 0 0 0 6 6 6 6 0
0 0 1 0 0 0 6 0 0 6 0
0 0 0 0 0 0 6 0 0 6 0
0 0 0 0 0 0 6 0 0 6 0
0 0 0 0 0 0 0 0 0 0 0
2 2 2 2 2 0 0 0 0 0 0
0 0 2 0 0 0 0 0 0 0 0
0 0 2 0 0 0 0 0 0 0 0
0 0 2 2 2 0 0 0 0 0 0
```
*transformed output:*
```
6 6 6 0 0 0 0 0 0 0 0
0 0 6 0 0 0 1 1 1 1 0
0 0 6 0 0 0 1 0 0 1 0
0 0 0 0 0 0 1 0 0 1 0
0 0 0 0 0 0 1 0 0 1 0
0 0 0 0 0 0 0 0 0 0 0
1 1 1 1 1 0 0 0 0 0 0
0 0 1 0 0 0 0 0 0 0 0
0 0 1 0 0 0 0 0 0 0 0
0 0 1 1 1 0 0 0 0 0 0
```
size: True
palette: True
color count: False
pixels off: 25
**FAILED!**

## example 3
*input:*
```
0 0 0 0 0 0 0 0 0 0 0 0
0 3 0 0 0 0 0 0 0 3 0 0
0 3 0 0 0 0 0 0 0 3 3 3
0 3 0 0 0 3 0 0 0 0 0 0
0 3 3 3 3 3 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 3 0 0 0 0
0 0 0 0 0 3 3 3 0 0 0 0
0 0 0 0 0 3 0 3 0 0 0 0
0 0 0 0 0 3 0 3 0 0 0 0
3 3 3 0 0 0 0 0 0 0 0 0
0 0 3 0 0 0 0 0 0 3 0 3
0 0 0 0 0 0 0 0 0 3 3 3
```
*expected output:*
```
0 0 0 0 0 0 0 0 0 0 0 0
0 6 0 0 0 0 0 0 0 1 0 0
0 6 0 0 0 0 0 0 0 1 1 1
0 6 0 0 0 6 0 0 0 0 0 0
0 6 6 6 6 6 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 2 0 0 0 0
0 0 0 0 0 2 2 2 0 0 0 0
0 0 0 0 0 2 0 2 0 0 0 0
0 0 0 0 0 2 0 2 0 0 0 0
1 1 1 0 0 0 0 0 0 0 0 0
0 0 1 0 0 0 0 0 0 6 0 6
0 0 0 0 0 0 0 0 0 6 6 6
```
*transformed output:*
```
0 0 0 0 0 0 0 0 0 0 0 0
0 6 0 0 0 0 0 0 0 1 0 0
0 6 0 0 0 0 0 0 0 1 1 1
0 6 0 0 0 6 0 0 0 0 0 0
0 6 6 6 6 6 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 2 0 0 0 0
0 0 0 0 0 1 2 2 0 0 0 0
0 0 0 0 0 1 0 2 0 0 0 0
0 0 0 0 0 1 0 2 0 0 0 0
1 1 1 0 0 0 0 0 0 0 0 0
0 0 1 0 0 0 0 0 0 2 0 2
0 0 0 0 0 0 0 0 0 2 2 2
```
size: True
palette: True
color count: False
pixels off: 8
**FAILED!**
