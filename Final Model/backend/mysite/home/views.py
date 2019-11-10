from django.shortcuts import render

from django.http import HttpResponse

home = "\
<img src=\"http://178.128.68.14/logo.png\" alt=\"logo\">\
<br>Please select a patient to view opioid reccomendations: <br><br>\
<a href=\"http://127.0.0.1:8000/patient1/\">Patient 1 (high risk)</a><br><br>\
<a href=\"http://127.0.0.1:8000/patient2/\">Patient 2 (low risk)</a><br><br>\
<a href=\"http://127.0.0.1:8000/patient3/\">Patient 3 (moderate risk)</a><br>\
"

def index(request):
    return HttpResponse(home)
	
def patient1(request):
	html = "Patient 1 (high risk)<br><br>\
	This patient shows significant inclinnation towards long-term opioid therapy at all prescription levels. We suggest that you consider alternative treatments or closely monitor this patient.<br>\
	<img src=\"http://178.128.68.14/p1.png\" alt=\"logo\">"

	return HttpResponse(html)
	
def patient2(request):
	html = "Patient 2 (low risk)<br><br>\
	This patient shows low inclination towards long-term opioid therapy at the current level you have specified. We believe that you may safely increase the initial supply count.<br>\
	<img src=\"http://178.128.68.14/p2.png\" alt=\"logo\">"

	return HttpResponse(html)
	
def patient3(request):
	html = "Patient 3 (moderate risk)<br><br>\
	This patient shows borderline inclination towards long-term opioid therapy at the current level you have specified. We believe that you should decrease the initial supply count.<br>\
	<img src=\"http://178.128.68.14/p3.png\" alt=\"logo\">"

	return HttpResponse(html)
