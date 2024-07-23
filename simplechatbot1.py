import streamlit as st
from PyPDF2 import PdfReader
import requests

# Simulated project content
projects = {
    "Internship Projects": {
        "Project 1": "Headline: 'Comprehensive Data Cleaning, Processing, and Analysis for Healthcare Insights', Introduction: The Healthcare Department seeks a qualified vendor to perform extensive data cleaning, processing, and analysis on the 2011 Census data, housing data, and hospital data. Aim is to extract meaningful insights that will inform policy and operational decisions. Selected vendor responsible for ensuring data consistency, filling gaps, creating visualizations to illustrate key findings. Project Objectives: Clean and standardize various datasets to ensure uniformity. Process and analyze data to generate actionable insights. Create visualizations that highlight important trends and disparities. Provide a comprehensive report with recommendations based on analysis. Scope of Work: Data Cleaning and Processing: Census Data Column Relevance Remove irrelevant columns retain essential ones such as State name, District name, Population, etc. Column Renaming Rename columns for consistency e.g., State name to State/UT, Male_Literate to Literate_Male. Standardize State/UT Names Ensure uniform naming conventions e.g., Andaman and Nicobar Islands, Arunachal Pradesh. New State/UT Handling Update dataset to reflect creation of Telangana and Laddakh. Missing Data Management Identify and fill missing data using logical imputation methods. Housing Data Relevant Data Extraction Extract and process columns relevant to housing e.g., District Name, Rural/Urban, Total Number of households Absolute Values Calculation Convert percentage data to absolute values using census data. Data Saving Save processed data with clear and meaningful column names Hospital Data Header Fix Correct headers using metadata ensuring they are understandable State/UT Name Uniformity Standardize State/UT names to match census and housing data Data Saving Save cleaned hospital data for further analysis Data Analysis and Visualization Discrepancy Reporting Identify and report major discrepancies between housing and census data Visual Insights Create visualizations for Number of households per 100 people Percentage of households with toilet facilities Urban to rural population ratios Healthcare Disparity Analysis Analyze and visualize hospital bed availability per 10,000 people WHO Standards Gap Analysis Visualize gap between available hospital beds and WHO standards estimating number of hospitals required to meet these standards Deliverables Cleaned and processed datasets census.csv housing.csv all_hospitals.csv Visualizations and analytical reports highlighting key insights Detailed documentation of methodologies used in data cleaning and analysis Project Timeline Project kick-off [Insert Date] Milestone 1 Census Data Cleaning [Insert Date] Milestone 2 Housing Data Processing [Insert Date] Milestone 3 Hospital Data Cleaning and Analysis [Insert Date] Final Deliverables [Insert Date] Evaluation Criteria Demonstrated expertise in data cleaning and processing Proficiency in data visualization and analysis tools Prior experience with healthcare data projects Quality of previous work and client testimonials Submission Requirements Company profile and experience Detailed proposal including methodology tools timeline Budget and cost breakdown References from past clients Contact Information Name [Contact Person] Title [Title] Email [Email] Phone [Phone] ",
        "Project 2": "Headline: 'Advanced Database Management and Comprehensive Report Generation for Healthcare Data', Introduction: The Healthcare Department requires an expert vendor to manage and integrate cleaned data into a relational database ensuring seamless access and comprehensive reporting capabilities. Project involves setting up the database verifying data integrity creating stored functions and procedures automating logs for data changes. Project Objectives: Establish a robust relational database for healthcare data Ensure data integrity and consistency across all datasets Develop stored functions and procedures for efficient data retrieval and reporting Automate logging for data changes to maintain historical records Scope of Work: Database Setup and Data Upload Database Establishment Set up a relational database tailored to the Healthcare Department's needs Data Upload Import cleaned data files ensuring appropriate primary and foreign key constraints are in place Data Verification Integrity Checks Verify the integrity of uploaded data by joining tables and checking for consistency Discrepancy Resolution Identify and resolve any discrepancies found during verification Stored Functions and Procedures Function Development Create stored functions for retrieving population data hospital bed data and other healthcare metrics Procedure Development Develop stored procedures for generating detailed healthcare reports Automated Logging Hospital Log Create a hospital_log table to record changes in hospital data including additions and removals Bed Log Create a hospital_bed_log table to record changes in hospital bed data including additions and removals Automatic Updates Ensure logs are updated automatically with every change Deliverables Fully functional relational database with cleaned and verified data Stored functions and procedures for various healthcare metrics Automated logging system for hospital and bed data changes Comprehensive documentation of database schema stored functions and procedures Project Timeline Project kick-off [Insert Date] Milestone 1 Database Setup - [Insert Date] Milestone 2 Data Upload and Verification - [Insert Date] Milestone 3 Stored Functions and Procedures - [Insert Date] Final Deliverables [Insert Date] Evaluation Criteria Proven experience in relational database management Proficiency in SQL and stored procedure development Ability to automate data logging processes Quality of previous work and client testimonials Submission Requirements Company profile and experience Detailed proposal including methodology tools timeline Budget and cost breakdown References from past clients Contact Information Name [Contact Person] Title [Title] Email [Email] Phone [Phone]"
    },
    "Final Year Projects": {
        "Project A": "Content will be updated soon.",
        "Project B": "Content will be updated soon."
    }
}

