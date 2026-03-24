from django.contrib import admin
from django.utils.html import format_html
from django.http import HttpResponse
import csv
from .models import Service, Doctor, GalleryItem, Testimonial, ContactMessage


# ─────────────────────────────────────────
#  SHARED IMAGE PREVIEW HELPER
# ─────────────────────────────────────────

def image_preview_field(url, label='Current image'):
    if url:
        return format_html(
            '<div style="margin-top:8px">'
            '<img src="{}" style="max-width:380px;max-height:220px;object-fit:cover;'
            'border-radius:10px;border:1px solid #e0ddd5;box-shadow:0 2px 10px rgba(0,0,0,0.08)">'
            '<br><small style="color:#888;font-size:0.75rem;margin-top:4px;display:block">'
            '{} · Upload a new file above to replace</small>'
            '</div>', url, label)
    return format_html(
        '<div style="margin-top:8px;padding:1.5rem 2rem;background:#f8f6f1;'
        'border:2px dashed #e0ddd5;border-radius:10px;text-align:center;color:#bbb">'
        '<div style="font-size:2rem;margin-bottom:0.4rem">🖼</div>'
        '<div style="font-size:0.8rem">No image yet — upload one above</div>'
        '</div>')


# ─────────────────────────────────────────
#  SERVICE
# ─────────────────────────────────────────

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display  = ['image_thumb', 'name', 'category_badge', 'is_featured', 'order']
    list_display_links = ['name']
    list_editable = ['is_featured', 'order']
    list_filter   = ['category', 'is_featured']
    search_fields = ['name', 'short_description']
    prepopulated_fields = {'slug': ('name',)}
    ordering = ['order']
    list_per_page = 20
    readonly_fields = ['service_image_preview']

    fieldsets = (
        ('Basic Info', {
            'fields': ('name', 'slug', 'category', 'icon', 'order', 'is_featured'),
            'description': 'Icon: use a Font Awesome class e.g. <code>fas fa-tooth</code>'
        }),
        ('🖼 Service Image', {
            'fields': ('image', 'service_image_preview'),
            'description': 'Recommended size: 800×500px. JPG or PNG.',
        }),
        ('Content', {
            'fields': ('short_description', 'full_description'),
        }),
    )

    @admin.display(description='')
    def image_thumb(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="width:52px;height:38px;object-fit:cover;'
                'border-radius:6px;border:1px solid #e0ddd5">', obj.image.url)
        return format_html('<span style="color:#ddd;font-size:1.2rem">🖼</span>')

    @admin.display(description='Category')
    def category_badge(self, obj):
        colors = {
            'orthodontics': ('#0d47a1','#e3f2fd'), 'implants': ('#4a148c','#f3e5f5'),
            'cosmetic': ('#880e4f','#fce4ec'), 'general': ('#1b5e20','#e8f5e9'),
            'pediatric': ('#f57f17','#fff8e1'), 'surgery': ('#004d40','#e0f2f1'),
        }
        tc, bg = colors.get(obj.category, ('#333','#eee'))
        return format_html(
            '<span style="background:{};color:{};padding:3px 10px;'
            'border-radius:100px;font-size:0.74rem;font-weight:700">{}</span>',
            bg, tc, obj.get_category_display())

    @admin.display(description='Image Preview')
    def service_image_preview(self, obj):
        return image_preview_field(obj.image.url if obj.image else None)


