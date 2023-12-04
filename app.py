import speech_recognition as sr
import pyttsx3
import openai
import datetime
import language_tool_python
import sys
from PySide6.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox

# Set your OpenAI API key here
openai.api_key = 'YOUR_API_KEY'

def speak_text(text, rate = 130):
    engine = pyttsx3.init() 
    engine.setProperty('rate',rate)
    engine.say(text)
    engine.runAndWait()
    
def listen_microphone():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        speak_text("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        print("Recognizing...")
        command = recognizer.recognize_google(audio)
        print("You said:", command)
        return command.lower()
    except sr.UnknownValueError:
        print("Sorry, I couldn't understand what you said.")
        return ""
    except sr.RequestError:
        print("Sorry, there was an error processing your request.")
        return ""
    
def create_report_template():
    # Define your report template here or load it from a file/database
    report_template = """
    Report
    ------
    Date: {date}
    Content: {content}
    """
    return report_template

def generate_file_from_template(template, content):
    current_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"generated_file_{current_time}.txt"
    file_content = template.format(date=current_time, content=content)
    with open(filename, "w") as file:
        file.write(file_content)
    return filename
    
def take_notes():
    speak_text("Sure, I'm ready to take notes. Start speaking.")
    notes = listen_microphone()
    return notes

def save_notes_to_file(notes):
    current_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"notes_{current_time}.txt"
    with open(filename, "w") as file:
        file.write(notes)
    return filename

def generate_email_template(recipient_name, email_subject, email_content):
    email_template = f"""
    To: {recipient_name}
    Subject: {email_subject}

    Hi {recipient_name},

    {email_content}

    Regards,
    Your Name
    """
    return email_template

def send_email(email_content):
    # Code to send the email goes here
    print("Email sent!")
    # You would typically integrate this part with an email service or API to send the email
    
def check_grammar(filename):
    tool = language_tool_python.LanguageTool('en-US')
    with open(filename, 'r') as file:
        text = file.read()
        matches = tool.check(text)
        return matches
    
def on_text_input():
    command = text_input.text()
    process_command(command)

def on_speech_input():
    command = listen_microphone()
    if command:
        process_command(command)
    else:
        show_message("Speech Recognition", "Sorry, I couldn't understand what you said.")
    pass



def process_command(command):

        if "hello" in command:
            speak_text("What's up with it")

        elif "goodbye" in command or "bye" in command:
            speak_text("Peace Out!")
        
        elif "take note" in command:
            taking_notes = True
            user_notes = take_notes()
            speak_text("Note taken. Is there anything else I can assist you with?")
            taking_notes = False
            pass
        
        elif "create report" in command:
            report_template = create_report_template()
            speak_text("What content would you like to include in the report?")
            report_content = listen_microphone()
            if report_content:
                filename = generate_file_from_template(report_template, report_content)
                speak_text(f"Report created. Filename is {filename}")
            pass
                
        elif "generate email" in command:
            speak_text("Who is the recipient?")
            recipient_name = listen_microphone()
            speak_text("What is the subject of the email?")
            email_subject = listen_microphone()
            speak_text("What should be the content of the email?")
            email_content = listen_microphone()

            email_template = generate_email_template(recipient_name, email_subject, email_content)
            # This is a placeholder. In a real scenario, you'd send the email using an email service/API.
            send_email(email_template)
            speak_text("Email created and sent!")
            pass
            
        elif "check grammar" in command:
            speak_text("Sure, please provide the filename or path of the file to check.")
            filename = listen_microphone()  # Assuming the user provides the file name
            matches = check_grammar(filename)
            if matches:
                speak_text(f"Found {len(matches)} grammar issues in the file.")
                for match in matches:
                    speak_text(f"Error: {match.ruleId}, Message: {match.msg}, Line: {match.fromy}, Column: {match.fromx}")
            else:
                speak_text("No grammar issues found.")
            pass
                
        elif taking_notes:
            user_notes += command
            pass
        
        
        # Add more command handling and responses here
        
        else:
            # Use OpenAI's API to generate a response
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[{"role": "system", "content": "User: " + command}],
            )
            assistant_response = response['choices'][0]['message']['content']
            speak_text(assistant_response)

def show_message(title, message):
    msg = QMessageBox()
    msg.setWindowTitle(title)
    msg.setText(message)
    msg.exec()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = QWidget()
    window.setWindowTitle("Genè")
    
    label = QLabel("Enter your command:")
    text_input = QLineEdit()
    text_button = QPushButton("Ask")
    text_button.clicked.connect(on_text_input)
    speech_button = QPushButton("Talk")
    speech_button.clicked.connect(on_speech_input)

    layout = QVBoxLayout()
    layout.addWidget(label)
    layout.addWidget(text_input)
    layout.addWidget(text_button)
    layout.addWidget(speech_button)

    window.setLayout(layout)
    window.show()
    
    #speak_text("HEY THERE!! My name is Genaè, and I will be your virtual assistant, How can I help you today?", 130)

    app.exec_()