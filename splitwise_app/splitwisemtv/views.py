from django.views import View
from django.shortcuts import render, redirect
from .models import User, Expense, Balance
from django.urls import reverse
from django.contrib import messages

class UserView(View):
    def get(self, request):
        users = User.objects.all()
        return render(request, 'users_list.html', {'users': users})

    def post(self, request):
        # Logic to add a new user
        name = request.POST['name']
        email = request.POST['email']
        mobile_number = request.POST['mobile_number']
        if not all([name, email, mobile_number]):
            users = User.objects.all()
            return render(request, 'users_list.html', {
                'users': users,
                'error': 'All fields are required.'
            })
        User.objects.create(name=name, email=email, mobile_number=mobile_number)
        return redirect(reverse('users_list'))

class ExpenseView(View):
    def get(self, request):
        users = User.objects.all()
        expenses = Expense.objects.all()
        return render(request, 'expenses_list.html', {'expenses': expenses, 'users': users})

    def post(self, request):
        # Logic to create a new expense
        paid_by_id = request.POST['paid_by']
        amount = round(float(request.POST['amount']), 2)
        split_type = request.POST['split_type']
        description = request.POST['description']
        participants = request.POST.getlist('participants')

        # Limiting participants to 1000
        if len(participants) > 1000:
            messages.error(request, "Participant limit exceeded. Maximum 1000 participants allowed per expense.")
            return redirect(reverse('expenses_list'))
        
        # amount should not exceed 1cr
        if amount > 10000000:
            messages.error(request, "Expense amount exceeds the maximum limit of 1,00,00,000 INR.")
            return redirect(reverse('expenses_list'))
        
        paid_by = User.objects.get(pk=paid_by_id)
        expense = Expense.objects.create(paid_by=paid_by, amount=amount, split_type=split_type, description=description)
        expense.participants.set(participants)

        # Calculate shares based on split_type
        self.calculate_shares(expense, split_type, participants, request.POST)

        return redirect(reverse('expenses_list'))

    def calculate_shares(self, expense, split_type, participants, post_data):
        # Logic to calculate and store the shares based on the split_type
        if split_type == 'EQUAL':
            share = expense.amount / len(participants)
            for participant in participants:
                Balance.objects.create(from_user=User.objects.get(pk=participant), to_user=expense.paid_by, amount=share)
        elif split_type == 'EXACT':
            for participant in participants:
                share = post_data[f'share_{participant}']
                Balance.objects.create(from_user=User.objects.get(pk=participant), to_user=expense.paid_by, amount=share)
        elif split_type == 'PERCENTAGE':
            for participant in participants:
                share_percentage = post_data[f'percentage_{participant}']
                share = expense.amount * (share_percentage / 100)
                Balance.objects.create(from_user=User.objects.get(pk=participant), to_user=expense.paid_by, amount=share)

class BalanceView(View):
    def get(self, request):
        balances = Balance.objects.all()
        return render(request, 'balances_list.html', {'balances': balances})
