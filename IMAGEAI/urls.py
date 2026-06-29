"""
URL configuration for IMAGEAI project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from imageapp.views.image.views import SignUpView

urlpatterns = [
    path('admin/', admin.site.urls),
   
    path('accounts/signup/', SignUpView.as_view(), name='signup'),
    # ログイン・ログアウト用のDjango標準URLを有効化
    
    path('accounts/', include('django.contrib.auth.urls')),
    # ルートURL（/）をプラットフォーム（home.html）に設定
    
    # 今回追加したサインアップ用URL
    path('accounts/signup/', SignUpView.as_view(), name='signup'),
    
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('', include('imageapp.urls')),# ... 既存のURL ...
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
