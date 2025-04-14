import asyncio
import aiosmtplib
from email.message import EmailMessage

async def send_test_email():
    msg = EmailMessage()
    msg["From"] = "Your Name <your_username@ethereal.email>"
    msg["To"] = "Recipient Name <recipient@example.com>"  # Can be your own email for testing
    msg["Subject"] = "Hello from Python"
    msg.set_content("This is a test email sent through Ethereal using aiosmtplib.")

    await aiosmtplib.send(
        msg,
        hostname="smtp.ethereal.email",
        port=587,
        start_tls=True,
        username="your_username@ethereal.email",      # Replace with your Ethereal username
        password="your_ethereal_password",            # Replace with your Ethereal password
    )
    print("✅ Test email sent successfully!")

# Run the async function
asyncio.run(send_test_email())
