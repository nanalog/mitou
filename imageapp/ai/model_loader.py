import torch
from PIL import Image
from torchvision import transforms
from imageapp.ai.network import create_model

class gcn():
    def __call__(self, x):
        mean = torch.mean(x)
        std = torch.std(x)
        return (x - mean) / (std + 1e-6)

transform = transforms.Compose([
    transforms.Resize((32, 32)),
    transforms.ToTensor(),
    gcn(),
])

device = torch.device(
    "cuda"
    if torch.cuda.is_available()
    else "cpu"
)

model = create_model()
model.load_state_dict(
    torch.load(
        'model/model.pth',
        map_location=device
    )
)
model.to(device)
model.eval()
class_names= {
    0: "airplane",
    1: "automobile",
    2: "bird",
    3: "cat",
    4: "deer",
    5: "dog",
    6: "frog",
    7: "horse",
    8: "ship",
    9: "truck",
}


def predict(image_path):
    image = Image.open(image_path)
    image = image.convert('RGB')
    x = transform(image)
    x = x.unsqueeze(0)
    x = x.to(device)
    with torch.no_grad():
        y = model(x)
        probs = torch.softmax(y, dim=1)
        pred = y.argmax(1).item()
        probability = probs[0][pred].item()
    return class_names[pred], probability
