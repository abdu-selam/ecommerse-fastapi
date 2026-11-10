from pathlib import Path
from jinja2 import Environment, FileSystemLoader, select_autoescape
from datetime import datetime, timezone

from app.utils.env import settings

TEMPLATE_DIR = Path(__file__).parent.parent / "templates"

environment = Environment(
    loader=FileSystemLoader(TEMPLATE_DIR),
    autoescape=select_autoescape(["html", "xml"])
)

def render_email(template_name: str, context: dict) -> str:
    template = environment.get_template(template_name)
    return template.render(**context)

def forgot_password_html(token: str) -> str:
    year = datetime.now().year
    context = {
        "token": f"{settings.CLIENT_URL}/auth/forgot-password/{token}",
        "year": year
    }
    html = render_email("forgot_password.html", context)
    return html