def set_server_urls(result, generator, request, public):
    host = request.get_host()
    is_local = host.startswith("localhost")
    scheme = "http" if is_local else "https"
    result["servers"] = [
        {"url": f"{scheme}://{host}/api/", "description": "API URL"},
    ]
    return result


def assign_schema_name_to_title(result, generator, **_kwargs):
    for name, schema in result["components"]["schemas"].items():
        if "title" not in schema:
            schema["title"] = name

    return result
