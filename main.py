import numpy as np
import pandas as pd

from torch.utils.data import DataLoader
from torchvision import datasets, transforms

from models import Model1, Model2, Model3
from utils import test_model, show_img

assets_path = f"./assets"
logs_path = f"{assets_path}/logs"
imagenet2012_path = f"{assets_path}/ImageNet2012"
rrdb_pretrained_weights_path = f"{assets_path}/models/RRDB_PSNR_x4.pth"

imagenet2012_dataset = datasets.ImageFolder(root=imagenet2012_path,
                                            transform=transforms.Compose([
                                                transforms.Resize(256),
                                                transforms.RandomCrop(224),
                                                transforms.ToTensor()
                                            ]))
imagenet2012_loader = DataLoader(imagenet2012_dataset,
                                 batch_size=2, shuffle=True, num_workers=4)

# computes tests on the different models
models = [
    Model1(),
    Model2(rrdb_pretrained_weights_path=rrdb_pretrained_weights_path),
    Model3()
]
losses, psnrs, avg_times, total_times = np.zeros(shape=len(models)), \
                                        np.zeros(shape=len(models)), \
                                        np.zeros(shape=len(models)), \
                                        np.zeros(shape=len(models))
for i_model, model in enumerate(models):
    results = test_model(model=model, data=imagenet2012_loader, early_stop=50, verbose=False)
    losses[i_model], psnrs[i_model], avg_times[i_model], total_times[i_model] = np.mean(results["loss"]), \
                                                                                np.mean(results["psnr"]), \
                                                                                np.mean(results["time"]), \
                                                                                results["total_time"]

print(pd.DataFrame(
    index=[f"Model {i + 1}" for i in range(len(models))],
    data={
        "Average loss": losses,
        "Average PSNR (dB)": psnrs,
        "Average time (s)": avg_times,
        "Total time (s)": total_times
    }
))
