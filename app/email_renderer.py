import os
from datetime import datetime
import re
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

OUTPUT_DIR = "agentic-email-campaign-engine/output/campaign_emails"

SMTP_SERVER = "appsmtpgw.core.kmtltd.net.au"
SMTP_PORT = 25
FROM_EMAIL = "campaign-agent@demo.ai"

def render_email(email_json: dict):
    """
    Convert structured email JSON into:
        1. Plain text email
        2. HTML email
    """

    subject = email_json.get("subject", "")
    preheader = email_json.get("preheader", "")
    greeting = email_json.get("greeting", "")
    headline = email_json.get("headline", "")
    intro = email_json.get("intro", "")
    closing = email_json.get("closing", "")
    cta_text = email_json.get("cta_text", "")

    products = email_json.get("products", [])

    # --------------------------------------------------
    # Build TEXT VERSION
    # --------------------------------------------------

    text_products = ""

    for i, p in enumerate(products, start=1):
        text_products += (
            f"\n{i}. {p.get('name','')}\n"
            f"   Price: {p.get('price','')}\n"
            f"   {p.get('description','')}\n"
            f"   Highlight: {p.get('highlight','')}\n"
        )

    email_text = f"""
    Subject: {subject}

    {preheader}

    {headline}

    {greeting}

    {intro}

    Top Picks:
    {text_products}

    CTA: {cta_text}

    {closing}
    """

    # --------------------------------------------------
    # Build BEAUTIFIED HTML VERSION
    # --------------------------------------------------

    html_products = ""

    for p in products:

        html_products += f"""
        <tr>
            <td style="padding:20px 0;border-bottom:1px solid #eee;">
                <table width="100%" cellpadding="0" cellspacing="0">
                    <tr>
                        <td width="160" valign="top">
                            <img src="{p.get('image_url','')}" width="150"
                                style="border-radius:8px;display:block;">
                        </td>

                        <td valign="top" style="padding-left:16px;">
                            <h3 style="margin:0;font-size:16px;color:#111;">
                                {p.get('name','')}
                            </h3>

                            <p style="margin:6px 0;color:#444;">
                                {p.get('description','')}
                            </p>

                            <p style="margin:6px 0;font-weight:bold;color:#000;">
                                {p.get('price','')}
                            </p>

                            <p style="margin:6px 0;color:#d35400;font-style:italic;">
                                {p.get('highlight','')}
                            </p>
                        </td>
                    </tr>
                </table>
            </td>
        </tr>
        """

    email_html = f"""
    <html>
    <body style="margin:0;background-color:#f5f5f5;font-family:Arial,sans-serif;">

    <table width="100%" cellpadding="0" cellspacing="0" style="background:#f5f5f5;padding:20px;">
    <tr>
    <td align="center">

    <table width="600" cellpadding="0" cellspacing="0"
        style="background:#ffffff;padding:30px;border-radius:8px;">

    <tr>
    <td>

    <p style="font-size:12px;color:#888;">{preheader}</p>

    <h1 style="margin-top:0;color:#111;">{headline}</h1>

    <p>{greeting}</p>

    <p style="color:#444;">{intro}</p>

    <table width="100%" cellpadding="0" cellspacing="0">
    {html_products}
    </table>

    <!-- CTA BUTTON -->
    <table width="100%" cellpadding="0" cellspacing="0" style="margin-top:20px;">
    <tr>
    <td align="center">
    <a href="#"
    style="
        background-color:#000;
        color:#fff;
        padding:14px 24px;
        text-decoration:none;
        border-radius:6px;
        font-weight:bold;
        display:inline-block;
    ">
    {cta_text}
    </a>
    </td>
    </tr>
    </table>

    <p style="margin-top:24px;color:#555;">{closing}</p>

    </td>
    </tr>
    </table>

    </td>
    </tr>
    </table>

    </body>
    </html>
    """

    return email_text.strip(), email_html.strip()


def write_email_to_files(subject: str, raw_text: str, html_text: str):
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


def send_campaign_email(
    email_json: dict,
    # email_text: str,
    # email_html: str,
    to_email: list,
    first_name: str = "Customer"
):
    """
    Send campaign email using structured output from Writer + Critic agents.
    """

    subject = email_json.get("subject", "Campaign Email")

    # --------------------------------------------------
    # Build MIME Message
    # --------------------------------------------------

    msg = MIMEMultipart("alternative")
    msg["From"] = FROM_EMAIL
    msg["To"] = ",".join(x for x in to_email)
    msg["Subject"] = subject


    email_text, email_html = render_email(email_json )

    # Attach both text + HTML versions
    msg.attach(MIMEText(email_text, "plain"))
    msg.attach(MIMEText(email_html, "html"))

    # --------------------------------------------------
    # Save email artifacts locally
    # --------------------------------------------------

    write_email_to_files(
        subject=subject,
        raw_text=email_text,
        html_text=email_html
    )

    # --------------------------------------------------
    # Send Email
    # --------------------------------------------------

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.sendmail(FROM_EMAIL, to_email, msg.as_string())

        print("✅ Campaign email sent successfully!")

    except Exception as e:
        print("⚠️ SMTP send failed — running in local/dev mode.")
        print(e)
        print("Prepared email with subject:", subject)
