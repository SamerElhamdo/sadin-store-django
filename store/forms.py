from django import forms

from .models import Product, ProductAttribute, Image, Order, Discount
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


class LoginForm(forms.ModelForm):
    
    class Meta:
        model = User
        fields = ("username", "password")

        widgets = {

            'password': forms.PasswordInput(),
            
        }

        labels = {
            'username': _('اسم المستخدم'),
            'password': _('كلمة السر'),

        }
        help_texts = {
            'username': _('مطلوب بدون مسافات'),
            'password': _('كلمة السر حساسة لحالة الأحرف'),
            
        }




class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = ('category', 'title', 'price', 'img', )


        labels = {
            'category': _('النوع '),
            'title': _('أسم المنتج'),
            
            'price': _(' سعر المنتج'),
            'img': _('صورة المنتج'),

            
            
        }
        widgets = {

            'img': forms.FileInput(attrs={'style':'display: none;'}),
            
        }




class ProductDiscountForm(forms.ModelForm):
    
    class Meta:
        model = Discount
        fields = ('product', 'title', 'percentage', 'date',)
    

        widgets = {

            'product': forms.HiddenInput(),
            'date': forms.DateInput(format=('%d/%m/%Y'), 
                                             attrs={'type': 'date',

                                             'min': '2019-7-5',
                                             'placeholder':'أدخل تاريخ صالحاً'}),
 
        }

        labels = {
            'title': _('أسم الحسم'),
            'percentage': _('قيمة الحسم'),
            'date': _('تاريخ إنتهاء الحسم'),

        }

        help_texts = {
            'percentage': _('نسبة مئوية'),
            
        }

class ProductAttributeForm(forms.ModelForm):
    
    class Meta:
        model = ProductAttribute
        fields = ('product', 'category', 'attr',)

        widgets = {
            'product': forms.HiddenInput(),
            
        }


        labels = {
            'category': _(' النوع'),
            'attr': _(' القيمة'),
            


        }

        help_texts = {
            'category': _(' لون أو قياس'),
            'attr': _(' قيمة اللون أو القياس '),
            
            
        }

    def __init__(self, *args, **kwargs):
        super(ProductAttributeForm, self).__init__(*args, **kwargs)
        self.fields['product'].required = False

        


class ImageForm(forms.ModelForm):   
    class Meta:
        model = Image
        fields = ('image', )


        labels = {
            'image': _('أرفع الصورة '),


        }



class OrderForm(forms.ModelForm):
    
    class Meta:
        model = Order
        fields = ('product', 'quantity', 'full_name', 'phonenumber', 'color', 'size')


        widgets = {
            'quantity': forms.TextInput(attrs={'min':'1',
            'max':'999',
            'type': 'number'}),
            'product': forms.HiddenInput(),
            'color': forms.HiddenInput(),
            'size': forms.HiddenInput(),
            
        }
        labels = {
            'quantity': _('الكمية'),
            'full_name': _('الأسم الكامل'),
            'phonenumber': _('رقم الهاتف'),
            
        }
        help_texts = {
            'phonenumber': _('أدخل رقم هاتف صحيح للتواصل معكم'),
        }

