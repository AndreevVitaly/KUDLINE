from django.db import models

class Project(models.Model):
    title = models.CharField("Название", max_length=240)
    slug = models.SlugField(unique=True)
    short_description = models.TextField("Краткое описание", blank=True)
    description = models.TextField("Описание задачи", blank=True)
    completed_work = models.TextField("Выполненные работы", blank=True)
    features = models.TextField("Особенности конструкции", blank=True)
    result = models.TextField("Результат", blank=True)
    location = models.CharField("Местоположение", max_length=200, blank=True)
    year = models.PositiveSmallIntegerField("Год", null=True, blank=True)
    cover_image = models.ImageField("Обложка", upload_to="projects/covers/", blank=True)
    published = models.BooleanField("Опубликовано", default=False)
    featured = models.BooleanField("На главной", default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        ordering = ("-year", "-created_at")
        verbose_name = "Проект"
        verbose_name_plural = "Проекты"
    def __str__(self): return self.title

class ProjectImage(models.Model):
    project = models.ForeignKey(Project, related_name="images", on_delete=models.CASCADE)
    image = models.ImageField("Фотография", upload_to="projects/gallery/")
    caption = models.CharField("Подпись", max_length=240, blank=True)
    order = models.PositiveIntegerField("Порядок", default=0)
    class Meta:
        ordering = ("order", "id")
        verbose_name = "Фотография проекта"
        verbose_name_plural = "Фотографии проектов"

