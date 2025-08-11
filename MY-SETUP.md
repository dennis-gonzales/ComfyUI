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

3. install pytorch for nvidia

   ```sh
   pip install --pre torch torchvision torchaudio --index-url https://download.pytorch.org/whl/nightly/cu129
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
