from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .models import Expense
from django.db.models import Sum


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You can now login.')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})


@login_required 
def expense_list(request):
    # Filter by 'user=request.user' so users only see their own data
    expenses = Expense.objects.filter(user=request.user).order_by('-date')
    
    total_amount = expenses.aggregate(Sum('amount'))['amount__sum'] or 0
    
    if request.method == "POST":
        amount = request.POST.get('amount')
        category = request.POST.get('category')
        description = request.POST.get('description')
        
        Expense.objects.create(
            user=request.user, # Links the expense to the logged-in person
            amount=amount,
            category=category,
            description=description
        )
        return redirect('expense_list')
      
    context = {
        'expenses': expenses,
        'total_amount': total_amount
    }
    
    return render(request, 'index.html', context)


@login_required
def delete_expense(request, id):
    # Added user=request.user to prevent people from deleting others' data by typing IDs in the URL
    expense = get_object_or_404(Expense, id=id, user=request.user)
    expense.delete()
    return redirect('expense_list')


@login_required
def edit_expense(request, id):
    expense = get_object_or_404(Expense, id=id, user=request.user)
    
    if request.method == "POST":
        expense.amount = request.POST.get('amount')
        expense.category = request.POST.get('category')
        expense.description = request.POST.get('description')
        expense.save()
        return redirect('expense_list')

    return render(request, 'edit_expense.html', {'expense': expense})