# ─────────────────────────────────────────
#  DOCTOR
# ─────────────────────────────────────────

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display  = ['photo_thumb', 'name', 'designation', 'qualification', 'experience_years', 'is_featured', 'order']
    list_display_links = ['name']
    list_editable = ['is_featured', 'order']
    search_fields = ['name', 'designation', 'qualification', 'specialization']
    ordering = ['order']
    list_per_page = 20
    readonly_fields = ['doctor_photo_preview']

    fieldsets = (
        ('👨‍⚕️ Doctor Identity', {
            'fields': ('name', 'designation', 'qualification', 'experience_years', 'order', 'is_featured'),
        }),
        ('🖼 Profile Photo', {
            'fields': ('photo', 'doctor_photo_preview'),
            'description': 'Upload a professional headshot. Recommended: 400×500px, JPG/PNG. '
                           'The photo appears on the Doctors page and homepage.',
        }),
        ('📋 Profile Details', {
            'fields': ('specialization', 'bio'),
            'description': 'Specialization: comma-separated list e.g. "Invisalign, Braces, Clear Aligners". '
                           'Bio: 2–4 sentences about the doctor\'s background and expertise.',
        }),
    )

    @admin.display(description='Photo')
    def photo_thumb(self, obj):
        if obj.photo:
            return format_html(
                '<img src="{}" style="width:44px;height:44px;border-radius:50%;'
                'object-fit:cover;border:2px solid #e0ddd5">', obj.photo.url)
        return format_html(
            '<div style="width:44px;height:44px;border-radius:50%;background:#1a4a4a;'
            'display:flex;align-items:center;justify-content:center;'
            'color:#c9a84c;font-weight:700;font-size:1.1rem">{}</div>',
            obj.name[0].upper() if obj.name else '?')

    @admin.display(description='Photo Preview')
    def doctor_photo_preview(self, obj):
        if obj.photo:
            return format_html(
                '<div style="margin-top:8px;display:flex;align-items:center;gap:1.5rem">'
                '<img src="{}" style="width:140px;height:170px;object-fit:cover;'
                'border-radius:12px;border:1px solid #e0ddd5;box-shadow:0 2px 12px rgba(0,0,0,0.1)">'
                '<div style="color:#888;font-size:0.8rem;line-height:1.8">'
                '✅ Photo uploaded<br>'
                '<small>Upload a new file above to replace</small>'
                '</div>'
                '</div>', obj.photo.url)
        return format_html(
            '<div style="margin-top:8px;padding:1.5rem 2rem;background:#f8f6f1;'
            'border:2px dashed #e0ddd5;border-radius:10px;text-align:center;color:#bbb">'
            '<div style="font-size:3rem;margin-bottom:0.5rem">👤</div>'
            '<div style="font-size:0.8rem">No photo uploaded yet</div>'
            '<div style="font-size:0.72rem;margin-top:4px">Recommended: 400×500px JPG/PNG</div>'
            '</div>')


# ─────────────────────────────────────────
#  GALLERY
# ─────────────────────────────────────────

@admin.register(GalleryItem)
class GalleryAdmin(admin.ModelAdmin):
    list_display  = ['preview_thumb', 'title', 'category_badge', 'treatment', 'has_before_after', 'created_at']
    list_display_links = ['title']
    list_filter   = ['category', 'treatment']
    search_fields = ['title', 'description']
    ordering = ['-created_at']
    list_per_page = 20
    readonly_fields = ['gallery_preview']

    fieldsets = (
        ('📋 Item Details', {
            'fields': ('title', 'category', 'treatment', 'description'),
            'description': (
                '<strong>Category guide:</strong><br>'
                '• <strong>Before & After</strong> — Upload both Before and After images below<br>'
                '• <strong>Clinic</strong> — Upload a single Clinic Photo<br>'
                '• <strong>Team</strong> — Upload a Team photo'
            ),
        }),
        ('🖼 Before & After Images', {
            'fields': ('before_image', 'after_image'),
            'description': 'For Before & After cases. Upload both images. Recommended: 600×450px each.',
            'classes': ('collapse',),
        }),
        ('📷 Single Image', {
            'fields': ('image',),
            'description': 'For Clinic or Team photos. Recommended: 800×600px.',
            'classes': ('collapse',),
        }),
        ('👁 Preview', {
            'fields': ('gallery_preview',),
        }),
    )

    @admin.display(description='Preview')
    def preview_thumb(self, obj):
        img = obj.after_image or obj.image or obj.before_image
        if img:
            return format_html(
                '<img src="{}" style="width:64px;height:46px;object-fit:cover;'
                'border-radius:7px;border:1px solid #e0ddd5">', img.url)
        return format_html(
            '<div style="width:64px;height:46px;border-radius:7px;background:#f0eeea;'
            'display:flex;align-items:center;justify-content:center;color:#ccc;font-size:1.3rem">🖼</div>')

    @admin.display(description='Category')
    def category_badge(self, obj):
        colors = {
            'before_after': ('#155724','#d4edda'),
            'clinic':       ('#004085','#cce5ff'),
            'team':         ('#856404','#fff3cd'),
        }
        tc, bg = colors.get(obj.category, ('#333','#eee'))
        return format_html(
            '<span style="background:{};color:{};padding:3px 10px;'
            'border-radius:100px;font-size:0.74rem;font-weight:700">{}</span>',
            bg, tc, obj.get_category_display())

    @admin.display(description='Before/After', boolean=False)
    def has_before_after(self, obj):
        if obj.before_image and obj.after_image:
            return format_html('<span style="color:#155724;font-weight:700">✅ Both</span>')
        if obj.before_image or obj.after_image:
            return format_html('<span style="color:#856404;font-weight:700">⚠️ Partial</span>')
        return format_html('<span style="color:#bbb">—</span>')

    @admin.display(description='Image Preview')
    def gallery_preview(self, obj):
        parts = []
        if obj.before_image:
            parts.append(format_html(
                '<div style="text-align:center">'
                '<div style="font-size:0.72rem;font-weight:700;color:#888;text-transform:uppercase;'
                'letter-spacing:0.08em;margin-bottom:6px">Before</div>'
                '<img src="{}" style="width:220px;height:160px;object-fit:cover;'
                'border-radius:10px;border:1px solid #e0ddd5"></div>',
                obj.before_image.url))
        if obj.after_image:
            parts.append(format_html(
                '<div style="text-align:center">'
                '<div style="font-size:0.72rem;font-weight:700;color:#2d7a5a;text-transform:uppercase;'
                'letter-spacing:0.08em;margin-bottom:6px">After</div>'
                '<img src="{}" style="width:220px;height:160px;object-fit:cover;'
                'border-radius:10px;border:1px solid #e0ddd5"></div>',
                obj.after_image.url))
        if obj.image:
            parts.append(format_html(
                '<div style="text-align:center">'
                '<div style="font-size:0.72rem;font-weight:700;color:#888;text-transform:uppercase;'
                'letter-spacing:0.08em;margin-bottom:6px">Photo</div>'
                '<img src="{}" style="width:280px;height:190px;object-fit:cover;'
                'border-radius:10px;border:1px solid #e0ddd5"></div>',
                obj.image.url))
        if parts:
            inner = ''.join(str(p) for p in parts)
            return format_html(
                '<div style="display:flex;gap:1.5rem;flex-wrap:wrap;margin-top:8px">{}</div>',
                inner)
        return format_html(
            '<div style="padding:1.5rem;background:#f8f6f1;border:2px dashed #e0ddd5;'
            'border-radius:10px;text-align:center;color:#bbb;margin-top:8px">'
            '<div style="font-size:2rem;margin-bottom:0.4rem">🖼</div>'
            '<div style="font-size:0.8rem">No images uploaded yet</div>'
            '</div>')


