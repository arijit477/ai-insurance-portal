class AIPrompts:
    """
    Centralized prompt templates for the AI Insurance Portal.
    """

    # ==========================================================
    # OCR Document Extraction
    # ==========================================================

    DOCUMENT_EXTRACTION = """
You are an expert insurance document parser.

Extract all important information from the document.

Return ONLY valid JSON.

Fields:

{
    "document_type":"",
    "invoice_number":"",
    "hospital":"",
    "garage":"",
    "patient_name":"",
    "vehicle_number":"",
    "policy_number":"",
    "claim_number":"",
    "date":"",
    "total_amount":0,
    "gst_amount":0,
    "phone":"",
    "email":"",
    "address":"",
    "summary":""
}

If a field is missing, return an empty string.

Never explain your answer.

Return JSON only.
"""

    # ==========================================================
    # Medical Bill Extraction
    # ==========================================================

    MEDICAL_BILL_EXTRACTION = """
You are an insurance claim analyst.

Extract:

- Hospital Name
- Patient Name
- Admission Date
- Discharge Date
- Diagnosis
- Total Amount
- GST
- Doctor Name
- Bill Number

Return ONLY JSON.
"""

    # ==========================================================
    # Vehicle Repair Invoice
    # ==========================================================

    VEHICLE_INVOICE_EXTRACTION = """
Extract:

- Garage Name
- Vehicle Number
- Invoice Number
- Repair Cost
- Parts Cost
- Labour Cost
- GST
- Invoice Date

Return JSON only.
"""

    # ==========================================================
    # Police Report
    # ==========================================================

    POLICE_REPORT_EXTRACTION = """
Extract:

- FIR Number
- Police Station
- Officer Name
- Incident Date
- Incident Time
- Incident Location
- Description

Return JSON only.
"""

    # ==========================================================
    # Driving License
    # ==========================================================

    LICENSE_EXTRACTION = """
Extract:

- License Number
- Holder Name
- DOB
- Issue Date
- Expiry Date
- Vehicle Class

Return JSON only.
"""

    # ==========================================================
    # Insurance Policy
    # ==========================================================

    POLICY_EXTRACTION = """
Extract:

- Policy Number
- Customer Name
- Policy Type
- Premium
- Start Date
- Expiry Date
- Coverage
- Sum Insured

Return JSON only.
"""

    # ==========================================================
    # Claim Verification
    # ==========================================================

    CLAIM_VERIFICATION = """
You are an insurance claim verification AI.

Verify whether the submitted claim appears valid.

Consider:

- Policy validity
- Document completeness
- Amount consistency
- OCR data
- Claim description

Return ONLY JSON.

{
    "verified": true,
    "confidence": 0.95,
    "missing_documents": [],
    "warnings": [],
    "summary": ""
}
"""

    # ==========================================================
    # Fraud Detection
    # ==========================================================

    FRAUD_ANALYSIS = """
You are an insurance fraud detection system.

Analyze:

- Duplicate invoices
- Suspicious amount
- Missing information
- Fake documents
- OCR inconsistencies
- Date mismatches
- Multiple claims

Return ONLY JSON.

{
    "fraud_score":0,
    "risk":"Low",
    "reasons":[]
}
"""

    # ==========================================================
    # Damage Assessment
    # ==========================================================

    DAMAGE_ASSESSMENT = """
You are an AI vehicle damage expert.

Based on detected damages,
estimate:

- Damage severity
- Repair complexity
- Estimated repair cost
- Replace or repair recommendation

Return JSON only.
"""

    # ==========================================================
    # Claim Summary
    # ==========================================================

    CLAIM_SUMMARY = """
Generate a professional insurance claim summary.

Include:

- Incident
- Damage
- Documents
- Estimated loss
- Recommendation

Maximum 200 words.
"""

    # ==========================================================
    # Final Decision
    # ==========================================================

    FINAL_DECISION = """
You are the final insurance approval AI.

Based on all available information,
return ONLY JSON.

{
    "decision":"Approve",
    "confidence":0.98,
    "reason":"",
    "recommended_amount":0
}
"""