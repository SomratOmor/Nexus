from flask import Flask, render_template, request, jsonify
import threading
import subprocess
import os
import gc

app = Flask(__name__)

# তোমার সেই ডার্ক থিম এবং সিস্টেম প্রম্পট
SYSTEM_PROMPT = "তুমি নেক্সাস কমান্ড সেন্টার, একজন সিনিয়র এআই আর্কিটেক্ট। সম্রাটের ফোনের জন্য তুমি অপ্টিমাইজড কোড এবং অটোমেশন প্রদান করো।"

# ব্যাকগ্রাউন্ডে বিল্ড করার ফাংশন
def start_build_process():
    print("--- বিল্ড প্রসেস শুরু হয়েছে সম্রাট! ---")
    try:
        # মেমোরি পরিষ্কার করা
        gc.collect()
        
        # সরাসরি বিল্ডোজার কমান্ড রান (আউটপুট টার্মিনালে দেখা যাবে)
        # Python 3.13 এর জন্য distutils প্যাচসহ
        env = os.environ.copy()
        env['SETUPTOOLS_USE_DISTUTILS'] = 'stdlib'
        
        process = subprocess.Popen(
            ['buildozer', '-v', 'android', 'debug'],
            env=env,
            cwd='/storage/emulated/0/Ai' # তোমার প্রজেক্ট পাথ
        )
        process.wait()
        
        if process.returncode == 0:
            # বিল্ড সফল হলে ফাইলটি স্টোরেজে পাঠানো
            os.system("mkdir -p /storage/emulated/0/app")
            os.system("cp bin/*.apk /storage/emulated/0/app/")
            print("--- APK সফলভাবে /storage/emulated/0/app ফোল্ডারে পাঠানো হয়েছে! ---")
    except Exception as e:
        print(f"বিল্ড এরর: {str(e)}")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get("message", "").lower()
    
    # ১ সেকেন্ডে রিপ্লাই দেওয়ার লজিক
    if "apk" in user_message or "build" in user_message:
        # থ্রেড ব্যবহার করে বিল্ড আলাদা রাস্তায় পাঠিয়ে দেওয়া হলো
        build_thread = threading.Thread(target=start_build_process)
        build_thread.daemon = True
        build_thread.start()
        
        return jsonify({"reply": "সম্রাট, কমান্ড সফল! ১ সেকেন্ডের মধ্যেই ব্যাকগ্রাউন্ডে APK বিল্ড ইঞ্জিন চালু করা হয়েছে। দয়া করে টার্মিনাল লগ চেক করুন।"})

    # সাধারণ চ্যাট রিপ্লাই
    reply = f"নেক্সাস রেডি। আপনার কমান্ড '{user_message}' প্রসেস করা হচ্ছে..."
    return jsonify({"reply": reply})

if __name__ == '__main__':
    # পোর্ট ৮০০০ এ রান হবে
    app.run(host='0.0.0.0', port=8000, debug=False)