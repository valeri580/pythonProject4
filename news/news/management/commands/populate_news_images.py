from django.core.management.base import BaseCommand
from news.models import News_post, NewsImage


class Command(BaseCommand):
	help = 'Создает по 10 изображений для каждой новости (picsum.photos)'

	def add_arguments(self, parser):
		parser.add_argument('--per_post', type=int, default=10, help='Сколько изображений на новость')

	def handle(self, *args, **options):
		per_post = options['per_post']
		created_total = 0
		for post in News_post.objects.all():
			# Существующие не трогаем, только добавляем до нужного количества
			existing = post.images.count()
			to_create = max(0, per_post - existing)
			for i in range(to_create):
				# Стабильный, но уникальный URL на основе id поста и индекса
				url = f'https://picsum.photos/seed/news{post.id}_{existing + i + 1}/800/400'
				NewsImage.objects.create(news_post=post, image_url=url)
				created_total += 1
		self.stdout.write(self.style.SUCCESS(f'Добавлено изображений: {created_total}'))


