from django.shortcuts import render
from django.http import HttpResponse
from plotly.offline import plot
import plotly.graph_objs as go
import plotly.express as px
from datetime import datetime
import pandas as pd
import numpy as np 
from .models import Dashboard

# Create your views here.
def home(request):
	return render(request, 'model/home.html')


def result(request):

	price = int(float(request.GET.get('price').replace(',', '')))
	dpayment = int(float(request.GET.get('dp').replace(',', '')))
	if request.GET.get('deposit'):
		deposit = int(float(request.GET.get('deposit').replace(',', '')))
	else:
		deposit=0
	cscore = float(request.GET.get('cscore'))
	term = float(request.GET.get('term'))
	if request.GET.get('pts'):
		pts = float(request.GET.get('pts').replace(',', ''))
	else:
		pts=0
	if request.GET.get('ARM_rate'):
		ARM_rate = float(request.GET.get('ARM_rate'))
	else:
			ARM_rate = 0

	morgage_type = request.GET.get('mtype')
	ref = request.GET.get('refinance')
	cref = request.GET.get('crefinance')
	fn = request.GET.get('foreign')

	context_list = Dashboard.dash(price, dpayment, deposit, cscore, term, pts, morgage_type, ref, cref, fn, ARM_rate)
	if term.is_integer()==False:
		term=int(term-0.1)
	context = {'r': context_list[0] , 'P': context_list[1] , 'n': context_list[2] , 'M': context_list[3] , 'ARM': context_list[4], 'r_adj': context_list[5], 'principal_list': context_list[6], 'interest_list': context_list[7], 'plt_div': context_list[8], 'dfp': context_list[9], 'dfi': context_list[10], 'dfa': context_list[11], 'ARM_rate': context_list[12], 'plt2_div': context_list[13],
		'price': price, 'dpayment': dpayment, 'deposit': deposit, 'cscore': cscore, 'term': term, 'pts': pts, 'morgage_type': morgage_type, 'ref': ref, 'cref': cref, 'fn': fn}

	return render(request, 'model/result.html', context)


def compare(request):
	return render(request, 'model/compare.html')


def rescompare(request):

	price = int(request.GET.get('price1').replace(',', ''))
	dpayment = int(request.GET.get('dp1').replace(',', ''))
	if request.GET.get('deposit1'):
		deposit = int(request.GET.get('deposit1').replace(',', ''))
	else:
		deposit=0
	cscore = float(request.GET.get('cscore1'))
	term = float(request.GET.get('term1'))
	if request.GET.get('pts1'):
		pts = float(request.GET.get('pts1').replace(',', ''))
	else:
		pts=0
	if request.GET.get('ARM_rate1'):
		ARM_rate = float(request.GET.get('ARM_rate1'))
	else:
			ARM_rate = 0

	morgage_type = request.GET.get('mtype1')
	ref = request.GET.get('refinance1')
	cref = request.GET.get('crefinance1')
	fn = request.GET.get('foreign1')


	price1 = int(request.GET.get('price2').replace(',', ''))
	dpayment1 = int(request.GET.get('dp2').replace(',', ''))
	if request.GET.get('deposit2'):
		deposit1 = int(request.GET.get('deposit2').replace(',', ''))
	else:
		deposit1=0
	cscore1 = float(request.GET.get('cscore2'))
	term1 = float(request.GET.get('term2'))
	if request.GET.get('pts2'):
		pts1 = float(request.GET.get('pts2').replace(',', ''))
	else:
		pts1=0
	if request.GET.get('ARM_rate2'):
		ARM_rate1 = float(request.GET.get('ARM_rate2'))
	else:
			ARM_rate1 = 0

	morgage_type1 = request.GET.get('mtype2')
	ref1 = request.GET.get('refinance2')
	cref1 = request.GET.get('crefinance2')
	fn1 = request.GET.get('foreign2')


	context_list1 = Dashboard.dash(price, dpayment, deposit, cscore, term, pts, morgage_type, ref, cref, fn, ARM_rate)
	context_list2 = Dashboard.dash(price1, dpayment1, deposit1, cscore1, term1, pts1, morgage_type1, ref1, cref1, fn1, ARM_rate1)
	context_list = context_list1 + context_list2

	context = {'r': context_list[0] , 'P': context_list[1] , 'n': context_list[2] , 'M': context_list[3] , 'ARM': context_list[4], 'r_adj': context_list[5], 'principal_list': context_list[6], 'interest_list': context_list[7], 'plt_div': context_list[8], 'dfp': context_list[9], 'dfi': context_list[10], 'dfa': context_list[11], 'ARM_rate': context_list[12], 'plt2_div': context_list[13],
		'r1': context_list[14] , 'P1': context_list[15] , 'n1': context_list[16] , 'M1': context_list[17] , 'ARM1': context_list[18], 'r_adj1': context_list[19], 'principal_list1': context_list[20], 'interest_list1': context_list[21], 'plt_div1': context_list[22], 'dfp1': context_list[23], 'dfi1': context_list[24], 'dfa1': context_list[25], 'ARM_rate1': context_list[26], 'plt2_div1': context_list[27],
			'price': price, 'dpayment': dpayment, 'deposit': deposit, 'cscore': cscore, 'term': term, 'pts': pts, 'morgage_type': morgage_type, 'ref': ref, 'cref': cref, 'fn': fn,
			'price1': price1, 'dpayment1': dpayment1, 'deposit1': deposit1, 'cscore1': cscore1, 'term1': term1, 'pts1': pts1, 'morgage_type1': morgage_type1, 'ref1': ref1, 'cref1': cref1, 'fn1': fn1}


	return render(request, 'model/rescompare.html', context)




