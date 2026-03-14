from django.views.generic import ListView, DetailView
from .models import ClothingItem, Category, Size
from django.db.models import Q

class CatalogView(ListView):
    model = ClothingItem
    template_name = 'main/product/list.html'
    context_object_name = 'cloting_items' # У шаблоні буде доступно як cloting_items
    
    def get_queryset(self):
        queryset = super().get_queryset()
        # Отримуємо списки з GET-запиту
        category_slugs = self.request.GET.getlist('category') # Виправлено назву змінної
        size_names = self.request.GET.getlist('size')
        min_price = self.request.GET.get('min_price')
        max_price = self.request.GET.get('max_price') 
        
        if category_slugs:
            queryset = queryset.filter(category__slug__in=category_slugs)

        if size_names:
            # Використовуємо distinct(), щоб уникнути дублікатів товарів, 
            # якщо у товара є кілька розмірів, що підпадають під фільтр
            queryset = queryset.filter(
                sizes__name__in=size_names,
                sizes__clothingitemsize__available=True # Перевір назву Related Name у моделі
            ).distinct()
            
        if min_price:
            queryset = queryset.filter(price__gte=min_price)       
                           
        if max_price:
            queryset = queryset.filter(price__lte=max_price)  
                                       
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['sizes'] = Size.objects.all() # Виправлено на 'sizes' для логіки
        context['selected_categories'] = self.request.GET.getlist('category')
        context['selected_sizes'] = self.request.GET.getlist('size')
        context['min_price'] = self.request.GET.get('min_price', '')
        context['max_price'] = self.request.GET.get('max_price', '')
        return context

# Виніс клас DetailView з CatalogView (раніше він був вкладеним)
class ClothingItemDetailView(DetailView):
    model = ClothingItem
    template_name = 'main/product/detail.html'
    context_object_name = 'clothing_item'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
