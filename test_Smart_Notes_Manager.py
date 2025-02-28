import pytest
import datetime
from Smart_Notes_Manager import Note, TextNote, ReminderNote, NoteManager

@pytest.fixture
def setup_NoteManager():
    """Fixture to set up a NoteManager instance for each test."""
    return NoteManager()

"""Note"""

# Testing Note Parent class if it's initializing correctly
def test_note_creation(setup_NoteManager):
    created_at = datetime.datetime.now()
    note = Note(created_at, "Sample note content")

    assert note.created_at == created_at
    assert note.content == "Sample note content"
    assert note.note_ID is None  

"""Text Note"""
# Test TextNote subclass if its initializing correctly
def test_text_note_creation(setup_NoteManager):
    created_at = datetime.datetime.now()
    text_note = TextNote(created_at, "This is a text note", "Sample Title")

    assert text_note.created_at == created_at
    assert text_note.content == "This is a text note"
    assert text_note.title == "Sample Title"
    assert text_note.display() == f"TextNote: {text_note.note_ID}: Sample Title - {created_at} (This is a text note)"



"""Reminder  Note"""
# Testing Reminder Note subclass with valif time format
def test_reminder_note_creation(setup_NoteManager):
    created_at = datetime.datetime.now()
    reminder_time = "2025-03-01 08:30 00"
    reminder_note = ReminderNote(created_at, "Doctor's appointment", reminder_time)

    assert reminder_note.created_at == created_at
    assert reminder_note.content == "Doctor's appointment"
   

# Testing  Reminder Note with invalid time format
def test_reminder_note_creation_invalid_time(setup_NoteManager):
    reminder_note = ReminderNote(datetime.datetime.now(), "Meeting", "invalid_time")
    assert reminder_note.reminder_time is None, "Reminder time should be None for an invalid input"
    


"""Testing Add_Note Method"""
# 1.Test adding Text note
def test_add_note(setup_NoteManager):
    setup_NoteManager.add_note("TextNote", "Meeting notes", title="Project Kickoff")

    assert len(setup_NoteManager.notes) == 1
    assert setup_NoteManager.notes[0][1].title == "Project Kickoff"

# 2  Test adding Reminder Note
def test_add_reminder_note(setup_NoteManager):
    setup_NoteManager.add_note("ReminderNote", "Team stand-up", reminder_time="2025-03-02 09:00 AM")

    assert len(setup_NoteManager.notes) == 1
    assert isinstance(setup_NoteManager.notes[0][1], ReminderNote)


# Test adding an invalid note type
def test_add_invalid_note_type(setup_NoteManager):
    with pytest.raises(ValueError, match="Wrong note type"):
        setup_NoteManager.add_note("InvalidNoteType", "This note should not be added")

# Test adding TextNote without a title
def test_add_text_note_without_title(setup_NoteManager):
    with pytest.raises(ValueError, match="TextNote requires a title."):
        setup_NoteManager.add_note("TextNote", "This note is missing a title")

# Test adding ReminderNote without a reminder_time
def test_add_reminder_note_without_time(setup_NoteManager):
    with pytest.raises(ValueError, match= "ReminderNote requires a reminder_time."):
        setup_NoteManager.add_note("ReminderNote", "This note is missing a reminder time")



"""Testing the Delete Method"""

# Test deleting an existing note
def test_delete_existing_note(setup_NoteManager):
    # add a text note
    setup_NoteManager.add_note("TextNote", "Delete me", title="To Be Deleted")
    # get the note ID of the added note
    note_ID = setup_NoteManager.notes[0][0]  
    #delete note using the fetched note ID
    setup_NoteManager.delete_note(note_ID)
    # Cheeck that after deletion the list is now empty
    assert len(setup_NoteManager.notes) == 0  

# Test deleting a non-existent note
def test_delete_non_existent_note(setup_NoteManager):
    with pytest.raises(ValueError, match="There is no note with such ID."):
        # Test using invalid note ID
        setup_NoteManager.delete_note(999)  
        



"""Testing the Search Method"""

def test_search_existing_note(setup_NoteManager):
    """Test searching for an existing note by keyword."""
    setup_NoteManager.add_note("TextNote", "This is an important note", title="Important")

    result = setup_NoteManager.search_note("important") 
    assert isinstance(result, list)  
    assert len(result) > 0  
    assert any("This is an important note" in note for note in result)  
    
def test_search_non_existing_note(setup_NoteManager):
    """Test searching for a non existig note"""
    setup_NoteManager.add_note("TextNote", "This is an important note", title="Important")

    result = setup_NoteManager.search_note("Assignment")  

    assert isinstance(result, list)  
    assert result == []  



"""Testing the Show Note Method"""

def test_show_notes(setup_NoteManager):
    setup_NoteManager.add_note("TextNote", "Fiction", title="Fairy-Tale")
    setup_NoteManager.add_note("TextNote", "Note Two", title="Second Note")

    result = setup_NoteManager.show_note()  

    assert isinstance(result, list) 
    assert any("Fiction" in note for note in result)  