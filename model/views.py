from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def home(request):
	return render(request, 'model/home.html')


def result(request):

	interest_rate = 4.5

	price = int(request.GET.get('price').replace(',', ''))
	dpayment = int(request.GET.get('dp').replace(',', ''))
	if request.GET.get('deposit'):
		deposit = int(request.GET.get('deposit').replace(',', ''))
	else:
		deposit=0
	cscore = float(request.GET.get('cscore'))
	term = float(request.GET.get('term'))
	if request.GET.get('pts'):
		pts = float(request.GET.get('pts').replace(',', ''))
	else:
		pts=0

	morgage_type = request.GET.get('mtype')
	ref = request.GET.get('refinance')
	cref = request.GET.get('crefinance')
	fn = request.GET.get('foreign')

	deposit_rr = (-0.88*(deposit/(price-dpayment)))+0.15
	pts_rr = -0.5*(pts)

	if ref:
		ref_rr = 0.25
	else:
		ref_rr = 0
	if cref:
		cref_rr = 0.5
	else:
		cref_rr = 0
	if fn:
		fn_rr = 1.5
	else:
		fn_rr = 0

	if term.is_integer():
		AMR = False
	else:
		term = term - 0.1
		AMR = True
	
	r = ((interest_rate + cscore + deposit_rr + pts_rr + ref_rr + cref_rr + fn_rr)/100)/12
	P = price-dpayment
	n = term*12
	M = ((P*(r)*((1+r)**n)))/(((1+r)**n)-1)
	M = round(M, 2)
	r = r*12*100


	return render(request, 'model/result.html', {'r': r , 'P': P , 'n': n , 'M': M , 'AMR': AMR})


def compare(request):
	return render(request, 'model/compare.html')


def rescompare(request):
	return render(request, 'model/rescompare.html')