from rest_framework import serializers
from .models import Category

class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = '__all__'
        extra_kwargs = {
            'user': {'write_only': True},
            'is_deleted': {'write_only': True}
        }

    def validate_title(self, value):
        """Ensure the category title is unique per user."""
        user = self.context['request'].user
        if Category.objects.filter(title=value, user=user).exists():
            raise serializers.ValidationError("You already have a category with this title.")
        return value
