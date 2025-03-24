from django.db import migrations
import re

def update_tag_slugs(apps, schema_editor):
    Tag = apps.get_model('blog', 'Tag')
    for tag in Tag.objects.all():
        # Replace any non-alphanumeric characters with hyphens
        slug = re.sub(r'[^a-zA-Z0-9]+', '-', tag.name.lower())
        # Remove leading/trailing hyphens
        slug = slug.strip('-')
        tag.slug = slug
        tag.save()

class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(update_tag_slugs),
    ] 