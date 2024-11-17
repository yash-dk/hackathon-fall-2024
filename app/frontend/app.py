import gradio as gr
from api_utils import register_user, login_user, call_api

# Register function
def register(email, password, is_admin):
    response = register_user(email, password, is_admin)
    return response

# Login function
def login(email, password):
    response = login_user(email, password)
    return response

# KV store actions
def perform_kv_action(action, key, value=None):
    data = {"key": key, "value": value}
    if action == "Insert":
        endpoint = "/kv/insert"
        method = "POST"
    elif action == "Update":
        endpoint = "/kv/update"
        method = "PUT"
    elif action == "Delete":
        endpoint = "/kv/delete"
        method = "DELETE"
    elif action == "Get":
        endpoint = "/kv/get"
        method = "GET"
    else:
        return {"error": "Invalid action"}
    
    response = call_api(endpoint, method, data)
    return response

# LLM control
def control_kv(prompt):
    response = call_api("/llm/control-kv", method="POST", data={"prompt": prompt})
    return response

# Gradio UI
with gr.Blocks() as app:
    gr.Markdown("# KV Store Frontend with LLM Integration")
    
    # Registration
    with gr.Tab("Register"):
        gr.Markdown("## Register a new user")
        email_input = gr.Textbox(label="Email")
        password_input = gr.Textbox(label="Password", type="password")
        is_admin_input = gr.Checkbox(label="Admin?")
        register_button = gr.Button("Register")
        register_output = gr.Textbox(label="Register Response")
        register_button.click(register, inputs=[email_input, password_input, is_admin_input], outputs=register_output)
    
    # Login
    with gr.Tab("Login"):
        gr.Markdown("## Login")
        login_email_input = gr.Textbox(label="Email")
        login_password_input = gr.Textbox(label="Password", type="password")
        login_button = gr.Button("Login")
        login_output = gr.Textbox(label="Login Response")
        login_button.click(login, inputs=[login_email_input, login_password_input], outputs=login_output)
    
    # KV Store Actions
    with gr.Tab("KV Store"):
        gr.Markdown("## Perform KV Store Actions")
        action_dropdown = gr.Dropdown(["Insert", "Update", "Delete", "Get"], label="Action")
        key_input = gr.Textbox(label="Key")
        value_input = gr.Textbox(label="Value (Optional)")
        kv_button = gr.Button("Perform Action")
        kv_output = gr.Textbox(label="KV Store Response")
        kv_button.click(perform_kv_action, inputs=[action_dropdown, key_input, value_input], outputs=kv_output)

    # Control KV via LLM
    with gr.Tab("LLM Control"):
        gr.Markdown("## Control KV Store via LLM")
        prompt_input = gr.Textbox(label="Prompt")
        llm_button = gr.Button("Send Prompt")
        llm_output = gr.Textbox(label="LLM Response")
        llm_button.click(control_kv, inputs=[prompt_input], outputs=llm_output)

# Launch the app
app.launch()
