# User Instructions
# 
# Implement the function escape_html(s), which replaces:
# > with &gt;
# < with &lt;
# " with &quot;
# & with &amp;
# and returns the escaped string
# Note that your browser will probably automatically 
# render your escaped text as the corresponding symbols, 
# but the grading script will still correctly evaluate it.
# 

def escape_html(s):
	result=''
	repl={">":"&gt;","<":"&lt;",'"':"&quot;", "&":"&amp;"}
	for i in s:
		if i not in repl:
			result=result+i
		else:
			result= result+repl[i]
	return result



#print escape_html('"hello, &=&amp;"')


import cgi
def escape_chars(s):
	return cgi.escape(s, quote = True)


#print escape_chars('"hello, &=&amp;"')
