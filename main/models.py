from django.db import models

class Size(models.Model):
    name = models.CharField(max_length=10, unique=True)
    
    def __str__(self):
        return self.name
    
class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(unique=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']
        indexes = [models.Index(fields=['name'])]
        verbose_name = 'category'
        verbose_name_plural = 'categories'
        
class ClothingItem(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    available = models.BooleanField(default=True)
    sizes = models.ManyToManyField(Size, through='ClothingItemSize', related_name='clothing_items', blank=True)
    # Changed related_name to 'clothing_items' for consistency

    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='clothing_items')
    # FIX: Corrected the upload_to path and added a comma
    image = models.ImageField(upload_to='product/%Y/%m/%d', blank=True)   
    description = models.TextField(blank=True)
    created_at = models.DateField(auto_now_add=True, null=True)
    update_at = models.DateTimeField(auto_now=True)
    price = models.DecimalField(max_digits=20, decimal_places=2)
    discount = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    # Added default=0 for discount field

    class Meta:
        # Added ordering by name by default
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def get_price_with_discount(self):
        if self.discount > 0:
            return self.price * (1 - (self.discount / 100))
        return self.price
    
class ClothingItemSize(models.Model):
    clothing_item = models.ForeignKey(ClothingItem, on_delete=models.CASCADE)
    size = models.ForeignKey(Size, on_delete=models.CASCADE)
    available = models.BooleanField(default=True)
    
    class Meta:
        unique_together = ('clothing_item', 'size')
