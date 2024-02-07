from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from . import util
import markdown2

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    content = util.get_entry(title)
    if content is None:
        return render(request, "encyclopedia/error.html", {
            "message": "The requested page was not found."
        })
    else:
        html_content = markdown2.markdown(content)
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": html_content
        })

def search(request):
    query = request.GET.get('q', '')
    entries = util.list_entries()
    matching_entries = [entry for entry in entries if query.lower() in entry.lower()]

    if query in entries:
        return HttpResponseRedirect(reverse('entry', kwargs={'title': query}))
    else:
        return render(request, "encyclopedia/search_results.html", {
            "entries": matching_entries,
            "query": query
        })

def create_entry(request):
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")
        if util.get_entry(title) is not None:
            messages.error(request, "An entry with this title already exists.")
            return render(request, "encyclopedia/create_entry.html", {
                "title": title,
                "content": content
            })
        else:
            util.save_entry(title, content)
            return HttpResponseRedirect(reverse("entry", kwargs={"title": title}))
    else:
        return render(request, "encyclopedia/create_entry.html")