# 🎓 AdmissionTestBD — মেডিকেল ও বিশ্ববিদ্যালয় ১০০ মডেল টেস্ট প্ল্যাটফর্ম

একটি আধুনিক, পূর্ণাঙ্গ এডমিশন টেস্ট প্রস্তুতি ও জাতীয় মেধা তালিকা প্ল্যাটফর্ম। এখানে রয়েছে মেডিকেল এবং বিশ্ববিদ্যালয় (ঢাবি, রাবি, চবি, জাবি ও সমন্বিত গুচ্ছ) ভর্তি পরীক্ষার ১০০টি করে পূর্ণাঙ্গ মডেল টেস্ট, ১৫ বছরের বিগত বছরের প্রশ্নব্যাংক এবং স্বয়ংক্রিয় bKash পেমেন্ট ভেরিফিকেশন সিস্টেম।

---

## 🌟 প্রধান বৈশিষ্ঠ্যসমূহ (Key Features)

1. **মেডিকেল ১০০ মডেল টেস্ট (Medical 100 Test Series)**:
   - ১ থেকে ৫ নম্বর টেস্ট সম্পূর্ণ **ফ্রি**!
   - ৬ থেকে ১০০ নম্বর টেস্ট (মোট ৯৫টি প্রিমিয়াম টেস্ট) মাত্র **৳৪৯৯**।
   - বোটানি, জুলজি, কেমিস্ট্রি, ফিজিক্স, সাধারণ জ্ঞান ও ইংরেজি সমন্বয়ে ১০০ নম্বরের পূর্ণাঙ্গ নেগেটিভ মার্কিংযুক্ত ওএমআর পরীক্ষা।

2. **ভার্সিটি ও গুচ্ছ ১০০ মডেল টেস্ট (Versity & GST 100 Test Series)**:
   - ১ থেকে ৫ নম্বর টেস্ট সম্পূর্ণ **ফ্রি**!
   - ৬ থেকে ১০০ নম্বর টেস্ট মাত্র **৳৪৯৯**।
   - পদার্থবিজ্ঞান, রসায়ন, গণিত, জীববিজ্ঞান ও শর্টকাট ট্রিকস।

3. **মেগা কম্বো প্যাক (Medical + Versity Combo)**:
   - উভয় পরীক্ষার ২০০টি টেস্টের এককালীন অ্যাক্সেস মাত্র **৳৭৯৯**।

4. **বিগত ১৫ বছরের রিয়েল প্রশ্নব্যাংক (Past 15 Years Archive)**:
   - ২০০৯ থেকে ২০২৪ পর্যন্ত সকল মেডিকেল ও বিশ্ববিদ্যালয় প্রশ্নব্যাংক ও বিস্তারিত ব্যাখ্যা।

5. **লাইভ ন্যাশনাল র‍্যাংকিং ও পার্সেন্টাইল (Live Ranking & Percentile)**:
   - পরীক্ষা জমা দেওয়ার সাথে সাথে ক্লাউড ডেটাবেজে সংরক্ষিত হয়ে লাইভ জাতীয় মেধা স্কোর, র‍্যাংক এবং পার্সেন্টাইল গণনা।

6. **পার্সোনাল বিকাশ অটোমেশন (Personal bKash SMS Automation)**:
   - ব্যক্তিগত বিকাশ একাউন্ট (`01644265766`) - Send Money।
   - শিক্ষার্থীর বিকাশ নাম্বার ও TrxID প্রদান করলেই স্বয়ংক্রিয়ভাবে ট্রানজেকশন ম্যাচ করে প্রিমিয়াম টেস্টগুলো আনলক হয়ে যায়।
   - অ্যান্ড্রয়েড SMS ফরোয়ার্ডারের মাধ্যমে রিয়েল-টাইম ক্লাউড ওয়েবহুক সিঙ্ক।

---

## 🏗️ টেকনোলজি স্ট্যাক (Tech Stack)

- **Frontend**: Single Page Application, Tailwind CSS, Lucide Icons, Glassmorphism UI
- **Backend API**: Python 3.12 Serverless Handler (`http.server.BaseHTTPRequestHandler`)
- **Cloud Database**: Neon Serverless PostgreSQL (`ep-spring-lake...`) with PgBouncer connection pooling
- **Hosting & CDN**: Vercel Edge Serverless Platform
- **Data Stores**: High-performance pre-indexed JSON test banks

