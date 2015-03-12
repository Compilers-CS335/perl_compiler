import re
string=""
with open('test.txt') as fp:
    for line in fp:
    	str=line.split()
    	for val in str:
    		# regex=r"*_[0-9]+"
    		if re.search("_",val) is not None:
    			val1=val.split("_")
    			string+= val + " [label " + val1[0] + "]\n"
    print string
    			