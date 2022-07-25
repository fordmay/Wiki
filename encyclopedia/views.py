import random
import markdown
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import render
from django import forms
from django.urls import reverse

from . import util


class Entry(forms.Form):
    title = forms.CharField(label='Title', widget=forms.TextInput(attrs={'class': 'form-control w-75'}))
    content = forms.CharField(label='Content', widget=forms.Textarea(attrs={'class': 'form-control w-75'}))


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry_page(request, title):
    if util.check_title_without_register(title) is not None:
        entry = util.get_entry(title)
        entry_html = markdown.markdown(entry)
        return render(request, "encyclopedia/entry_page.html", {
            "title": title,
            "entry_html": entry_html
        })
    else:
        return HttpResponseNotFound()


def search(request):
    if request.method == 'POST':
        query = request.POST['q']
        if util.check_title_without_register(query) is not None:
            return HttpResponseRedirect(reverse("entry_page", args=(util.check_title_without_register(query),)))
        else:
            results = []
            for entry in util.list_entries():
                if entry.lower().count(query.lower()) > 0:
                    results.append(entry)
            return render(request, "encyclopedia/search.html", {
                "results": results
            })


def create_new_page(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = Entry(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            title = form.cleaned_data["title"]
            if util.check_title_without_register(title) is None:
                content = form.cleaned_data["content"]
                util.save_entry(title, content)
                # redirect to a new URL:
                return HttpResponseRedirect(reverse("entry_page", args=(title,)))
            else:
                messages.add_message(request, messages.WARNING, 'Entry already exists with the provided title.')
    # if a GET (or any other method) we'll create a blank form
    else:
        form = Entry()
    return render(request, "encyclopedia/create_new_page.html", {
        "form": form
    })


def edit_page(request, title):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = Entry(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            content = form.cleaned_data["content"]
            util.save_entry(title, content)
            # redirect to a new URL:
            return HttpResponseRedirect(reverse("entry_page", args=(title,)))
    # if a GET (or any other method) we'll create a blank form
    else:
        if util.check_title_without_register(title) is not None:
            content = util.get_entry(title)
            # adds data to forms
            form = Entry({'title': title, 'content': content})
            # locks field title
            form.fields['title'].widget.attrs['readonly'] = True
            return render(request, "encyclopedia/edit_page.html", {
                "form": form,
                "title": title
            })
        else:
            return HttpResponseNotFound()


def random_page(request):
    title = random.choice(util.list_entries())
    return HttpResponseRedirect(reverse("entry_page", args=(title,)))
