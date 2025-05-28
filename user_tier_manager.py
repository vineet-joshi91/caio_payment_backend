def get_user_tier(email):
    try:
        with open("user_tiers.txt", "r") as f:
            for line in f:
                stored_email, tier = line.strip().split(",")
                if stored_email == email:
                    return tier
    except FileNotFoundError:
        return "free"
    return "free"
