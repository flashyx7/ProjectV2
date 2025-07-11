
import PyPDF2
import re
from typing import List, Optional, Dict, Any
from io import BytesIO
import tempfile
import os

# Try to import pyresparser, fallback to basic parsing if not available
try:
    from pyresparser import ResumeParser
    PYRESPARSER_AVAILABLE = True
except ImportError:
    PYRESPARSER_AVAILABLE = False
    print("Warning: pyresparser not available, using basic parsing")

def extract_text_from_pdf(pdf_bytes: bytes) -> str:
    """Extract text from PDF resume"""
    try:
        pdf_reader = PyPDF2.PdfReader(BytesIO(pdf_bytes))
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        return text
    except Exception as e:
        raise Exception(f"Error extracting text from PDF: {str(e)}")

def extract_skills_from_text_basic(text: str) -> List[str]:
    """Basic skill extraction using keyword matching (fallback method)"""
    skill_keywords = [
        # Programming languages
        'python', 'java', 'javascript', 'typescript', 'c++', 'c#', 'php', 'ruby', 'go', 'rust',
        'swift', 'kotlin', 'scala', 'r', 'matlab', 'sql', 'html', 'css',
        
        # Frameworks and libraries
        'react', 'angular', 'vue', 'node.js', 'express', 'django', 'flask', 'spring', 'laravel',
        'fastapi', 'bootstrap', 'jquery', 'tensorflow', 'pytorch', 'pandas', 'numpy',
        
        # Databases
        'mysql', 'postgresql', 'mongodb', 'redis', 'sqlite', 'oracle', 'sql server',
        
        # Tools and technologies
        'git', 'docker', 'kubernetes', 'aws', 'azure', 'gcp', 'jenkins', 'linux', 'windows',
        'jira', 'agile', 'scrum', 'ci/cd', 'devops', 'microservices', 'rest api', 'graphql',
        
        # Soft skills
        'leadership', 'communication', 'teamwork', 'problem solving', 'project management',
        'analytical', 'creative', 'adaptable', 'detail oriented'
    ]
    
    text_lower = text.lower()
    found_skills = []
    for skill in skill_keywords:
        if skill.lower() in text_lower:
            found_skills.append(skill.title())
    
    return list(set(found_skills))

def extract_contact_info_basic(text: str) -> Dict[str, Optional[str]]:
    """Basic contact information extraction"""
    contact_info = {
        'email': None,
        'phone': None,
        'name': None
    }
    
    # Extract email
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    email_match = re.search(email_pattern, text)
    if email_match:
        contact_info['email'] = email_match.group()
    
    # Extract phone
    phone_pattern = r'(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
    phone_match = re.search(phone_pattern, text)
    if phone_match:
        contact_info['phone'] = phone_match.group()
    
    return contact_info

def parse_resume_with_pyresparser(pdf_bytes: bytes) -> Dict[str, Any]:
    """Parse resume using the advanced ResumeParser library"""
    try:
        # Create a temporary file to save the PDF
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_file:
            temp_file.write(pdf_bytes)
            temp_file_path = temp_file.name
        
        try:
            # Parse the resume using ResumeParser
            data = ResumeParser(temp_file_path).get_extracted_data()
            
            # Clean up and format the extracted data
            parsed_data = {
                'name': data.get('name', ''),
                'email': data.get('email', ''),
                'mobile_number': data.get('mobile_number', ''),
                'skills': data.get('skills', []),
                'education': data.get('education', []),
                'experience': data.get('experience', []),
                'company_names': data.get('company_names', []),
                'designation': data.get('designation', []),
                'degree': data.get('degree', []),
                'college_name': data.get('college_name', []),
                'total_experience': data.get('total_experience', 0)
            }
            
            return parsed_data
            
        finally:
            # Clean up the temporary file
            if os.path.exists(temp_file_path):
                os.unlink(temp_file_path)
                
    except Exception as e:
        raise Exception(f"Error parsing resume with ResumeParser: {str(e)}")

def parse_resume(pdf_bytes: bytes) -> tuple[str, List[str], Dict[str, Any]]:
    """
    Parse resume PDF and extract text, skills, and additional information
    Returns: (text, skills, parsed_data)
    """
    # Always extract text using PyPDF2
    text = extract_text_from_pdf(pdf_bytes)
    
    # Try advanced parsing first, fallback to basic if needed
    if PYRESPARSER_AVAILABLE:
        try:
            parsed_data = parse_resume_with_pyresparser(pdf_bytes)
            
            # Use parsed skills if available, otherwise fallback
            skills = parsed_data.get('skills', [])
            if not skills:
                skills = extract_skills_from_text_basic(text)
            
            # Ensure skills are properly formatted
            skills = [skill.title() if isinstance(skill, str) else str(skill).title() for skill in skills]
            
            return text, list(set(skills)), parsed_data
            
        except Exception as e:
            print(f"Advanced parsing failed, using basic parsing: {str(e)}")
            # Fallback to basic parsing
            skills = extract_skills_from_text_basic(text)
            contact_info = extract_contact_info_basic(text)
            
            parsed_data = {
                'name': contact_info.get('name', ''),
                'email': contact_info.get('email', ''),
                'mobile_number': contact_info.get('phone', ''),
                'skills': skills,
                'education': [],
                'experience': [],
                'company_names': [],
                'designation': [],
                'degree': [],
                'college_name': [],
                'total_experience': 0
            }
            
            return text, skills, parsed_data
    else:
        # Basic parsing only
        skills = extract_skills_from_text_basic(text)
        contact_info = extract_contact_info_basic(text)
        
        parsed_data = {
            'name': contact_info.get('name', ''),
            'email': contact_info.get('email', ''),
            'mobile_number': contact_info.get('phone', ''),
            'skills': skills,
            'education': [],
            'experience': [],
            'company_names': [],
            'designation': [],
            'degree': [],
            'college_name': [],
            'total_experience': 0
        }
        
        return text, skills, parsed_data

# Legacy function for backward compatibility
def extract_skills_from_text(text: str) -> List[str]:
    """Legacy function for backward compatibility"""
    return extract_skills_from_text_basic(text)
