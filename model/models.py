from django.db import models
from django.http import HttpResponse
from plotly.offline import plot
import plotly.graph_objs as go
import plotly.express as px
from datetime import datetime
import pandas as pd
import numpy as np 

# Create your models here.
class Dashboard(models.Model):

	def dash(price, dpayment, deposit, cscore, term, pts, morgage_type, ref, cref, fn, ARM_rate):

		interest_rate = 4.5
		r_adj = 0

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
			ARM = False
			extra = 0
		else:
			term = term - 0.1
			ARM = True
			r_adj = (ARM_rate)/12/100
			extra = (30*12) - (term*12)
		
		r = ((interest_rate + cscore + deposit_rr + pts_rr + ref_rr + cref_rr + fn_rr)/100)/12
		P = price-dpayment
		n = term*12 + extra
		M = ((P*(r)*((1+r)**n)))/(((1+r)**n)-1)
		M = round(M, 2)
		r = round(r*12*100, 2)

		month_list = []
		years_list = []
		principal_list = []
		interest_list = []
		principal_left = P
		rr = r/12/100
		MM = M

		if ARM == False:

			y = datetime.now().year
			for month in range(int(term)*12):
				month_list.append(month+1)
				monthly_interest = principal_left*rr
				p1 = M - monthly_interest
				principal_left = principal_left - p1

				principal_list.append(p1)
				interest_list.append(monthly_interest)

			for year in range(int(term)):
				years_list.append(y)
				y+=1

		else:

			y = datetime.now().year
			term2 = int(30-term)
			for month in range(int(term)*12):
				month_list.append(month+1)
				monthly_interest = principal_left*rr
				p1 = M - monthly_interest
				principal_left = principal_left - p1

				principal_list.append(p1)
				interest_list.append(monthly_interest)
			for month in range(term2*12):
				if float(month/12).is_integer():
					rr = rr + r_adj
					MM = ((principal_left*(rr)*((1+rr)**(n-(term*12)-month)))/(((1+rr)**(n-(term*12)-month))-1))

				month_list.append(month+(1+(term*12)))
				monthly_interest = principal_left*rr
				p1 = MM - monthly_interest
				principal_left = principal_left - p1

				principal_list.append(p1)
				interest_list.append(monthly_interest)

			for year in range(int(term)+(int(extra/12))):
				years_list.append(int(y))
				y+=1


		all_lists = [principal_list, interest_list]
		all_lists_np = np.array(all_lists)
		df = pd.DataFrame(all_lists_np.T)
		df.columns = ['Principal', 'Interest']
		dfp = round(df['Principal'].sum(),2)
		dfi = round(df['Interest'].sum(),2)
		dfa = dfp + dfi
		
		years_np = np.array(years_list)
		df2 = pd.DataFrame(columns = ['Year','Principal', 'Interest'])
		df2['Principal'] = df['Principal'].iloc[::12] #.iloc[::12]
		df2['Interest'] = df['Interest'].iloc[::12]
		df2['Year'] = years_np
		df2 = df2.set_index('Year', drop=True)


		fig = px.line(df, height=500, width=700, labels={'index':"Months", 'value':"Monthly Payment Breakdown ($)", 'variable': ""}, title="Amortization over Loan Term (Monthly)")
		plt_div = plot(fig, output_type='div')

		fig2 = px.bar(df2, height=500, width=700, labels={'index':"Years", 'value':"Monthly Payment Breakdown ($)", 'variable': ""}, title="Amortization over Loan Term (Yearly)")
		plt2_div = plot(fig2, output_type='div')

		return [r, P , n , M , ARM, r_adj, principal_list, interest_list, plt_div, dfp, dfi,  dfa, ARM_rate, plt2_div]




