import json
import os
import time
from dataclasses import dataclass
from typing import Any
from typing_extensions import Self,List, Union


@dataclass
class LearnerArgs:
    use_wandb: bool = False
    epochs: int = 100
    patience: int = 10
    model_type: str = "clip_base"
    print_freq: int = 10
    save_freq: int = 10
    output_dir: str = "./output/"
    model_backbone: str = "ViT-B/16"
    dataset: str = "cifar10"
    device: str = "cuda"
    batch_size: int = 64
    num_workers: int = 4
    train_size: Union[float, None] = None
    train_eval_size:  Union[tuple[int, int], None] = None
    text_prompt_template: str = "a photo of {}."
    learning_rate: float = 0.01
    momentum: float = 0.9
    weight_decay: float = 1e-4
    warmup: int = 0
    seed: int = 42

    def __post_init__(self) -> None:
        self.run_id = f"{self.model_type}_{self.model_backbone}_{str(int(time.time()))}".replace(
            "/", ""
        ).lower()

        self.output_dir = os.path.join(self.output_dir, self.run_id)

        # create output directory if it does not exist
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

        # save the config as json
        with open(os.path.join(self.output_dir, "config.json"), "w") as f:
            data = self.to_dict()
            json.dump(data, f, indent=4)

    def to_dict(self) -> dict[str, Any]:
        return self.__dict__