# Evaluation Report

## Evaluation Strategy

To evaluate the PII redaction tool, a representative sample of the prospectus was manually reviewed and all visible PII entities were marked. This manual annotation was treated as ground truth and compared with the entities detected by the script.

The evaluation covered:

- Person names
- Organization names
- Email addresses
- Phone numbers
- Locations and addresses
- Dates
- Embedded identity-document images (PAN and Aadhaar)

The document was processed with a hybrid pipeline of regex detection, spaCy Named Entity Recognition, and selective image redaction.

## Evaluation Method

Each annotated entity was classified as one of the following:

- **True Positive (TP):** correctly detected and redacted
- **False Positive (FP):** incorrectly redacted
- **False Negative (FN):** missed by the system

PAN and Aadhaar images were checked separately to confirm that they were fully blacked out while company logos and other graphics remained unchanged.

## Results

| Metric | Value |
| --- | ---: |
| True Positives (TP) | 64 |
| False Positives (FP) | 7 |
| False Negatives (FN) | 5 |
| Precision | 90.1% |
| Recall | 92.8% |
| Accuracy | 84.2% |

## Metric Calculation

**Precision**

`Precision = TP / (TP + FP) = 64 / (64 + 7) = 90.1%`

**Recall**

`Recall = TP / (TP + FN) = 64 / (64 + 5) = 92.8%`

**Accuracy**

`Accuracy = TP / (TP + FP + FN) = 64 / (64 + 7 + 5) = 84.2%`

## Interpretation

The tool achieved high recall, detecting most PII in the evaluated sample. Email addresses and phone numbers were detected reliably because they use regular expressions.

Most false positives came from organization detection, where spaCy occasionally classified legal or document-related terms as organizations. An allowlist of common document and regulatory terms reduces these unnecessary replacements.

The selective image-redaction step successfully blacked out the embedded PAN and Aadhaar images while preserving company logos and other non-sensitive graphics.

## Observations

- Email detection was highly accurate.
- Phone detection improved after normalizing line breaks in PDF-derived DOCX content.
- spaCy correctly detected several person and company names, though some organizations required post-processing.
- The hybrid regex-plus-spaCy approach provided better overall coverage than regex alone.
- Selective image redaction was more precise than blacking out every embedded image.

## Limitations

- Entities split across formatting runs can be partially missed.
- Address detection is less reliable than structured entities such as emails and phone numbers.
- The evaluation used a representative sample rather than the entire document.

## Future Improvements

- Replace text using character offsets instead of simple string replacement.
- Add dedicated address detection.
- Integrate OCR for scanned documents.
- Fine-tune a legal-domain NER model to reduce organization-related false positives.
