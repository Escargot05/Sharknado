import re

def determineAge(age):
    if str(age).find("months") != -1:
        return "infant"
    
    value = re.search(r"\d+", str(age))
    if value == None:
        return "unknown"

    value = int(value.group())

    if value < 2:
        return "infant"
    elif  value < 12:
        return "child"
    elif  value < 18:
        return "adolescent"
    elif  value < 24:
        return "young adult"
    elif  value < 64:
        return "middle aged"
    else :
        return "aged"
    
def determineSex(sex):
    if sex.find("M") != -1:
        return "male"
    elif sex.find("F") != -1:
        return "female"
    else:
        return "unknown"
