from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from django.contrib.auth.views import LoginView
from . import views


urlpatterns = [
    path('', views.home_view, name='home_view'),
    path('control/login/', views.login_user, name='login'),
    path('control/logout/', views.logout_view, name='logout'),
    path('control/home/', views.control_home, name='control_home'),
    path('home/<category_id>', views.category_list, name='category_list'),
    path('control/list-product/', views.control_list_product, name='control_list_product'),
    path('control/add-product/', views.control_add_product, name='new_product'),
    path('control/edit-product/<product_id>', views.ProductUpdate.as_view(), name='edit_product'),
    path('control/edit-album-product/<product_id>', views.control_update_image_album_product, name='edit_album_product'),
    path('control/delete-product/<product_id>', views.control_delete_product, name='delete_product'),
    path('control/add-product-attribute/<product_id>', views.control_add_product_attribute, name='add_product_attribute'),
    path('control/list-new-orders/', views.list_new_orders, name='list_new_orders'),
    path('control/list-history-orders/', views.list_history_orders, name='list_history_orders'),
    path('control/order-detail/<order_id>', views.order_detail, name='order_detail'),
    path('control/order-accept/<order_id>', views.order_accept, name='order_accept'),
    path('control/add-product-discount/<product_id>', views.control_add_product_discount, name='add_product_discount'),
    path('product-detail/<product_id>', views.product_detail, name='product_detail'),
    path('new-order/<product_id>', views.order_form, name='order_form'),
    path('confirm-order/<order_id>', views.confirm_order, name='confirm_order'),
    
    
    
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