---

## 🚀 Vercel ডিপ্লয়মেন্ট গাইড (Vercel Deployment)

### ধাপ ১: Vercel-এ প্রজেক্ট ইম্পোর্ট
1. [Vercel Dashboard](https://vercel.com/dashboard)-এ যান।
2. **"Add New..."** -> **"Project"** ক্লিক করুন।
3. GitHub সিলেক্ট করে **`karim8siam/AdmissionTestBD`** রিপোজিটরি ইম্পোর্ট (Import) করুন।

### ধাপ ২: Environment Variables সেট করা
Vercel Settings-এ গিয়ে **Environment Variables** ট্যাবে নিচের ভেরিয়েবলটি যুক্ত করুন:
- **Key**: `DATABASE_URL`
- **Value**: আপনার Neon PostgreSQL Connection String:
  ```text
  postgresql://neondb_owner:npg_YIR9cGa5MqOP@ep-spring-lake-b45687pc-pooler.c-6.us-east-2.aws.neon.tech/neondb?sslmode=require
  ```

### ধাপ ৩: Deploy
- **"Deploy"** বাটনে ক্লিক করুন। কয়েক সেকেন্ডে সাইট লাইভ হয়ে যাবে!

---

## 📱 অ্যান্ড্রয়েড bKash SMS ফরোয়ার্ডার সেটআপ (SMS Forwarder Setup)

শিক্ষার্থী টাকা পাঠালে আপনার ফোনে bKash-এর মেসেজ আসা মাত্রই যাতে স্বয়ংক্রিয়ভাবে সার্ভারে লগ হয়ে যায়:

1. গুগল প্লে স্টোর থেকে **"SMS Forwarder"** (বা **"Webhook SMS Forwarder"**) ডাউনলোড করুন।
2. একটি নতুন Forward Rule তৈরি করুন:
   - **Sender Filter**: `bKash` (অথবা আপনার সিমের বিকাশ সেন্ডার আইডি)
   - **Target / Action**: **Webhook (HTTP POST)**
   - **URL**: `https://<YOUR-VERCEL-DOMAIN>.vercel.app/api/payment/sms-webhook`
   - **Method**: `POST`
   - **Content-Type**: `application/json`
   - **Payload Template**:
     ```json
     {
       "sender": "{from}",
       "message": "{sms}"
     }
     ```
3. "Save" করে সক্রিয় রাখুন। এখন থেকে যেকোনো বিকাশ পেমেন্ট স্বয়ংক্রিয়ভাবে ক্লাউড ডাটাবেজে সিঙ্ক হয়ে যাবে!

---

## 📂 প্রোজেক্ট স্ট্রাকচার (Project Structure)

```text
AdmissionTestBD/
├── index.html               # প্রধান ওয়েব অ্যাপ্লিকেশন ও ওএমআর টেস্ট ইঞ্জিন
├── vercel.json              # Vercel সার্ভারলেস ও ক্যাশিং কনফিগারেশন
├── requirements.txt         # পাইথন সার্ভারলেস ডিপেন্ডেন্সি (psycopg2-binary)
├── api/
│   └── index.py             # Vercel Serverless Function (Webhook, Ranking, Payment)
├── data/                    # ১০০ টেস্ট ও বিগত ১৫ বছরের ডেটাব্যাংক (.json)
│   ├── medical_100_tests.json
│   ├── versity_100_tests.json
│   ├── past_15years_tests.json
│   └── ...
├── web/
│   ├── index.html
│   └── assets/              # ইলাস্ট্রেশন ও ইউজার ইন্টারফেস অ্যাসেটস
└── server.py                # লোকাল ডেভেলপমেন্ট ও প্রিভিউ সার্ভার
```

---

## 👨‍💻 লোকাল রান (Local Development)

```bash
# লোকাল সার্ভার চালু করতে:
python3 server.py
# ব্রাউজারে ওপেন করুন: http://127.0.0.1:8080
```
