from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from .models import Event, Venue
from django.contrib.auth.models import User
from .forms import VenueForm, EventForm, EventFormAdmin
import csv, io
from datetime import datetime
from django.http import FileResponse
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
from django.core.paginator import Paginator
from django.contrib import messages


def venue_pdf(request):
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=letter, bottomup=0)
    text = c.beginText()
    text.setTextOrigin(inch, inch)
    text.setFont('Helvetica', 14)

    venues = Venue.objects.all()
    lines = []
    for venue in venues:
        lines.append(venue.name)
        lines.append(venue.address)
        lines.append(venue.zip_code)
        lines.append(venue.phone)
        lines.append(venue.web)
        lines.append(venue.email_address)
        lines.append(' ')

    for line in lines:
        text.textLine(line)

    c.drawText(text)
    c.showPage()
    c.save()
    buf.seek(0)

    return FileResponse(buf, as_attachment=True, filename='venues.pdf')


def venue_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=venues.csv'

    writer = csv.writer(response)
    writer.writerow(['Venue Name', 'address', 'Zip Code', 'Phone', 'Web', 'Email'])
    venues = Venue.objects.all()
    for venue in venues:
        writer.writerow([venue, venue.address, venue.zip_code, venue.phone, venue.web, venue.email_address])

    return response


def venue_text(request):
    response = HttpResponse(content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename=venues.txt'
    venues = Venue.objects.all()
    lines = []
    for venue in venues:
        lines.append(f'{venue}\n{venue.address}\n{venue.zip_code}\n{venue.phone}\n{venue.web}\n{venue.email_address}\n')
    response.writelines(lines)
    return response


def delete_event(request, event_id):
    event = Event.objects.get(pk=event_id)
    if request.user == event.manager:
        event.delete()
        messages.success(request, ('Event Delete!!!'))
        return redirect('event_list')
    else:
        messages.success(request, ('You Are Not Authorized To Delete This Event...'))
        return redirect('event_list')


def delete_venue(request, venue_id):
    venue = Venue.objects.get(pk=venue_id)
    venue.delete()
    return redirect('list_venues')


def my_events(request):
    if request.user.is_authenticated:
        me = request.user.id
        events = Event.objects.filter(manager=me)
        context = {
            'me': me,
            'events': events,
        }
        return render(request, 'polls/my_events.html', context=context)
    else:
        messages.success(request, ('You Are Not Authorized To View This Page...'))
        return redirect('login_user')


def show_event(request, event_id):
    event = Event.objects.get(pk=event_id)
    return render(request, 'polls/show_event.html', {'event': event})


def venue_events(request, venue_id):
    venue = Venue.objects.get(pk=venue_id)
    event_list = venue.event_set.all()
    if event_list:
        return render(request, 'polls/venue_events.html', {'event_list': event_list})
    else:
        messages.success(request, ('That Venue Has Not Events...'))
        return redirect('admin_approval')


def admin_approval(request):
    event_count = Event.objects.all().count()
    venue_count = Venue.objects.all().count()
    user_count = User.objects.all().count()
    venue_list = Venue.objects.all()
    if request.user.is_superuser:
        event_list = Event.objects.all().order_by('-event_date')
        if request.method == 'POST':
            id_list = request.POST.getlist('boxes')
            event_list.update(approved=False)
            for x in id_list:
                Event.objects.filter(pk=int(x)).update(approved=True)
            messages.success(request, ('Event List Approval Has Been Update'))
            return redirect('event_list')
        else:
            return render(request, 'polls/admin_approval.html', {'venue_list': venue_list, 'event_list': event_list, 'event_count': event_count, 'venue_count': venue_count, 'user_count': user_count})
    else:
        messages.success(request, ('You are not authorized to view this page!'))
        return redirect('home')


def all_events(request):
    event_list = Event.objects.all().order_by('-event_date')
    context = {
        'event_list': event_list,
    }
    return render(request, 'polls/event_list.html', context=context)


def add_event(request):
    submitted = False
    if request.method == 'POST':
        if request.user.is_superuser:
            form = EventFormAdmin(request.POST)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect('/add_event?submitted=True')
        else:
            form = EventForm(request.POST)
            if form.is_valid():
                event = form.save(commit=False)
                event.manager = request.user
                event.save()
                return HttpResponseRedirect('/add_event?submitted=True')
    else:
        if request.user.is_superuser:
            form = EventFormAdmin
        else:
            form = EventForm
        if 'submitted' in request.GET:
            submitted = True
    context = {
        'form': form,
        'submitted': submitted,
    }
    return render(request, 'polls/add_event.html', context)


def add_venue(request):
    submitted = False
    if request.method == 'POST':
        form = VenueForm(request.POST, request.FILES)
        if form.is_valid():
            venue = form.save(commit=False)
            venue.owner = request.user.id
            venue.save()
            return HttpResponseRedirect('/add_venue?submitted=True')
    else:
        form = VenueForm
        if 'submitted' in request.GET:
            submitted = True
    context = {
        'form': form,
        'submitted': submitted,
    }
    return render(request, 'polls/add_venue.html', context)


def search_venues(request):
    if request.method == 'POST':
        searched = request.POST['searched']
        venues = Venue.objects.filter(name__contains=searched)
        context = {'searched': searched, 'venues': venues}
        return render(request, 'polls/search_venues.html', context=context)
    else:
        return render(request, 'polls/search_venues.html')


def search_events(request):
    if request.method == 'POST':
        searched = request.POST['searched']
        events = Event.objects.filter(name__contains=searched)
        context = {'searched': searched, 'events': events}
        return render(request, 'polls/search_events.html', context=context)
    else:
        return render(request, 'polls/search_events.html')


def show_venue(request, venue_id):
    venue = Venue.objects.get(pk=venue_id)
    event_list = venue.event_set.all()
    venue_owner = User.objects.get(pk=venue.owner)
    context = {
        'venue': venue,
        'venue_owner': venue_owner,
        'event_list': event_list,
    }
    return render(request, 'polls/show_venue.html', context=context)


def update_event(request, event_id):
    event = Event.objects.get(pk=event_id)
    if request.user.is_superuser:
        form = EventFormAdmin(request.POST or None, instance=event)
    else:
        form = EventForm(request.POST or None, instance=event)

    if form.is_valid():
        form.save()
        return redirect('event_list')
    context = {
        'event': event,
        'form': form,
    }
    return render(request, 'polls/update_event.html', context=context)


def update_venue(request, venue_id):
    venue = Venue.objects.get(pk=venue_id)
    form = VenueForm(request.POST or None, request.FILES or None, instance=venue)
    if form.is_valid():
        form.save()
        return redirect('list_venues')
    context = {
        'venue': venue,
        'form': form,
    }
    return render(request, 'polls/update_venue.html', context=context)


def list_venues(request):
    venue_list = Venue.objects.all().order_by('name')

    p = Paginator(venue_list, 2)
    page = request.GET.get('page')
    venues = p.get_page(page)
    nums = 'a' * venues.paginator.num_pages

    context = {
        'venue_list': venue_list,
        'venues': venues,
        'nums': nums,
    }
    return render(request, 'polls/venue.html', context=context)


def home(request):
    event_list = Event.objects.filter(
        event_date__year=datetime.now().year,
    )
    return render(request, 'polls/home.html', {'event_list': event_list})
