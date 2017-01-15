from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.utils.translation import ugettext_lazy as _

from kn.leden import views, api, graphs

urlpatterns = [
    url(r'^$',
    login_required(TemplateView.as_view(template_name='leden/home.html')),
               name='smoelen-home'),
    url(_(r'^gebruikers/(?:p/(?P<page>[0-9]+)/)?$'),
        views.user_list, name='user-list'),
    url(_(r'^naamdrager/(?P<name>[^/]+)/$'),
        views.entity_detail, name='entity-by-name'),
    url(_(r'^id/(?P<_id>[^/]+)/$'),
        views.entity_detail, name='entity-by-id'),
    url(_(r'^gebruiker/(?P<name>[^/]+)/$'),
        views.entity_detail, {'type': 'user'}, name='user-by-name'),
    url(_(r'^gebruiker/id/(?P<_id>[^/]+)/$'),
        views.entity_detail, {'type': 'user'}, name='user-by-id'),
    url(_(r'^gebruiker/id/(?P<_id>[^/]+)/reset-wachtwoord$'),
        views.user_reset_password, name='user-reset-password'),
    url(_(r'^groep/(?P<name>[^/]+)/$'),
        views.entity_detail, {'type': 'group'}, name='group-by-name'),
    url(_(r'^groep/id/(?P<_id>[^/]+)/$'),
        views.entity_detail, {'type': 'group'}, name='group-by-id'),
    url(_(r'^brand/(?P<name>[^/]+)/$'),
        views.entity_detail, {'type': 'brand'}, name='brand-by-name'),
    url(_(r'^brand/id/(?P<_id>[^/]+)/$'),
        views.entity_detail, {'type': 'brand'}, name='brand-by-id'),
    url(_(r'^stempel/(?P<name>[^/]+)/$'),
        views.entity_detail, {'type': 'tag'}, name='tag-by-name'),
    url(_(r'^stempel/id/(?P<_id>[^/]+)/$'),
        views.entity_detail, {'type': 'tag'}, name='tag-by-id'),
    url(_(r'^studie/(?P<name>[^/]+)/$'),
        views.entity_detail, {'type': 'tag'}, name='study-by-name'),
    url(_(r'^studie/id/(?P<_id>[^/]+)/$'),
        views.entity_detail, {'type': 'study'}, name='study-by-id'),
    url(_(r'^instituut/(?P<name>[^/]+)/$'),
        views.entity_detail, {'type': 'institute'},
        name='institute-by-name'),
    url(_(r'^instituut/id/(?P<_id>[^/]+)/$'),
        views.entity_detail, {'type': 'institute'},
        name='institute-by-id'),
    url(_(r'^bouwjaar/$'),
        views.years_of_birth, name='years-of-birth'),
    url(_(r'^bouwjaar/(?P<year>\d+)/$'),
        views.entities_by_year_of_birth, name='entities-by-year-of-birth'),
    url(_(r'^smoel/(?P<name>[^.]+).jpg$'),
        views.user_smoel, name='user-smoel'),
    url(_(r'^geenalcohol/$'),
        views.users_underage, name='users-underage'),
    url(_(r'^ik/?$'), views.ik, name='ik'),
    url(_(r'^ik/balans/?$'), views.ik_balans, name='ik-balans'),
    url(_(r'^ik/wachtwoord$'), views.ik_chpasswd, name="chpasswd"),
    url(_(r'^ik/wachtwoord/villanet/$'), views.ik_chpasswd_villanet,
        name="chpasswd-villanet"),
    url(_(r'^ik/smoel$'), views.ik_chsmoel, name="ik-chsmoel"),
    url(_(r'^api/users$'), views.api_users),
    url(_(r'^api/?$'), api.view, name='leden-api'),
    url(_(r'^ik/openvpn/$'), views.ik_openvpn, name="ik-openvpn"),
    url(_(r'^ik/openvpn/(?P<filename>.+(exe|zip))$'), views.ik_openvpn_download,
                name="ik-openvpn-download"),
    url(_(r'^secretariaat/inschrijven$'),
        views.secr_add_user, name='secr-add-user'),
    url(_(r'^secretariaat/update-site-agenda/$'),
        views.secr_update_site_agenda, name='secr-update-site-agenda'),
    url(_(r'^secretariaat/addgroup$'),
        views.secr_add_group, name='secr-add-group'),
    url(_(r'^secretariaat/notes$'),
        views.secr_notes, name='secr-notes'),
    url(_(r'^relaties/(?P<_id>[^/]+)/beindig$'),
        views.relation_end, name='relation-end'),
    url(_(r'^relaties/begin$'),
        views.relation_begin, name='relation-begin'),
    url(_(r'^tags/tag$'),
        views.tag, name='tag'),
    url(_(r'^tags/untag$'),
        views.untag, name='untag'),
    url(_(r'^noteer$'),
        views.note_add, name='add-note'),

    url(_(r'^statistieken/?$'), login_required(TemplateView.as_view(
            template_name='leden/stats.html')), name='stats'),
    url(_(r'^grafiek/(?P<graph>[-a-z/]+)\.(?P<ext>[a-z]+)/?$'),
        graphs.view, name='graphs'),

    # style
    url(_(r'^styles/leden/$'),
        TemplateView.as_view(template_name='leden/base.css',
                             content_type='text/css'), name='leden-base'),

    # for now, just shows the guessed language
    url(_(r'^taal$'),
        views.language, name='taal'),
        ]

# vim: et:sta:bs=2:sw=4:
