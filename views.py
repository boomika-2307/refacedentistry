from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .models import Service, Doctor, GalleryItem, Testimonial, ContactMessage
from django.http import JsonResponse
from appointments.models import Appointment
from blog.models import BlogPost 

def dashboard_stats(request):

    today = date.today()

    data = {
        "today": Appointment.objects.filter(date=today).count(),
        "pending": Appointment.objects.filter(status="pending").count(),
        "patients": User.objects.count(),
        "messages": ContactMessage.objects.filter(is_read=False).count(),
    }

    return JsonResponse(data)


def home(request):
    featured_services = Service.objects.filter(is_featured=True)[:6]
    doctors = Doctor.objects.filter(is_featured=True)
    testimonials = Testimonial.objects.filter(is_featured=True)[:6]
    gallery_items = GalleryItem.objects.filter(category='before_after')[:6]
    latest_posts = BlogPost.objects.filter(is_published=True).order_by('-created_at')[:3]
    context = {
        'featured_services': featured_services,
        'doctors': doctors,
        'testimonials': testimonials,
        'gallery_items': gallery_items,
        'latest_posts': latest_posts,
    }
    return render(request, 'core/home.html', context)


def about(request):
    doctors = Doctor.objects.all()
    testimonials = Testimonial.objects.filter(is_featured=True)[:4]
    return render(request, 'core/about.html', {
        'doctors': doctors,
        'testimonials': testimonials,
    })


