import os
import re
string=""
first=1
with open('answer.dot') as fp:
    for line in fp:
    	# if re.search(r'empty',line) is not None:
    	# 	line.replace("empty"," ")
    	line=re.sub(r'empty'," ",line)
    	if re.search(r'{\s+}',line) is  None:
    	    print line
            if first==0:
                line1=line
                line2=line1.split("{")
                line4=""
                for val3 in line2:
                    if re.search(r'}',val3) is not None:
                        
                        line3=val3.split("}")
                        line5=line3[0].split(" ")
                        if len(line5) > 3:
                            line4="{rank=same ; "
                            for val1 in line5:
                                line4+=val1
                                line4+=" "
                            line4+="; rankdir=LR}\n"
                
                print line4            
    	str=line.split()
        first=0
    	for val in str:
    		# regex=r"*_[0-9]+"
    		if re.search("_[0-9]",val) is not None:
    			val1=val.split("_")
    			string+= val + " [label =" + "\""+val1[0] +"\""+ "];\n"
    string +=" }"
    print string
    			