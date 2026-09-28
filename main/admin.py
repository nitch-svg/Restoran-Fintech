from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Menu, Branch, Xodim, Savat



admin.site.register(Savat)


    
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'slug', 'is_active', 'is_menu', 'prod_cnt']    
    list_display_links = ['id', 'name']
     
    @admin.display(description='Ovqatlar soni', empty_value='???')
    def prod_cnt(self, obj):
        html = "<a href = ''>"
        return obj.foods.all().count()
    
    
    
    
    
@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'category', 'show_price', 'is_active', "show_info", 'show_image']
    list_display_links = ['id', 'name']
    ordering = ['name']
    search_fields = ['name', 'info', 'category__name' ]
    list_filter = ['is_active', 'category']
    
    
    @admin.display(description='Ovqatning rasmi',empty_value='???')
    def show_image(self, obj):
        if obj.image:
            html = '<img src = "{}" width = "120px" height="100px">'
            return format_html(html, obj.image.url)
    
    
    
    @admin.display(description='Narx', empty_value='???', ordering = 'price')
    def show_price(self, obj):
        if obj.discount:
            html = "<del style = 'color: red;'>{} UZS</del><br>"\
                   "<span style = 'color: green;'>{} UZS</span>"
            return format_html(html, obj.price, obj.get_price())
        else:
            html = '<span style="color: deepskyblue;">{} UZS</span>'
            return format_html(html, obj.get_price())
      
      
    @admin.display(description='Info', empty_value='???', ordering='info')    
    def show_info(self, obj):
        info = ' '.join(obj.info.split()[:3])
        html = '{} <a href="/admin/main/menu/{}/change/">...</a>'
        
        return format_html(html, info, obj.id)
       
    


@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ['name', 'address', 'show_phone', 'show_time', 'show_amount_workers', 'is_24_7']
    list_display_links = ['address', 'name']
    
    @admin.display(description='Ish vaqti')
    def show_time(self, obj):
        if obj.start_time and obj.end_time:
            start = obj.start_time.strftime("%H:%M")
            end = obj.end_time.strftime("%H:%M")
            html = "<span style='color: #16a34a;'>{}</span>- <span style='color: #dc2626;'>{}</span>"
            return format_html(html, start, end)
        
    @admin.display(description='Telefon raqam')
    def show_phone(self, obj):
        return obj.get_phone()
    
    @admin.display(description='Xodimlar soni', empty_value='???')
    def show_amount_workers(self, obj):
        return obj.get_workers()
        




@admin.register(Xodim)
class XodimAdmin(admin.ModelAdmin):
    list_display = ['fio', 'position', 'yosh', 'exp', 'maosh', 'show_info', 'filial']
    list_display_links = ['fio', 'position']
    
    @admin.display(description='Info', empty_value='???', ordering='info')
    def show_info(self, obj):
        info = ' '.join(obj.info.split()[:3])
        html = '{}<a href="/admin/main/xodim/{}/change/">...</a>'
        return format_html(html,  info, obj.id,)
    

# @admin.register(Product)
# class ProductAdmin(admin.ModelAdmin):
#     list_display = ['id', 'name', 'category', 'show_price', 'show_info']
#     list_display_links = ['id', 'name', 'category']
#     search_fields = ['name']
#     list_filter = ['category']
    
#     @admin.display(description='Price', empty_value='???', ordering='price')
#     def show_price(self, obj):
#         if obj.discount:
#             html = "<del style = 'color: red;'>{}</del><br>"\
#                     "<span style = 'color: green;'>{}</span>"
                    
#             return format_html(html, obj.price, obj.get_price())
        
#         return f'{obj.get_price()} UZS'
    
#     @admin.display(description='info', empty_value='???', ordering='info')
#     def show_info(self, obj):
#         info = ' '.join(obj.description.split()[:5])
#         html = "{} <a href = '/admin/main/product/{}/change/'>...</a>"
#         return format_html(html, info, obj.id)
    

    
    
    
    
    
# Register your models here.
