from django.db import models

class SiteContent(models.Model):
    key = models.SlugField("Ключ", unique=True)
    title = models.CharField("Заголовок", max_length=200, blank=True)
    body = models.TextField("Текст", blank=True)
    image = models.ImageField("Изображение", upload_to="content/", blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        verbose_name = "Информационный блок"
        verbose_name_plural = "Информационные блоки"
    def __str__(self): return self.title or self.key

