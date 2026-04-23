from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Expense
from django.db.models import Sum

@login_required 
def expense_list(request):
    # 1. Fetch all expenses from the database
    expenses = Expense.objects.all().order_by('-date')
    
    # 2. Calculate the total amount spent
    # 'amount__sum' will be None if the list is empty, so we use 'or 0'
    total_amount = expenses.aggregate(Sum('amount'))['amount__sum'] or 0
    
    # 3. Handle adding a new expense via POST request
    if request.method == "POST":
        amount = request.POST.get('amount')
        category = request.POST.get('category')
        description = request.POST.get('description')
        
        # Save to database (linking to current user)
        Expense.objects.create(
            user=request.user,
            amount=amount,
            category=category,
            description=description
        )
        return redirect('expense_list') # Refresh page to show new data
      

    context = {
        'expenses': expenses,
        'total_amount': total_amount
    }
    
    return render(request, 'index.html', context)

def delete_expense(request, id):
    expense = get_object_or_404(Expense, id=id)
    expense.delete()
    return redirect('expense_list')


def edit_expense(request, id):
    expense = get_object_or_404(Expense, id=id)
    
    if request.method == "POST":
        # Update the object with new data from the form
        expense.amount = request.POST.get('amount')
        expense.category = request.POST.get('category')
        expense.description = request.POST.get('description')
        expense.save() # Save changes
        return redirect('expense_list')

    # Pass the existing expense to the template to fill the fields
    return render(request, 'edit_expense.html', {'expense': expense})