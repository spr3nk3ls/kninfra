from django.conf.urls.defaults import *

from kn.fotos import views
from kn.fotos import api

urlpatterns = patterns('',
        # TODO add fallback for old foto links
        # TODO change wiki links, etc.
        url(r'^foto/admin/?$',
            views.fotoadmin_move, name='fotoadmin-move'),
        url(r'^foto/admin/create/?$',
            views.fotoadmin_create_event, name='fotoadmin-create-event'),
        url(r'^fotos/api/?$',
            api.view, name='fotos-api'),
        url(r'^fotos/?$',
            views.fotos, name='fotos'),
        # NOTE keep up to date with media/fotos.js
        url(r'^foto/(?P<cache>[^/]+)/(?P<path>.*)$',
            views.cache, name='fotos-cache'),
)

# vim: et:sta:bs=2:sw=4:
