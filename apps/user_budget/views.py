from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.exceptions import APIException, NotFound
from django.db.models import Sum
from django.shortcuts import get_object_or_404
from .models import Budget
from .serializers import BudgetSerializer

class BudgetViewSet(viewsets.ModelViewSet):

    serializer_class = BudgetSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        
        return Budget.objects.filter(user=self.request.user) # Ensures users can only access their own budgets.

    def perform_create(self, serializer):
        
        serializer.save(user=self.request.user) # Automatically assigns the authenticated user to the budget when creating.

    def update(self, request, pk=None):

        current_budget = self.get_object() # get_object() method handles the try and except block itself 
        
        data = request.data.copy()
        data['user'] = request.user.pk

        # Ensure the new amount is not less than existing expenses
        total_expense_amount = current_budget.expenses_set.aggregate(Sum('amount'))['amount__sum'] or 0
        if 'amount' in data and float(data['amount']) < total_expense_amount:
            return Response("This amount is already used in some expense",
                               code=status.HTTP_424_FAILED_DEPENDENCY)
        
        serializer = self.get_serializer(current_budget, data=data, partial=True)

        if serializer.is_valid():
            serializer.save(user=self.request.user)
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

        return Response(serializer.errors, status=status.HTTP_417_EXPECTATION_FAILED)

    def destroy(self, request, pk=None):

        budget = self.get_object()

        if budget.expenses_set.count() == 0:
            budget.delete()
            return Response({'detail': 'Budget has been deleted successfully'},
                            status=status.HTTP_202_ACCEPTED)

        raise APIException("Budget consists multiple expenses. Remove all the associated expenses first.",
                           code=status.HTTP_406_NOT_ACCEPTABLE)
