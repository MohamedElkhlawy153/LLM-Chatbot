FROM python:3.9-slim

  WORKDIR /app

  # تثبيت المتطلبات
  COPY requirements.txt .
  RUN pip install --no-cache-dir -r requirements.txt

  # إنشاء مجلد السجلات
  RUN mkdir -p /app/logs

  # نسخ الملفات
  COPY . .

  # تعريف المنفذ
  EXPOSE 8000

  # متغيرات البيئة
  ENV PYTHONUNBUFFERED=1
  ENV PYTHONDONTWRITEBYTECODE=1

  # تشغيل التطبيق
  CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]