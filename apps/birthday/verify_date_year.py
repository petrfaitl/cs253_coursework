# -----------
# User Instructions
# 
# Modify the valid_year() function to verify 
# whether the string a user enters is a valid 
# year. If the passed in parameter 'year' 
# is not a valid year, return None. 
# If 'year' is a valid year, then return 
# the year as a number. Assume a year 
# is valid if it is a number between 1900 and 
# 2020.
#

def valid_year(year):
	if year and year.isdigit():
		if int(year) >1900 and int(year)<2030:
			return year
	else:
		None


#print valid_year('20300')
# => None    
# valid_year('-11') => None
# valid_year('1950') => 1950
# valid_year('2000') => 2000
