def assign_schema_name_to_title(result, generator, **_kwargs):
    for name, schema in result["components"]["schemas"].items():
        if "title" not in schema:
            schema["title"] = name

    return result
