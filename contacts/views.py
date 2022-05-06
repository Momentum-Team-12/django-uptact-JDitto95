from django.shortcuts import render, redirect, get_object_or_404
from .models import Contact
from .forms import ContactForm, NoteForm, Note


# Create your views here.
def contact_detail(request, pk):
    contact = get_object_or_404(Contact, pk=pk)
    # notes = Note.objects.filter(contact_id=contact.pk)
    form = NoteForm()
    return render(request, "contacts/contact_detail.html", {"contact": contact }) # this what I am trying to do at line 71-81

def list_contacts(request):
    contacts = Contact.objects.all()
    return render(request, "contacts/list_contacts.html",
                {"contacts": contacts})


def add_contact(request):
    if request.method == 'GET':
        form = ContactForm()
    else:
        form = ContactForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect(to='list_contacts')

    return render(request, "contacts/add_contact.html", {"form": form})


def edit_contact(request, pk):
    contact = get_object_or_404(Contact, pk=pk)
    if request.method == 'GET':
        form = ContactForm(instance=contact)
    else:
        form = ContactForm(data=request.POST, instance=contact)
        if form.is_valid():
            form.save()
            return redirect(to='list_contacts')

    return render(request, "contacts/edit_contact.html", {
        "form": form,
        "contact": contact
    })


def delete_contact(request, pk):
    contact = get_object_or_404(Contact, pk=pk)
    if request.method == 'POST':
        contact.delete()
        return redirect(to='list_contacts')

    return render(request, "contacts/delete_contact.html",
                  {"contact": contact})
    
    
def add_note(request, pk):
    # get the associated contact
    contact = get_object_or_404(Contact, pk=pk)
    # We need a form!
    form = NoteForm(data=request.POST)
    if form.is_valid():
        note = form.save(commit=False)
        note.contact = contact 
        note.save()
        return redirect(to="contact_detail", pk=pk)

    return render(
        request, "contacts/contact_detail.html", {"form": form, "contact": contact}
    )


def Notes(request, pk):
    contact = get_object_or_404(Contact, pk=pk)
    if request.method == 'GET':
        form = NoteForm()
    else:
        form = NoteForm(data=request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.contact = contact
            note.save()
            return redirect(to='notes_contact', pk=pk)
# def contact_detail(request):
#     if request.method == 'POST':
#         form = ContactForm()
#     else:
#         form = ContactForm(data=request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect(to='contact_detail.html')

#     return render(request, "contacts/contact_detail.html", {"form": form})