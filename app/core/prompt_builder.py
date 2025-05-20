

def build_prompt(schema: str, user_question: str) -> str:
    prompt = f"""Sistema: Eres un asistente que convierte preguntas en lenguaje natural en consultas SQL.
Genera consultas compatibles con PostgreSQL.
{schema}

Usuario: {user_question}
SQL:"""
    print(f"Prompt:\n{prompt}\n")
    
    return prompt
