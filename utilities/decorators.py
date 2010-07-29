from functools import wraps
from django.template.context import Context
from django.shortcuts import render_to_response

def private_context(f):
    """
    Source at: http://djangosnippets.org/snippets/1687/
    
    Simple decorator which avoids the need to a) copy-and-paste code to force
    context variables into inclusion_tag templates and b) carefully avoid
    inclusion tag variables conflicting with global variables.
    
    Instead each inclusion tag will be called with a *copy* of the provided
    context variable and its results will be merged in to avoid leaking into
    the global context
    """

    @wraps(f)
    def private_context_wrapper(context, *args, **kwargs):
        c = Context(context)
        rc = f(c, *args, **kwargs)
        c.update(rc)
        return c

    return private_context_wrapper


def render_to(template):
    """
    Source at: http://djangosnippets.org/snippets/821/
    
    Decorator for Django views that sends returned dict to render_to_response function
    with given template and RequestContext as context instance.

    If view doesn't return dict then decorator simply returns output.
    Additionally view can return two-tuple, which must contain dict as first
    element and string with template name as second. This string will
    override template name, given as parameter

    Parameters:

     - template: template name to use
    """
    @wraps(func)
    def wrapper(request, *args, **kw):
        output = func(request, *args, **kw)
        if isinstance(output, (list, tuple)):
            return render_to_response(output[1], output[0], RequestContext(request))
        elif isinstance(output, dict):
            return render_to_response(template, output, RequestContext(request))
        return output
    return wrapper
