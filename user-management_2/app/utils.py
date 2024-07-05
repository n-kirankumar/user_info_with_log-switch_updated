"""
utils.py
---------
Contains utility functions for validating user data, adding users, and retrieving user information.
"""

import re
from log import log_message
from constants import VALID_COUNTRY_LIST, EXCLUDED_NUMBERS, VALID_GENDERS, VALID_BLOOD_GROUPS


def validate_email(email):
    """
    Validates the given email address.

    Args:
        email (str): The email address to validate.

    Raises:
        ValueError: If the email format is invalid.

    Returns:
        bool: True if the email is valid, False otherwise.
    """
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    if not re.match(email_regex, email):
        log_message('error', f"Invalid email format: {email}")
        raise ValueError("Invalid email format")
    log_message('info', f"Valid email: {email}")
    return True


def validate_age(age):
    """
    Validates the given age.

    Args:
        age (int): The age to validate.

    Raises:
        ValueError: If the age is not within the valid range (0-120).

    Returns:
        bool: True if the age is valid, False otherwise.
    """
    if not (0 <= age <= 120):
        log_message('error', f"Invalid age: {age}")
        raise ValueError("Invalid age")
    log_message('info', f"Valid age: {age}")
    return True


def validate_mobile(mobile):
    """
    Validates the given mobile number.

    Args:
        mobile (str): The mobile number to validate.

    Raises:
        ValueError: If the mobile number format is invalid.

    Returns:
        bool: True if the mobile number is valid, False otherwise.
    """
    mobile_regex = r'^\d{10}$'
    if not re.match(mobile_regex, mobile):
        log_message('error', f"Invalid mobile number: {mobile}")
        raise ValueError("Invalid mobile number")
    if mobile in EXCLUDED_NUMBERS:
        log_message('info', f"Excluded mobile number: {mobile}")
        return False
    log_message('info', f"Valid mobile number: {mobile}")
    return True


def validate_gender(gender):
    """
    Validates the given gender.

    Args:
        gender (str): The gender to validate.

    Raises:
        ValueError: If the gender is not valid.

    Returns:
        bool: True if the gender is valid, False otherwise.
    """
    if gender.lower() not in VALID_GENDERS:
        log_message('error', f"Invalid gender: {gender}")
        raise ValueError("Invalid gender")
    log_message('info', f"Valid gender: {gender}")
    return True


def validate_blood_group(blood_group):
    """
    Validates the given blood group.

    Args:
        blood_group (str): The blood group to validate.

    Raises:
        ValueError: If the blood group is not valid.

    Returns:
        bool: True if the blood group is valid, False otherwise.
    """
    if blood_group.upper() not in VALID_BLOOD_GROUPS:
        log_message('error', f"Invalid blood group: {blood_group}")
        raise ValueError("Invalid blood group")
    log_message('info', f"Valid blood group: {blood_group}")
    return True


def get_user_info(username, current_user, is_admin):
    """
    Retrieves information for the specified user.

    Args:
        username (str): The username of the user whose information is to be retrieved.
        current_user (str): The username of the current user making the request.
        is_admin (bool): Whether the current user is an admin.

    Raises:
        PermissionError: If the current user is not authorized to view the requested user's information.
        ValueError: If the requested user is not found.

    Returns:
        dict: The user information if the user is found and the current user is authorized.
    """
    from data import data
    user_info = data['records'].get(username)
    if user_info:
        if username == current_user or is_admin:
            log_message('info', f"User info for {username}: {user_info}")
            return user_info
        else:
            log_message('warning', f"Unauthorized access attempt by {current_user} to view {username}'s information")
            raise PermissionError("Unauthorized access")
    else:
        log_message('error', f"User {username} not found")
        raise ValueError("User not found")


def list_all_users(current_user, is_admin):
    """
    Lists all users if the requester is an admin.

    Args:
        current_user (str): The username of the current user making the request.
        is_admin (bool): Whether the current user is an admin.

    Raises:
        PermissionError: If the current user is not authorized to list all users.

    Returns:
        dict: A dictionary containing all users' information.
    """
    from data import data
    if is_admin:
        log_message('info', f"Admin {current_user} listing all users")
        return data['records']
    else:
        log_message('warning', f"Unauthorized access attempt by {current_user} to list all users")
        raise PermissionError("Unauthorized access")


def add_user(username, email, age, mobile, gender, blood_group, role, current_user, is_admin):
    """
    Adds a new user to the system.

    Args:
        username (str): The username of the new user.
        email (str): The email address of the new user.
        age (int): The age of the new user.
        mobile (str): The mobile number of the new user.
        gender (str): The gender of the new user.
        blood_group (str): The blood group of the new user.
        role (str): The role of the new user (admin or user).
        current_user (str): The username of the current user making the request.
        is_admin (bool): Whether the current user is an admin.

    Raises:
        PermissionError: If the current user is not authorized to add users.
        ValueError: If any of the user details are invalid.

    Returns:
        dict: The updated records with the new user added.
    """
    from data import data
    if is_admin:
        validate_email(email)
        validate_age(age)
        validate_mobile(mobile)
        validate_gender(gender)
        validate_blood_group(blood_group)
        if username in data['records']:
            log_message('error', f"User {username} already exists")
            raise ValueError("User already exists")
        data['records'][username] = {
            "email": email,
            "age": age,
            "mobile": mobile,
            "gender": gender,
            "blood_group": blood_group,
            "role": role
        }
        log_message('info', f"Admin {current_user} added new user {username}")
        return data['records']
    else:
        log_message('warning', f"Unauthorized access attempt by {current_user} to add new user {username}")
        raise PermissionError("Unauthorized access")


def update_user(username, updates, current_user, is_admin):
    """
    Updates an existing user's information.

    Args:
        username (str): The username of the user to update.
        updates (dict): A dictionary of the updates to apply.
        current_user (str): The username of the current user making the request.
        is_admin (bool): Whether the current user is an admin.

    Raises:
        PermissionError: If the current user is not authorized to update users.
        ValueError: If any of the updated user details are invalid.

    Returns:
        dict: The updated user information.
    """
    from data import data
    user_info = data['records'].get(username)
    if not user_info:
        log_message('error', f"User {username} not found")
        raise ValueError("User not found")

    if current_user != username and not is_admin:
        log_message('warning', f"Unauthorized access attempt by {current_user} to update user {username}")
        raise PermissionError("Unauthorized access")

    if 'email' in updates:
        validate_email(updates['email'])
    if 'age' in updates:
        validate_age(updates['age'])
    if 'mobile' in updates:
        validate_mobile(updates['mobile'])
    if 'gender' in updates:
        validate_gender(updates['gender'])
    if 'blood_group' in updates:
        validate_blood_group(updates['blood_group'])

    data['records'][username].update(updates)
    log_message('info', f"User {current_user} updated user {username}: {updates}")
    return data['records'][username]
