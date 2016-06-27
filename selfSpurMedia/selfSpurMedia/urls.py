from django.conf.urls import patterns, include, url
from templateEngine.views import home, product, products, register, contact, spur, \
    dashboard, subscriber, logout_now, login, unblock, block, active, package, \
    package_request, submit_spur, other_request
from django.conf.urls.static import static
from django.conf import settings

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
                       # Examples:
                       # url(r'^$', 'selfSpurMedia.views.home', name='home'),
                       # url(r'^blog/', include('blog.urls')),

                       url(r'^admin/', include(admin.site.urls)),
                       # common URLS start
                       url(r'^$', view=home, name='home'),
                       url(r'^product/', view=product, name='product'),
                       url(r'^products/', view=products, name='products'),
                       url(r'^register/', view=register, name='register'),
                       url(r'^logout/', view=logout_now, name='logout'),
                       url(r'^login/', view=login, name='login'),
                       url(r'^spur/', view=spur, name='spur'),
                       url(r'^submit-spur/', view=submit_spur, name='submit-spur'),
                       url(r'^contact/', view=contact, name='contact'),
                       # common URLS end

                       # admin URLS start
                       url(r'^dashboard/', view=dashboard, name='dashboard'),
                       url(r'^subscriber/', view=subscriber, name='subscriber'),
                       url(r'^unblock/([0-9]+)/', view=unblock, name='unblock'),
                       url(r'^block/([0-9]+)/', view=block, name='block'),
                       url(r'^active/([0-9]+)/', view=active, name='active'),
                       url(r'^package/', view=package, name='package'),
                       url(r'^package_request/', view=package_request, name='package_request'),
                       url(r'^other_request/', view=other_request, name='other_request'),
                       # admin URLS end

                       )

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
