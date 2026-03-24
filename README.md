# 🦷 Reface Dentofacial Centre — Django Website

A full-featured dental clinic website built with Django + Python.

## 📦 Features
- ✅ Beautiful responsive homepage (Hero, Services, Doctors, Gallery, Testimonials, Blog, CTA)
- ✅ Patient login & registration portal
- ✅ Patient dashboard (view/cancel appointments)
- ✅ Patient profile management
- ✅ Online appointment booking
- ✅ Before & After gallery
- ✅ Blog with categories
- ✅ Contact form with Google Maps
- ✅ WhatsApp float button
- ✅ Django Admin panel (full control over all content)

## 🚀 Setup Instructions

### 1. Install Python
Make sure Python 3.10+ is installed.

### 2. Create virtual environment
```bash
python -m venv venv
source venv/bin/activate       # On Mac/Linux
venv\Scripts\activate          # On Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Create superuser (admin)
```bash
python manage.py createsuperuser
```

### 6. Run the server
```bash
python manage.py runserver
```

### 7. Open in browser
- Website: http://127.0.0.1:8000/
- Admin Panel: http://127.0.0.1:8000/admin/

---

## 📁 Project Structure
```
reface_dental/
├── reface/              # Main project settings
│   ├── settings.py
│   └── urls.py
├── core/                # Home, Services, Doctors, Gallery, Testimonials, Contact
│   ├── models.py        # Service, Doctor, GalleryItem, Testimonial, ContactMessage
│   ├── views.py
│   └── urls.py
├── appointments/        # Appointment booking system
│   ├── models.py        # Appointment, TimeSlot
│   ├── views.py
│   └── urls.py
├── patients/            # Patient portal (login/register/dashboard/profile)
│   ├── models.py        # PatientProfile
│   ├── views.py
│   └── urls.py
├── blog/                # Blog / Articles
│   ├── models.py        # BlogPost, BlogCategory
│   ├── views.py
│   └── urls.py
├── templates/           # All HTML templates
│   ├── base.html        # Master layout (navbar + footer)
│   ├── core/
│   │   ├── home.html
│   │   └── contact.html
│   ├── appointments/
│   │   └── book.html
│   ├── patients/
│   │   ├── login.html
│   │   ├── register.html
│   │   ├── dashboard.html
│   │   └── profile.html
│   └── blog/
│       ├── list.html
│       └── detail.html
├── static/              # CSS, JS, Images
├── media/               # Uploaded images
├── requirements.txt
└── manage.py
```

## 🎨 Adding Content via Admin
1. Go to http://127.0.0.1:8000/admin/
2. Add **Services** (with slugs like `invisalign`, `braces`, `dental-implants`)
3. Add **Doctors** with photos and bios
4. Add **Gallery Items** with before/after images
5. Add **Testimonials** from Google/Practo reviews
6. Add **Blog Posts** for SEO

## 📱 URL Routes
| URL | Page |
|-----|------|
| `/` | Homepage |
| `/about/` | About Us |
| `/services/` | All Services |
| `/services/<slug>/` | Service Detail |
| `/doctors/` | Doctor Profiles |
| `/gallery/` | Before & After Gallery |
| `/testimonials/` | Patient Reviews |
| `/blog/` | Blog List |
| `/blog/<slug>/` | Blog Post Detail |
| `/contact/` | Contact + Map |
| `/appointments/book/` | Book Appointment |
| `/patients/login/` | Patient Login |
| `/patients/register/` | Patient Register |
| `/patients/dashboard/` | Patient Dashboard |
| `/patients/profile/` | Patient Profile |
| `/admin/` | Admin Panel |

## 🔒 Security Notes (for Production)
- Change `SECRET_KEY` in settings.py
- Set `DEBUG = False`
- Set `ALLOWED_HOSTS` to your domain
- Use PostgreSQL instead of SQLite
- Configure proper email backend (e.g., SendGrid)

## 📞 Clinic Details
Update contact information in `templates/base.html` footer section.
