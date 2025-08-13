# My Setup

1. Fork and clone comfyui

   ```sh
   git@github.com:comfyanonymous/ComfyUI.git
   ```

2. Install Anaconda

   create new conda env

   ```sh
   conda create --prefix ./comfy_env python=3.12
   ```

   and activate

   ```sh
   conda activate ./comfy_env
   ```

3. Install stuff

   pytorch for nvidia

   ```sh
   pip install --pre torch torchvision torchaudio --index-url https://download.pytorch.org/whl/nightly/cu129
   ```

   python packages

   ```sh
   pip install -r requirements.txt
   ```

4. Run comfyui

   ```sh
   python main.py
   ```

5. Deactivate

   ```sh
   conda deactivate
   ```

6. View all envs

   ```sh
   conda env list
   ```

7. Install Comfy UI Manager

   ```sh
   cd custom_nodes
   git clone git@github.com:tianqirumeng/ComfyUI-Manager.git
   cd ..
   python main.py
   ```

8. Git

   Pull from upstream

   ```sh
   git remote set-url origin git@github.com:dennis-gonzales/ComfyUI.git
   git remote add upstream git@github.com:comfyanonymous/ComfyUI.git
   git pull upstream master
   ```

9. Recommended Nodes

   - ComfyUI-Easy-Use

     To enhance the usability of ComfyUI, optimizations and integrations have been implemented for several commonly used nodes.

   - ComfyUI-Manager

     ComfyUI-Manager provides features to install and manage custom nodes for ComfyUI, as well as various functionalities to assist with ComfyUI.

   - ComfyUI-WD14-Tagger

     A ComfyUI extension allowing the interrogation of booru tags from images.

   - ComfyUI_UltimateSDUpscale

     ComfyUI nodes for the Ultimate Stable Diffusion Upscale script by Coyote-A.

   - ComfyUI_DanTagGen

     ComfyUI node of [a/Kohaku's DanTagGen Demo](https://huggingface.co/KBlueLeaf/DanTagGen?not-for-all-audiences=true).
