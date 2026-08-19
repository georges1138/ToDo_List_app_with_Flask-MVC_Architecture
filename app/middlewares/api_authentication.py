from flask import request, jsonify, g
from functools import wraps
from services.token_service import TokenService


def require_api_token(view_func):

    @wraps(view_func)
    def wrapped(*args, **kwargs):

        # 1. read Authorization header
        authorization_header = request.headers.get("Authorization", "")
        parts = authorization_header.split(None, 1)


        # 2. verify it starts with Bearer
        if len(parts) != 2 or parts[0].lower() != "bearer":
            return jsonify({"error": "Missing or malformed Authorization header"}), 401

        # 3. extract raw token
        raw_token = parts[1]
        if len(raw_token) == 0:
            return jsonify({"error": "Missing Authorization token"}), 401

        # 4. resolved = TokenService.resolve_token(raw_token)
        resolved = TokenService.resolve_token(raw_token)

        # 5. if invalid:
        #       return JSON 401
        if resolved is None:
            return jsonify({"error": "Invalid or expired token"}), 401

        # 6. g.user_id = resolved.user_id
        g.user_id = resolved.user_id

        # 7. return view_func(*args, **kwargs)
        return view_func(*args, **kwargs)

    return wrapped
