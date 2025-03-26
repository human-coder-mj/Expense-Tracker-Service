from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from django.db import IntegrityError
from .serializers import CategorySerializer, ExpenseSerializer
from .models import Category, Expenses

class CategoryViewSet(viewsets.ModelViewSet):

    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):

        return Category.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        try:
            serializer.save(user=self.request.user)
        except IntegrityError:
            raise ValidationError({"error": "This record already exists."})
    
    def update(self, request, *args, **kwargs):

        instance = self.get_object()
        data = {**request.data, "user": request.user.pk}
        serializer = self.get_serializer(instance, data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_205_RESET_CONTENT)

        return Response(serializer.errors, status=status.HTTP_424_FAILED_DEPENDENCY)

    def destroy(self, request, *args, **kwargs):

        instance = self.get_object()
        instance.delete()
        return Response({'message': 'Category has been deleted'}, status=status.HTTP_204_NO_CONTENT)

    
class ExpenseViewSet(viewsets.ModelViewSet):
    queryset = Expenses.objects.all()
    serializer_class = ExpenseSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):

        return Expenses.objects.filter(user=self.request.user)

    
    def perform_create(self, serializer):
        """Validate budget constraints before saving a new expense"""
        expense_amount = serializer.validated_data['expense_amount']
        budget = serializer.validated_data['budget']

        if budget.remaining < expense_amount:
            raise ValidationError(
                f"This amount: {expense_amount} is too large to fit in budget: {budget}."
            )
        serializer.save(user=self.request.user)
    
    def perform_update(self, serializer):
        instance = self.get_object()
        validated_data = serializer.validated_data

        old_amount = instance.expense_amount
        old_budget = instance.budget
        amount = validated_data.get('expense_amount', old_amount)
        budget = validated_data.get('budget', old_budget)

        if old_budget == budget:
            if budget.remaining + old_amount < amount:
                raise ValidationError(
                    detail=f"This amount: {amount} is too large to fit in budget: {budget}" 
                )
        else:
            if budget.remaining < amount:
                raise ValidationError(
                    detail=f"This amount: {amount} is too large to fit in budget: {budget}" 
                )

        serializer.save()

    def perform_destroy(self, instance):
        instance.delete()
        return Response({'message': f'Expense titled {instance.title} has been deleted'}, 
                        status=status.HTTP_204_NO_CONTENT)