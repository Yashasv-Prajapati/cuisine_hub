def check_role(role_required):
    def decorator(func):
        def wrapper(*args, **kwargs):
            if USER["role"] == role_required or USER["role"] == 'admin':
                return func(*args, **kwargs)
            else:
                print(f"Unauthorized. Only {role_required}s and admin are allowed to use this function.")
                # You can raise an exception or return a specific response if needed.
                return None  # For illustration purposes

        return wrapper
    return decorator