# Function to extract text from PDF
def extract_text_from_pdf(pdf_file):
    pdf = PdfReader(pdf_file)
    text = ""
    for page in pdf.pages:
        text += page.extract_text()
    return text

# Function to interact with the Llama 3 model via Ollama
def query_llama(prompt):
    url = "http://localhost:11434/v1/chat/completions"  # Update with your Ollama instance endpoint
    headers = {
        "Content-Type": "application/json",
    }
    payload = {
        "model": "llama3",  # Updated model name
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 150  # Adjust as needed
    }
    
    response = requests.post(url, headers=headers, json=payload)
    
    # Print the entire response for debugging
    response_data = response.json()
    print("API Response:", response_data)
    
    # Extract and return the content from the response
    if 'choices' in response_data and len(response_data['choices']) > 0:
        message = response_data['choices'][0].get('message', {})
        return message.get('content', 'No content field found')
    elif 'text' in response_data:
        return response_data['text']
    else:
        return "Unexpected response format. Please check the API documentation or response."

# Streamlit UI
st.sidebar.image(r"C:\Users\Miles\Desktop\Logo.jpg", width=200) 

st.title("Futurense Chatbot")
mode = st.sidebar.selectbox("Select Mode", ["PDF Question-Answering", "General Conversation", "Projects & RFPs"])

if mode == "PDF Question-Answering":
    st.header("PDF Question-Answering")
    pdf_file = st.file_uploader("Upload a PDF file", type=["pdf"])
    if pdf_file:
        text = extract_text_from_pdf(pdf_file)
        st.text_area("PDF Content", text, height=300)
        question = st.text_input("Ask a question about the PDF")
        if question:
            prompt = f"Based on the following text from the PDF:\n\n{text}\n\nAnswer the question: {question}"
            answer = query_llama(prompt)
            st.write("Answer:", answer)

elif mode == "General Conversation":
    st.header("General Conversation")
    conversation_history = st.session_state.get("conversation_history", "")
    user_input = st.text_input("You: ")
    if user_input:
        conversation_history += f"You: {user_input}\n"
        response = query_llama(user_input)
        conversation_history += f"Llama 3: {response}\n"  # Show only the response
        st.session_state["conversation_history"] = conversation_history
    st.text_area("Conversation History", st.session_state.get("conversation_history", ""), height=300)

elif mode == "Projects & RFPs":
    st.header("Projects & RFPs")
    folder = st.selectbox("Select a Folder", list(projects.keys()))
    project = st.selectbox("Select your Project", list(projects[folder].keys()))
    
    # Show the selected project content
    project_content = projects[folder][project]
    st.text_area("Here is the Project Content", project_content, height=300)
    
    # Ask a question based on the selected project content
    question = st.text_input("Feel free to Ask a question about the project")
    if question:
        prompt = f"Based on the following content from the project:\n\n{project_content}\n\nAnswer the question: {question}"
        answer = query_llama(prompt)
        st.write("Answer:", answer)
