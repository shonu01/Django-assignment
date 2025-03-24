from django.core.management.base import BaseCommand
from blog.models import Tag

class Command(BaseCommand):
    help = 'Creates default tags for the blog'

    def handle(self, *args, **kwargs):
        default_tags = [
            'Technology',
            'Programming',
            'Web Development',
            'Python',
            'Django',
            'JavaScript',
            'HTML',
            'CSS',
            'Database',
            'API',
            'Frontend',
            'Backend',
            'DevOps',
            'Cloud',
            'Security',
            'Testing',
            'Design',
            'UI/UX',
            'Mobile',
            'AI/ML'
        ]

        for tag_name in default_tags:
            Tag.objects.get_or_create(
                name=tag_name,
                defaults={'slug': tag_name.lower().replace(' ', '-')}
            )

        self.stdout.write(self.style.SUCCESS('Successfully created default tags')) 