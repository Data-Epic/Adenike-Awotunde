import datetime

# A parent class for Note
class Note:
    # Creatie a base class 
    def __init__(self, created_at, content):
        """ Initialize a note object
            created_at(datetime): The time the note was created.
            content(str): The content of the note.
        """
        self.created_at = created_at
        self.content = content
        self.note_ID= None
          
    # Display Note
    def display(self):
        #Display the content of a note 
        return f"{self.note_id}: {self.created_at} ({self.content})"
    
#A subclass for TextNote
class TextNote(Note):
    # A subclass for Text note
    def __init__(self, created_at, content, title):
        super().__init__(created_at, content)
        self.title = title
        
    def display(self):
        return f"TextNote: {self.note_ID}: {self.title} - {self.created_at} ({self.content})"

#A Subclass for reminder Note
class ReminderNote(Note):
    # A subclass for Reminder note
    def __init__(self, created_at, content, reminder_time):
        super().__init__(created_at, content)
        self.reminder_time = reminder_time
        valid_formats = ["%Y-%m-%d %H:%M:%S", "%Y-%m-%d %I:%M %p"]
        for fmt in valid_formats:
            try:
                 self.reminder_time = datetime.datetime.strptime(reminder_time, fmt)
            except ValueError:
                print("Invalid date/time format")
            self.reminder_time = None
        
    def display(self):
        return f"ReminderNote: {self.note_ID}:{self.reminder_time} | {self.created_at} ({self.content})"
        
# A subclass for Note Manager
class NoteManager:
    # A class for note manager
    def __init__(self):
        self.notes = []
        self.note_ID = 0 
    
    """Add Note method"""
    def add_note(self, note_type, content, title=None, reminder_time=None):
        self.note_ID += 1  # Increment ID
        
        if note_type == "TextNote":
            if title is None:
                raise ValueError("TextNote requires a title.")
            note = TextNote(datetime.datetime.now(), content, title)
            note.note_ID = self.note_ID
            
        elif note_type == "ReminderNote": 
            if reminder_time is None:
                raise ValueError("ReminderNote requires a reminder_time.")
            note = ReminderNote(datetime.datetime.now(), content, reminder_time)
            note.note_ID = self.note_ID 
            
        else:
            raise ValueError("Wrong note type")
        self.notes.append((self.note_ID, note))
        
        
    """Delete Method"""
    def delete_note(self, note_ID):
        # Delete a Note
        initial_count = len(self.notes)
        self.notes = [(id, note) for id, note in self.notes if id != note_ID]  
        if len(self.notes) < initial_count:
            print(f"Note with ID {note_ID} has been deleted.")
        else:
            raise ValueError("There is no note with such ID.")
    
    
    """Show Method"""
    def show_note(self):
        """Display all stored notes and return them as a list."""
        notes_list = [f"{id}: {note.display()}" for id, note in self.notes]
    
        for note in notes_list:  # Keep the existing print functionality
            print(note)
        return notes_list  
            
            
    """Search Methid"""
    def search_note(self, keyword):
    
        """Find note that contains a specific keyword and return matching notes."""
        results = [note.display() for _, note in self.notes if keyword.lower() in note.content.lower()]
    
        if results:
            for result in results:
                print(result)
            return results  # Return matching notes
        else:
            print("There is no note with this keyword.")
            return []  # Return an empty list if no match is found

    
# Making the app interactive for users
def run_app():
    my_notes=NoteManager()
    while True:
        print("\nSmart Notes Manager")
        print("1. Add Text Note")
        print("2. Add Reminder Note")
        print("3. Show Notes")
        print("4. Search Notes")
        print("5. Delete Note")
        print("6. Exit")
    
        choice = input("Enter your choice: ")
    
        if choice == "1":
            title = input("Enter title: ")
            content = input("Enter content: ")
            my_notes.add_note("TextNote", content, title=title)
        
        elif choice == "2":
            content = input("Enter reminder content: ")
            reminder_time = input("Enter reminder time (YYYY-MM-DD HH:MM AM/PM): ")
            my_notes.add_note("ReminderNote", content, reminder_time=reminder_time)
        
        elif choice == "3":
            my_notes.show_note()
        
        elif choice == "4":
            keyword = input("Enter keyword to search: ")
            my_notes.search_note(keyword)
        
        elif choice == "5":
            try:
                note_ID = int(input("Enter Note ID to delete: "))
                my_notes.delete_note(note_ID)
            except ValueError:
                print("Invalid ID. Please enter a numeric value.")
        
        elif choice == "6":
            print("Exiting Smart Notes Manager. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")
    run_app() 
