import os
from pathlib import Path
from langgraph.graph.state import CompiledStateGraph


def visualize_and_display_graph(
    app: CompiledStateGraph, filename: str = "graph.png"
) -> None:
    """Prints Mermaid code, saves PNG to disk under 'src/images/'"""
    print("Mermaid diagram:")
    print(app.get_graph().draw_mermaid())

    try:
        # Define target output directory
        script_dir = Path(__file__).resolve().parent.parent
        output_dir = script_dir / "images"
        
        # Ensure 'src/images/' directory exists before saving
        output_dir.mkdir(parents=True, exist_ok=True)

        # Construct full file path
        filepath = output_dir / filename

        # Render PNG bytes
        png_bytes = app.get_graph().draw_mermaid_png()

        # Save to local directory
        with open(filepath, "wb") as f:
            f.write(png_bytes)
        print(f"Graph saved as {filepath}")

    except Exception as e:
        print(f"Could not render/save PNG: {e}")