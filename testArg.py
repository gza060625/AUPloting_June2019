import sys
import datetime

def checkArguments(num=4):
    
    def strAndFill(num):
        num=str(num)
        num=num.zfill(2)
        return num
    
    length=len(sys.argv)
    if length>=num:
        return sys.argv[1:4]
    if length==1:
        date=datetime.datetime.utcnow()
        date=[date.year, date.month, date.day]
        date=list(map(strAndFill,date))
        
        return date    
    return False
    

r=checkArguments()
print(r)