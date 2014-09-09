from django.contrib import admin
from polls.models import Choice, Question

# Register your models here.

class ChoiceInline(admin.TabularInline):
	model = Choice
	extra = 3

class QuestionAdmin(admin.ModelAdmin):
	fieldsets = [
		(None, {'fields': ['question_text']}),
		('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
	]
	inlines = [ChoiceInline]
	list_display = ('question_text', 'pub_date', 'was_published_recently')
	def was_published_recently(self):
		return self.pub_date >= timezone.new() - datetime.timedelta(days=1)
	was_published_recently.admin_order_field = 'pub_date'
	was_published_recently.boolean = True
	was_published_recently.short_description = 'Published recently?'
	list_filter = ['pub_date']
	search_fields = ['question_date']

admin.site.register(Question, QuestionAdmin)

