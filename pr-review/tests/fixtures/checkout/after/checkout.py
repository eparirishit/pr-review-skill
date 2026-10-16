def checkout(total, discount):
    if not 0 <= discount < 100:
        raise ValueError("discount")
    return {"total": total * (100 - discount) / 100}
