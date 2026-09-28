from django.shortcuts import render, HttpResponse, redirect
from .models import Category, Menu, Xodim, Branch, Savat
from .utils import send_receipt_tg
import requests




def navbar(index=0):
    active_class_name = 'text-amber-600 border-b-2 border-amber-600 px-1 py-2 text-sm'
    not_active = 'text-gray-600 hover:text-amber-600 transition px-1 py-2 text-sm'
    links = [
        {
          'name': 'Bosh sahifa',
          "class":not_active,
          'url_name':'home'  
        },
        {
          'name': 'Biz haqimizda',
          "class":not_active,
          'url_name':'about_us'  
        },
        {
          'name': 'Menyu',
          "class":not_active,
          'url_name':'menu'  
        },
        {
          'name': 'Xodimlarimiz',
          "class":not_active,
          'url_name':'xodimlar'  
        },
        {
          'name': 'Filiallar',
          "class":not_active,
          'url_name':'branch'  
        },
        {
         'name': 'Aloqa',
         "class":not_active,
         'url_name':'aloqa'  
        },
    ]
    
    links[index]['class'] = active_class_name
    
    return links


def index(request):
    maxsulotlar=Savat.objects.all().order_by('-id')
    categories = Category.objects.filter(is_menu =True)
    ovqatlar = Menu.objects.filter(is_active = True)
    xodimlar = Xodim.objects.all()
    branches = Branch.objects.all()
    
    ctx = {
        'categories':categories,
        'ovqatlar':ovqatlar,
        'xodimlar':xodimlar,
        'branches':branches,
        'links':navbar(index=0),
        'savat_count':maxsulotlar.count()
    }
    return render(request, 'index.html', ctx)




def menu(request):
    maxsulotlar=Savat.objects.all().order_by('-id')
    categories = Category.objects.all()
    
    ctx = {
        'categories':categories,
        'links':navbar(index=2),
        'savat_count':maxsulotlar.count()
    }
    return render(request, 'menu.html', ctx)



def branch(request):
    filiallar = Branch.objects.all()
    maxsulotlar=Savat.objects.all().order_by('-id')
    
    ctx = {
        'links':navbar(index=4),
        'filiallar':filiallar,
        'savat_count':maxsulotlar.count()
    }
    return render(request, 'filiallar.html', ctx)



def about(request):
    maxsulotlar=Savat.objects.all().order_by('-id')
    ctx={
        'links':navbar(index=1),
        'savat_count':maxsulotlar.count()
    }
    return render(request, 'about.html', ctx)



def xodimlar(request):
    xodimlar=Xodim.objects.all()
    maxsulotlar=Savat.objects.all().order_by('-id')
    
    ctx={
        'links':navbar(index=3),
        'xodimlar':xodimlar,
        'savat_count':maxsulotlar.count()
    }
    return render(request, 'xodimlar.html', ctx)



def contact(request):
    contactlar = Branch.objects.all()
    maxsulotlar=Savat.objects.all().order_by('-id')
    ctx={
        'contactlar':contactlar,
        'links':navbar(index=5), 
        'savat_count':maxsulotlar.count()
    }
    return render(request, 'contact.html', ctx)


def savat(request):
    maxsulotlar=Savat.objects.all().order_by('-id')
    abs_total = sum([x.total_price for x in maxsulotlar])
    ctx={
        'maxsulotlar':maxsulotlar,
        "savat_count":maxsulotlar.count(),
        'absolute_total_price':f'{abs_total:,}',
        'with_dostavka':f'{(abs_total+10000):,}'
    }
    return render(request, 'savat.html', ctx)


def add_savat(request, ovqat_id):
    ovqat = Menu.objects.filter(id = ovqat_id).first()
    if not ovqat:
        return redirect('menu')
    
    savat, created = Savat.objects.get_or_create(ovqat=ovqat)
    if not created:
        savat.quantity+=1
        savat.save()
        
    url = request.GET.get('url', 'savat')
    return redirect(url)


def remove_savat(request, savat_id, one_delete=0):
    savat = Savat.objects.filter(id=savat_id).first()
    if not savat:
        return redirect('savat')
    
    if one_delete:
        savat.delete()
    else:
        savat.quantity -= 1
        if savat.quantity <= 0:
            savat.delete()
        else:    
            savat.save()
    return redirect('savat')
        

def clear_savat(request):
    try:
        Savat.objects.all().delete()
    except:
        ...
    return redirect('savat')





def order(request):

    if request.method == "POST":

        # savat = Savat.objects.filter(user=request.user)
        savat = Savat.objects.all()

        ism = request.POST.get("ism")
        phone = request.POST.get("phone")
        address = request.POST.get("address")

        shablon = ""

        for i in savat:
            shablon += rf"""
Maxsulot Nomi: {i.ovqat.name}
Maxsulot Soni: {i.quantity}
Maxsulot Narxi: {i.ovqat.get_price()}
Umumiy qiymati: {i.get_total_price()}

"""

        message = rf"""
<b>Yangi Buyurtma</b>

{shablon}

<b>Buyurtmachi:</b> {ism}
<b>Phone:</b> {phone}
<b>Manzil:</b> {address}
"""

        send_receipt_tg(message)

        savat.delete()


        return redirect("savat")
    return redirect("savat")

    return render(request, "order.html")
# Create your views here.
