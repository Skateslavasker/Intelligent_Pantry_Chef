def parse_mixtral_response(response: str):
    title = ""
    ingredients = []
    instructions = []

    lines = response.strip().splitlines()
    section = None 

    for line in lines:
        line = line.strip()
        if line.lower().startswith("title"):
            title = line.split(":", 1)[1].strip() 
            continue
        elif line.lower().startswith("ingredients"):
            section = "ingredients"
            continue
        elif line.lower().startswith("instructions"):
            section = "instructions"
            continue

        
        if section == "ingredients" and line:
            item = line.strip("- ").split(",")[0].strip()
            if item:
                ingredients.append(item)
        elif section == "instructions" and line:
            instructions.append(line) 

    return title, ingredients, instructions