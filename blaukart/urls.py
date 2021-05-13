"""blaukart URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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

#from django.contrib import admin
from django.urls import path, include

from django.views.generic import TemplateView
from django.conf.urls import (handler400, handler403, handler404, handler500)
from django.conf.urls.i18n import i18n_patterns

import debug_toolbar

urlpatterns = [
	#path('managers/', admin.site.urls, name='managers'),
	path('__debug__/', include(debug_toolbar.urls)),
	#path('', TemplateView.as_view(template_name="shop/index.html"), name="home"),
	path('', include('modules.shop.urls')),
]

# Multi-Lingual URL
urlpatterns += i18n_patterns(
	#path('', TemplateView.as_view(template_name="shop/index.html"), name="home"),
	path('', include('modules.shop.urls')),
)

# Error Handlers:
handler404 = 'modules.appcore.accounts.views.error404'
# handler400 = 'modules.appcore.accounts.error_views.bad_request'
# handler403 = 'modules.appcore.accounts.error_views.permission_denied'
# handler404 = 'django.views.defaults.page_not_found'
handler500 = 'modules.appcore.accounts.views.error500'
