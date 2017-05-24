from django.db import models
from django.contrib.auth.models import User

class Budget(models.Model):
	MONTH_CHOICES = (
		('January','January'),
		('February','February'),
		('March','March'),
		('April','April'),
		('May','May'),
		('June','June'),
		('July','July'),
		('August','August'),
		('September','September'),
		('October','October'),
		('November','November'),
		('December','December'),
	)
	YEAR_CHOICES = (('2017','2017'),('2018','2018'))
	month = models.CharField(
		max_length=9,
		choices=MONTH_CHOICES,
		default='January',
	)
	year = models.CharField(
		max_length=4, 
		choices=YEAR_CHOICES, 
		default=2017,
	)
	income = models.DecimalField(max_digits=8, decimal_places=2)
	budget_remaining = 0
	completeness = "incomplete"
	money_budgeted = 0
	owner = models.ForeignKey(User)
	red_or_black = models.CharField(max_length =5, default='black')
	STATUS_CHOICES = (('active','active'),('inactive','inactive'))
	status = models.CharField(
		max_length=8,
		choices=STATUS_CHOICES,
		default='inactive',
	)
		
	def __str__(self):
		return self.month + ", " + self.year
		
class Category(models.Model):
	'''A budget category created by the user.'''
	name = models.CharField(max_length=50)
	budget = models.DecimalField(max_digits=7, decimal_places=2)
	budget_month = models.ForeignKey(Budget)
	red_or_black = models.CharField(max_length =5, default='black')
	total_expense = 0
	budget_remaining = 0
	class Meta:
		verbose_name_plural = 'categories'
	def __str__(self):
		'''Return string of category.'''
		return self.name
		
class Expense(models.Model):
	'''An expense entered by the user.'''
	expense = models.DecimalField(max_digits=7, decimal_places=2)
	category = models.ForeignKey(Category)
	tag = models.CharField(max_length=20, default='none')
	date_added = models.DateTimeField(auto_now_add=True)
	def __str__(self):
		'''Return string of expense.'''
		return str(self.expense)


