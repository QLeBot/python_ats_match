import spacy
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class ATSMatcher:
    def __init__(self):
        # Load English language model from spaCy
        self.nlp = spacy.load("en_core_web_sm")
        self.tfidf_vectorizer = TfidfVectorizer(stop_words='english')
        
    def clean_text(self, text):
        # Remove special characters and extra whitespace
        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'[^\w\s]', '', text)
        return text.lower().strip()
    
    def extract_keywords(self, text):
        # Process the text with spaCy
        doc = self.nlp(text)
        
        # Extract relevant parts of speech (nouns, proper nouns, and adjectives)
        keywords = []
        for token in doc:
            if token.pos_ in ['NOUN', 'PROPN', 'ADJ'] and not token.is_stop:
                keywords.append(token.text.lower())
                
        return list(set(keywords))
    
    def parse_latex_resume(self, latex_text):
        # Remove LaTeX commands and formatting
        clean_text = re.sub(r'\\[a-zA-Z]+(?:\[.*?\])?{([^}]*)}', r'\1', latex_text)
        clean_text = re.sub(r'[\\{}]', '', clean_text)
        return clean_text
    
    def calculate_match_score(self, job_description, resume_text):
        # Clean and prepare texts
        clean_job = self.clean_text(job_description)
        clean_resume = self.clean_text(resume_text)
        
        # Transform texts to TF-IDF vectors
        tfidf_matrix = self.tfidf_vectorizer.fit_transform([clean_job, clean_resume])
        
        # Calculate cosine similarity
        similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
        
        # Extract keywords from both texts
        job_keywords = self.extract_keywords(job_description)
        resume_keywords = self.extract_keywords(resume_text)
        
        # Find matching keywords
        matching_keywords = set(job_keywords) & set(resume_keywords)
        
        return {
            'similarity_score': round(similarity * 100, 2),
            'matching_keywords': list(matching_keywords),
            'missing_keywords': list(set(job_keywords) - set(resume_keywords)),
            'job_keywords': job_keywords,
            'resume_keywords': resume_keywords
        }

