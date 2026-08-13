# PII Redaction Tool

## Overview

This Django application redacts personally identifiable information (PII) from DOCX files and generates a downloadable redacted copy. It was designed for a Red Herring Prospectus containing company information, contact details, names, addresses, dates, and embedded identity-document images.

The web interface lets users upload a DOCX file, shows a loading indicator with an estimated processing time, then provides a browser preview and a DOCX download once redaction is complete.

## Approach

The project uses a hybrid detection pipeline:

- **Regular expressions** identify structured PII such as email addresses, phone numbers, IP addresses, SSNs, credit-card numbers, and date-like values.
- **spaCy Named Entity Recognition (NER)** identifies contextual entities such as person names, organization names, locations, and dates.
- **Faker** creates realistic replacement values.
- **Mapping dictionaries** ensure every occurrence of the same source value receives the same replacement within a run.
- **python-docx** processes document paragraphs and tables while preserving most DOCX formatting.

## Image Redaction

The prospectus includes PAN and Aadhaar images. The tool selectively blacks out `image4.png` and `image5.png`, preserving logos and other non-sensitive graphics instead of removing every image in the document.

## Features

- Redacts person names, organization names, locations, emails, phone numbers, and dates
- Detects additional structured values, including IP addresses, SSNs, and credit-card numbers
- Produces consistent fake replacements for repeated values
- Processes document paragraphs and tables
- Preserves logos and non-sensitive images
- Blacks out the specified embedded PAN and Aadhaar images
- Provides a loading state, estimated processing time, in-browser text preview, and DOCX download

## Requirements

- Python 3.14 (the included environment was created with this version)
- The packages listed in `requirements.txt`

## Installation

```bash
cd /Users/kundankumarsingh/scalar_project/pii_web
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
```

`requirements.txt` installs the compatible `en_core_web_sm` spaCy language model, so no separate `spacy download` command is needed.

## Run the Web Application

```bash
python manage.py runserver
```

Open <http://127.0.0.1:8000/> in a browser. Upload a `.docx` file, wait for redaction to finish, then choose **Preview** or **Download .docx**.

## Standalone Script

`redact_pii.py` also includes a standalone entry point. It expects the following paths to exist:

- `input/Red Herring Prospectus.docx`
- `output/Red_Herring_Prospectus_Redacted.docx`

Run it with:

```bash
python redact_pii.py
```

## Libraries Used

- Django
- spaCy
- python-docx
- Faker
- Pillow

## Design Decisions

Regex is reliable for values with fixed formats, whereas spaCy is more effective for names and organizations that do not follow strict patterns. Because spaCy can classify legal or document-related terms as organizations, the project includes an allowlist to reduce unnecessary replacements.

## Limitations

- Entities split between DOCX formatting runs can be partially missed.
- spaCy can still produce false positives for legal or financial terminology.
- Address detection is less reliable than detection of structured values.
- The selective image-redaction logic targets the known PAN and Aadhaar image filenames from the source prospectus.

## Future Improvements

- Replace text using character offsets instead of simple string replacement.
- Add dedicated address detection.
- Add OCR support for scanned PDFs and images.
- Fine-tune a legal-domain NER model or integrate Microsoft Presidio.

## Evaluation

See [Evaluation_Report.md](Evaluation_Report.md) for the test methodology, results, and interpretation.
