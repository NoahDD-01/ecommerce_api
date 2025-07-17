from django.db import models
from ckeditor.fields import RichTextField
from django.conf import settings
import uuid
# Create your models here.
class Category(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    parent = models.ForeignKey("self",null=True,blank=True,related_name="children",on_delete=models.CASCADE)
    name = RichTextField()
    image = models.ImageField(upload_to="categories",null=True,blank=True)
    description = RichTextField(null=True,blank=True)
    created_by=models.ForeignKey(settings.AUTH_USER_MODEL,null=True,blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Categories"
    def __str__(self):
        return f"{self.parent} > {self.name}" if self.parent else str(self.name)