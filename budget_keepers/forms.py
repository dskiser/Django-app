from django import forms

from .models import Budget, Category, Expense

class CreateBudget(forms.ModelForm):
	class Meta:
		model = Budget
		fields = ['year','month','income','status']
		labels = {'year': 'year', 'month': 'month', 'income':'income',
				'status':'status'}
		
class EditCategory(forms.ModelForm):
	class Meta:
		model = Category
		fields = ['name', 'budget']
		labels = {'name': 'category', 'budget': 'budget'}
		
class BudgetStatus(forms.ModelForm):
	class Meta:
		model = Budget
		fields = ['month','year','income','status']
		labels = {'month': 'month', 'year':'year', 'status':'change budget status', 'income':'income'}
		
class EnterExpense(forms.ModelForm):
	class Meta:
		model = Expense
		fields = ['expense','category','tag']
		labels = {
			'expense': 'expense', 
			'category': 'category',
			'tag': 'tag',
			}
	def __init__(self, budget=None, **kwargs):
		super(EnterExpense, self).__init__(**kwargs)
		if budget:
			self.fields['category'].queryset = Category.objects.filter(budget_month=budget)

		
		
