import smtplib, os, math
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders

MAX_EMAIL_SIZE_MB = 20   # Stay well under Gmail's 25 MB limit

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
        if not os.path.exists(filepath):
            print(f"⚠️ File missing: {filepath}, skipping.")
            continue
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
    
    # Always include caption in every email (tiny)
    base_attachments = [caption_file]
    # Group images into batches such that total size per email < MAX_EMAIL_SIZE_MB
    # Compute sizes
    file_sizes = {}
    for f in image_files + [video_file]:
        if os.path.exists(f):
            file_sizes[f] = os.path.getsize(f)
    
    # Send video + caption in first email (video usually ~5-10 MB)
    video_batch = [video_file] + base_attachments
    video_size = file_sizes.get(video_file, 0) + os.path.getsize(caption_file)
    if video_size < MAX_EMAIL_SIZE_MB * 1024 * 1024:
        send_email(video_batch, "🎬 Today's AI influencer video + caption", "Your daily video and caption are attached!")
    else:
        print("⚠️ Video too large, sending without attachment (you can download from artifacts).")
        send_email(base_attachments, "🎬 Video ready (download link in artifacts)", "Video was too large for email. Download from GitHub Actions artifacts.")
    
    # Now split images into groups that fit under 20 MB
    current_batch = []
    current_size = 0
    batch_num = 1
    for img in image_files:
        img_size = file_sizes.get(img, 0)
        # If adding this image would exceed limit, send current batch and start new one
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
