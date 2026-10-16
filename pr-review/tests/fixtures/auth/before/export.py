def export(document, user):
    if document.owner_id != user.id:
        raise PermissionError("owner only")
    return document.content
