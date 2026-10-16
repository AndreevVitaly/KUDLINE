from django.db import models

class Direction(models.Model):
    title = models.CharField("Название", max_length=200)
    slug = models.SlugField(unique=True)
    short_description = models.TextField("Краткое описание", blank=True)
    description = models.TextField("Полное описание", blank=True)
    image = models.ImageField("Изображение", upload_to="directions/", blank=True)
    order = models.PositiveIntegerField("Порядок", default=0)
    published = models.BooleanField("Опубликовано", default=True)
    class Meta:
        ordering = ("order", "title")
        verbose_name = "Направление"
        verbose_name_plural = "Направления"
    def __str__(self): return self.title

class ContactInfo(models.Model):
    company_name = models.CharField("Компания", max_length=200, default="ООО «КУДЛАЙН»")
    phone = models.CharField("Телефон", max_length=50)
    email = models.EmailField("Email")
    address = models.CharField("Адрес производства", max_length=300)
    requisites = models.TextField("Реквизиты", blank=True)
    is_active = models.BooleanField("Активно", default=True)
    class Meta:
        verbose_name = "Контактные данные"
        verbose_name_plural = "Контактные данные"
    def __str__(self): return self.company_name

