from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db_work.dao.models.model import Users, Notes  # Замените "your_module_name" на имя вашего модуля с объявлением таблиц

# Создаем соединение с базой данных
engine = create_engine('sqlite:///notes.db_work')

# Создаем сессию
Session = sessionmaker(bind=engine)
session = Session()

# Задайте значение user_id_tg, для которого хотите найти Notes
target_user_id_tg = 1362055393  # Замените на нужный вам user_id_tg

# Находим пользователя по user_id_tg
user = session.query(Users).filter_by(user_id_tg=target_user_id_tg).first()

if user:
    # Create a new note for the user with the correct date format
    new_note = Notes(
        user=user,
        date="test",  # Convert to Python date object
        time="12:30 PM",  # Replace this with the correct time
        category="Some Category",
        sub_category="Some Sub-category"
    )

    # Add the new note to the session and commit the changes
    session.add(new_note)
    session.commit()

    # Now you can fetch all notes for the user again
    user_notes = user.notes
    for note in user_notes:
        print(f"Note ID: {note.id}, Date: {note.date}, Time: {note.time}, Category: {note.category}, Sub-category: {note.sub_category}")
else:
    print("Пользователь не найден")

# Close the session
session.close()
