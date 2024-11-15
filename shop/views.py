from django.shortcuts import render
from django.http import HttpResponse
from .models import Product,Contact,Orders,Orderupdate
from math import ceil
import json
from django.views.decorators.csrf import csrf_exempt
from paytm import checksum
MERCHANT_KEY = 'Your-Merchant-Key-Here'
# Create your views here.


def index(request):
    # products= Product.objects.all()
    # n= len(products)
    # nSlides= n//4 + ceil((n/4) + (n//4))
   #params={'no_of_slides':nSlides, 'range':range(1,nSlides), 'product': products}
    # allprods=[[products,range(1,nSlides),nSlides],
    #           [products,range(1,nSlides),nSlides]]
    allprods=[]
    catprods=Product.objects.values('category','id')
    cats={item['category'] for item in catprods}
    for cat in cats:
        prod = Product.objects.filter(category=cat)
        n=len(prod)
        nSlides=n // 4 + ceil((n/4)-(n//4))
        allprods.append([prod,range(1, nSlides), nSlides])
    params={'allprods':allprods}  
    return render(request,"shop/index.html", params)
def searchmatch(query, item):
    
    if query in item.desc.lower() or query in item.product_name.lower() or query in item.category.lower():
        return True
    else:
        return False

def search(request):
    query= request.GET.get('search')
    allProds = []
    catprods = Product.objects.values('category', 'id')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prodtemp = Product.objects.filter(category=cat)
        prod=[item for item in prodtemp if searchmatch(query, item)]
        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        if len(prod)!= 0:
            allProds.append([prod, range(1, nSlides), nSlides])
    params = {'allProds': allProds, "msg":""}
    if len(allProds)==0 or len(query)<4:
        params={'msg':"Please make sure to enter relevant search query"}
    return render(request, 'shop/search.html', params)

def about(request):
    return render(request,'shop/about.html')


def contact(request):
    thank=False
    if request.method == "POST":
        print(request)
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        desc = request.POST.get('desc', '')
        print(name, email, phone, desc)
        contact = Contact(name=name, email=email, phone=phone, desc=desc)
        contact.save()
        thank=True
    return render(request, 'shop/contact.html',{'thank':thank})


def tracker(request):
    if request.method=="POST":
        orderId = request.POST.get('orderId', '')
        email = request.POST.get('email', '')
        try:
            order = Orders.objects.filter(order_id=orderId, email=email)
            if len(order)>0:
                update = Orderupdate.objects.filter(order_id=orderId)
                updates = []
                for item in update:
                    updates.append({'text': item.update_desc, 'time': item.timestamp})
                    response = json.dumps({"status":"success", "updates": updates, "itemsJson": order[0].items_json}, default=str)
                return HttpResponse(response)
            else:
                return HttpResponse('{"status":"noitem"}')
        except Exception as e:
            return HttpResponse('{"status":"error"}')

    return render(request, 'shop/tracker.html')



# def tracker(request):
#     if request.method == "POST":
#         OrderId= request.POST.get('OrderId', '')
#         email = request.POST.get('email', '')
        
#     try:
#         order=Orders.objects.filter(order_id=OrderId,email=email)
#         if len(order)>0:
#                 update=Orderupdate.objects.filter(order_id=OrderId)
#                 updates=[]
#                 for item in update:
#                     updates.append({'text':item.update_desc,})
#                 response=json.dumps({"status":"success","updates":updates,"itemsJson":order[0].items_json},default=str)
#                 return HttpResponse(response)
#         else:
#             return HttpResponse('{"status":"noitem"}')
#     except Exception as e:
#         return HttpResponse('{"status":"error"}')     
                   
#     return render(request,'shop/tracker.html')

# def tracker(request):
#     if request.method == "POST":
#         OrderId = request.POST.get('OrderId', '')
#         email = request.POST.get('email', '')
        
