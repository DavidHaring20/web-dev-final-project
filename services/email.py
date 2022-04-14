def build_plaintext_mail():
    email = """\
        Hi, 
        Thanky you for registering.
    """
    return email


def build_html_mail():
    email = """\
        <html>
            <body>
                <p style="color: blue;">
                    Hi,<br>
                    thank you for registering.
                </p>   
            </body>
        </html>
    """
    return email