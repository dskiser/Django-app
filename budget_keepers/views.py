from django.shortcuts import render
from django.http import HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required

from .models import Category, Expense, Budget
from .forms import CreateBudget, EditCategory, BudgetStatus, EnterExpense

@login_required
def index(request):
	'''The home page for Budget Keeper.'''
	budgets = Budget.objects.filter(status='active').filter(owner=request.user)
	categories = []
	budget_categories = {}
	forms = {}
	for budget in budgets:
		money_spent = 0
		categories = budget.category_set.all()
		budget_categories[budget] = categories
		budget.budget_remaining = budget.income
		for category in categories:
			expenses = category.expense_set.all()
			for expense in expenses:
				increment = expense.expense
				category.total_expense += increment
			category.budget_remaining = category.budget - category.total_expense
			if category.budget_remaining >= 0:
				category.red_or_black = 'black'
			else:
				category.red_or_black = 'red'
				category.budget_remaining = abs(category.budget_remaining)
			money_spent += category.total_expense
			budget.budget_remaining = budget.income - money_spent
			if budget.budget_remaining < 0:
				budget.red_or_black = 'red'
				budget.budget_remaining = abs(budget.budget_remaining)
			else:
				budget.red_or_black = 'black'
		if request.method != 'POST':
			# No data submitted; create a blank form.
			forms[budget] = EnterExpense(budget)
		else:
			# POST data submitted; process data.
			forms[budget] = EnterExpense(budget, data=request.POST)
			if forms[budget].is_valid():
				forms[budget].save()
				return HttpResponseRedirect(reverse('budget_keepers:index'))
	context = {
		'budget_categories': budget_categories,
		'budgets': budgets, 
		'categories': categories,
		'forms': forms,
		}
	return render(request, 'budget_keepers/index.html', context)

@login_required	
def create_budget(request):
	'''Create a new budget or modify an existing budget'''
	if request.method != 'POST':
		# No data submitted; create a blank form.
		form = CreateBudget()
	else:
		# POST data submitted; process data.
		form = CreateBudget(data=request.POST)
		if form.is_valid():
			new_budget = form.save(commit=False)
			new_budget.owner = request.user
			new_budget.save()
			return HttpResponseRedirect(reverse('budget_keepers:view_budgets'))
	
	context = {'form': form}
	return render(request, 'budget_keepers/create_budget.html', context)
	
@login_required		
def view_budgets(request):
	'''View existing budgets and categories in each budget.'''
	budgets = Budget.objects.filter(owner=request.user).order_by('year','month')
	for budget in budgets:
		categories = budget.category_set.all()
		for category in categories:
			budget.money_budgeted += category.budget
		for budget in budgets:
			if budget.money_budgeted == budget.income:
				budget.completeness = "complete"
			else:
				budget.completeness = "incomplete"
		
	context = {'budgets': budgets}
	return render(request, 'budget_keepers/view_budgets.html', context)

@login_required		
def view_budget(request, budget_id):
	'''View existing budget and change active/inactive status.'''
	budget = Budget.objects.get(id=budget_id)
	categories = budget.category_set.all()
	for category in categories:
		budget.money_budgeted += category.budget
		expenses = category.expense_set.all()
		for expense in expenses:
			increment = expense.expense
			category.total_expense += increment
		category.budget_remaining = category.budget - category.total_expense
		
	if budget.money_budgeted < budget.income:
		message = "You have money that has not yet been budgeted!  Please add more categories or expand existing categories."
	elif budget.money_budgeted > budget.income:
		message = "You have too much money budgeted!  Please remove categories or reduce categories."
	else:
		message = ''
		budget.completeness = "complete"
	if budget.owner != request.user:
		raise Http404
	categories = budget.category_set.order_by('name')
	if budget.owner != request.user:
			raise Http404
	if request.method != 'POST':
		# No data submitted; create a blank form.
		form = BudgetStatus(instance=budget)
	else:
		# POST data submitted; process data.
		form = BudgetStatus(instance=budget, data=request.POST)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect(reverse('budget_keepers:view_budget', args=[budget.id]))
	context = {'budget': budget, 'categories': categories, 'form': form, 'message': message}
	return render(request, 'budget_keepers/view_budget.html', context)

