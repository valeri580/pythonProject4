from django.core.management.base import BaseCommand
from news.models import News_post

class Command(BaseCommand):
    help = 'Одобряет все существующие новости'

    def handle(self, *args, **options):
        # Одобряем все существующие новости
        news_count = News_post.objects.filter(is_approved=False).update(is_approved=True)
        
        self.stdout.write(
            self.style.SUCCESS(f'✅ Одобрено {news_count} новостей!')
        )
        
        total_news = News_post.objects.count()
        self.stdout.write(
            self.style.SUCCESS(f'📰 Всего новостей в системе: {total_news}')
        )
