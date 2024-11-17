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

# Fetch key revisions
def get_revisions(key):
    """
    Fetch all revisions for a specific key and display as a table.
    """
    response = call_api("/kv/get_revisions", method="GET", data={"key": key})
    
    if response.get("status") == "success":
        revisions = response["data"]
        table_data = [["Revision Number", "Value", "Created At"]]  # Table header
        for rev in revisions:
            table_data.append([
                rev["revision_number"], 
                rev["value"], 
                rev["created_at"]
            ])
        return table_data
    return [["Error"], [response.get("message", "Unknown error")]]



def get_all_pairs():
    """
    Fetch all key-value pairs from the KV store and display as a table.
    """
    response = call_api("/kv/get_all_pairs", method="GET")
    print(response)
    
    if response.get("status") == "success":
        pairs = response["data"]
        table_data = [["Key", "Value"]]  # Table header
        for pair in pairs:
            table_data.append([
                pair["key"], 
                pair["value"]
            ])
        return table_data
    return [["Error"], [response.get("message", "Unknown error")]]


# LLM control
def control_kv(prompt):
    response = call_api("/llm/control-kv", method="POST", data={"prompt": prompt})
    return response

# Gradio UI
with gr.Blocks() as app:
    gr.Markdown("# KV Store Frontend with LLM Integration")

    # Registration Tab
    with gr.Tab("Register"):
        gr.Markdown("## Register a new user")
        email_input = gr.Textbox(label="Email")
        password_input = gr.Textbox(label="Password", type="password")
        is_admin_input = gr.Checkbox(label="Admin?")
        register_button = gr.Button("Register")
        register_output = gr.Textbox(label="Register Response")
        register_button.click(register, inputs=[email_input, password_input, is_admin_input], outputs=register_output)

    # Login Tab
    with gr.Tab("Login"):
        gr.Markdown("## Login")
        login_email_input = gr.Textbox(label="Email")
        login_password_input = gr.Textbox(label="Password", type="password")
        login_button = gr.Button("Login")
        login_output = gr.Textbox(label="Login Response")
        login_button.click(login, inputs=[login_email_input, login_password_input], outputs=login_output)

    # KV Store Actions Tab
    with gr.Tab("KV Store"):
        gr.Markdown("## Perform KV Store Actions")
        with gr.Accordion("Key-Value Operations", open=False):
            action_dropdown = gr.Dropdown(["Insert", "Update", "Delete", "Get"], label="Action")
            key_input = gr.Textbox(label="Key")
            value_input = gr.Textbox(label="Value (Optional)")
            kv_button = gr.Button("Perform Action")
            kv_output = gr.Textbox(label="KV Store Response")
            kv_button.click(perform_kv_action, inputs=[action_dropdown, key_input, value_input], outputs=kv_output)

        with gr.Accordion("Get Revisions", open=False):
            key_revisions_input = gr.Textbox(label="Key")
            revisions_button = gr.Button("Get Revisions")
            revisions_output = gr.Dataframe(label="Revisions Table", col_count=3)
            revisions_button.click(get_revisions, inputs=[key_revisions_input], outputs=revisions_output)

        with gr.Accordion("Get All Key-Value Pairs", open=False):
            all_pairs_button = gr.Button("Get All Pairs")
            all_pairs_output = gr.Dataframe(label="All Key-Value Pairs Table", col_count=2)
            all_pairs_button.click(get_all_pairs, inputs=[], outputs=all_pairs_output)

    # Control KV via LLM Tab
    with gr.Tab("LLM Control"):
        gr.Markdown("## Control KV Store via LLM")
        prompt_input = gr.Textbox(label="Prompt")
        llm_button = gr.Button("Send Prompt")
        llm_output = gr.Textbox(label="LLM Response")
        llm_button.click(control_kv, inputs=[prompt_input], outputs=llm_output)


# Launch the app
app.launch()
