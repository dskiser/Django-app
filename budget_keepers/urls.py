'''Defines URL patterns for budget_keepers.'''

from django.conf.urls import url

from . import views

urlpatterns = [
	# Home page
	url(r'^$', views.index, name='index'),
	
	# Create new budget
	url(r'^create_budget/$', views.create_budget, name='create_budget'),
	
	# View existing budgets
	url(r'^view_budgets/$', views.view_budgets, name='view_budgets'),
	
	# View existing budget
	url(r'^view_budget/(?P<budget_id>\d+)/$', views.view_budget, name='view_budget'),
	
	# Edit budget category
	url(r'^edit_category/(?P<category_id>\d+)/$', views.edit_category, name='edit_category'),
	
	# Add budget category
	url(r'^add_category/(?P<budget_id>\d+)/$', views.add_category, name='add_category'),
	
	# Delete category
	url(r'^delete_category/(?P<category_id>\d+)/$', views.delete_category, name='delete_category'),
	
	# Delete budget
	url(r'^delete_budget/(?P<budget_id>\d+)/$', views.delete_budget, name='delete_budget'),
	
	# Delete expense
	url(r'^delete_expense/(?P<expense_id>\d+)/$', views.delete_expense, name='delete_expense'),
	
	# View expenses
	url(r'^view_expenses/(?P<budget_id>\d+)/$', views.view_expenses, name='view_expenses'),
	
	# Edit expenses
	url(r'^edit_expense/(?P<expense_id>\d+)/$', views.edit_expense, name='edit_expense'),
]

