from django.core.management.base import BaseCommand
from blog.models import Category

class Command(BaseCommand):
    help = 'Creates default categories for the blog'

    def handle(self, *args, **kwargs):
        default_categories = [
            'Technology',
            'Lifestyle',
            'Travel',
            'Food',
            'Health',
            'Business',
            'Education',
            'Entertainment',
            'Sports',
            'Science'
        ]

        for category_name in default_categories:
            Category.objects.get_or_create(
                name=category_name,
                defaults={'slug': category_name.lower().replace(' ', '-')}
            )

        self.stdout.write(self.style.SUCCESS('Successfully created default categories')) 