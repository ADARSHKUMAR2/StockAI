import gradio as gr
from actions.explanation import explain_concept
from actions.flashcards import generate_flashcards
from actions.quiz import quiz_me
from actions.summary import summarize_text
import sys

def build_demo():
    with gr.Blocks() as demo:
        gr.Markdown("# AI Tutor MCP Toolkit – Demo Console")
        with gr.Tab("Explain Concept"):
            q = gr.Textbox(label="Concept / Question")
            lvl = gr.Slider(1, 5, value=3, step=1, label="Explanation Level")
            out1 = gr.Markdown()
            gr.Button("Explain").click(explain_concept, inputs=[q, lvl], outputs=out1)
        with gr.Tab("Summarize Text"):
            txt = gr.Textbox(lines=8, label="Long Text")
            ratio = gr.Slider(0.1, 0.8, value=0.3, step=0.05, label="Compression Ratio")
            out2 = gr.Markdown()
            gr.Button("Summarize").click(summarize_text, inputs=[txt, ratio], outputs=out2)
        with gr.Tab("Flashcards"):
            topic_fc = gr.Textbox(label="Topic")
            n_fc = gr.Slider(1, 20, value=5, step=1, label="# Cards")
            out3 = gr.Markdown()
            gr.Button("Generate").click(generate_flashcards, inputs=[topic_fc, n_fc], outputs=out3)
        with gr.Tab("Quiz Me"):
            topic_q = gr.Textbox(label="Topic")
            lvl_q = gr.Slider(1, 5, value=3, step=1, label="Difficulty Level")
            n_q = gr.Slider(1, 15, value=5, step=1, label="# Questions")
            out4 = gr.Markdown()
            gr.Button("Start Quiz").click(quiz_me, inputs=[topic_q, lvl_q, n_q], outputs=out4)
    return demo


if __name__ == "__main__":
    # print("Starting AI Tutor MCP Toolkit...", file=sys.stderr)
    build_demo().launch(
        server_name="127.0.0.1", 
        mcp_server=True
)
# --- END OF FILE ---