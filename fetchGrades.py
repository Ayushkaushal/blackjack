import os
from subprocess import call, check_output
import re
import json

def load(file):
    def convert(input):
        if isinstance(input, dict):
            return {convert(key): convert(value) for key, value in input.iteritems()}
        elif isinstance(input, list):
            return [convert(element) for element in input]
        elif isinstance(input, unicode):
            return input.encode('utf-8')
        else:
            return input

    dict_unicode = json.loads(open(file).read())
    return convert(dict_unicode)

def save(dic, name):
    with open(name + ".json", "w") as outfile:
        json.dump(dic, outfile)

allcourse = load('../kakashi/c.json')
	
def getGrades(code):
	b = check_output("curl 'https://erp.iitkgp.ernet.in/Acad/Pre_Registration/subject_grade_status.jsp?subno={}' -H 'DNT: 1' -H 'Accept-Encoding: gzip, deflate, sdch, br' -H 'Accept-Language: en-US,en;q=0.8' -H 'Upgrade-Insecure-Requests: 1' -H 'User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.75 Safari/537.36' -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8' -H 'Cookie: JSESSIONID=596DA65DF03FE6E7AC01B9E7B60060CD.worker3' -H 'Connection: keep-alive' --compressed".format(code),shell = True)
	nums = re.findall('([A-Z\s]+)\(No. of Student\) : ([0-9]+)', b)
	grades = {str(d[0].strip()):int(d[1]) for d in nums}
	return grades

allCourses = {}
for i in allcourse:
    while True:
        try:
            allCourses[i] = {'grades':getGrades(i)}
            print i, allCourses[i]
        except Exception as e:
            print i, e
        break

save(allCourses,'allSubs')
