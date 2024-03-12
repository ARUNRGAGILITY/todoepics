from django import template
from markdownx.utils import markdownify
from django.template import Template, Context
from app_web.models import Profile

register = template.Library()

@register.filter(name='render_markdown')
def render_markdown(text):
    return markdownify(text)

register = template.Library()

@register.filter(name='replace_variables')
def replace_variables(value, context):
    return value.format(**context)

register = template.Library()

@register.simple_tag(takes_context=True)
def render_markdown_with_context(context, content):
    # Preprocess the content by expanding variables in the context
    preprocessed_content = content.format(**context)
    # Apply markdownify to the preprocessed content
    markdown_output = markdownify(preprocessed_content)
    return markdown_output
register = template.Library()

@register.filter(name='markdown_with_context')
def markdown_with_context(value, context):
    template = Template(value)
    expanded_text = template.render(Context(context))
    return markdownify(expanded_text)



# app_web todoepics
@register.simple_tag(takes_context=True)
def has_admin_roles(context):
    request = context['request']
    user = request.user
    if user.is_authenticated:
        profile = Profile.objects.get(user=user)
        return profile.roles.filter(name__in=["Admin", "SiteAdmin"]).exists()
    return False