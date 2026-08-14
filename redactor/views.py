from django.shortcuts import render

# Create your views here.
import logging
import tempfile
from pathlib import Path
from uuid import uuid4

from django.http import FileResponse
from django.shortcuts import redirect, render

from docx import Document

from redact_pii import (
    redact_document,
    blackout_identity_images_in_docx,
)

logger = logging.getLogger(__name__)


def index(request):
    if request.method == "POST" and request.FILES.get("document"):
        uploaded = request.FILES["document"]

        try:
            # Write uploaded file to a temp path
            with tempfile.NamedTemporaryFile(
                delete=False,
                suffix=".docx"
            ) as temp_input:
                for chunk in uploaded.chunks():
                    temp_input.write(chunk)
                input_path = temp_input.name

            output_path = str(
                Path(tempfile.gettempdir()) / f"redacted-{uuid4()}.docx"
            )

            doc = Document(input_path)
            redacted = redact_document(doc)
            redacted.save(output_path)

            blackout_identity_images_in_docx(output_path)

            # Stream the file directly in this response — avoids storing
            # a temp-file path in the session, which breaks on Render's
            # ephemeral filesystem when a different worker handles /download.
            output_name = f"{Path(uploaded.name).stem}_redacted.docx"
            return FileResponse(
                open(output_path, "rb"),
                as_attachment=True,
                filename=output_name,
            )

        except Exception as exc:
            logger.exception("Redaction failed: %s", exc)
            return render(
                request,
                "redactor/index.html",
                {"error": "Redaction failed. Please ensure the file is a valid .docx document and try again."},
            )

    return render(request, "redactor/index.html")


def _redacted_document(request):
    """Return the current visitor's generated document, if it still exists."""
    path = request.session.get("redacted_document_path")

    if not path or not Path(path).is_file():
        return None

    return path


def preview(request):
    output_path = _redacted_document(request)
    if not output_path:
        return redirect("index")

    doc = Document(output_path)
    paragraphs = [paragraph.text for paragraph in doc.paragraphs if paragraph.text.strip()]

    for table in doc.tables:
        for row in table.rows:
            paragraphs.extend(
                cell.text.strip() for cell in row.cells if cell.text.strip()
            )

    return render(
        request,
        "redactor/preview.html",
        {"paragraphs": paragraphs},
    )


def download(request):
    output_path = _redacted_document(request)
    if not output_path:
        return redirect("index")

    return FileResponse(
        open(output_path, "rb"),
        as_attachment=True,
        filename=request.session.get(
            "redacted_document_name", "redacted_document.docx"
        ),
    )
