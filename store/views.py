from django.shortcuts import render, HttpResponse, get_object_or_404, redirect, HttpResponseRedirect
from .forms import ProductForm, ProductAttributeForm, ImageForm, OrderForm, ProductDiscountForm, LoginForm
from .models import Category, Product, Image, Order, ProductAttribute, Discount
from django.utils import timezone
from django.db.models import F, DecimalField
from django.contrib import messages
from django.forms.models import modelformset_factory
from django.contrib.auth import logout, login, authenticate
from django.views.generic.edit import UpdateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.contrib.auth.models import User







# Create your views here.


def home_view(request):

    title = 'الرئيسية'
    categorys = Category.objects.all()
    query_list = Product.objects.all()
    query = request.GET.get("q")
    if query:
        query_list = query_list.filter(title__icontains=query)

    return render(request, 'store/list.html', {'title': title, 'products': query_list, 'categorys': categorys })

def category_list(request, category_id ):
    categorys = Category.objects.all()
    title = get_object_or_404(Category,pk=category_id)
    query_list = Product.objects.filter(category_id=category_id)
    query = request.GET.get("q")
    if query:
        query_list = query_list.filter(title__icontains=query)

    return render(request, 'store/category-list.html', {'title': title, 'products': query_list, 'categorys': categorys })

def login_user(request):
    title = 'تسجيل الدخول'
    if request.method == 'POST':
        form = LoginForm()
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('control_home')

        else:
            messages.warning(request, 'هناك خطأ في أسم المستخدم أو كلمة المرور')
    
    else:
        if request.user.is_authenticated:
            return redirect('control_home')
        form = LoginForm()
    context = {
        'form': form,
        'title': title,
    }
    return render(request, 'control/control-login.html', context)
        




    
    
    #return HttpResponse("Hello World!")

def order_form(request, product_id):
    categorys = Category.objects.all()
    title = 'شراء منتج '
    product = get_object_or_404(Product,pk=product_id)
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            form.cleaned_data['color'] = request.POST.get('color')
            form.cleaned_data['size'] = request.POST.get('size')
            order = form.save()
            order = get_object_or_404(Order,pk=order.id)
            return redirect('confirm_order', order_id=order.id)
        else:
            return HttpResponse('erorr form')
        
    else:
        form = OrderForm(initial = {'product': product_id})
    context = {
        'categorys': categorys,
        'title': title,
        'form': form,
        'product':product,
    }
    return render(request, 'store/new-order.html', context)

def confirm_order(request, order_id):
    categorys = Category.objects.all()
    title = 'تم تقديم طلبك '
    order = get_object_or_404(Order,pk=order_id)
    context = {
        'categorys': categorys,
        'title': title,
        'order': order,
    }

    return render(request,'store/confirm-order.html', context)


@login_required
def list_new_orders(request):
    title = 'الطلبات الجديدة'
    orders = Order.objects.all()
    orders_new = orders.exclude(accept=True)
    return render(request, 'control/list-orders.html', {'title': title, 'orders': orders_new})

@login_required
def list_history_orders(request):
    title = 'سجل الطلبات القديمة '
    orders = Order.objects.all()
    orders_history = orders.exclude(accept=False)
    return render(request, 'control/list-orders.html', {'title': title, 'orders': orders_history})




@login_required
def order_detail(request, order_id):
    title = ' تفاصيل الطلبية '
    order = get_object_or_404(Order,pk=order_id)
    context = {
        'title': title,
        'order': order,
        'title': 'صفحة تفاصيل الطلبية',
        
    }
    return render(request, 'control/order-detail.html', context) 
        

@login_required
def order_accept(request, order_id):
    order = Order.objects.filter(pk=order_id).update(accept=True)
    
    return redirect('list_new_orders')





# start control panel

@login_required
def control_home(request):
    context = {
        'title': 'لوحة التحكم'
    }

    return render(request, 'control/control-home.html', context)