# ─────────────────────────────────────────
#  TESTIMONIAL
# ─────────────────────────────────────────

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display  = ['patient_name', 'star_rating', 'treatment', 'source_badge', 'is_featured', 'created_at']
    list_editable = ['is_featured']
    list_filter   = ['rating', 'is_featured', 'source']
    search_fields = ['patient_name', 'review']
    ordering = ['-created_at']

    @admin.display(description='Rating', ordering='rating')
    def star_rating(self, obj):
        return format_html(
            '<span style="color:#c9a84c;font-size:1rem;letter-spacing:1px">{}</span>',
            '★' * obj.rating + '☆' * (5 - obj.rating))

    @admin.display(description='Source')
    def source_badge(self, obj):
        colors = {'Google': ('#c0392b','#fde8e8'), 'Practo': ('#1565c0','#e3f2fd')}
        tc, bg = colors.get(obj.source, ('#333','#eee'))
        return format_html(
            '<span style="background:{};color:{};padding:3px 10px;'
            'border-radius:100px;font-size:0.74rem;font-weight:700">{}</span>',
            bg, tc, obj.source)


# ─────────────────────────────────────────
#  CONTACT MESSAGES
# ─────────────────────────────────────────

def export_messages_csv(modeladmin, request, queryset):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="contact_messages.csv"'
    writer = csv.writer(response)
    writer.writerow(['Name','Email','Phone','Subject','Message','Read','Date'])
    for msg in queryset:
        writer.writerow([msg.name, msg.email, msg.phone, msg.subject,
                         msg.message, 'Yes' if msg.is_read else 'No',
                         msg.created_at.strftime('%d %b %Y %I:%M %p')])
    return response
export_messages_csv.short_description = "📥 Export to CSV"

def mark_read(ma, req, qs):   qs.update(is_read=True)
def mark_unread(ma, req, qs): qs.update(is_read=False)
mark_read.short_description   = "✅ Mark as Read"
mark_unread.short_description = "🔵 Mark as Unread"


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display  = ['unread_dot', 'name', 'email', 'phone', 'subject', 'created_at']
    list_display_links = ['name']
    list_filter   = ['is_read', 'created_at']
    search_fields = ['name', 'email', 'phone', 'subject', 'message']
    readonly_fields = ['name','email','phone','subject','message','created_at','is_read']
    ordering = ['-created_at']
    actions = [mark_read, mark_unread, export_messages_csv]

    @admin.display(description='')
    def unread_dot(self, obj):
        color = '#c9a84c' if not obj.is_read else '#ddd'
        return format_html(
            '<span style="display:inline-block;width:9px;height:9px;'
            'border-radius:50%;background:{}" title="{}"></span>',
            color, 'Unread' if not obj.is_read else 'Read')

    def change_view(self, request, object_id, form_url='', extra_context=None):
        try:
            ContactMessage.objects.filter(pk=object_id).update(is_read=True)
        except Exception:
            pass
        return super().change_view(request, object_id, form_url, extra_context)
