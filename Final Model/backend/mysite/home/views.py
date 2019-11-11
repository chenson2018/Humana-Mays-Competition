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
	header = "<p style=\"color:black;font-size:24px;\">Patient 1 (high risk)</p><br><br>"
	
	html = "<p style=\"color:black;font-size:24px;\">Supply Count Analysis:</p><img src=\"http://178.128.68.14/p1.png\" alt=\"logo\"> <p style=\"color:red;font-size:24px;\">This patient shows significant inclination towards long-term opioid therapy at all prescription levels. <br>We suggest that you consider alternative treatments or closely monitor this patient.</p><br>\
	<br>"

	table = 'Patient History: <br><br> <table border="1" class="dataframe">\n  <thead>\n    <tr style="text-align: right;">\n      <th></th>\n      <th>id</th>\n      <th>event_descr</th>\n      <th>diagnosis</th>\n      <th>place_of_treatment</th>\n      <th>charge_amount</th>\n      <th>net_paid_amount</th>\n      <th>member_responsible_amount</th>\n      <th>Days</th>\n    </tr>\n  </thead>\n  <tbody>\n    <tr>\n      <th>1354298</th>\n      <td>ID14418595663</td>\n      <td>Fully Paid Claim</td>\n      <td>ENLARGED PROSTATE WITHOUT LOWER URINARY TRACT ...</td>\n      <td>OFFICE</td>\n      <td>160.0</td>\n      <td>1.5</td>\n      <td>96.6</td>\n      <td>-806</td>\n    </tr>\n    <tr>\n      <th>1354300</th>\n      <td>ID14418595663</td>\n      <td>Fully Paid Claim</td>\n      <td>MALIGNANT NEOPLASM OF PROSTATE</td>\n      <td>INDEPENDENT LABORATORY</td>\n      <td>3156.0</td>\n      <td>803.33</td>\n      <td>0.0</td>\n      <td>-767</td>\n    </tr>\n    <tr>\n      <th>1354302</th>\n      <td>ID14418595663</td>\n      <td>Fully Paid Claim</td>\n      <td>MALIGNANT NEOPLASM OF PROSTATE</td>\n      <td>OFFICE</td>\n      <td>112.0</td>\n      <td>62.48</td>\n      <td>2.59</td>\n      <td>-757</td>\n    </tr>\n    <tr>\n      <th>1354303</th>\n      <td>ID14418595663</td>\n      <td>Fully Paid Claim</td>\n      <td>MALIGNANT NEOPLASM OF PROSTATE</td>\n      <td>OFFICE</td>\n      <td>600.0</td>\n      <td>146.73</td>\n      <td>6.24</td>\n      <td>-751</td>\n    </tr>\n    <tr>\n      <th>1354305</th>\n      <td>ID14418595663</td>\n      <td>Fully Paid Claim</td>\n      <td>MALIGNANT NEOPLASM OF PROSTATE</td>\n      <td>OFFICE</td>\n      <td>36262.24</td>\n      <td>6591.829999999998</td>\n      <td>425.00000000000006</td>\n      <td>-661</td>\n    </tr>\n    <tr>\n      <th>1354306</th>\n      <td>ID14418595663</td>\n      <td>Fully Paid Claim</td>\n      <td>MALIGNANT NEOPLASM OF PROSTATE</td>\n      <td>OFFICE</td>\n      <td>2640.14</td>\n      <td>516.51</td>\n      <td>21.97</td>\n      <td>-637</td>\n    </tr>\n    <tr>\n      <th>1354315</th>\n      <td>ID14418595663</td>\n      <td>Fully Paid Claim</td>\n      <td>FEVER, UNSPECIFIED</td>\n      <td>ON CAMPUS-HOSPITAL OUTPATIENT</td>\n      <td>578.0</td>\n      <td>135.95</td>\n      <td>0.0</td>\n      <td>-456</td>\n    </tr>\n    <tr>\n      <th>1354316</th>\n      <td>ID14418595663</td>\n      <td>Fully Paid Claim</td>\n      <td>LOCAL INFECTION OF THE SKIN AND SUBCUTANEOUS T...</td>\n      <td>OFFICE</td>\n      <td>120.0</td>\n      <td>0.0</td>\n      <td>80.81</td>\n      <td>-456</td>\n    </tr>\n    <tr>\n      <th>1354325</th>\n      <td>ID14418595663</td>\n      <td>Fully Paid Claim</td>\n      <td>INJURY OF CONJUNCTIVA AND CORNEAL ABRASION WIT...</td>\n      <td>EMERGENCY ROOM - HOSPITAL</td>\n      <td>1201.0</td>\n      <td>0.0</td>\n      <td>115.2</td>\n      <td>0</td>\n    </tr>\n  </tbody>\n</table> <br>'

	return HttpResponse(header + table + html)
	
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
