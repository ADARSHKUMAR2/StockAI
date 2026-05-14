import gradio as gr
from actions.explanation import explain_concept
from actions.flashcards import generate_flashcards
from actions.quiz import quiz_me
from actions.summary import summarize_text
from actions.email import send_email
import sys

# ==========================================
# UI WRAPPERS: Accumulate chunks for Gradio
# ==========================================
async def ui_explain(q, lvl):
    full_text = ""
    async for chunk in explain_concept(q, lvl):
        full_text += chunk
        yield full_text

async def ui_summarize(txt, ratio):
    full_text = ""
    async for chunk in summarize_text(txt, ratio):
        full_text += chunk
        yield full_text

async def ui_flashcards(topic, n):
    full_text = ""
    async for chunk in generate_flashcards(topic, n):
        full_text += chunk
        yield full_text

async def ui_quiz(topic, lvl, n):
    full_text = ""
    async for chunk in quiz_me(topic, lvl, n):
        full_text += chunk
        yield full_text

async def ui_email(to_addr, subj, body):
    full_text = ""
    async for chunk in send_email(to_addr, subj, body):
        full_text += chunk
        yield full_text

# ==========================================
# GRADIO INTERFACE
# ==========================================
def build_demo():
    with gr.Blocks() as demo:
        gr.Markdown("# AI Tutor MCP Toolkit – Demo Console")
        
        with gr.Tab("Explain Concept"):
            q = gr.Textbox(label="Concept / Question")
            lvl = gr.Slider(1, 5, value=3, step=1, label="Explanation Level")
            out1 = gr.Markdown()
            # Notice we use the ui_explain wrapper here!
            gr.Button("Explain").click(ui_explain, inputs=[q, lvl], outputs=out1)
            
        with gr.Tab("Summarize Text"):
            txt = gr.Textbox(lines=8, label="Long Text")
            ratio = gr.Slider(0.1, 0.8, value=0.3, step=0.05, label="Compression Ratio")
            out2 = gr.Markdown()
            gr.Button("Summarize").click(ui_summarize, inputs=[txt, ratio], outputs=out2)
            
        with gr.Tab("Flashcards"):
            topic_fc = gr.Textbox(label="Topic")
            n_fc = gr.Slider(1, 20, value=5, step=1, label="# Cards")
            out3 = gr.Markdown()
            gr.Button("Generate").click(ui_flashcards, inputs=[topic_fc, n_fc], outputs=out3)
            
        with gr.Tab("Quiz Me"):
            topic_q = gr.Textbox(label="Topic")
            lvl_q = gr.Slider(1, 5, value=3, step=1, label="Difficulty Level")
            n_q = gr.Slider(1, 15, value=5, step=1, label="# Questions")
            out4 = gr.Markdown()
            gr.Button("Start Quiz").click(ui_quiz, inputs=[topic_q, lvl_q, n_q], outputs=out4)
            
        with gr.Tab("Send Email"):
            to_addr = gr.Textbox(label="To Address")
            subj = gr.Textbox(label="Subject")
            body = gr.Textbox(lines=5, label="Email Body")
            out_email = gr.Markdown()
            gr.Button("Send").click(ui_email, inputs=[to_addr, subj, body], outputs=out_email)

    return demo

if __name__ == "__main__":
    build_demo().launch(
        server_name="127.0.0.1", 
        mcp_server=True
    )