@login_required
def view_expenses(request, budget_id):
	'''View expenses for a selected budget.'''
	budget = Budget.objects.get(id=budget_id)
	category_expenses = {}
	categories = budget.category_set.all()
	for category in categories:
		expenses = category.expense_set.all()
		for expense in expenses:
			increment = expense.expense
			category.total_expense += increment
		category.budget_remaining = category.budget - category.total_expense
		if category.budget_remaining >= 0:
			category.red_or_black = 'black'
		else:
			category.red_or_black = 'red'
			category.budget_remaining = abs(category.budget_remaining)
		category_expenses[category] = category.expense_set.all()
	context = {
		'budget': budget,
		'category_expenses': category_expenses,
	}
	return render(request, 'budget_keepers/view_expenses.html', context)
			

@login_required		
def edit_category(request, category_id):
	'''Edit existing category name or budget.'''
	category = Category.objects.get(id=category_id)
	budget = category.budget_month
	if budget.owner != request.user:
		raise Http404
	if request.method != 'POST':
		edit_form = EditCategory(instance=category)
	else:
		edit_form = EditCategory(instance=category, data=request.POST)
		if edit_form.is_valid():
			edit_form.save()
			return HttpResponseRedirect(reverse('budget_keepers:view_budget',
												args=[budget.id]))
	
	context = {'category': category, 'budget': budget, 'edit_form': edit_form}
	return render(request, 'budget_keepers/edit_category.html', context)

@login_required	
def add_category(request, budget_id):
	'''Add a new category to a budget.'''
	budget = Budget.objects.get(id=budget_id)
	categories = budget.category_set.all()
	money_budgeted = 0
	for category in categories:
		money_budgeted += category.budget
	money_left = budget.income - money_budgeted
	message = 'You have $' + str(money_left) + ' left to allocate.'
	if request.method != 'POST':
		form = EditCategory()
	else:
		form = EditCategory(data=request.POST)
		if form.is_valid():
			new_category = form.save(commit=False)
			new_category.budget_month = budget
			money_budgeted += new_category.budget
			if money_budgeted <= budget.income:
				new_category.save()
				return HttpResponseRedirect(reverse('budget_keepers:view_budget', args=[budget_id]))
			else:
				message = 'You do not have enough room in your budget for that!  You have only $' + str(money_left) + ' remaining.'
	
	context = {'form': form, 'budget': budget, 'message': message}
	return render(request, 'budget_keepers/add_category.html', context)
	
@login_required
def delete_category(request, category_id):
	'''Delete category.'''
	category = Category.objects.get(id=category_id)
	budget = category.budget_month
	category.delete()
	return HttpResponseRedirect(reverse('budget_keepers:view_budget', args=[budget.id]))
	
@login_required
def delete_budget(request, budget_id):
	'''Delete budget.'''
	budget = Budget.objects.filter(id=budget_id).delete()
	return HttpResponseRedirect(reverse('budget_keepers:view_budgets'))
	
@login_required
def delete_expense(request, expense_id):
	'''Delete expense.'''
	expense = Expense.objects.get(id=expense_id)
	category = expense.category
	budget = category.budget_month
	expense.delete()
	return HttpResponseRedirect(reverse('budget_keepers:view_expenses',
										args=[budget.id]))

@login_required
def edit_expense(request, expense_id):
	'''Edit expense.'''
	expense = Expense.objects.get(id=expense_id)
	category = expense.category
	budget = category.budget_month
	if budget.owner != request.user:
		raise Http404
	if request.method != 'POST':
		form = EnterExpense(instance=expense, budget=budget)
	else:
		form = EnterExpense(instance=expense, budget=budget, data=request.POST)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect(reverse('budget_keepers:view_expenses',
												args=[budget.id]))
	
	context = {'budget': budget, 'form': form, 'expense': expense}
	return render(request, 'budget_keepers/edit_expense.html', context)
