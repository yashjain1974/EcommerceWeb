from django.shortcuts import render
from .import models
from django.http import HttpResponse
from .models import Product,Contact,Orders,OrderUpdate
from django.utils import timezone
from math import ceil
import json
from django.views.decorators.csrf import csrf_exempt
from .paytm import Checksum
MERCHANT_KEY = 'kbzk1DSbJiV_O3p5' #your merchant key here
import random
# Create your views here.

def index(request):
    # product=Product.objects.all()

    # allProds=[[product,range(1,nSlides),nSlides],
    #           [product,range(1,nSlides),nSlides]]

    # params = {'no_of_slides':nSlides, 'range': range(1,nSlides),'product': products}
    allProds=[]
    catProds=Product.objects.values('category','id')
    cats={item['category'] for item in catProds}
    for cat in cats:

        prod=Product.objects.filter(category=cat)

        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - n // 4)
        allProds.append([prod , range(1,nSlides),nSlides])

    params={'allProds':allProds}
    return render(request,'shop/index.html',params)
    # return HttpResponse("Hello world Welcome to shop")

def search(request):
    query=request.GET.get('search')
    allProds = []
    catProds = Product.objects.values('category', 'id')
    cats = {item['category'] for item in catProds}
    for cat in cats:
        prodtemp = Product.objects.filter(category=cat)
        prod=[item for item in prodtemp if searchMatch(query,item)]

        n = len(prod)

        nSlides = n // 4 + ceil((n / 4) - n // 4)


        if (len(prod) != 0):
            allProds.append([prod, range(1, nSlides), nSlides])

    params = {'allProds': allProds,"msg":""}
    if(len(allProds)==0 or len(query)<3):
        params={'msg':"Unable to find you Product"}

    return render(request, 'shop/search.html', params)
    # return HttpResponse("Hello world Welcome to shop"
def searchMatch(query,item):
    #return true only if query matches the item
    if(query in item.product_desc.lower() or query in item.product_name.lower() or query in item.category.lower()):
        return True
    else:
        return False
def about(request):
    return render(request,'shop/about.html')

def contact(request):
    thank=False
    if request.method=="POST":

        name=request.POST.get('name',"")
        email=request.POST.get('email',"")
        phone=request.POST.get('phone',"")
        date=request.POST.get('date',"")
        message=request.POST.get('message',"")
        cont=Contact(name=name,email=email,phone=phone,date=date,desc=message)
        cont.save()
        thank=True
    return render(request, 'shop/contact.html',{'thank':thank})


def tracker(request):
    if request.method=="POST":
        order_id=request.POST.get('order_id')
        email=request.POST.get('email')
        try:
            order=Orders.objects.filter(order_id=order_id,email=email)

            if(len(order)>0):
                update=OrderUpdate.objects.filter(order_id=order_id)
                updates=[]
                response={}
                for item in update:
                    updates.append({"text":item.update_desc,"time":item.timestamp})
                    response=json.dumps({"status":"success","updates":updates,"itemsJson":order[0].items_json},default=str)
                return HttpResponse(response)
            else:
                return HttpResponse('{"status":"No Item"}')
        except Exception as e:
            return HttpResponse('{"status":"error"}')
    return render(request, 'shop/tracker.html')





def productview(request,myid):
    #Fetch the product using the id
    product=Product.objects.filter(id=myid)
    list1=[]

    allProds = []
    catProds = Product.objects.values('category', 'id')
    cats = {item['category'] for item in catProds}
    random_cat=""
    for index, cat in enumerate(cats):
        list1.append(cat)
        random_cat = random.choice(list1)


    for index,cat in enumerate(cats):
        prod = Product.objects.filter(category=cat)


        if(cat==random_cat):
            n = len(prod)
            nSlides = n // 4 + ceil((n / 4) - n // 4)
            allProds.append([prod, range(1, nSlides), nSlides])


    param={'product':product[0],'allProds':allProds}
    return render(request, 'shop/prodview.html',param)
def checkout(request):
    if request.method == "POST":
        items_json=request.POST.get('itemsjson', "")
        name = request.POST.get('name', "")
        amount = request.POST.get('amount', "0")
        email = request.POST.get('email', "")
        address = request.POST.get('address', "")
        address2 = request.POST.get('address2', "")
        city= request.POST.get('city', "")
        state= request.POST.get('state', "")
        zip_code= request.POST.get('zip_code', "")
        phone = request.POST.get('phone', "")
        order = Orders(items_json=items_json,name=name, email=email, address=address,date=timezone.now(), address_line_2=address2, city=city,state=state,zip_code=zip_code,phone=phone,amount=amount)
        order.save()
        update=OrderUpdate(order_id=order.order_id,update_desc="Your order has been placed successfully...")
        update.save()
        thank=True
        id=order.order_id
        # return render(request, 'shop/checkout.html',{'thank':thank,'id':id})
        #Request paytm to transfer the amoun t to your account after payment by user
        param_dict={
            'MID': 'WorldP64425807474247',
            'ORDER_ID': str(order.order_id),
            'TXN_AMOUNT': str(amount),
            'CUST_ID': email,
            'INDUSTRY_TYPE_ID': 'Retail',
            'WEBSITE': 'WEBSTAGING',
            'CHANNEL_ID': 'WEB',
            'CALLBACK_URL': 'http://127.0.0.1:8000/shop/handlerequest/',
        }
        param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(param_dict, MERCHANT_KEY)
        return render(request,'shop/paytm.html',{'param_dict':param_dict})

    return render(request, 'shop/checkout.html')
# def cart(request):
#     return render(request, 'shop/cart.html')

@csrf_exempt
def handlerequest(request):
        # paytm will send you post request here
        form = request.POST
        response_dict = {}
        for i in form.keys():
            response_dict[i] = form[i]
            if i == 'CHECKSUMHASH':
                checksum = form[i]

        verify = Checksum.verify_checksum(response_dict, MERCHANT_KEY, checksum)
        if verify:
            if response_dict['RESPCODE'] == '01':
                print('order successful')
            else:
                print('order was not successful because' + response_dict['RESPMSG'])
        return render(request, 'shop/paymentstatus.html', {'response': response_dict})