def services(request):
    all_services = Service.objects.all()
    categories = Service.CATEGORY_CHOICES

    # Static fallback shown when no services added in admin yet
    static_services = [
        {
            'id': 'orthodontics', 'name': 'Orthodontics', 'icon': 'fas fa-teeth',
            'items': [
                {'name': 'Invisalign & Clear Aligners', 'icon': 'fas fa-magic', 'popular': True,
                 'desc': 'Straighten teeth discreetly with virtually invisible aligners. Certified Invisalign provider with hundreds of successful cases across all age groups.'},
                {'name': 'Metal Braces', 'icon': 'fas fa-teeth-open', 'popular': False,
                 'desc': 'Traditional metal braces for reliable, cost-effective orthodontic correction. Suitable for complex bite issues and all ages.'},
                {'name': 'Ceramic Braces', 'icon': 'fas fa-star', 'popular': False,
                 'desc': 'Tooth-colored ceramic brackets that blend with your natural teeth for a more aesthetic orthodontic experience.'},
                {'name': 'Lingual Braces', 'icon': 'fas fa-smile', 'popular': False,
                 'desc': 'Hidden braces placed on the inner surface of teeth — completely invisible from the outside. Perfect for professionals.'},
            ]
        },
        {
            'id': 'implants', 'name': 'Dental Implants', 'icon': 'fas fa-tooth',
            'items': [
                {'name': 'Single Tooth Implants', 'icon': 'fas fa-tooth', 'popular': True,
                 'desc': 'Replace a missing tooth permanently with a titanium implant and a natural-looking crown that blends seamlessly.'},
                {'name': 'Full Arch / All-on-4', 'icon': 'fas fa-teeth', 'popular': True,
                 'desc': 'Restore a full arch of teeth with just 4 implants. Same-day loading available for immediate results.'},
                {'name': 'Corticobasal Implants', 'icon': 'fas fa-bone', 'popular': False,
                 'desc': 'Advanced implant system anchored in cortical bone — ideal for patients with low bone density who were previously told they cannot get implants.'},
                {'name': 'Implant-Supported Dentures', 'icon': 'fas fa-smile-beam', 'popular': False,
                 'desc': 'Secure, stable dentures supported by implants — no slipping, no adhesives, just confident chewing and speaking.'},
            ]
        },
        {
            'id': 'cosmetic', 'name': 'Cosmetic Dentistry', 'icon': 'fas fa-star',
            'items': [
                {'name': 'Teeth Whitening', 'icon': 'fas fa-sun', 'popular': True,
                 'desc': 'Professional-grade in-clinic and take-home whitening treatments. Safe, effective and long-lasting results in as little as one hour.'},
                {'name': 'Gummy Smile Correction', 'icon': 'fas fa-smile', 'popular': False,
                 'desc': 'Laser gum contouring and surgical gummy smile correction to achieve a balanced, confident smile with the ideal tooth-to-gum ratio.'},
                {'name': 'Dental Veneers', 'icon': 'fas fa-layer-group', 'popular': True,
                 'desc': 'Ultra-thin porcelain or composite veneers that transform the shape, size, color and overall appearance of your smile.'},
                {'name': 'Smile Makeover', 'icon': 'fas fa-magic', 'popular': False,
                 'desc': 'A custom combination of cosmetic treatments — whitening, veneers, aligners — designed to achieve your dream smile.'},
            ]
        },
        {
            'id': 'general', 'name': 'General Dentistry', 'icon': 'fas fa-stethoscope',
            'items': [
                {'name': 'Dental Checkup & Cleaning', 'icon': 'fas fa-search', 'popular': False,
                 'desc': 'Comprehensive oral examination, professional scaling and polishing to keep your teeth and gums healthy.'},
                {'name': 'Root Canal Treatment', 'icon': 'fas fa-syringe', 'popular': False,
                 'desc': 'Painless, single-sitting root canal procedures to save infected teeth using advanced rotary endodontics.'},
                {'name': 'Tooth Extractions', 'icon': 'fas fa-tooth', 'popular': False,
                 'desc': 'Simple and surgical tooth extractions performed with minimal discomfort and maximum care.'},
                {'name': 'Dental Fillings', 'icon': 'fas fa-fill', 'popular': False,
                 'desc': 'Tooth-coloured composite fillings that restore decayed teeth to natural appearance and function.'},
            ]
        },
        {
            'id': 'pediatric', 'name': 'Pediatric Dentistry', 'icon': 'fas fa-child',
            'items': [
                {'name': 'Children\'s Dental Checkup', 'icon': 'fas fa-child', 'popular': False,
                 'desc': 'Gentle, child-friendly dental exams designed to make kids comfortable and establish good oral health habits early.'},
                {'name': 'Pit & Fissure Sealants', 'icon': 'fas fa-shield-alt', 'popular': False,
                 'desc': 'Protective coatings applied to the chewing surfaces of back teeth to prevent cavities in children.'},
                {'name': 'Interceptive Orthodontics', 'icon': 'fas fa-teeth', 'popular': False,
                 'desc': 'Early orthodontic intervention for growing children to guide jaw development and reduce future treatment needs.'},
            ]
        },
        {
            'id': 'surgery', 'name': 'Oral Surgery', 'icon': 'fas fa-bone',
            'items': [
                {'name': 'Orthognathic (Jaw) Surgery', 'icon': 'fas fa-bone', 'popular': False,
                 'desc': 'Corrective jaw surgery with 3D virtual surgical planning. Fixes skeletal misalignments affecting bite, breathing and facial aesthetics.'},
                {'name': 'Wisdom Tooth Removal', 'icon': 'fas fa-tooth', 'popular': False,
                 'desc': 'Safe surgical extraction of impacted or problematic wisdom teeth under local or general anaesthesia.'},
                {'name': 'Bone Grafting', 'icon': 'fas fa-layer-group', 'popular': False,
                 'desc': 'Rebuilds jawbone volume needed for dental implants using advanced grafting materials and techniques.'},
            ]
        },
    ]

    return render(request, 'core/services.html', {
        'services': all_services,
        'categories': categories,
        'static_services': static_services,
    })


def service_detail(request, slug):
    service = get_object_or_404(Service, slug=slug)
    related = Service.objects.exclude(id=service.id).filter(category=service.category)[:3]
    return render(request, 'core/service_detail.html', {'service': service, 'related': related})


def gallery(request):
    before_after = GalleryItem.objects.filter(category='before_after')
    clinic_photos = GalleryItem.objects.filter(category='clinic')
    return render(request, 'core/gallery.html', {
        'before_after': before_after,
        'clinic_photos': clinic_photos,
    })


def testimonials_view(request):
    all_testimonials = Testimonial.objects.all().order_by('-created_at')
    return render(request, 'core/testimonials.html', {'testimonials': all_testimonials})


def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        subject = request.POST.get('subject')
        message_text = request.POST.get('message')
        ContactMessage.objects.create(
            name=name, email=email, phone=phone,
            subject=subject, message=message_text
        )
        messages.success(request, 'Thank you! Your message has been received. We will contact you soon.')
        return redirect('contact')
    return render(request, 'core/contact.html')


def doctors(request):
    all_doctors = Doctor.objects.all()
    return render(request, 'core/doctors.html', {'doctors': all_doctors})