from django.urls import path, re_path
from random import randint
from django import forms
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.shortcuts import redirect
# from django.urls import reverse
import markdown2
# from markdown2 import Markdown

from . import util


class SearchForm(forms.Form):
    q = forms.CharField(label="Search Page")


class PageForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea)

    # Enter the title
    # Write the text and click Save

# Form(initial=dict(field_name=value)


def index(request):
    if request.method == "POST":
        form = SearchForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["q"].strip().lower()

            entries = util.list_entries()
            result = []
            result_OK = False
            for entrie in entries:
                if entrie.lower().find(title) != -1:
                    result.append(entrie)
                    if entrie.lower() == title:
                        result_OK = True

            if len(result) <= 1 or result_OK:
                result = util.get_entry(title)
                if result == None:
                    content = f"Сторінки <b>{title}</b> у енциклопедії Wiki не знайдено.\n"
                else:
                    content = markdown2.markdown(result).strip()

                return render(request, "encyclopedia/article.html", {
                    "form": form,
                    "title": title,
                    "content": content
                })

            else:
                return render(request, "encyclopedia/search.html", {
                    "form": form,
                    "entries": result
                })
        else:
            return render(request, "encyclopedia/index.html", {
                "form": form,
                "entries": util.list_entries()
            })

    return render(request, "encyclopedia/index.html", {
        "form": SearchForm(),
        "entries": util.list_entries()
    })


def article(request, title, randomPage=False):
    if request.method == "POST":
        formPage = PageForm(request.POST)
        if formPage.is_valid():
            content = formPage.cleaned_data["content"]
            title = content.split('\n')[0][1:-1].strip()
            util.save_entry(title, content.encode(encoding="utf-8"))
            return render(request, "encyclopedia/article.html", {
                "form": SearchForm(),
                "title": title,
                "content": markdown2.markdown(content).strip()
            })
    else:
        """
        Returns a list of all names of encyclopedia entries.
        """
        if randomPage:
            entries = util.list_entries()
            title = entries[randint(0, len(entries) - 1)]

        result = util.get_entry(title)
        if result == None:
            content = f"Сторінки <b>{title}</b> у енциклопедії Wiki не знайдено.\n"
        else:
            content = markdown2.markdown(result)

        return render(request, "encyclopedia/article.html", {
            "form": SearchForm(),
            "title": title,
            "content": content
        })


def createNewPage(request):
    if request.method == "POST":
        formPage = PageForm(request.POST)
        if formPage.is_valid():
            content = formPage.cleaned_data["content"]
            title = content.split('\n')[0][1:-1].strip().lower()

            entries = util.list_entries()
            result = []
            result_OK = False
            for entrie in entries:
                if entrie.lower().find(title) != -1:
                    result.append(entrie)
                    if entrie.lower() == title:
                        result_OK = True

            if len(result) == 1 or result_OK:
                message = f'Стаття з назвою "<b>{title.capitalize()}</b>" у енциклопедії Wiki вже існує.\n'
                return render(request, "encyclopedia/message.html", {
                    "form": SearchForm(),
                    "title": "New Page",
                    "content": message
                })
            else:
                util.save_entry(title.capitalize(),
                                content.encode(encoding="utf-8"))
                return render(request, "encyclopedia/article.html", {
                    "form": SearchForm(),
                    "title": title,
                    "content": markdown2.markdown(content).strip()
                })
        else:
            return render(request, "encyclopedia/message.html", {
                "form": SearchForm(),
                "title": "Create new Article",
                "content": "Введені дані не валідні"
            })

    return render(request, "encyclopedia/new.html", {
        "formPage": PageForm()
    })


def editPage(request, title):
    content = util.get_entry(title)
    formEdit = PageForm(initial={'content': content})
    return render(request, "encyclopedia/edit.html", {
        "title": title,
        "formPage": formEdit
    })
