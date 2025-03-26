from rest_framework import serializers
from .models import Budget

class BudgetSerializer(serializers.ModelSerializer):
    remaining = serializers.ReadOnlyField()
    amount_used = serializers.ReadOnlyField()
    expense_count = serializers.ReadOnlyField(source="expenses_set.count")

    class Meta:
        model = Budget
        exclude = ('id',)

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Budget amount must be greater than zero.")
        return value

    def validate(self, data):
        user = data.get("user")
        name = data.get("name")
        
        if Budget.objects.filter(user=user, name=name).exists():
            raise serializers.ValidationError("A budget with this name already exists for this user.")
        return data
