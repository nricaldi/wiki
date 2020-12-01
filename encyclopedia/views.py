from django.shortcuts import render, redirect
from django.contrib import messages
from random import randint
from . import util

from markdown2 import Markdown

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title): 
    # Get entry
    entry = util.get_entry(title)

    markdowner = Markdown()
    entry = markdowner.convert(entry)

    # Check if entry exists
    if entry:
        # Save data into context dictionary to use in template
        context = {
            "title": title,
            "markdown": entry
        }
        
        return render(request, "encyclopedia/entry.html", context)
    else: 
        # If no entry exists render the error page
        return render(request, "encyclopedia/error.html")

def search(request):

    # Using our util function to save all entries in a variable
    query_list = util.list_entries()
    # Getting the search query from the form
    query = request.GET['q']

    does_contain = False    
    if filter_func(query_list, query):
        query_list = filter_func(query_list, query)
        does_contain = True

    context = {
        "results": query_list,
        "query": query,
        "contains": does_contain
    }
    return render(request, "encyclopedia/results.html", context)

def create(request):

    # Check if the request was a post request AKA submitting a form
    if request.method == "POST":
        # Get all entries
        all_entries = util.list_entries()
        # Retrieve data from form
        title = request.POST['title']
        content = request.POST['content']

        # Check if an entry has the same title
        if title in all_entries: 
            # Add error messages to form    
            messages.error(request, 'An entry with this title already exists.')
            return redirect("create")
        else:
            util.save_entry(title, content)
            return redirect('entry', title)
    else:
        return render(request, "encyclopedia/create.html")


def edit(request, title):

    # Check if the request was a post request AKA submitting a form
    if request.method == "POST":
        # Get all entries
        all_entries = util.list_entries()

        # Retrieve data from form
        form_title = request.POST['title']
        content = request.POST['content']

        # # Check if an entry has the same title
        # if title in all_entries: 
        #     # Add error messages to form    
        #     messages.error(request, 'An entry with this title already exists.')
        #     return render(request, "edit", title)
        # else:
        util.save_entry(form_title, content)
        return redirect('entry', title)

    else:
        # Get current entry
        entry = util.get_entry(title)
        
        # Save data into context dictionary to use in template
        context = {
            "title": title,
            "markdown": entry,
        }
        return render(request, "encyclopedia/edit.html", context)


def random(request):
    # Get all the entries into an array 
    all_entries = util.list_entries()
    # Choose a random number between 0 and the length of the array
    random = randint(0, len(all_entries))
    # Use the random number to select a random enrty in the array
    random_entry = all_entries[random]

    return redirect("entry", random_entry)

# Could not find a pre built filter function so i made a custom one
# The method accepts 2 parameters; list: the list to filter through, q: the query we are using to filter with
def filter_func(list, q):
    # Make new list to return with filtered entries
    result = []

    # Loop through the list and test if the query is in the current string item
    for i in range(len(list)):
        # print(list[i])
        # print(q)
        # Convert item and query to uppercase to see if the item contains the query
        if q.upper() in list[i].upper():
            # print(True)
            # If the item contains the query then it will be appended to the new list
            result.append(list[i])
        # else: 
        #     print(False)

    return result


