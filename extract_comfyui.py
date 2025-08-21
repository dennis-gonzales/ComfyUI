import os
import json
from PIL import Image

def extract_comfyui_metadata(image_path, output_dir):
    try:
        img = Image.open(image_path)
        info = img.info
        
        workflow = info.get("workflow")
        prompt = info.get("prompt")

        if not workflow and not prompt:
            return False  # No ComfyUI metadata

        base_name = os.path.splitext(os.path.basename(image_path))[0]

        if workflow:
            workflow_data = json.loads(workflow)
            workflow_file = os.path.join(output_dir, f"{base_name}_workflow.json")
            with open(workflow_file, "w", encoding="utf-8") as f:
                json.dump(workflow_data, f, indent=2)

            # Print workflow summary
            nodes = workflow_data.get("nodes", [])
            links = workflow_data.get("links", [])
            node_types = [n.get("type") for n in nodes[:5]]  # first 5 node types
            print(f"[WORKFLOW] {base_name}: {len(nodes)} nodes, {len(links)} links, sample: {node_types}")

        if prompt:
            prompt_data = json.loads(prompt)
            prompt_file = os.path.join(output_dir, f"{base_name}_prompt.json")
            with open(prompt_file, "w", encoding="utf-8") as f:
                json.dump(prompt_data, f, indent=2)

            print(f"[PROMPT]   {base_name}: {len(prompt_data)} entries")

        return True

    except Exception as e:
        print(f"Error processing {image_path}: {e}")
        return False


def scan_folder_for_pngs(folder, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for root, _, files in os.walk(folder):  # recursive
        for file in files:
            if file.lower().endswith(".comfy"):
                image_path = os.path.join(root, file)
                extract_comfyui_metadata(image_path, output_dir)


if __name__ == "__main__":
    input_folder = "user/default/workflows"        # change this to your folder of PNGs
    output_folder = "extracted"    # where JSON files will go
    scan_folder_for_pngs(input_folder, output_folder)
