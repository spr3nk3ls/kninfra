from html2text import HTML2Text

import django.core.mail
import django.template
import django.template.loader
from django.conf import settings
from django.template.loader_tags import BlockNode
from django.utils import translation
from django.utils.translation import ugettext as _

import kn.leden.entities as Es

# https://stackoverflow.com/a/7088472
try:
    from html import unescape  # python 3.4+
except ImportError:
    from HTMLParser import HTMLParser  # python 2.x
    unescape = HTMLParser().unescape

# TODO translate e-mail to the language preferred by the recipient


def render_then_email(
        template_name,
        to,
        ctx={},
        cc=[],
        bcc=[],
        from_email=None,
        reply_to=None,
        headers=None):
    """ Render an e-mail from a template and send it. """
    # What language to send the mail in?
    language = settings.LANGUAGE_CODE
    if isinstance(to, Es.User):
        language = to.preferred_language

    # Normalize arguments
    addrs = {'to': to, 'cc': cc, 'bcc': bcc}
    for what in ('to', 'cc', 'bcc'):
        if not isinstance(addrs[what], (tuple, list)):
            addrs[what] = [addrs[what]]
        addrs[what] = [x.canonical_full_email if isinstance(x, Es.User) else x
                       for x in addrs[what]]
    if headers is None:
        headers = {}

    # Render template
    request_language = translation.get_language()
    translation.activate(language)
    try:
        template = django.template.loader.get_template(template_name)
        rendered_nodes = {}
        ctx['BASE_URL'] = settings.BASE_URL
        context = django.template.Context(ctx)
        for node in template.nodelist:
            if isinstance(node, BlockNode):
                rendered_nodes[node.name] = node.render(context)
    finally:
        translation.activate(request_language)
    if 'subject' not in rendered_nodes:
        raise KeyError(_("subject blok mist"))
    if 'plain' not in rendered_nodes and 'html' not in rendered_nodes:
        raise KeyError(_("html of plain blok mist"))

    # Set up e-mail
    if addrs['cc']:
        headers['CC'] = ', '.join(addrs['cc'])
    if reply_to:
        headers['Reply-To'] = reply_to
    if not from_email:
        from_email = rendered_nodes.get('from',
                                        settings.DEFAULT_FROM_EMAIL).strip()

    if 'plain' in rendered_nodes:
        plain = rendered_nodes['plain'].strip()
    else:
        h = HTML2Text()
        h.ignore_links = True
        plain = h.handle(rendered_nodes['html']).strip()

    email = django.core.mail.EmailMultiAlternatives(
        unescape(rendered_nodes['subject'].strip()),
        plain,
        from_email,
        addrs['to'],
        headers=headers,
        bcc=(addrs['cc'] + addrs['bcc'])
    )

    if 'html' in rendered_nodes:
        email.attach_alternative(rendered_nodes['html'].strip(), "text/html")

    # And send!
    email.send()

# vim: et:sta:bs=2:sw=4:
