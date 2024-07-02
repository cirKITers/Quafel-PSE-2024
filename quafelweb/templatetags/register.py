from django import template

register = template.Library()

@register.inclusion_tag('labeled_button.html', name='labeled_button')
def labeled_function_template(design : str, **kwargs):
  return {
    'design' : design,
    'html_class' : " ".join(kwargs.get("class", [])),
    'html_id' : kwargs.get('id', '')
  }