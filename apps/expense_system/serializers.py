from rest_framework import serializers
from .models import Category, Expenses
from user_budget.serializers import BudgetSerializer 

class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = '__all__'
        extra_kwargs = {
            'user': {'write_only': True},
            'is_deleted': {'write_only': True}
        }


class ExpenseSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Expenses
        fields = '__all__'
        extra_kwargs = {
            'user' : {'write_only' : True}
        }

    def validate_expense_amount(self, value):
        """Ensure expense amount is greater than zero."""
        if value <= 0:
            raise serializers.ValidationError("Expense amount must be greater than zero.")
        return value

    def validate_categories(self, value):
        """Ensure that the categories belong to the user."""
        user = self.context['request'].user
        for category in value:
            if category.user != user:
                raise serializers.ValidationError(f"Category '{category.title}' does not belong to the user.")
        return value

    def validate_budget(self, value):
        """Ensure that the budget exists for the user."""
        user = self.context['request'].user
        if value.user != user:
            raise serializers.ValidationError("This budget does not belong to the user.")
        return value