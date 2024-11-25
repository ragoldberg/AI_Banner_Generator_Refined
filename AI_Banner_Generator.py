from tkinter import messagebox
import tkinter as tk
from PIL import Image, ImageDraw, ImageFont, ImageTk

# Mock API Functions
def generate_dalle_image(style_prompt):
    return f"Generated image with style: {style_prompt}"

def generate_chatgpt_text(prompt):
    headline = f"AI-generated headline for '{prompt}'"
    subline = f"Engaging subline for '{prompt}'"
    cta = f"Click Here for '{prompt}'"
    return {"headline": headline, "subline": subline, "cta": cta}

def refined_export_banner_as_png(banner, filename="generated_banner.png"):
    try:
        img = Image.new("RGB", (1080, 1080), color="#FFE4B5")
        draw = ImageDraw.Draw(img)
        font = ImageFont.load_default()
        headline = banner["text_content"]["headline"]
        subline = banner["text_content"]["subline"]
        cta = banner["text_content"]["cta"]
        draw.text((headline["x"], headline["y"]), headline["content"], fill="#1F2937", font=font)
        draw.text((subline["x"], subline["y"]), subline["content"], fill="#374151", font=font)
        draw.text((cta["x"], cta["y"]), cta["content"], fill="#3B82F6", font=font)
        img.save(filename)
        return f"Banner saved as {filename}."
    except Exception as e:
        return f"Error while saving banner: {e}"

def generate_banner(template_name, generated_text, style_prompt):
    return {
        "background_image": generate_dalle_image(style_prompt),
        "text_content": {
            "headline": {"content": generated_text["headline"], "x": 100, "y": 50},
            "subline": {"content": generated_text["subline"], "x": 100, "y": 150},
            "cta": {"content": generated_text["cta"], "x": 100, "y": 250},
        },
    }

def generate_banner_preview():
    style_prompt = style_var.get()
    text_prompt = text_entry.get()
    if not style_prompt or not text_prompt:
        messagebox.showerror("Error", "Please fill in all fields!")
        return
    generated_text = generate_chatgpt_text(text_prompt)
    banner = generate_banner("Template 1", generated_text, style_prompt)
    export_status = refined_export_banner_as_png(banner, "banner_preview.png")
    preview_image = ImageTk.PhotoImage(Image.open("banner_preview.png"))
    preview_label.config(image=preview_image)
    preview_label.image = preview_image
    messagebox.showinfo("Success", export_status)

app = tk.Tk()
app.title("AI Banner Generator")
app.geometry("800x600")
tk.Label(app, text="Background Style:", font=("Arial", 12)).pack(pady=10)
style_var = tk.StringVar()
tk.Entry(app, textvariable=style_var, font=("Arial", 12), width=50).pack(pady=5)
tk.Label(app, text="Text Prompt:", font=("Arial", 12)).pack(pady=10)
text_entry = tk.Entry(app, font=("Arial", 12), width=50)
text_entry.pack(pady=5)
tk.Button(app, text="Generate Banner", font=("Arial", 12), command=generate_banner_preview).pack(pady=20)
tk.Label(app, text="Preview:", font=("Arial", 12)).pack(pady=10)
preview_label = tk.Label(app)
preview_label.pack()
app.mainloop()
