from django.contrib import admin

class BookAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'country', 'publish_year', 'slug')
    list_display_links = ('id', 'name')
    search_fields = ('name', 'country', 'publish_year')
    prepopulated_fields = {'slug':['name']}
