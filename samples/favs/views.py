from favs.models import Thing

from django.views import View
from django.views import generic
from django.shortcuts import render

from owner.util import OwnerListView, OwnerDetailView, OwnerCreateView, OwnerUpdateView, OwnerDeleteView

class ThingListView(OwnerListView):
    model = Thing
    template_name = "favs/list.html"

    def get(self, request) :
        thing_list = Thing.objects.all()
        favorites = list()
        if request.user.is_authenticated:
            # rows = [{'id': 2}]  (A list of rows)
            rows = request.user.favorite_things.values('id')  
            favorites = [ row['id'] for row in rows ]
        ctx = {'thing_list' : thing_list, 'favorites': favorites}
        return render(request, self.template_name, ctx)

class ThingDetailView(OwnerDetailView):
    model = Thing
    template_name = "favs/detail.html"

class ThingCreateView(OwnerCreateView):
    model = Thing
    fields = ['title', 'text']
    template_name = "favs/form.html"

class ThingUpdateView(OwnerUpdateView):
    model = Thing
    fields = ['title', 'text']
    template_name = "favs/form.html"

class ThingDeleteView(OwnerDeleteView):
    model = Thing
    template_name = "favs/delete.html"

# Below this line, we see raw sql...   With great power comes great responsibility
# https://docs.djangoproject.com/en/2.1/topics/db/sql/

class RawSQLListView(OwnerListView):
    template_name = "favs/rawsql.html"

    def get(self, request) :
        if not request.user.is_authenticated:
            thing_list = Thing.objects.all()
        else:
            sql = """SELECT *, favs_fav.user_id AS FAV_USER_ID FROM favs_thing 
                LEFT JOIN favs_fav ON favs_thing.id = favs_fav.thing_id
                AND favs_fav.user_id = """ + str(self.request.user.id)
            print(sql)
            thing_list = Thing.objects.raw(sql)
        ctx = {'thing_list' : thing_list}
        return render(request, self.template_name, ctx)

# https://stackoverflow.com/questions/2314920/django-show-log-orm-sql-calls-from-python-shell
# pip install django-extensions
# ./manage.py shell_plus --print-sql

# Notes from the shell:
# sql = "SELECT *, favs_fav.user_id AS FAV_USER_ID FROM favs_thing LEFT JOIN favs_fav ON favs_thing.id = favs_fav.thing_id AND favs_fav.user_id = 1"
# thing_list2 = Thing.objects.raw(sql)
# row0 = thing_list2[0]
# row0.FAV_USER_ID
# row1 = thing_list2[1]
# row1.FAV_USER_ID

