from django.db import models
from django.utils.text import slugify
import re

# Create your models here.
# Models нужна чтоб создавать базу данных, то есть SQL-таблицы
# Models работает на основе системы ORM(Object Relational Mapping)
# С помощью обычных пайтон комманд создаются SQL таблицы
# Django же работает на основе MVT(Model, view, templates)
# Class based - на основе классов 
# Function based - на основе функций

# MVT -> Model- создает дата базу
#        View- передает эту дату базу на фронтенд
#        Templates- то что выводится на экран

class Category(models.Model):
    name = models.CharField(max_length=56)
    slug = models.CharField(max_length=56, blank=True)
    is_menu = models.BooleanField(default=True, choices=[
        (True, 'Menuda chiqadi'),
        (False, 'Menudf chiqmaydi'),
    ])
    is_active = models.BooleanField(default = True, choices=[
        (True, 'Category Faol'),
        (False, 'Category Mavjudmas')
    ])
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super(Category, self).save(*args, **kwargs)
    
    def __str__(self):
         return f'{self.name}'
     
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
    
    
    
     
    
class Menu(models.Model):
    image = models.ImageField(upload_to='menu/')
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='foods')
    is_active = models.BooleanField(default=True, choices=[
        (True, 'Ovqat sotuvda mavjud'),
        (False, 'Ovqat sotuvda mavjud emas')
    ])
    info = models.TextField()
    price = models.PositiveBigIntegerField(default = 50000)
    discount = models.SmallIntegerField(default = 0, verbose_name='Skidka (0-100%)')
    
    def get_raw_price(self):
        return int(self.price * (1 - self.discount / 100))
    
    def get_int_price(self):
        return f'{self.get_raw_price()}'
    
    def get_price(self):
        return self.get_int_price()
    
    def __str__(self):
             return f'{self.name}'

    class Meta:
        verbose_name = 'Ovqat'
        verbose_name_plural = 'Ovqatlar'
        
        
        
        
class Branch(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=100)
    start_time = models.TimeField(default='09:00:00')
    end_time = models.TimeField(default='22:00:00')
    is_24_7 = models.BooleanField(default = False,choices=[
        (True, 'Filial toxtamasdan ishlaydi'),
        (False, 'Filial toxtab ishlamaydi')
    ])
    
    def get_time(self):
        return f'{self.start_time.strftime("%H:%M")}-{self.end_time.strftime("%H:%M" )}'
    
            
    def get_phone(self):
        if not self.phone:
            return '---'
        
        
        p = re.sub(r'\D', '', str(self.phone))
        if len(p) == 9:
            return f"+998 ({p[:2]}) {p[2:5]}-{p[5:7]}-{p[7:]}"
        elif len(p) == 12:
            return f"+{p[:3]} ({p[3:5]}) {p[5:8]}-{p[8:10]}-{p[10:]}"
        return p
    
    
    def get_int_workers(self):
        amount = self.xodimlar.count() 
        return f"{amount:,}"
    
    
    def get_workers(self):
        return self.get_int_workers() 
    
    
    def __str__(self):
             return f'{self.name}'
    
    class Meta:
        verbose_name = 'Branch'
        verbose_name_plural = 'Branches'
    
     
     
        
class Xodim(models.Model):
    image = models.ImageField(upload_to='xodim/')
    position = models.CharField(max_length=10, choices=[
        ('chef', 'Bosh Oshpaz(Chef)'),
        ('conditer', 'Shirinliklar ustasi'),
        ('manajer', 'Bosh Menedjer'),
        ('barmen', 'Katta Barmen'),
        ('oficiant', 'Oficiant'),
        ('Farrosh', 'Tozalik xodimi')
    ])
    info = models.TextField()
    exp = models.PositiveSmallIntegerField(default=3, verbose_name='Tajribasi(yillarda)')
    fio = models.CharField(max_length=255, verbose_name='FullName')
    yosh = models.PositiveSmallIntegerField(default=18)
    maosh = models.PositiveBigIntegerField(default=4_000_000)
    filial = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True, related_name='xodimlar')
    
     
    def __str__(self):
        return f'{self.fio}'




    
class Savat(models.Model):
    ovqat = models.ForeignKey(Menu, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(default=1)
    total_price = models.PositiveIntegerField(default=0, null=True,blank=True, editable=False)

    def get_total_price(self):
        return f"{self.total_price:,}"

    def save(self,*args, **kwargs):
        self.total_price = int(self.ovqat.get_raw_price() * self.quantity)
        return super(Savat, self).save(*args, **kwargs)

    def __str__(self):
        return f'Ovqat:{self.ovqat.name}| Total price:{self.total_price}| Quantity:{self.quantity}'
    
    class Meta:
        verbose_name = 'Savat'
        verbose_name_plural = 'Savatchadagi narsalar'
    