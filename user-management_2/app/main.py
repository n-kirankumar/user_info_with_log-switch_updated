"""
main.py
--------
Demonstrates various user scenarios including admin and normal user actions.
"""

from utils import (
    validate_email, validate_age, validate_mobile, validate_gender, validate_blood_group,
    get_user_info, list_all_users, add_user, update_user
)
from log import log_message


def main():
    """
    Main function demonstrating various user scenarios.
    """
    # Scenarios

    # Admin adding a new user
    try:
        admin_username = "kiran"
        new_user_data = {
            "username": "dummy",
            "email": "dummy@example.com",
            "age": 30,
            "mobile": "7776543210",
            "gender": "male",
            "blood_group": "A+",
            "role": "user"
        }
        updated_records = add_user(
            new_user_data['username'],
            new_user_data['email'],
            new_user_data['age'],
            new_user_data['mobile'],
            new_user_data['gender'],
            new_user_data['blood_group'],
            new_user_data['role'],
            admin_username,
            is_admin=True
        )
        log_message('info', f"Admin {admin_username} added new user {new_user_data['username']}")
    except (ValueError, PermissionError) as e:
        log_message('critical', str(e))

    # Admin updating a user
    try:
        admin_username = "kiran"
        user_to_update = "dummy"
        updates = {"email": "new_dummy@example.com"}
        updated_user_info = update_user(user_to_update, updates, admin_username, is_admin=True)
        log_message('info', f"Admin {admin_username} updated user {user_to_update}: {updates}")
    except (ValueError, PermissionError) as e:
        log_message('critical', str(e))

    # Admin viewing a specific user information
    try:
        admin_username = "kiran"
        user_to_view = "ndines"
        user_info = get_user_info(user_to_view, admin_username, is_admin=True)
        log_message('info', f"Admin {admin_username} viewed user {user_to_view}: {user_info}")
    except (ValueError, PermissionError) as e:
        log_message('critical', str(e))

    # Admin listing all users
    try:
        admin_username = "nkiran"
        all_users = list_all_users(admin_username, is_admin=True)
        log_message('info', f"Admin {admin_username} listed all users: {all_users}")
    except (ValueError, PermissionError) as e:
        log_message('critical', str(e))

    # Normal user viewing their own information
    try:
        normal_username = "radha2"
        user_info = get_user_info(normal_username, normal_username, is_admin=False)
        log_message('info', f"Normal user {normal_username} viewed their information: {user_info}")
    except (ValueError, PermissionError) as e:
        log_message('critical', str(e))


# Run the main function
main()
