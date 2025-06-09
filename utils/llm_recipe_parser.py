def parse_mixtral_response(response: str):
    title = ""
    ingredients = []
    instructions = []

    lines = response.strip().splitlines()
    section = None 

    for line in lines:
        line = line.strip()
        if line.lower().startswith("title"):
            section = "title"
            continue
        elif line.lower().startswith("ingredients"):
            section = "ingredients"
            continue
        elif line.lower().startswith("instructions"):
            section = "instructions"
            continue

        if section == "title" and line:
            title = line
        elif section == "ingredients":
            ingredients = [i.strip() for i in line.split(",") if i.strip()]
        elif section == "instructions" and line:
            instructions.append(line)

    return title, ingredients, instructions