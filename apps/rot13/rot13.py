#shift letters by 13 chars. Loop after z. preserve !, ? blank spaces


def rot13(text):
	result=''
	escaped={'!':'!', '?':'?', ' ':' ', '"':"&quot;","<":"&lt;","&":"&amp",">":"&gt;" }
	for char in text:
		if char in escaped:
			result=result+escaped[char]
		else:
			if (ord(char)>96 and ord(char)<123):
				rot_lower=(ord(char)+13)%123
				if rot_lower<97:
					rot_lower=rot_lower+97
				result=result+chr(rot_lower)
				continue

			if (ord(char)>64 and ord(char)<91):
				rot_upper=(ord(char)+13)%91
				if rot_upper<65:
					rot_upper=rot_upper+65
				result=result+chr(rot_upper)
				continue
			result=result+char
	return result


import webapp2
#from libs.escaping_chars import escape_chars





form = """
<form method="post">
  Cypher your text below
  <br>
  
	  <textarea name="text" rows="10" cols="50" >
%(output)s</textarea>
  
  <br>

  <input type="submit" value="Cypher">
</form>
"""

class Rot13Handler(webapp2.RequestHandler):

	def get(self):  
		
		self.write_form()

	def post(self):
		text_entry = self.request.get("text")
		output=rot13(text_entry)
		
		self.write_form(output)

	def write_form(self,output=''):
		self.response.out.write(form % {"output":output})
  

      


