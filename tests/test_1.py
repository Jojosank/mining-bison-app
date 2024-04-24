from streamlit.testing.v1 import AppTest

at = AppTest.from_file("/home/joemota/final-project-team-mining-bisons/Main.py")
at.run()

def test_initial_page_state():
    assert len(at.text_input) == 2  
    assert len(at.button) == 2
