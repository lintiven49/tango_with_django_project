import os
#from rango.models import Page, Category


def populate():
    python_cat = add_cat('Python', views=128, likes=64)
    python_titles = ("Official Python Tutorial", "How to Think like a Computer Scientist",
                     "Learn Python in 10 Minutes")
    python_urls = ("http://docs.python.org/2/tutorial/",
                   "http://www.greenteapress.com/thinkpython/",
                   "http://www.korokithakis.net/tutorials/python/")
    for t, u in zip(python_titles, python_urls):
        add_page(python_cat, t, u)

    django_cat = add_cat("Django", views=64, likes=32)
    django_titles = ("Official Django Tutorial", "Django Rocks", "How to Tango with Django")
    django_urls = ("https://docs.djangoproject.com/en/1.5/intro/tutorial01/",
                   "http://www.djangorocks.com/",
                   "http://www.tangowithdjango.com/")
    for t, u in zip(django_titles, django_urls):
        add_page(django_cat, t, u)

    frame_cat = add_cat("Other Frameworks", views=32, likes=16)
    frame_titles = ("Bottle", "Flask")
    frame_urls = ("http://bottlepy.org/docs/dev/",
                  "http://flask.pocoo.org")
    for t, u in zip(frame_titles, frame_urls):
        add_page(frame_cat, t, u)

    for c in Category.objects.all():
        for p in c.page_set.all():
            print "- {0} - {1}".format(str(c), str(p))


def add_page(cat, title, url, views=0):
    p = Page.objects.get_or_create(category=cat, title=title, url=url, views=views)[0]
    return p


def add_cat(name, views, likes):
    c = Category.objects.get_or_create(name=name, views=views, likes=likes)[0]
    return c

if __name__ == '__main__':
    print "Starting Rango population script..."
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tango_with_django_project.settings')
    from rango.models import Category, Page
    populate()