#         order = Orders.objects.filter(order_id=OrderId, email=email)
#         if len(order) > 0:
#             update = Orderupdate.objects.filter(order_id=OrderId)
#             updates = []
#             for item in update:
#                 updates.append({
#                     'text': item.update_desc,
#                     'time': item.update_time.strftime('%Y-%m-%d %H:%M:%S')  # Convert datetime to string
#                 })
#             response = json.dumps(updates)
#             return HttpResponse(response, content_type="application/json")
#         else:
#             # You might want to handle the case when no orders are found
#             return HttpResponse(json.dumps({'error': 'No order found'}), content_type="application/json")
    
#     return render(request, 'shop/tracker.html')






def productview(request, myid):
    product=Product.objects.filter(id=myid)
    print(product)
    return render(request, "shop/prodview.html", {'product':product[0]})


# def checkout(request):
#     if request.method == "POST":
#         print(request)
#         items_json=request.POST.get('itemsJson', '')
#         name = request.POST.get('name', '')
#         amount= request.POST.get('amount', '')
#         email = request.POST.get('email', '')
#         address= request.POST.get('address1', '') + " " + request.POST.get('address2', '')
#         city= request.POST.get('city', '')
#         state= request.POST.get('state', '')
#         zip_code= request.POST.get('zip_code', '')
#         phone= request.POST.get('phone', '')
#         order = Orders(items_json=items_json, name=name, email=email, address=address, city=city, state= state , zip_code=zip_code, phone=phone,amount=amount)
#         order.save()
#         update=Orderupdate(order_id=order.order_id,update_desc="The order has been placed")
#         update.save()
#         thank=True
#         id=order.order_id
#        # return render(request, 'shop/checkout.html', {'thank':thank, 'id':id})
#         #request to paytm to reecive money
#     param_dict={

#             'MID': '',
#             'ORDER_ID': 'order.order_id',
#             'TXN_AMOUNT': '1',
#             'CUST_ID': 'email',
#             'INDUSTRY_TYPE_ID': 'Retail',
#             'WEBSITE': 'WEBSTAGING',
#             'CHANNEL_ID': 'WEB',
#             'CALLBACK_URL':'http://127.0.0.1:8000/shop/handlerequest/',

#     }
#     return  render(request, 'shop/paytm.html', {'param_dict': param_dict})
        

#  return render(request,'shop/checkout.html')
def checkout(request):
    if request.method=="POST":
        items_json = request.POST.get('itemsJson', '')
        name = request.POST.get('name', '')
        amount = request.POST.get('amount', '')
        email = request.POST.get('email', '')
        address = request.POST.get('address1', '') + " " + request.POST.get('address2', '')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        zip_code = request.POST.get('zip_code', '')
        phone = request.POST.get('phone', '')
        order = Orders(items_json=items_json, name=name, email=email, address=address, city=city,
                       state=state, zip_code=zip_code, phone=phone, amount=amount)
        order.save()
        update = Orderupdate(order_id=order.order_id, update_desc="The order has been placed")
        update.save()
        thank = True
        id = order.order_id
        # return render(request, 'shop/checkout.html', {'thank':thank, 'id': id})
        # Request paytm to transfer the amount to your account after payment by user
        param_dict = {

                'MID': 'AZUPOe27859329743477',
                'ORDER_ID': str(order.order_id),
                'TXN_AMOUNT': str(amount),
                'CUST_ID': email,
                'INDUSTRY_TYPE_ID': 'Retail',
                'WEBSITE': 'WEBSTAGING',
                'CHANNEL_ID': 'WEB',
                'CALLBACK_URL':'http://127.0.0.1:8000/shop/handlerequest/',

        }
        param_dict['CHECKSUMHASH'] = checksum.generate_checksum(param_dict, MERCHANT_KEY)
        return render(request, 'shop/paytm.html', {'param_dict': param_dict})

    return render(request, 'shop/checkout.html')


@csrf_exempt
def handlerequest(request):
    form = request.POST
    response_dict = {}
    for i in form.keys():
        response_dict[i] = form[i]
        if i == 'CHECKSUMHASH':
            checksum = form[i]

    verify = checksum.verify_checksum(response_dict, MERCHANT_KEY, checksum)
    if verify:
        if response_dict['RESPCODE'] == '01':
            print('order successful')
        else:
            print('order was not successful because' + response_dict['RESPMSG'])
    return render(request, 'shop/paymentstatus.html', {'response': response_dict})