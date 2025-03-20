import streamlit as st
import json

class BookCollection:
    def __init__(self):
        self.book_list = []
        self.storage_file = "books_data.json"
        self.read_from_file()

    def read_from_file(self):
        try:
            with open(self.storage_file, "r") as file:
                self.book_list = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            self.book_list = []

    def save_to_file(self):
        with open(self.storage_file, "w") as file:
            json.dump(self.book_list, file, indent=4)

    def add_book(self, title, author, year, genre, read):
        new_book = {
            "title": title,
            "author": author,
            "year": year,
            "genre": genre,
            "read": read,
        }
        self.book_list.append(new_book)
        self.save_to_file()

    def delete_book(self, book_title):
        self.book_list = [book for book in self.book_list if book["title"].lower() != book_title.lower()]
        self.save_to_file()

    def search_books(self, search_text):
        return [book for book in self.book_list if search_text.lower() in book["title"].lower() or search_text.lower() in book["author"].lower()]

    def update_book(self, old_title, new_title, new_author, new_year, new_genre, new_read):
        for book in self.book_list:
            if book["title"].lower() == old_title.lower():
                book["title"] = new_title or book["title"]
                book["author"] = new_author or book["author"]
                book["year"] = new_year or book["year"]
                book["genre"] = new_genre or book["genre"]
                book["read"] = new_read
                self.save_to_file()
                return True
        return False

    def reading_progress(self):
        total_books = len(self.book_list)
        completed_books = sum(1 for book in self.book_list if book["read"])
        return total_books, completed_books

book_manager = BookCollection()

st.title("📚 Book Collection Manager")
menu = {
    "📖 Add Book": "Add Book",
    "🗑 Remove Book": "Remove Book",
    "🔍 Search Book": "Search Book",
    "✏ Update Book": "Update Book",
    "📚 View All Books": "View All Books",
    "📊 Reading Progress": "Reading Progress",
    "🚪 Exit": "Exit"
}
choice = st.sidebar.selectbox("Menu", list(menu.keys()))

if choice == "📖 Add Book":
    st.subheader("Add a New Book")
    title = st.text_input("Book Title")
    author = st.text_input("Author")
    year = st.text_input("Publication Year")
    genre = st.text_input("Genre")
    read = st.checkbox("Have you read this book?")
    if st.button("Add Book"):
        book_manager.add_book(title, author, year, genre, read)
        st.success("Book added successfully! ✅")

elif choice == "🗑 Remove Book":
    st.subheader("Remove a Book")
    book_title = st.text_input("Enter the title of the book to remove")
    if st.button("Remove Book"):
        book_manager.delete_book(book_title)
        st.success("Book removed successfully! 🗑")

elif choice == "🔍 Search Book":
    st.subheader("Search for Books")
    search_text = st.text_input("Enter title or author to search")

    if st.button("Search"):
        results = book_manager.search_books(search_text)

        if results:
            for book in results:
                col1, col2 = st.columns([3, 1])  # Columns for book details and checkbox
                
                with col1:
                    st.write(f"📖 **{book['title']}** by {book['author']} ({book['year']}) - {book['genre']}")
                
                with col2:
                    # Checkbox to mark book as read/unread
                    new_read_status = st.checkbox("Read", value=book["read"], key=book["title"])

                # Button to update read status
                if st.button(f"Update '{book['title']}' Read Status", key=f"update_{book['title']}"):
                    book_manager.update_book(
                        old_title=book["title"],
                        new_title=book["title"],
                        new_author=book["author"],
                        new_year=book["year"],
                        new_genre=book["genre"],
                        new_read=new_read_status
                    )
                    st.success(f"Updated '{book['title']}' to {'Read' if new_read_status else 'Unread'}! ✅")
        else:
            st.warning("No matching books found. ❌")

elif choice == "✏ Update Book":
    st.subheader("Update Book Details")
    old_title = st.text_input("Enter the title of the book you want to update")
    new_title = st.text_input("New Title (leave blank to keep same)")
    new_author = st.text_input("New Author (leave blank to keep same)")
    new_year = st.text_input("New Year (leave blank to keep same)")
    new_genre = st.text_input("New Genre (leave blank to keep same)")
    new_read = st.checkbox("Have you read this book?")
    if st.button("Update Book"):
        if book_manager.update_book(old_title, new_title, new_author, new_year, new_genre, new_read):
            st.success("Book updated successfully! ✅")
        else:
            st.warning("Book not found! ❌")

elif choice == "📚 View All Books":
    st.subheader("Your Book Collection")
    books = book_manager.book_list
    if books:
        for book in books:
            status = "✔ Read" if book["read"] else "❌ Unread"
            st.write(f"📖 **{book['title']}** by {book['author']} ({book['year']}) - {book['genre']} - {status}")
    else:
        st.info("No books in your collection. 📚")

elif choice == "📊 Reading Progress":
    st.subheader("Your Reading Progress")
    total, completed = book_manager.reading_progress()
    st.write(f"📚 Total Books: {total}")
    st.write(f"✅ Books Read: {completed}")
    progress = (completed / total * 100) if total > 0 else 0
    st.progress(progress / 100)
    st.write(f"Progress: {progress:.2f}%")

elif choice == "🚪 Exit":
    st.balloons()
    st.success("🎉 Thanks for using Book📚 Collection Manager! See You Next Time!😊")





