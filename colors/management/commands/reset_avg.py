from django.core.management.base import BaseCommand
from colors.models import ReviewAvg

class Command(BaseCommand):
	help = 'Resets Averages'

	def handle(self, *args, **options):
		for review_avg in ReviewAvg.objects.all():
			review_avg.reset_average()
