from django.core.management.base import BaseCommand
from core.models import SiteSettings, Education, Skill, Project, Referee

EDU = [
    ("Bachelor Degree in Computer Sciences", "Kampala International University in Tanzania (KIUT)", "2019 – 2022", "Bachelor degree in Computer Science", "bi-mortarboard"),
    ("Certificate in Cybersecurity Essentials", "Cisco Networking Academy / Netcad", "2021 – 2022", "Certificate in Cybersecurity Essentials", "bi-shield-check"),
    ("Advanced Level Education", "Baobab High School", "2017 – 2019", "Advanced Certificate for Secondary Education (ACSEE)", "bi-book"),
    ("Ordinary Level Education", "Pio High School", "2013 – 2016", "Certificate for Secondary Education (CSEE)", "bi-book"),
    ("Primary School Education", "Rainbow Primary School", "2006 – 2012", "Certificate for Basic Education", "bi-book"),
]
SKILLS = [("Python", "bi-filetype-py"), ("Django", "bi-hdd-stack"), ("HTML5", "bi-filetype-html"),
          ("CSS3", "bi-filetype-css"), ("JavaScript", "bi-filetype-js"), ("PostgreSQL", "bi-database"),
          ("Git & GitHub", "bi-github"), ("VS Code", "bi-code-square"), ("Bootstrap", "bi-bootstrap"), ("Docker", "bi-box-seam")]
PROJECTS = [
    ("School Management System", "school-management-system", "Django", "A modern school management system with student, parent and teacher modules. Built with Django & PostgreSQL.", "Django, PostgreSQL, Bootstrap"),
    ("E-Commerce Platform", "e-commerce-platform", "Django", "A modern e-commerce platform with product catalog, cart and order management system. Built with Django.", "Django, PostgreSQL, JavaScript"),
    ("Personal Portfolio Website", "portfolio-website", "HTML/CSS/JS", "A personal portfolio website to showcase my skills, projects and experience.", "HTML, CSS, JavaScript"),
]
REFEREES = [
    ("Neil P. Mboma", "Branch Manager, Five Travels (T) Ltd; Director of Marketing & Public Relations", "Kampala International University in Tanzania", "neilmboma@gmail.com", "+255 768 000 808"),
    ("Eng. Noel R. Lema", "CEO", "CODE255 Development Technologies Company Limited", "noellematech@gmail.com", "+255 762 478 893"),
    ("Dr. Mboni Kibelloh", "Lecturer & Co-Founder, Darasa Tech", "Kampala International University in Tanzania", "mboni.kibelloh@gmail.com", "+255 786 067 681"),
]


class Command(BaseCommand):
    help = "Load initial education, skills and sample projects (safe to re-run)."

    def handle(self, *args, **kw):
        SiteSettings.load()
        for i, (t, inst, per, award, icon) in enumerate(EDU):
            Education.objects.get_or_create(title=t, defaults=dict(institution=inst, period=per, award=award, icon=icon, order=i))
        for i, (n, icon) in enumerate(SKILLS):
            Skill.objects.get_or_create(name=n, defaults=dict(icon=icon, order=i))
        for i, (t, slug, cat, d, tech) in enumerate(PROJECTS):
            Project.objects.get_or_create(slug=slug, defaults=dict(title=t, category=cat, short_description=d, tech_stack=tech, order=i))
        for i, (n, jt, org, em, ph) in enumerate(REFEREES):
            Referee.objects.get_or_create(email=em, defaults=dict(full_name=n, job_title=jt, organization=org, phone=ph, order=i, published=True))
        self.stdout.write(self.style.SUCCESS("Seed data loaded."))
