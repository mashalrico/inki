#!/bin/bash

# === إعداد المشروع لرفع Django على GitHub ===

# 1. تأكد من تشغيل السكربت من مجلد المشروع الرئيسي
echo "تأكد انك بالمجلد الرئيسي للمشروع (اللي يحتوي manage.py)"
pwd
echo "==============================="

# 2. إنشاء Git repository جديد
git init

# 3. ربط الريموت بالمستودع
read -p "ادخل رابط GitHub repo (مثال: https://github.com/mashalrico/inki.git): " REPO
git remote add origin $REPO

# 4. إنشاء .gitignore تلقائياً
echo "إنشاء ملف .gitignore..."
cat > .gitignore <<EOL
*.pyc
__pycache__/
db.sqlite3
venv/
*.log
*.pot
*.py[cod]
*.sqlite3
.DS_Store
EOL
echo ".gitignore تم إنشاؤه"

# 5. إضافة كل الملفات للمستودع
git add .

# 6. إنشاء commit
git commit -m "Upload full Django project"

# 7. دفع الملفات إلى GitHub مع force
git push -u origin main --force

echo "تم رفع المشروع كامل على GitHub!"
