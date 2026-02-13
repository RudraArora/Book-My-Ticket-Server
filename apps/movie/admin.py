from django.contrib import admin

from apps.movie import models as movie_models


class MovieModelAdmin(admin.ModelAdmin):
    readonly_fields = ("slug",)


admin.site.register(movie_models.Movie, MovieModelAdmin)
admin.site.register(movie_models.Language)
admin.site.register(movie_models.Genre)
