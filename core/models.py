from django.db import models


class SiteSettings(models.Model):
    """Single editable record: branding, profile, contact and social details."""
    brand_name = models.CharField(max_length=60, default="Erique")
    full_name = models.CharField(max_length=100, default="Erick Benjamin")
    title = models.CharField(max_length=100, default="Web Developer")
    intro = models.TextField(default="I build modern, fast and scalable web applications that solve real problems. Passionate about technology, clean code and continuous learning.")
    summary = models.TextField(default="I am Erick Benjamin, a Computer Science graduate and passionate web developer. I am ambitious, focused on continuous professional development, and dedicated to building modern web applications that solve real problems and create value.")
    focus = models.CharField(max_length=120, default="Web Development (Full Stack / Django)")
    location = models.CharField(max_length=120, default="Dar es Salaam, Tanzania")
    email = models.EmailField(default="erictimothy123@gmail.com")
    profile_photo = models.ImageField(upload_to="profile/", blank=True)
    github_url = models.URLField(default="https://github.com/codewitherique")
    youtube_url = models.URLField(default="https://youtube.com/@codewitherique")
    whatsapp_url = models.URLField(blank=True)
    show_referees = models.BooleanField(default=True)
    meta_title = models.CharField(max_length=70, default="Erick Benjamin (Erique) | Web Developer")
    meta_description = models.CharField(max_length=160, default="Portfolio of Erick Benjamin, a Django web developer based in Dar es Salaam, Tanzania.")

    class Meta:
        verbose_name = "Website Settings"
        verbose_name_plural = "Website Settings"

    def __str__(self):
        return "Website Settings"

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        return cls.objects.get_or_create(pk=1)[0]


class Education(models.Model):
    title = models.CharField(max_length=150)
    institution = models.CharField(max_length=150)
    period = models.CharField(max_length=30)
    award = models.CharField(max_length=200)
    icon = models.CharField(max_length=50, default="bi-book")
    order = models.PositiveIntegerField(default=0)
    published = models.BooleanField(default=True)

    class Meta:
        ordering = ["order"]
        verbose_name_plural = "Education"

    def __str__(self):
        return self.title


class Skill(models.Model):
    name = models.CharField(max_length=50)
    icon = models.CharField(max_length=60, help_text="Bootstrap Icons class, e.g. bi-code-slash")
    level = models.CharField(max_length=30, blank=True, help_text="Optional label, e.g. Intermediate")
    order = models.PositiveIntegerField(default=0)
    published = models.BooleanField(default=True)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.name


class Project(models.Model):
    title = models.CharField(max_length=120)
    slug = models.SlugField(unique=True)
    category = models.CharField(max_length=60, blank=True)
    short_description = models.CharField(max_length=250)
    description = models.TextField(blank=True)
    thumbnail = models.ImageField(upload_to="projects/", blank=True)
    tech_stack = models.CharField(max_length=200, help_text="Comma-separated, e.g. Django, PostgreSQL")
    live_url = models.URLField(blank=True)
    github_url = models.URLField(blank=True)
    featured = models.BooleanField(default=True)
    published = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["order", "-created_at"]

    def __str__(self):
        return self.title

    @property
    def tech_list(self):
        return [t.strip() for t in self.tech_stack.split(",") if t.strip()]


class Referee(models.Model):
    full_name = models.CharField(max_length=100)
    job_title = models.CharField(max_length=100)
    organization = models.CharField(max_length=120)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=30, blank=True)
    photo = models.ImageField(upload_to="referees/", blank=True)
    order = models.PositiveIntegerField(default=0)
    published = models.BooleanField(default=False)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.full_name


class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=150)
    message = models.TextField(max_length=3000)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.subject} — {self.name}"
