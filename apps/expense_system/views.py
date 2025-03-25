from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from .serializers import CategorySerializer
from .models import Category

class CategoryViewSet(viewsets.ModelViewSet):

    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):

        return Category.objects.filter(user=self.request.user)

    def perform_create(self, serializer):

        serializer.save(user=self.request.user)

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
