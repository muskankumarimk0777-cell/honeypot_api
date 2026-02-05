def agent_reply(history):
    turns = len(history)

    if turns < 2:
        return "Hello, I received your message. Can you explain clearly?"
    elif turns < 4:
        return "I’m a bit confused. What details do you need?"
    elif turns < 6:
        return "It’s asking for some info. Can you send the UPI or link?"
    else:
        return "The page is not loading. Can you resend everything?"
