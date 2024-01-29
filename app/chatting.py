from app.models import Chat, User


def create_chat(current_username, chat_form):
    """Helper function for creating a new chat."""
    selected_users = {k for (k, v) in chat_form.data.items() if
                      (k != 'submit' and k != 'csrf_token' and
                       v is True)}
    valid_users = {user for user in selected_users if
                   User.query.filter_by(username=user).first()}
    chat = Chat()

    if current_username not in valid_users:
        chat.users.append(User.query.filter_by(username=current_username)
                          .first())
    for user in valid_users:
        chat.users.append(User.query.filter_by(username=user).first())
    return chat
