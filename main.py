from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List
from fastapi.responses import StreamingResponse
from openai import OpenAI
import os
import uvicorn

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = FastAPI()

# In-memory storage
product_store = {}
selected_platform_store = {}
template_store = {}
hooks_store = {}
selected_hook_store = {}

# Request Models
class ProductInput(BaseModel):
    product_name: str

class PlatformInput(BaseModel):
    platform: str

class TemplateInput(BaseModel):
    template_name: str

class HookSelection(BaseModel):
    hook_number: int

class CombinedRequest(BaseModel):
    user_input: str
    template_number: int
    selected_hook_number: int

# Templates
templates = {
    "Standard": {
        "description": "A well-rounded post that explains the product’s purpose, features, and why it’s the perfect solution to a common problem. It's detailed but not overwhelming.",
        "style": "Standard",
        "post_length": 300
    },
    "Formatted": {
        "description": "A structured post that is broken down into clear sections highlighting the product's key features, benefits, and how it works. This template is great for a more formal approach to product introduction.",
        "style": "Formatted",
        "post_length": 500
    },
    "Chunky": {
        "description": "A long-form post that provides an in-depth analysis of the product, its impact, and why it’s a game-changer. This template works well for more complex products.",
        "style": "Chunky",
        "post_length": 400
    },
    "Short": {
        "description": "A concise, punchy post that highlights the core feature of the product. This template is best for audiences that want quick, impactful content.",
        "style": "Short",
        "post_length": 150
    },
    "Emojis": {
        "description": "A fun and engaging post that uses emojis to convey the key benefits of the product. It's designed to capture attention and encourage interaction, great for social media platforms.",
        "style": "Emojis",
        "post_length": 200
    }
}

# Helper Functions
def generate_hooks(product_name: str, platform: str, template: dict) -> List[str]:
    prompt = f"""
    You are a marketing copy expert for {platform.title()}. Generate 5 creative, engaging, and product-specific hook lines for the product '{product_name}'.
    These hooks should align with the following content style: {template['description']} and appeal to a professional audience.
    Output only the list of 5 hooks as bullet points.
    """
    
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.8
    )
    text = response['choices'][0].message.content
    hooks = [line.lstrip("-• ").strip() for line in text.strip().splitlines() if line.strip()]
    return hooks[:5]

def generate_final_post(hook: str, template: dict, platform: str, product_name: str):
    prompt = f"""
    You are a marketing assistant. Using the following hook: "{hook}", write a {platform.title()} post for the product "{product_name}".
    Follow this style: {template['description']}. The post should be compelling, clearly tailored to the product's use case, and fit well on {platform}.
    Do not use generic placeholders—make it sound specific to {product_name}'s real-world benefits.
    """
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )
    return response.choices[0].message.content

# Endpoints
@app.post("/product")
def submit_product(data: ProductInput):
    product_store["name"] = data.product_name
    return {"message": f"Product '{data.product_name}' saved successfully."}

@app.post("/select-platform")
def select_platform(data: PlatformInput):
    if data.platform.lower() not in ["instagram", "twitter"]:
        raise HTTPException(status_code=400, detail="Invalid platform. Choose 'Instagram' or 'Twitter'.")
    selected_platform_store["platform"] = data.platform
    return {"message": f"Platform '{data.platform}' selected."}

@app.get("/templates")
def get_templates():
    return templates

@app.post("/select-template")
def select_template(data: TemplateInput):
    if data.template_name not in templates:
        raise HTTPException(status_code=400, detail="Template not found.")
    template_store["template"] = templates[data.template_name]
    return {"message": f"Template '{data.template_name}' selected."}

@app.get("/hooks")
def get_hooks():
    product_name = product_store.get("name")
    platform = selected_platform_store.get("platform")
    template = template_store.get("template")
    if not all([product_name, platform, template]):
        raise HTTPException(status_code=400, detail="Missing product, platform or template selection.")
    hooks = generate_hooks(product_name, platform, template)
    hooks_store["hooks"] = hooks
    return {"hooks": hooks}

@app.post("/select-hook")
def select_hook(data: HookSelection):
    hooks = hooks_store.get("hooks")
    if not hooks:
        raise HTTPException(status_code=400, detail="Hooks not generated yet.")
    if not (1 <= data.hook_number <= len(hooks)):
        raise HTTPException(status_code=400, detail="Invalid hook number.")
    selected_hook_store["hook"] = hooks[data.hook_number - 1]
    return {"message": f"Hook {data.hook_number} selected."}

@app.get("/generate-post")
def get_final_post():
    hook = selected_hook_store.get("hook")
    product_name = product_store.get("name")
    platform = selected_platform_store.get("platform")
    template = template_store.get("template")

    if not all([hook, product_name, platform, template]):
        raise HTTPException(status_code=400, detail="Missing required selections.")

    post = generate_final_post(hook, template, platform, product_name)
    return {"final_post": post}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, limit_concurrency=10)
