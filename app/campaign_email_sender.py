import os
from datetime import datetime

# =====================================================
# CONFIG — EMAIL DETAILS
# =====================================================

# FROM_EMAIL = "cogniversal-agent@demo.ai"
# TO_EMAIL = "prajwal.sk@anko.com"

OUTPUT_DIR = "agentic-email-campaign-engine/output/campaign_emails"

import re
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# =====================================================
# CONFIG (DUMMY SMTP — replace later if needed)
# =====================================================

SMTP_SERVER = "localhost"
SMTP_PORT = 1025
FROM_EMAIL = "campaign-agent@demo.ai"


# =====================================================
# PARSE SUBJECT + BODY FROM GENERATED EMAIL
# =====================================================
def parse_generated_email(raw_text: str):

    # Extract subject line dynamically
    subject_match = re.search(r'\*\*Subject Line:\*\*\s*"(.*?)"', raw_text)
    subject = subject_match.group(1) if subject_match else "Campaign Update"

    # Remove markdown stars for cleaner rendering
    clean_body = re.sub(r"\*\*", "", raw_text)

    return subject, clean_body


# =====================================================
# BUILD HTML EMAIL (CAMPAIGN STYLE)
# =====================================================
def build_html_email(body_text: str, first_name="Customer"):

    # Replace placeholders dynamically
    body_text = body_text.replace("[First Name]", first_name)
    body_text = body_text.replace("\n", "<br>")

    html = f"""
    <html>
        <body style="font-family:Arial;padding:20px;">
            <div style="max-width:700px;margin:auto;">
                {body_text}
                <hr>
                <p style="color:gray;font-size:12px;">
                Sent via Cogniversal Agent Campaign Engine 🚀
                </p>
            </div>
        </body>
    </html>
    """

    return html

def write_email_to_file(subject: str, raw_text: str, html_text: str):
    """
    Writes campaign email artifacts locally.
    Creates:
        - raw email file
        - html email file
    """

    # Create folder safely
    # Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)

    # Clean subject for filename safety
    safe_subject = re.sub(r"[^\w-]", "", subject)[:60]

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    os.makedirs(f"{OUTPUT_DIR}/{safe_subject}", exist_ok=True)

    raw_path = f"{OUTPUT_DIR}/{safe_subject}/{timestamp}.txt"
    html_path = f"{OUTPUT_DIR}/{safe_subject}/{timestamp}.html"


    # Write RAW email
    with open(raw_path, "w", encoding="utf-8") as f:
        f.write(raw_text)

    # Write HTML email
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_text)

    print(f"Email artifacts saved:")
    print(f"   RAW  → {raw_path}")
    print(f"   HTML → {html_path}")

# =====================================================
# SEND EMAIL FUNCTION (DYNAMIC CONTENT)
# =====================================================
def send_campaign_email(raw_generated_email, to_email, first_name="Customer"):

    subject, body_text = parse_generated_email(raw_generated_email)

    html_content = build_html_email(body_text, first_name)

    msg = MIMEMultipart("alternative")
    msg["From"] = FROM_EMAIL
    msg["To"] = to_email
    msg["Subject"] = subject

    msg.attach(MIMEText(html_content, "html"))

    write_email_to_file(
        subject=subject,
        raw_text=raw_generated_email,
        html_text=html_content
    )

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.send_message(msg)

        print("Campaign email sent successfully!")

    except Exception as e:
        print(e)
        print("Dummy send (no SMTP server running)")
        print("Email prepared with subject:", subject)


# # =====================================================
# # EXAMPLE AGENT OUTPUT (YOUR DYNAMIC INPUT)
# # =====================================================
# generated_email_example = """
# ====== FINAL EMAIL ======

# **Subject Line:** "Create Magical Holiday Memories with Our Exclusive Christmas Decors!"

# **Preheader Text:** "Get ready to sparkle this holiday season with our stunning Christmas decors!"

# Dear [First Name],

# As the holiday season approaches, we're thrilled to bring you the most enchanting Christmas decors...
# """


# # =====================================================
# # RUN
# # =====================================================
# if __name__ == "__main__":
#     send_campaign_email(
#         generated_email_example,
#         to_email="dummy.personal@email.com",
#         first_name="Prajwal"
#     )