@login_required
def control_list_product(request):
    title = 'صفحة تعديل المنتجات'
    products = Product.objects.all()

    return render(request, 'control/control-list.html', {'title': title, 'products': products})
    


@login_required
def control_add_product(request):
    title = 'أضافة منتج'
    #ImageFormSet = modelformset_factory(Image, form=ImageForm, extra=3)
    AttributeFormSet = modelformset_factory(ProductAttribute, form=ProductAttributeForm)

    if request.method == 'POST':
        productForm = ProductForm(request.POST or None, request.FILES or None)
        #formset = ImageFormSet(request.POST or None, request.FILES or None)
        
        if productForm.is_valid():
            productForm.save()
            instance_product = productForm.save()

            for file in request.FILES.getlist('images'):
                instance = Image(product=get_object_or_404(Product,pk=instance_product.id),image=file)
                instance.save()
            
            return HttpResponseRedirect("/")


        else:
            return HttpResponse('postForm.errors, formset.errors')

    else:
        productForm = ProductForm()
        #formset = ImageFormSet(queryset=Image.objects.none())
        

    context = {
        'title': title, 
        'prodectForm': productForm,
        #'formset': formset,
    }
    return render(request, 'control/control-new-product.html', context)


class ProductUpdate(UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'control/control-edit-product.html'
    success_url = '/control/list-product/'

    def get_object(self):
        id_ = self.kwargs.get('product_id')
        return get_object_or_404(Product, id=id_)

@login_required
def control_update_image_album_product(request, product_id):
    title = 'تعديل البوم الصور '
    if request.method == 'POST':

        Image.objects.filter(id__in=request.POST.getlist('delete_list')).delete()
        if request.FILES.getlist('images'):
            for file in request.FILES.getlist('images'):
                instance = Image(product=get_object_or_404(Product,pk=product_id),image=file)
                instance.save()

        return redirect('control_list_product')
    else:
        product = get_object_or_404(Product,pk=product_id)
        context = {
            'title': title,
            'product': product,
        }
    return render(request, 'control/control-update-image-album-product.html', context)


@login_required
def control_add_product_attribute(request, product_id):
    title = 'أضافة قياس و لون '
    product = get_object_or_404(Product,pk=product_id)
    AttributeFormSet = modelformset_factory(ProductAttribute, form=ProductAttributeForm)

    if request.method == 'POST':
        formset = AttributeFormSet(request.POST, queryset=ProductAttribute.objects.filter(product__id=product.id))
        if formset.is_valid():
            instances = formset.save(commit=False)
            for instance in instances:
                instance.product_id = product.id
                instance.save()

            return redirect('add_product_attribute', product_id=product.id )
        else:
            return HttpResponse('erroe')
    
    else:

        formset = AttributeFormSet(queryset=ProductAttribute.objects.filter(product__id=product.id))
    context = {
        'title': title,
        'formsetattr': formset,
        'product': product,

    }
    return render(request, 'control/control-new-product-attribute.html', context)
@login_required
def control_add_product_discount(request, product_id):
    title = 'أضافة  حسم '
    product = get_object_or_404(Product,pk=product_id)
    if request.method == 'POST':
        form = ProductDiscountForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('control_list_product')
    else:
        form = ProductDiscountForm(initial = {'product': product_id})
    context = {
        'title': title,
        'product':product,
        'form': form,
    }
    return render(request, 'control/control-new-product-discount.html', context)
@login_required
def control_delete_product(request, product_id):
    title = 'حذف المنتج   '
    product = get_object_or_404(Product,pk=product_id)
    if request.method == 'POST':
        product.delete()
        return redirect('control_list_product')
    return render(request, 'control/confirm-delete.html', {'title': title, 'product': product})
    
    



def logout_view(request):
    logout(request)
    return redirect('login')


# end control panel




def product_detail(request, product_id):
    title = 'تفاصيل المنتج'
    product = get_object_or_404(Product,pk=product_id)
    context = {
        'title': title, 
        'product': product
    }
    return render(request, 'store/product-detail.html', context)

