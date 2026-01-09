from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission

class UserOtherInfo(AbstractUser):
    # user_city = models.CharField(max_length=50)
    # user_pincode = models.IntegerField()
    

    groups = models.ManyToManyField(
        Group,
        related_name="userotherinfo_groups",
        blank=True,
    )

    user_permissions = models.ManyToManyField(
        Permission,
        related_name="userotherinfo_permissions",
        blank=True,
    )

    def __str__(self):
        return self.username
    
class ProductCategory(models.Model):
    id = models.AutoField(primary_key= True)
    category = models.CharField(max_length=100) 

    def __str__(self):
        return self.category  
    
class ProductInfo(models.Model):
    id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=100)
    product_description = models.CharField(max_length=1000)
    product_image = models.ImageField(upload_to='images/')
    # product_img = models.URLField(max_length=10000)
    product_price = models.CharField(max_length=100)
    product_category = models.ForeignKey(ProductCategory, on_delete=models.SET_NULL,null=True,blank=True)

    def __str__(self):
        return self.product_name

      
    




