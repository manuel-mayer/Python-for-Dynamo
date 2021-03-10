import clr
import System.IO.FileInfo
files = IN
mbytes = []
for file in files:
	size = file.Length
		
mbytes_raw = float(size)/1048576
mbytes = round(mbytes_raw,1)

OUT = mbytes
