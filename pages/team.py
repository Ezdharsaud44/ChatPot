import streamlit as st

# Set up the page layout
st.set_page_config(page_title="Meet The Team", layout="wide", page_icon="👨‍💻")

# Create three columns for horizontal page links
col1, col2, col3 = st.columns(3)

with col1:
    st.page_link("main.py", label="Home", icon="🏠")

with col2:
    st.page_link("pages/chatBot.py", label="ChatBot", icon="🤖")

with col3:
    st.page_link("pages/team.py", label="Our Team", icon="👥", disabled=True)

# Add title and subtitle (without any picture)
st.markdown('<h1 style="text-align: center; color: #FF5733; font-weight: bold; margin-bottom: 10px;">Meet Our Amazing Team</h1>', unsafe_allow_html=True)
st.markdown('<h3 style="text-align: center; color: #666; margin-bottom: 30px;">The talented minds behind CommitMate</h3>', unsafe_allow_html=True)


# Custom CSS for styling with orange theme

st.markdown("""
    <style>
        /* Main background */
       
        
        /* Profile card styling */
        .profile-card {
            background-color: white;
            border-radius: 10px;
            padding: 20px;
            text-align: center;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            height: 100%;
        }
        
        /* Circular profile image */
        .profile-image {
            width: 150px;
            height: 150px;
            border-radius: 50%;
            object-fit: cover;
            border: 3px solid #FF5733;
            margin: 0 auto 15px auto;
            display: block;
        }
        
        /* Team member name */
        .member-name {
            color: #333;
            font-size: 18px;
            font-weight: bold;
            margin-bottom: 5px;
        }
        
        /* Role title */
        .member-role {
            color: #FF5733;
            font-size: 16px;
            margin-bottom: 15px;
        }
        
        /* Description text */
        .member-description {
            color: #666;
            font-size: 14px;
            line-height: 1.4;
            margin-bottom: 15px;
        }
        
        /* LinkedIn button */
        .linkedin-button {
            background-color: #FF5733;
            color: white;
            padding: 8px 15px;
            border-radius: 5px;
            text-decoration: none;
            font-size: 14px;
            display: inline-block;
            margin-top: 10px;
            transition: background-color 0.3s;
        }
        
        .linkedin-button:hover {
            background-color: #E64A19;
        }
    </style>
""", unsafe_allow_html=True)

# Create team members data with LinkedIn URLs
team_members = [
    {
        "name": "Najla Almarshde",
        "role": "Full-Stack Developer",
        "description": "Najla works on the back-end aspect of the project, particularly on integrating and storing the chatbot’s history and data. She ensures that all previous conversations or interactions with the bot are captured and processed efficiently with fixing user interface.",
        "image": "https://static.vecteezy.com/system/resources/previews/020/911/731/original/profile-icon-avatar-icon-user-icon-person-icon-free-png.png",
        "linkedin": "http://linkedin.com/in/najlayasm"
    },
    {
        "name": "Ezdhar Altamimi",
        "role": "Front-End Developer",
        "description": "Responsible for creating the Team Page. She designs and implements the front-end features to display the team members' information, ensuring that it is visually organized and easy for users to understand. Ezdhar also ensures that the page is responsive and fits well on different devices.",
        "image": "https://static.vecteezy.com/system/resources/previews/020/911/731/original/profile-icon-avatar-icon-user-icon-person-icon-free-png.png",
        "linkedin": "https://www.linkedin.com/in/ezdhar-saud-265999221?utm_source=share&utm_campaign=share_via&utm_content=profile&utm_medium=ios_app"
    },
    {
        "name": "Ghada Alamri",
        "role": " Front-End Developer",
        "description": "Focuses on the front-end development of the main entry page (CommitMate). She works on the design, layout, and user interface to ensure the page is engaging and provides an overview of the project. She makes the page visually appealing and intuitive for users to navigate.",
        "image": "https://static.vecteezy.com/system/resources/previews/020/911/731/original/profile-icon-avatar-icon-user-icon-person-icon-free-png.png",
        "linkedin": "https://www.linkedin.com/in/ghada-alamri-7855a526a?utm_source=share&utm_campaign=share_via&utm_content=profile&utm_medium=ios_app"
    },
    {
        "name": "Faisal Almufarrih",
        "role": "Back-End Developer",
        "description": "focused on testing the back-end functionality of the project. This involves ensuring the core logic of the CommitMate chatbot works smoothly, performing unit testing and identifying potential bugs or issues within the back-end code. He ensures that the system performs well and communicates seamlessly with the front-end.",
        "image": "https://static.vecteezy.com/system/resources/previews/020/911/731/original/profile-icon-avatar-icon-user-icon-person-icon-free-png.png",
        "linkedin": "https://www.linkedin.com/in/faisal-almufarrih-b8090628b?utm_source=share&utm_campaign=share_via&utm_content=profile&utm_medium=ios_app"
    },
    {
        "name": "Faisal Alkhunain",
        "role": "Full-Stack Developer",
        "description": "Full-stack developer responsible for writing the core code and logic of the CommitMate chatbot. He works primarily on the back-end algorithms, including the pattern matching and substitution logic that powers the chatbot. Faisal ensures the functionality of the chatbot, focusing on its internal code and logic, without directly working on the front-end",
        "image": "https://static.vecteezy.com/system/resources/previews/020/911/731/original/profile-icon-avatar-icon-user-icon-person-icon-free-png.png",
        "linkedin": "https://www.linkedin.com/in/faisal-alkhunain-a97a6922b?utm_source=share&utm_campaign=share_via&utm_content=profile&utm_medium=android_app"
    }
]

# Display team members in a single row with 5 columns
cols = st.columns(5)
for i, member in enumerate(team_members):
    with cols[i]:
        st.markdown(f"""
            <div class="profile-card">
                <img src="{member['image']}" class="profile-image" alt="{member['name']}">
                <div class="member-name">{member['name']}</div>
                <div class="member-role">{member['role']}</div>
                <div class="member-description">{member['description']}</div>
                <a href="{member['linkedin']}" target="_blank" class="linkedin-button">LinkedIn</a>
            </div>
        """, unsafe_allow_html=True)

# Add simple footer
# st.markdown('<div style="text-align: center; margin-top: 50px; color: #666;">© 2025 CommitMate. All rights reserved.</div>', unsafe_allow_html=True)