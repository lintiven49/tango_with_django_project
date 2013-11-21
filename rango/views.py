from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login, logout

from rango.bing_search import run_query
from rango.models import Category, Page
from rango.forms import CategoryForm, PageForm, UserForm, UserProfileForm

from datetime import datetime
# Create your views here.


def index(request):
    page_list = Page.objects.order_by('-views')[:5]

    context_dict = {'categories': get_category_list(), 'pages': page_list}
    if request.session.get('last_visit'):
        last_visit = request.session.get('last_visit')
        visits = request.session.get('visits')
        if (datetime.now() - datetime.strptime(last_visit[:-7], "%Y-%m-%d %H:%M:%S")).seconds > 30:
            request.session['visits'] = visits + 1
            request.session['last_visit'] = str(datetime.now())
    else:
        visits = 1
        request.session['last_visit'] = str(datetime.now())
        request.session['visits'] = 1
    context_dict['visits'] = visits
    return render(request, 'rango/index.html', context_dict)


def about(request):
    if request.session.get('visits'):
        visits = request.session.get('visits')
    return render(request, 'rango/about.html', {'visits': visits})


def category(request, category_name_url):
    category_name = _url_to_name(category_name_url)
    context_dict = {'category_name': category_name,
                    'category_name_url': category_name_url}
    try:
        category = Category.objects.get(name=category_name)
        pages = category.page_set.all()
        context_dict['pages'] = pages
        context_dict['category'] = category
    except Category.DoesNotExist:
        pass
    return render(request, 'rango/category.html', context_dict)


def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            return HttpResponseRedirect(reverse('rango:index'))
        else:
            print form.errors
    else:
        form = CategoryForm()
    return render(request, 'rango/add_category.html', {'form': form})


def add_page(request, category_name_url):
    category_name = _url_to_name(category_name_url)
    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            page = form.save(commit=False)
            category = Category.objects.get(name=category_name)
            page.category = category
            page.save()
            return HttpResponseRedirect(reverse('rango:category', args=(category_name_url,)))
        else:
            print form.errors
    else:
        form = PageForm()
    return render(request, 'rango/add_page.html',
                  {'category_name_url': category_name_url,
                   'category_name': category_name,
                   'form': form})


def register(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            #hash the password
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']
            profile.save()
            registered = True
        else:
            print user_form.errors, profile_form.errors
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()
    return render(request, 'rango/register.html',
                  {'user_form': user_form,
                   'profile_form': profile_form,
                   'registered': registered})


def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('rango:index'))
            return HttpResponse('disabled')
        print 'invalid login detail {0} {1}'.format(username, password)
        return render(request, 'rango/login.html', {'username': username})
    return render(request, 'rango/login.html')


@login_required
def restricted(request):
    return render(request, 'rango/restricted.html')


def search(request):
    result_list = []
    if request.method == 'POST':
        query = request.POST['query'].strip()
        if query:
            result_list = run_query(query)
    return render(request, 'rango/category.html', {'result_list': result_list})


def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('rango:index'))


def get_category_list():
    category_list = Category.objects.order_by('-likes')[:5]

    for category in category_list:
        category.url = _name_to_url(category.name)
    return category_list


def _url_to_name(category_name_url):
    return category_name_url.replace('_', ' ')


def _name_to_url(category_name):
    return category_name.replace(' ', '_')


