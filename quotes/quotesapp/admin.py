from django.contrib import admin
from .models import Tag, Quote
# from .scrapper import execute

# class Scrap(admin.ModelAdmin):

#     def run_scraper(self, request, queryset):
#         for obj in queryset:
#             execute(obj.url)  # передайте URL в вашу функцию скрапинга

#     actions = ['run_scraper']

# Register your models here.
admin.site.register(Tag)
admin.site.register(Quote)
# admin.site.register(Quote, Scrap)