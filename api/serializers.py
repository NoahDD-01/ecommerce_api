from rest_framework import serializers
from .models import *
from accounts.serializers import *
from accounts.helpers import mmt 

class CategorySerializer(serializers.ModelSerializer):
    created_by = UserListSerializer(read_only = True)
    created_at = serializers.SerializerMethodField(read_only = True)
    updated_at = serializers.SerializerMethodField()
    children = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = [
            "id",
            "parent",
            "children",
            "name",
            "image",
            "description",
            "created_by",
            "created_at",
            "updated_at",
        ]

    def get_children(self,obj):
        children = obj.children.all()
        return CategorySerializer(children,many =True,context=self.context).data
    def get_created_at(self,obj):
        return mmt(obj.created_at)
    def get_updated_at(self,obj):
        return mmt(obj.updated_at)
    def create(self, validated_data):
        validated_data["created_by"] = self.context["request"].user
        return super().create(validated_data)