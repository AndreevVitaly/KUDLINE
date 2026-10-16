from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from tempfile import TemporaryDirectory

class InquiryApiTests(TestCase):
    def test_creates_inquiry(self):
        response = self.client.post("/api/inquiries/", {"name":"Иван", "phone":"+7 900 000-00-00", "description":"Нужен расчёт", "consent":"true"})
        self.assertEqual(response.status_code, 201)

    def test_rejects_unsafe_extension(self):
        with TemporaryDirectory() as media:
            with override_settings(MEDIA_ROOT=media):
                file = SimpleUploadedFile("payload.exe", b"unsafe")
                response = self.client.post("/api/inquiries/", {"name":"Иван", "phone":"123", "description":"Задача", "consent":"true", "attachment":file})
                self.assertEqual(response.status_code, 400)
