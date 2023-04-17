from django.urls import path
from . import views
from .views import (
    PostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    UserPostListView,
    TicketCreateView,
    TicketDetailView,
    TicketDetailView1,
    MpesaCreateView,
    # PayConfirmation,
    # PostDetailView2

    # CreateCheckoutSessionView,

    
)
urlpatterns = [
    path('', PostListView.as_view(), name='events-home'),
    path('user/<str:username>', UserPostListView.as_view(), name='user-posts'),
    path('post/<str:pk>/',  views.PostDetailView, name='post_detail'),
    # path('post2/<pk>/<uuid>/',  PostDetailView2.as_view(), name='post_detail2'),
    # path('post/<pk>/<uuid>/',  PayConfirmation.as_view(), name='pay_confirm'),

    # path('post/<pk>/',  views.PostDetailView, name='post_detail'),
    #path('ticket/<int:pk>/',  TicketDetailView.as_view(), name='ticket_detail'),
    path('ticket/<int:pk>/',  TicketDetailView, name='ticket_detail'),
    path('ticket/<int:ticket_no>/',  TicketDetailView, name='ticket_detail3'),
    # path('ticket/<int:pk>/',  TicketDetailView1, name='ticket_detail1'),
    # path('post/<pk>/update', PostUpdateView.as_view(), name='post-update'),
    path('post/<pk>/update', PostUpdateView.as_view(), name='post-update'),
    path('post/<pk>/delete', PostDeleteView.as_view(), name='post-delete'),
    path('post/', PostCreateView.as_view(), name='post-create'),
    path('ticket/new/', TicketCreateView.as_view(), name='ticket-create'),
    # path('create-checkout-session/<pk>/', CreateCheckoutSessionView.as_view(), name="create-checkout-session"),
    path('about/', views.about, name='events-about'),
    path('cancel/', views.cancel, name='cancel'),
    path('success/', views.success, name='success'),
    path('mpesa/', MpesaCreateView.as_view(), name='mpesa'),
    # MPESA URLS
    path('access/token', views.getAccessToken, name='get_mpesa_access_token'),
    path('order/', views.TicketConfirmation, name='order'),
    path('stkinfo/', views.StkInfo, name='stkinfo'),
    
    path('c2b/register', views.register_urls, name="register_mpesa_validation"),
    path('c2b/confirmation', views.confirmation, name="confirmation"),
    path('c2b/validation', views.validation, name="validation"),
    path('c2b/callback', views.call_back, name="call_back"),

    path('b2c/queue', views.call_back, name="b2cq"),
    path('b2c/result', views.call_back, name="b2cr"),
    # path('b2c/trial', views.b2ctemplate, name="b2ctrial"),
    path('b2c/', views.b2c, name="b2c"),
    # path('b2c2/', views.b2c2, name="b2c"),

    path('totals/', views.event_totals, name="totals"),
    # path('totals2/', views.b2c_totals, name="totals2"),

    path('detail1/', views.detailtry, name="detailtry"),
   
]
