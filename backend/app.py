from flask import Flask, jsonify, request
from flask_cors import CORS

from dotenv import load_dotenv
load_dotenv()

from openai import OpenAI
from pylatex import Command, Document, Section, Subsection
from pylatex.utils import NoEscape, italic

client = OpenAI()

app = Flask(__name__)
CORS(app)

@app.route('/api/test', methods=['GET'])
def test_route():
    return jsonify({"message": "Backend is working!"})

@app.route('/api/generate-cover-letter', methods=['POST'])
def generate_cover_letter():
    data = request.json
    job_description = data.get('jobDescription')
    resume = data.get('resume')

    # Prompt for OpenAI
    prompt = f"""
    Please write a professional cover letter based on the following job description and resume.
    
    Job Description:
    {job_description}
    
    Resume:
    {resume}
    
    Write a compelling cover letter that highlights the relevant experience and skills from the resume that match the job requirements. The tone should be professional and enthusiastic.
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4",  # or "gpt-3.5-turbo" for a more economical option
            messages=[
                {"role": "system", "content": "You are a professional cover letter writer."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1000,
            temperature=0.7
        )
        
        cover_letter = response.choices[0].message.content

        return jsonify({
            "coverLetter": cover_letter
        })

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500
    
@app.route('/api/generate-resume', methods=['POST'])
def generate_resume():
    data = request.json
    resume = data.get('resume')

    # use pylatex to generate a resume
    doc = Document(filepath='resume.tex')
    doc.generate_pdf(clean_tex=True, compiler='pdflatex')
    

if __name__ == '__main__':
    app.run(debug=True)
