
## example 1
*input:*
```
3 3 0
3 2 0
0 0 0
```
*expected output:*
```
3 3 3 3 0 0 0 0 0
3 3 3 3 0 0 0 0 0
3 3 3 3 0 0 0 0 0
3 3 3 3 0 0 0 0 0
0 0 0 0 3 3 3 3 0
0 0 0 0 3 3 3 3 0
0 0 0 0 3 3 3 3 0
0 0 0 0 3 3 3 3 0
0 0 0 0 0 0 0 0 0
```
*transformed output:*
```
3 3 0 0 0 0 0
3 2 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 3 3
0 0 0 0 0 3 0
```
size: False
palette: False
color count: False
pixels off: None
**FAILED!**

## example 2
*input:*
```
0 0 0
0 2 3
0 3 3
```
*expected output:*
```
0 0 0 0 0 0 0 0 0
0 3 3 3 3 0 0 0 0
0 3 3 3 3 0 0 0 0
0 3 3 3 3 0 0 0 0
0 3 3 3 3 0 0 0 0
0 0 0 0 0 3 3 3 3
0 0 0 0 0 3 3 3 3
0 0 0 0 0 3 3 3 3
0 0 0 0 0 3 3 3 3
```
*transformed output:*
```
0 0 0 0 0 0 0
0 2 3 0 0 0 0
0 3 3 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 3
0 0 0 0 0 3 3
```
size: False
palette: False
color count: False
pixels off: None
**FAILED!**
