import os
import re
string=""
with open('answer.dot') as fp:
    for line in fp:
    	# if re.search(r'empty',line) is not None:
    	# 	line.replace("empty"," ")
    	line=re.sub(r'empty'," ",line)
    	if re.search(r'{\s+}',line) is  None:
    		print line
    	str=line.split()
    	for val in str:
    		# regex=r"*_[0-9]+"
    		if re.search("_[0-9]",val) is not None:
    			val1=val.split("_")
    			string+= val + " [label =" + "\""+val1[0] +"\""+ "];\n"
    string +=" }"
    print string
