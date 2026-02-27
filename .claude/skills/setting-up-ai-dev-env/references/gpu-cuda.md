# GPU/CUDA Setup

## Check GPU

```bash
# Check for NVIDIA GPU
lspci | grep -i nvidia
nvidia-smi                 # Shows driver version, GPU info, memory
```

## NVIDIA Drivers (Ubuntu)

```bash
# Check current driver
nvidia-smi

# Install recommended driver
sudo apt update
sudo ubuntu-drivers autoinstall
sudo reboot

# Or specific version
sudo apt install nvidia-driver-535
sudo reboot

# Verify
nvidia-smi
```

## CUDA Toolkit

```bash
# Via conda (recommended — avoids system conflicts)
conda install -c conda-forge cudatoolkit=12.1

# Via apt (Ubuntu)
wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2204/x86_64/cuda-keyring_1.1-1_all.deb
sudo dpkg -i cuda-keyring_1.1-1_all.deb
sudo apt update
sudo apt install cuda-toolkit-12-1

# Verify
nvcc --version
```

## PyTorch with GPU

```bash
# CUDA 12.1
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121

# CUDA 12.4
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu124

# Verify
python -c "import torch; print(f'CUDA available: {torch.cuda.is_available()}'); print(f'Device: {torch.cuda.get_device_name(0)}')"
```

## Version Compatibility

| Driver | CUDA | PyTorch |
|--------|------|---------|
| 535+   | 12.1 | 2.1+    |
| 545+   | 12.4 | 2.4+    |
| 550+   | 12.6 | 2.5+    |

## Troubleshooting
- **`nvidia-smi` not found**: Install NVIDIA driver first
- **CUDA version mismatch**: `nvidia-smi` shows max CUDA, `nvcc` shows installed
- **torch.cuda.is_available() = False**: PyTorch CUDA version must match installed CUDA
- **Out of memory**: Check `nvidia-smi` for memory usage, reduce batch size
