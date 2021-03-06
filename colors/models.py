from django.db import models

class Item(models.Model):
	name = models.CharField(max_length=16)
	highest_avg = models.ForeignKey('ReviewAvg', on_delete=models.CASCADE, related_name='items', null=True)

	def __str__(self):
		return self.name

	def reset_highest(self):
		self.highest_avg = max(self.review_avgs.all(), key=lambda x:x.score)
		self.save()

class Color(models.Model):
	name = models.CharField(max_length=16)

	def __str__(self):
		return self.name

class Review(models.Model):
	item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='reviews')
	color = models.ForeignKey(Color, on_delete=models.CASCADE, related_name='reviews')
	score = models.IntegerField()

class ReviewAvg(models.Model):
	item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='review_avgs')
	color = models.ForeignKey(Color, on_delete=models.CASCADE, related_name='review_avgs')
	score = models.FloatField(default=0)
	count = models.IntegerField(default=0)

	def add_review(self, review):
		'''Adjust the score and count based on a review'''
		rev_total = self.score * self.count
		rev_total += review.score
		self.count += 1
		self.score = rev_total / self.count
		self.save()

	def reset_average(self):
		'''Totally reset the count and score for a review average'''
		reviews = Review.objects.filter(item=self.item).filter(color=self.color)
		count = len(reviews)
		agg = sum((review.score for review in reviews))
		self.count = count
		self.score = agg/count
		self.save()
