"""
Definition of views.
"""

from datetime import datetime
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse

def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/index.html',
        {
            'title':'Home Page',
            'year':datetime.now().year,
        }
    )

def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        {
            'title':'Contact',
            'message':'Your contact page.',
            'year':datetime.now().year,
        }
    )

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        {
            'title':'About',
            'message':'Your application description page.',
            'year':datetime.now().year,
        }
    )

def manage(request):
    """ All-encompassing view for management stuff """
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/manage.html',
        {
            'title':'Dashboard',
        }
    )

def account(request):
    """ View for account management """
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/account.html',
        {
            'title':'Account',
        }
    )

def calendar(request):
    """ View for displaying calendar """
    assert isinstance(request, HttpRequest)
    if request.user.is_authenticated:
        return render(
            request,
            'app/calendar.html',
            {
                'title':'Calendar (editable)',
            }
        )
    else:
        return render(
            request,
            'app/calendar.html',
            {
                'title':'Calendar',
            }
        )



