from django.db import models


class Service(models.Model):
    CATEGORY_CHOICES = [
        ('orthodontics', 'Orthodontics'),
        ('implants', 'Dental Implants'),
        ('cosmetic', 'Cosmetic Dentistry'),
        ('general', 'General Dentistry'),
        ('pediatric', 'Pediatric Dentistry'),
        ('surgery', 'Oral Surgery'),
    ]
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    short_description = models.TextField()
    full_description = models.TextField()
    icon = models.CharField(max_length=100, blank=True, help_text='Font Awesome icon class')
    image = models.ImageField(upload_to='services/', blank=True, null=True)
    is_featured = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)
    slug = models.SlugField(unique=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.name


class Doctor(models.Model):
    name = models.CharField(max_length=200)
    designation = models.CharField(max_length=200)
    qualification = models.CharField(max_length=300)
    specialization = models.TextField()
    bio = models.TextField()
    photo = models.ImageField(upload_to='doctors/', blank=True, null=True)
    experience_years = models.PositiveIntegerField(default=0)
    is_featured = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.name


class GalleryItem(models.Model):
    CATEGORY_CHOICES = [
        ('before_after', 'Before & After'),
        ('clinic', 'Clinic'),
        ('team', 'Team'),
    ]
    title = models.CharField(max_length=200)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    before_image = models.ImageField(upload_to='gallery/before/', blank=True, null=True)
    after_image = models.ImageField(upload_to='gallery/after/', blank=True, null=True)
    image = models.ImageField(upload_to='gallery/', blank=True, null=True)
    description = models.TextField(blank=True)
    treatment = models.ForeignKey(Service, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Testimonial(models.Model):
    patient_name = models.CharField(max_length=200)
    patient_photo = models.ImageField(upload_to='testimonials/', blank=True, null=True)
    treatment = models.ForeignKey(Service, on_delete=models.SET_NULL, null=True, blank=True)
    rating = models.PositiveIntegerField(default=5)
    review = models.TextField()
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    source = models.CharField(max_length=50, default='Google', help_text='e.g. Google, Practo')

    def __str__(self):
        return f"{self.patient_name} - {self.rating}★"


class ContactMessage(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    subject = models.CharField(max_length=300)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} - {self.subject}"
