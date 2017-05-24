from django.contrib import admin

from budget_keepers.models import Category, Expense, Budget

admin.site.register(Category)
admin.site.register(Expense)
admin.site.register(Budget)
