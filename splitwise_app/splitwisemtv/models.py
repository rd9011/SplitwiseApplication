from django.db import models

# User model
class User(models.Model):
    userid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    mobile_number = models.CharField(max_length=15, unique=True)
    
    def __str__(self):
        return self.name

# Expense model
class Expense(models.Model):
    expenseid = models.AutoField(primary_key=True)
    paid_by = models.ForeignKey(User, related_name='expenses_paid', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    split_type = models.CharField(max_length=10, choices=[('EQUAL', 'Equal'), ('EXACT', 'Exact'), ('PERCENTAGE', 'Percentage')])
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    participants = models.ManyToManyField(User, related_name='expenses_participated')
    split_values = models.JSONField(blank=True, null=True, help_text="Used for EXACT or PERCENTAGE splits")

    def __str__(self):
        return f'{self.description} - {self.amount}'

# Balance model (for tracking user balances)
class Balance(models.Model):
    balanceid = models.AutoField(primary_key=True)  # Explicitly define the primary key
    from_user = models.ForeignKey(User, related_name='balances_owed', on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name='balances_due', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'{self.from_user.name} owes {self.amount} to {self.to_user.name}'
