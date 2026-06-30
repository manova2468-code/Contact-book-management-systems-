from django.shortcuts import render, redirect
from .db import collection
import csv
from django.http import HttpResponse


def index(request):
    contacts = list(collection.find())
    return render(request, "contacts/index.html", {"contacts": contacts})


def add_contact(request):
    if request.method == "POST":
        data = {
            "name": request.POST.get("name"),
            "phone": request.POST.get("phone"),
            "relationship": request.POST.get("relationship"),
            "priority": request.POST.get("priority"),
            "emergency": request.POST.get("emergency") == "on",
            "favorite": request.POST.get("favorite") == "on",
            "notes": request.POST.get("notes", ""),
            "email": request.POST.get("email", ""),
            "views": 0
        }
        collection.insert_one(data)
        return redirect("/")

    return render(request, "contacts/add.html")


def edit_contact(request, contact_id):
    from bson import ObjectId

    if request.method == "POST":
        data = {
            "name": request.POST.get("name"),
            "phone": request.POST.get("phone"),
            "relationship": request.POST.get("relationship"),
            "priority": request.POST.get("priority"),
            "emergency": request.POST.get("emergency") == "on",
            "favorite": request.POST.get("favorite") == "on",
            "notes": request.POST.get("notes", ""),
            "email": request.POST.get("email", "")
        }
        collection.update_one({"_id": ObjectId(contact_id)}, {"$set": data})
        return redirect("/")

    contact = collection.find_one({"_id": ObjectId(contact_id)})
    return render(request, "contacts/edit.html", {"contact": contact})


def delete_contact(request, contact_id):
    from bson import ObjectId
    collection.delete_one({"_id": ObjectId(contact_id)})
    return redirect("/")


def search_contact(request):
    name = request.GET.get("name")

    if not name:
        return redirect("/")

    contact = collection.find_one({
        "name": {"$regex": name, "$options": "i"}
    })

    if contact:
        collection.update_one({"_id": contact["_id"]}, {"$inc": {"views": 1}})
        return render(request, "contacts/index.html", {"contacts": [contact]})
    else:
        return render(request, "contacts/index.html", {"contacts": []})


def emergency(request):
    contacts = list(collection.find({"emergency": True}))
    return render(request, "contacts/emergency.html", {"contacts": contacts})


def frequent(request):
    contacts = list(collection.find({"views": {"$gt": 0}}).sort("views", -1))
    return render(request, "contacts/frequent.html", {"contacts": contacts})


def favorites(request):
    contacts = list(collection.find({"favorite": True}))
    return render(request, "contacts/favorites.html", {"contacts": contacts})


def relationship(request):
    role = request.GET.get("role")

    contacts = list(collection.find({
        "relationship": {"$regex": role, "$options": "i"}
    }))

    return render(request, "contacts/index.html", {"contacts": contacts})


def export_contacts(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="contacts.csv"'

    writer = csv.writer(response)
    writer.writerow(['Name', 'Phone', 'Email', 'Relationship', 'Priority', 'Emergency', 'Favorite', 'Notes', 'Views'])

    contacts = collection.find()
    for contact in contacts:
        writer.writerow([
            contact.get('name', ''),
            contact.get('phone', ''),
            contact.get('email', ''),
            contact.get('relationship', ''),
            contact.get('priority', ''),
            'Yes' if contact.get('emergency', False) else 'No',
            'Yes' if contact.get('favorite', False) else 'No',
            contact.get('notes', ''),
            contact.get('views', 0)
        ])

    return response