def main():
    # Example usage
    matcher = ATSMatcher()
    
    # Sample job description and resume
    job_description = """
    Bring your data analytics and data mining skills to a unique team seeking to understand and shape the future of marketing technology. We are interested in technology adoption patterns, the respect of visitors' data and the use of open source in marketing. We are also interested in those marketing data analysts who are curious enough to embrace new technologies and are ready to work with unfamiliar tools, if needed.

The role of a Junior Data Engineer at Canonical

Canonical has provided developers with open source since 2004, helping them build innovations such as public cloud, machine learning, robotics or blockchain. Marketing at Canonical means being at the forefront of innovation, for our customers and for our own martech stack. We're on the look out for a marketing data analyst to join our team and execute on our growth hacking strategy.

The ideal candidate will be passionate about technology, technology marketing and the use of technology in marketing. You will prefer to work in an environment that has emphasis on ownership of campaigns, collaboration, learning, curiosity and a drive to continually improve oneself / the team / the organisation. You will also love to problem solve, get hands-on, experiment, measure and use automation to make daily life easier.

The Marketing team at Canonical drives commercial outcomes for the company across its portfolio of products and grows the addressable market through digital marketing campaigns, lifecycle management, events, partnerships and community development. If these things are important to you and you're motivated by driving data engineering, delighting customers and filling the sales funnel, we want to talk with you.

This role sits in the Marketing team reporting to the Growth Engineering Manager.

Location: This role will be based remotely in the EMEA region.

What your day will look like

    Utilise advanced data analytics to grow Canonical's product adoption and market penetration
    Focus on quantitative and qualitative data analytics to find insights and meaningful business outcomes
    Design and conduct experiments with data, visualisation and insights into Canonical's target audiences
    Collaborate with stakeholder teams (Product Management, Engineering, Information Systems, Finance, RevOps, etc) to improve the data and tool ecosystem
    Put in place and maintain systems to ensure teams across the company have self-service access to data dashboards

What we are looking for in you?

    Background in data science, mathematics, actuarial science, or engineering
    Knowledge in advanced statistics, data sciences, coding/scripting languages (Python, JS, etc), and databases (SQL, etc)
    Strength in data analytics and visualisation (Looker Studio, Tableau, Apache Superset, etc)
    Ability to translate business questions to key research objectives
    Ability to identify the best methodology to execute research, synthesise and analyse findings
    Excellent writing and communication skills
    Willingness to examine the status quo and resilient in the face of challenges

    """
    
    resume_latex = """
    \begin{document}

    \begin{center}
    {\large \textbf{Quentin LECOMTE}}\\
    \vspace{1mm}
    \faEnvelope \space \href{mailto:lecomteq.ql@gmail.com}{lecomteq.ql@gmail.com} \faMobile \space +33644365603 \faLinkedinSquare \space \href{https://www.linkedin.com/in/lecomte-quentin/}{lecomte-quentin} \\ French Nationality - Work Permit G willing to relocate
    %Franclens, France \textbullet{} Permis G, possibilité permis B\\
\end{center}
\vspace{-5mm}
%==============================================================================================================================================

% Section Summary
\section*{Summary}
% Separation
\vspace{-3mm}
\hrulefill
\vspace{1mm}
\\
Junior Data Professional, graduated from ESME Sudria, with significant experiences in data engineering, data visualization, cloud computing, data manipulation and analysis, the creation of ETL pipelines and data warehousing.
%==============================================================================================================================================

% Section Education
\section*{Education}
% Separation
\vspace{-3mm}
\hrulefill

\subsection*{ESME Sudria - Engineering Master Degree in Artificial Intelligence\hfill {\fontsize{9pt}{9pt}\selectfont 2023}}
{\fontsize{8pt}{8pt}\selectfont Ivry-sur-Seine, France}
%Engineering Master's Degree in Artificial Intelligence

%\vspace{4mm}

\subsection*{California State University Monterey Bay CSUMB - Semester Abroad\hfill {\fontsize{9pt}{9pt}\selectfont August 2021 - December 2021}}
{\fontsize{8pt}{8pt}\selectfont Monterey, USA}
%International Semester - Computer Science, Monterey, USA
%Semester Abroad\\
%Mathematics for Computer Science - Web Programming - Responsive Web Programming - Networking

%\subsection*{Lycée Présentation de Marie}
%09/2014 – 06/2017 – Saint-Julien-en-Genevois, FRANCE\\
%Baccalauréat Scientifique - Mention Assez Bien
%==============================================================================================================================================

% Section Expérience Professionnelle
\section*{Work Experience}
% Separation
\vspace{-3mm}
\hrulefill

\subsection*{\fontsize{11pt}{11pt}\selectfont Data Consultant - Talan \hfill {\fontsize{9pt}{9pt}\selectfont April 2023 – March 2024}}
{\fontsize{8pt}{8pt}\selectfont Geneva, Switzerland}
\vspace{-2mm}
%\begin{adjustwidth}{1cm}{0cm} % Adjusts the left margin by 1cm; adjust this value as needed
\subsubsection*{\fontsize{9pt}{9pt}\selectfont Data Analyst for the City of Geneva}
\vspace{-2mm}
\begin{itemize}[label=\raisebox{0.25ex}{\tiny$\bullet$}]
    \item Developed QlikSense dashboards adhering to best practices for production, cost, and consumption data management.
    \item Utilized data modeling techniques in QlikSense to optimize data structures, improve performance, and ensure accurate reporting for production, cost, and consumption data.
    \item Optimized QlikSense data table structures to enhance efficiency and ensure reliability.
    \item Refactored cost and consumption calculations by incorporating specific technical parameters for greater accuracy.
    \item Authored comprehensive documentation on dashboards and data table structures, tailored for both technical\\ and non-technical audiences.
\end{itemize}

%\vspace{-3mm} % Adjust the space before the second subsubsection
\subsubsection*{\fontsize{9pt}{9pt}\selectfont Internal Proof of Concept on Microsoft Fabric}
\vspace{-2mm}
\begin{itemize}[label=\raisebox{0.25ex}{\tiny$\bullet$}]
    \item Established a demo environment on Microsoft Fabric to explore and evaluate its technical capabilities.
    \item Managed LakeHouse environments in Microsoft Fabric by implementing ETL development pipelines using PySpark notebooks\\ and medallion architecture.
    \item Generated synthetic data to simulate data lake and data warehouse scenarios for testing and analysis.
    \item Documented a comparative analysis of Microsoft Fabric versus traditional Azure Services, highlighting the pros and cons.
\end{itemize}

%\vspace{-3mm} % Adjust the space before the second subsubsection
\subsubsection*{\fontsize{9pt}{9pt}\selectfont Data Engineer intern for Bulgari Watches}
\vspace{-2mm}
\begin{itemize}[label=\raisebox{0.25ex}{\tiny$\bullet$}]
    \item Implemented ETL pipelines on Azure Data Factory using both time-driven and event-driven triggers.
    \item Transformed and loaded data from SAP and on-premise Microsoft Server databases into the Azure environment.
    \item Developed SQL queries tailored to the specific needs of cross-functional users.
    \item Optimized and monitored pipeline performance to ensure efficiency and reliability.
    \item Automated metadata-driven and data flows pipeline creation through Python scripting, increasing operational efficiency.
    \item Documented pipeline architecture and dependencies to provide clear guidance for ongoing and future projects.
\end{itemize}

\vspace{-2mm} % Adjust the space before the second subsubsection
{\fontsize{9pt}{9pt}\selectfont
\subsubsection*{\fontsize{9pt}{9pt}\selectfont References :}
\vspace{-1mm}
\begin{itemize}[label=\raisebox{0.25ex}{\tiny$\bullet$}]
    \item Amaury Languillat - Data Intelligence Director - \href{mailto:amaury.languillat@talan.com}{amaury.languillat@talan.com}
    \item Guillaume Reboullet - Talent Acquisition Manager - \href{mailto:guillaume.reboullet@talan.com}{guillaume.reboullet@talan.com}
\end{itemize}
} 

\vspace{2mm}

\subsection*{\fontsize{11pt}{11pt}\selectfont Data \& Cloud intern - Infotel \hfill {\fontsize{9pt}{9pt}\selectfont June 2022 - September 2022}}
{\fontsize{8pt}{8pt}\selectfont Nanterre, France}\\
\vspace{-2mm}
\begin{itemize}[label=\raisebox{0.25ex}{\tiny$\bullet$}]
    \item Enhanced video speech-to-text extraction using AWS Transcribe with Custom Vocabulary for improved accuracy.
    \item Developed AWS Lambda functions in Python to manipulate and enrich data, streamlining processing workflows.
    \item Extracted and ingested data in and out of S3 buckets through Lambda functions, ensuring seamless data flow.
    \item Documented the entire process and presented the final results and conclusions of the Proof of Concept (PoC) to stakeholders.
\end{itemize}

%==============================================================================================================================================

% Section Skills
\section*{Skills}
% Separation
\vspace{-3mm}
\hrulefill
\begin{itemize}[label=\raisebox{0.25ex}{\tiny$\bullet$}]
    \item French : Native, English : C1, 990 TOEIC, 8 IELTS, German : B1
    \item QlikSense, PowerBI
    \item Relational database, Non-Relational database, SQL, T-SQL, MS-SQL, PL/SQL, MongoDB, PostgreSQL, MySQL
    \item Python (Data Science \& Analytics libraries), PySpark
    \item Git, GitHub Actions, GitLab, Docker, Terraform
    \item Azure : Fabric, Azure Data Factory (ADF), Data Flows, Metadata Driven Copy (MDDC), Azure DevOps, Blob Storage
    \item AWS : S3, Lambda, Transcribe, Augmented AI, Sagemaker
    %\item C/C++, Java, HTML/CSS, JavaScript
\end{itemize}

%==============================================================================================================================================

% Section Certifications
\section*{Certifications}
% Separation
\vspace{-3mm}
\hrulefill
\begin{itemize}[label=\raisebox{0.25ex}{\tiny$\bullet$}]
    \item Microsoft Azure AI Fundamentals \hfill December 2023
    \item Microsoft Azure Data Fundamentals \hfill November 2023
\end{itemize}


\end{document}
    """
    
    # Parse resume from LaTeX
    resume_text = matcher.parse_latex_resume(resume_latex)
    
    # Calculate match
    result = matcher.calculate_match_score(job_description, resume_text)
    
    # Print results
    print(f"Match Score: {result['similarity_score']}%")
    print("\nMatching Keywords:", ', '.join(result['matching_keywords']))
    print("\nMissing Keywords:", ', '.join(result['missing_keywords']))
    
if __name__ == "__main__":
    main()
