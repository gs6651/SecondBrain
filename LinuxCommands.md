
`grep <keyword> <file_name.txt>`

`cat <file_name.txt> | grep <keyword>`

##### To find all files with .txt extension in the same directory containing <keyword>
`grep <keyword> *.txt`
`grep <keyword> *.txt` -vc
`grep -x <div> *.txt`
`grep -w <iv> *.txt`

* -v		# Prints all lines that do NOT match pattern.
* -n		# Prints the matched line and its line number.
* -l		# Prints only the names of files with matching lines
* -c		# Prints only the count of matching lines.
* -i		# Makes grep searches case insensitive
* -x		# Searches the "string" in that file
* -w		# Searches only the "string" in that file
* -e		# Excludes the flag




### The sort Command
* -n		# Sorts numerically. (Ignores blanks and tabs.)
* -r		# Reverses the order of sort.
* -f		# Sorts upper and lowercase together.
* +x		# Ignores first x fields when sorting.

> Below example will sort the files based on its size, modified in Aug month
> +4 is ignoring first 4 fileds here
```
$ls -l | grep "Aug" | sort +4n
-rw-rw-r--  1 carol doc      1605 Aug 23 07:35 macros
-rw-rw-r--  1 john  doc      2488 Aug 15 10:51 intro
-rw-rw-rw-  1 john  doc      8515 Aug  6 15:30 ch07
-rw-rw-rw-  1 john  doc     11008 Aug  6 14:10 ch02
$
```
