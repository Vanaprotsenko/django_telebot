from django.shortcuts import render
from .models import Expense
from django.db.models import Sum

from django.http import HttpResponseRedirect



# Create your views here.


def main(request):
    context = {}

    if request.method == 'POST':
        income = request.POST.get('income')
        expense = request.POST.get('expense')

        if income and expense:
            Expense.objects.create(income=income,expense = expense)
        return HttpResponseRedirect(request.path)  # Перенаправляем обратно на страницу для избежания повторной отправки формы

    expenses = Expense.objects.all().order_by('-date')  # Получаем записи в порядке убывания даты
    total_income = expenses.filter(income__isnull=False).aggregate(Sum('income'))['income__sum'] or 0
    total_expense = expenses.filter(expense__isnull=False).aggregate(Sum('expense'))['expense__sum'] or 0
    monthly_profit = total_income - total_expense

    context = {
        'monthly_profit': monthly_profit,
        'expenses': expenses,
    }
    return render(request, 'app1/main.html', context)


    
    