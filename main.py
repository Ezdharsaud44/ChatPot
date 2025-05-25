import streamlit as st


def main():
    st.set_page_config(page_title="CommitMate", page_icon="🤖")

    # Create three columns for horizontal page links
    col1, col2, col3 = st.columns(3)

    with col1:
        st.page_link("main.py", label="Home", icon="🏠", disabled=True)

    with col2:
        st.page_link("pages/chatBot.py", label="ChatBot", icon="🤖")

    with col3:
        st.page_link("pages/team.py", label="Our Team", icon="👥")



    # Custom CSS for horizontal orange lines
    st.markdown(
    """
    <style>
        .horizontal-lines {
            border-top: 5px solid;
            padding-top: 20px;
            text-align: center;
            color: #FF5733;
        }
    </style>
    """,
    unsafe_allow_html=True
    )

    st.title("Welcome to your CommitMate")

    # Apply the horizontal lines to the main content
    st.markdown('<div class="horizontal-lines">', unsafe_allow_html=True)
    
    st.markdown(
        """
        **CommitMate** is an intelligent bot designed to assist you with your Git-related questions.
        Whether you're troubleshooting errors, learning Git commands, or managing repositories,
        Commit Mate is here to help!
        
        ### Features:
        - Provides answers to Git commands and concepts
        - Helps debug common Git issues
        - Assists with repository management
        - Enhances developer productivity
        
        Explore further and get started now!
        """
    )

    st.write("")
    st.write("")
    st.write("") 

    st.markdown(
    """
    <div style="text-align: left;">
        <img src="https://upload.wikimedia.org/wikipedia/commons/e/e0/Git-logo.svg" width="300" style="margin-bottom: 20px;">
        <p style="font-size: 14px;"><em>CommitMate - Your Git Companion</em></p>
    </div>
    """,
    unsafe_allow_html=True
    )

    st.write("")
    st.write("")

if __name__ == "__main__":
    main()
