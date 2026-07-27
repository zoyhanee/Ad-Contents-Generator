import gc
import logging
import psutil
import torch

logger = logging.getLogger("model_loader")


def _mem_snapshot(tag: str):
    vm = psutil.virtual_memory()
    gpu_info = ""
    if torch.cuda.is_available():
        allocated = torch.cuda.memory_allocated() / 1e9
        reserved = torch.cuda.memory_reserved() / 1e9
        gpu_info = f" | GPU allocated={allocated:.2f}GB reserved={reserved:.2f}GB"
    logger.info(
        f"[{tag}] RAM used={vm.percent:.1f}% available={vm.available/1e9:.2f}GB{gpu_info}"
    )


class ManagedModel:

    def __init__(self, loader_fn, name: str = "model"):
        self.loader_fn = loader_fn
        self.name = name
        self.model = None

    def __enter__(self):
        _mem_snapshot(f"{self.name} - 로드 전")
        self.model = self.loader_fn()
        _mem_snapshot(f"{self.name} - 로드 후")
        return self.model

    def __exit__(self, exc_type, exc_val, exc_tb):
        if isinstance(self.model, dict):
            for key in list(self.model.keys()):
                del self.model[key]
        else:
            for attr_name in ("transformer", "text_encoder", "text_encoder_2", "vae", "unet"):
                component = getattr(self.model, attr_name, None)
                if component is not None and hasattr(component, "to"):
                    try:
                        component.to("cpu")
                    except Exception:
                        pass
                    setattr(self.model, attr_name, None)
                    del component

        del self.model
        self.model = None

        gc.collect()
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
            torch.cuda.ipc_collect()
            torch.cuda.synchronize()
            gc.collect()
            torch.cuda.empty_cache()

        _mem_snapshot(f"{self.name} - 언로드 후")
        return False

def load_sequential(*named_loaders):
    results = {}
    for name, loader_fn, use_fn in named_loaders:
        with ManagedModel(loader_fn, name=name) as model:
            results[name] = use_fn(model)
    return results
