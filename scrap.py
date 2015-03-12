from time import sleep
import time
import curl
import re
import mail

course = "ECE419"
year = "2015"
term = 1 # Comment this line if the course is a fall one
term = 9 # Comment this line if the course is a winter one
from = "a@a.com"
password = "123456"
to = "b@utoronto.ca"


Lec = True
Pra = False 
Tut = False

while True:
	content = curl.Curl("http://coursefinder.utoronto.ca/course-search/search/courseInquiry?methodToCall=start&viewId=CourseDetails-InquiryView&courseId="+course+"H1S"+str(year)+str(term)).get()
	lines = content.split("\r\n")
	i = lines.index('<table id="u172" class="uif-tableCollectionLayout">')
	lines = lines[i:]
	i = lines.index('</table>')
	lines = lines[0:i]
	i = lines.index('<tbody>')
	lines = lines[i:]
	i = lines.index('</tbody>')
	lines = lines[0:i]

	l, temp = [], []
	Line = False

	for i,x in enumerate(lines):
		if Line == False and x.find("line"+str(len(l))) > 0:
			Line = True
		elif x.find("line"+str(len(l)+1)) > 0:
			Line = False
			l.append(temp)
			temp = []
		if Line == True:
			temp.append(x)

	for i,x in enumerate(l):
		temp = []
		for y in ''.join(x).split('</td>'):
			if len(temp) < 6:
				temp.append(re.search(r'<span id="u\d+_line\d+">(.*?)<\/span>', y).group(1))
			else:
				break
		l[i] = temp
	vagas = False
	print "("+time.strftime('%X %x %Z')+"): "
	for x in l:
		if x[4] > x[5]:
			if (x[0].find("Lec") == 0 and Lec) or (x[0].find("Pra") == 0 and Pra) or (x[0].find("Tut") == 0 and Tut):
				print "   [Course "+course+"] "+x[0]+" has "+str(int(x[4])-int(x[5]))+" spot"+("s" if int(x[4])-int(x[5]) > 1 else "")+"!!!"
				vagas = True	
	if vagas == False:	
		print("   No spots at "+course+"  :(")
	else:
		break
	sleep(20*60)
gm = mail.Gmail(from, password)
content = open("email", 'r').read()
gm.send_message(to, course+' - Enrollment', content)
print("E-mail sent :)")
