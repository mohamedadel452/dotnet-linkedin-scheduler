# 🔑 دليل ربط حسابك في LinkedIn API للنشر التلقائي (في 3 دقائق)

لتتمكن أتمتة **`Daily .NET LinkedIn Publisher`** من النشر المباشر على حسابك يومياً في الساعة **10:00 صباحاً**، اتبع هذه الخطوات البسيطة لاستخراج **Access Token** مجاني من منصة مطوري LinkedIn:

---

### الخطوة 1️⃣: إنشاء تطبيق على LinkedIn Developers
1. افتح الرابط الرسمي: [https://www.linkedin.com/developers/apps/new](https://www.linkedin.com/developers/apps/new)
2. املأ البيانات كالتالي:
   - **App name**: `Mohamed Adel DotNet Publisher`
   - **LinkedIn Page**: اختر أي صفحة شركة عامة أو أنشئ صفحة بسيطة باسمك (Create a new LinkedIn Page) — هذا شرط شكلي من LinkedIn لإنشاء أي تطبيق.
   - **App logo**: ارفع أي صورة أو شعار.
   - ضع علامة صح على *I have read and agree to these terms* ثم اضغط **Create app**.

---

### الخطوة 2️⃣: تفعيل صلاحية النشر (`Share on LinkedIn`)
1. من داخل صفحة التطبيق الذي أنشأته، اذهب إلى تبويب **Products**.
2. ستجد خيارين أساسيين، اضغط **Request access** أمام كل منهما (يتم تفعيلهما فوراً في نفس اللحظة):
   - ✅ **Share on LinkedIn** (يمنح صلاحية `w_member_social` لنشر المنشورات والصور).
   - ✅ **Sign In with LinkedIn using OpenID Connect** (يمنح صلاحيتي `openid` و `profile` لمعرفة معرّف حسابك تلقائياً).

---

### الخطوة 3️⃣: توليد الـ Access Token (بدون كتابة كود)
1. افتح أداة OAuth الرسمية من LinkedIn: [https://www.linkedin.com/developers/tools/oauth](https://www.linkedin.com/developers/tools/oauth)
2. اضغط على **Create token** واختر تطبيقك (`Mohamed Adel DotNet Publisher`).
3. تحت قسم **Scopes**، حدد الخيارات الثلاثة التالية:
   - `openid`
   - `profile`
   - `w_member_social`
4. اضغط **Request access token** ووافق على الصلاحيات، ثم انسخ الـ **Access Token** الذي سيظهر لك.

---

### الخطوة 4️⃣: حفظ الـ Token في المحرك
يمكنك حفظ الـ Token بإحدى طريقتين:
- **الطريقة الأولى**: أرسله لي هنا في المحادثة وسأقوم بحفظه واختباره لك فوراً.
- **الطريقة الثانية**: شغّل الأمر التالي في الـ Terminal:
  ```powershell
  python "D:\مذاكرة\Dot-Net\LinkedIn_Branding_Engine\publish_to_linkedin.py" --set-token "ضع_التوكن_هنا"
  ```
