from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.views.generic.simple import direct_to_template
from semiocoder import settings
from semiocoder.core.libs import getAARFeed

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

# FIXME: probleme de redirection suite a connexion

urlpatterns = patterns('',

    url(r'^$', direct_to_template, { 'template': 'home.html', 'extra_context' : { 'news' : getAARFeed(), }, }, name="home"),
    url(r'^contact/$', direct_to_template, {'template': 'contact.html'}, name="contact"),
    url(r'^about/$', direct_to_template, {'template': 'about.html'}, name="about"),
    url(r'^%s$' % settings.LOGIN_URL[1:], 'django.contrib.auth.views.login', {'template_name' : 'registration/login.html', 'extra_context' : { 'next' : '/', }, }, name="login"),
    url(r'^%s$' % settings.LOGOUT_URL[1:], 'django.contrib.auth.views.logout', {'next_page' : '/'}, name="logout"),
    url(r'^user/change_password$', 'django.contrib.auth.views.password_change', {'template_name' : 'registration/password_change.html', 'post_change_redirect' : '/'}),
    (r'^', include('semiocoder.encoder.urls')),
    (r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
#    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    