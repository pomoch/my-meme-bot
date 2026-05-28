import smtplib, os
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders

MAX_EMAIL_SIZE_MB = 20   # under Gmail's 25 MB limit

def safe_getsize(filepath):
    """Return file size in bytes, or 0 if file does not exist."""
    if os.path.exists(filepath):
        return os.path.getsize(filepath)
    else:
        print(f"⚠️ File not found (skipping): {filepath}")
        return 0

def send_email(attachments, subject, body):
    username = os.getenv("EMAIL_USERNAME")
    password = os.getenv("EMAIL_PASSWORD")
    to_email = os.getenv("EMAIL_TO")
    
    msg = MIMEMultipart()
    msg["From"] = f"AI Influencer Bot <{username}>"
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))
    
    total_size = 0
    for filepath in attachments:
        size = safe_getsize(filepath)
        if size == 0:
            continue   # skip missing files
        with open(filepath, "rb") as f:
            data = f.read()
        total_size += len(data)
        part = MIMEBase("application", "octet-stream")
        part.set_payload(data)
        encoders.encode_base64(part)
        part.add_header("Content-Disposition", f"attachment; filename={os.path.basename(filepath)}")
        msg.attach(part)
    
    # Send
    try:
        server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server.login(username, password)
        server.send_message(msg)
        server.quit()
        print(f"✅ Email sent: {subject} ({total_size/(1024*1024):.1f} MB)")
    except Exception as e:
        print(f"❌ Failed to send {subject}: {e}")

def main():
    # Gather all files
    image_files = sorted([f for f in os.listdir() if f.startswith("image_") and f.endswith(".jpg")])
    video_file = "daily_video.mp4"
    caption_file = "caption.txt"
    
    # Always include caption only if it exists
    base_attachments = [caption_file] if os.path.exists(caption_file) else []
    
    # Compute sizes for existing files
    file_sizes = {}
    for f in image_files + [video_file]:
        size = safe_getsize(f)
        if size > 0:
            file_sizes[f] = size
    
    # Send video + caption (if video exists)
    video_attachments = []
    if os.path.exists(video_file):
        video_attachments.append(video_file)
    video_attachments.extend(base_attachments)
    video_size = sum(file_sizes.get(f, 0) for f in video_attachments)
    if video_attachments and video_size < MAX_EMAIL_SIZE_MB * 1024 * 1024:
        send_email(video_attachments, "🎬 Today's AI influencer video + caption", "Your daily video and caption are attached!")
    elif os.path.exists(video_file):
        print("⚠️ Video too large, sending without attachment (download from artifacts).")
        send_email(base_attachments, "🎬 Video ready (download in artifacts)", "Video was too large for email. Download from GitHub Actions artifacts.")
    else:
        print("⚠️ No video file found; skipping video email.")
    
    # Split images into batches that fit under 20 MB
    if not image_files:
        print("⚠️ No image files found.")
        return
    
    current_batch = []
    current_size = 0
    batch_num = 1
    for img in image_files:
        img_size = file_sizes.get(img, 0)
        if current_size + img_size > MAX_EMAIL_SIZE_MB * 1024 * 1024 and current_batch:
            attachments = current_batch + base_attachments
            send_email(attachments, f"📸 AI influencer photos (part {batch_num})", "Ultra‑sharp 6K images attached!")
            batch_num += 1
            current_batch = [img]
            current_size = img_size
        else:
            current_batch.append(img)
            current_size += img_size
    # Send remaining
    if current_batch:
        attachments = current_batch + base_attachments
        send_email(attachments, f"📸 AI influencer photos (part {batch_num})", "Ultra‑sharp 6K images attached!")
        batch_num += 1

if __name__ == "__main__":
    main()
