
## example 1
*input:*
```
1 1 1
1 0 1
1 1 1
```
*expected output:*
```
0 1 0
1 0 1
0 1 0
```
*transformed output:*
```
0 1 0
1 0 1
0 1 0
```
size: True
palette: True
color count: True
pixels off: 0
PASSED

## example 2
*input:*
```
2 2 2 2 2
2 2 2 2 2
2 2 0 2 2
2 2 2 2 2
2 2 2 2 2
```
*expected output:*
```
0 2 2 2 0
2 0 2 0 2
2 2 0 2 2
2 0 2 0 2
0 2 2 2 0
```
*transformed output:*
```
0 2 2 2 0
2 2 2 2 2
2 2 0 2 2
2 2 2 2 2
0 2 2 2 0
```
size: True
palette: True
color count: False
pixels off: 4
**FAILED!**

## example 3
*input:*
```
3 3 3 3 3 3 3
3 3 3 3 3 3 3
3 3 3 3 3 3 3
3 3 3 0 3 3 3
3 3 3 3 3 3 3
3 3 3 3 3 3 3
3 3 3 3 3 3 3
```
*expected output:*
```
0 3 3 3 3 3 0
3 0 3 3 3 0 3
3 3 0 3 0 3 3
3 3 3 0 3 3 3
3 3 0 3 0 3 3
3 0 3 3 3 0 3
0 3 3 3 3 3 0
```
*transformed output:*
```
0 3 3 3 3 3 0
3 3 3 3 3 3 3
3 3 3 3 3 3 3
3 3 3 0 3 3 3
3 3 3 3 3 3 3
3 3 3 3 3 3 3
0 3 3 3 3 3 0
```
size: True
palette: True
color count: False
pixels off: 8
**FAILED!**
