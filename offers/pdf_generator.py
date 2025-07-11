
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from datetime import datetime
import os

def generate_offer_letter_pdf(
    applicant_name: str,
    position_title: str,
    company_name: str,
    salary: float = None,
    start_date: str = None,
    output_path: str = None
) -> str:
    """Generate a professional offer letter PDF"""
    
    if not output_path:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"offer_letter_{applicant_name.replace(' ', '_')}_{timestamp}.pdf"
        output_path = os.path.join("offer_letters", filename)
    
    # Ensure directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Create PDF document
    doc = SimpleDocTemplate(output_path, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []
    
    # Header style
    header_style = ParagraphStyle(
        'CustomHeader',
        parent=styles['Heading1'],
        fontSize=18,
        spaceAfter=30,
        alignment=1  # Center alignment
    )
    
    # Add header
    story.append(Paragraph("OFFER LETTER", header_style))
    story.append(Spacer(1, 20))
    
    # Date
    date_str = datetime.now().strftime("%B %d, %Y")
    story.append(Paragraph(f"Date: {date_str}", styles['Normal']))
    story.append(Spacer(1, 20))
    
    # Recipient
    story.append(Paragraph(f"Dear {applicant_name},", styles['Normal']))
    story.append(Spacer(1, 12))
    
    # Main content
    content = f"""
    We are pleased to extend an offer of employment for the position of <b>{position_title}</b> 
    at {company_name}. We believe your skills and experience make you an excellent fit for our team.
    """
    story.append(Paragraph(content, styles['Normal']))
    story.append(Spacer(1, 12))
    
    # Position details
    details = f"<b>Position:</b> {position_title}<br/>"
    if salary:
        details += f"<b>Annual Salary:</b> ${salary:,.2f}<br/>"
    if start_date:
        details += f"<b>Start Date:</b> {start_date}<br/>"
    
    story.append(Paragraph(details, styles['Normal']))
    story.append(Spacer(1, 12))
    
    # Terms and conditions
    terms = """
    This offer is contingent upon:
    <br/>• Successful completion of background verification
    <br/>• Verification of employment eligibility
    <br/>• Signed acceptance of this offer letter
    """
    story.append(Paragraph(terms, styles['Normal']))
    story.append(Spacer(1, 20))
    
    # Closing
    closing = f"""
    We are excited about the possibility of you joining our team at {company_name}. 
    Please confirm your acceptance by signing and returning this letter.
    """
    story.append(Paragraph(closing, styles['Normal']))
    story.append(Spacer(1, 30))
    
    # Signature lines
    story.append(Paragraph("Sincerely,", styles['Normal']))
    story.append(Spacer(1, 20))
    story.append(Paragraph(f"{company_name} HR Department", styles['Normal']))
    story.append(Spacer(1, 40))
    
    story.append(Paragraph("Acceptance:", styles['Normal']))
    story.append(Spacer(1, 20))
    story.append(Paragraph("_" * 30 + "  Date: _" * 15, styles['Normal']))
    story.append(Paragraph(f"{applicant_name}", styles['Normal']))
    
    # Build PDF
    doc.build(story)
    return output_path
