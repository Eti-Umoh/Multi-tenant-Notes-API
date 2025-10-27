from fastapi import APIRouter, Request
from server.authentication.schemas import LoginUser

router = APIRouter()


@router.post('/login')
async def login_user(request: Request, payload: LoginUser):

    user = await get_user_by_email(payload.email_address.lower(), db)
    if user:
        # Convert password to bytes
        password_bytes = payload.password.encode('utf-8')
        hashed_password = user.password.encode('utf-8')
    
    login_trial = await get_trial(payload.email_address.lower(), db)
    if login_trial:
        # Calculate the time difference between now and the last attempt
        current_time = datetime.now(timezone.utc)
        time_since_last_attempt = current_time - login_trial.last_attempt_at

        if login_trial.trials >= 3 and time_since_last_attempt < timedelta(minutes=15):
            msg = "Try again in 15 minutes"
            return bad_request_response(msg)
        
        # If the lockout period has passed, reset the trials counter
        if time_since_last_attempt >= timedelta(minutes=15):
            login_trial.trials = 0

    if not user or not bcrypt.checkpw(password_bytes, hashed_password):
        if not login_trial:
            login_trial = await create_login_trial(payload.email_address.lower(), db)
        else:
            login_trial.trials += 1
            login_trial.last_attempt_at = datetime.now()  # Update the timestamp
            db.commit()
        if login_trial.trials >= 3:
            msg = "Try again in 15 minutes"
            return bad_request_response(msg)
        
        msg = "Invalid Email or Password"
        return bad_request_response(msg)
    
    # Reset the login trials on successful login
    if login_trial:
        login_trial.trials = 0
        db.commit()

    access_token = create_access_token(user.email_address)
    if not access_token:
        msg = "Error generating access token"
        return internal_server_error_response(msg)

    if not user.initial_login:
        user.initial_login = True
        db.commit()

    return success_response(message="successful",
                            body={"user": await user_serializer(user, db),
                                  "access-token": access_token,
                                  "token_type": "bearer"})
