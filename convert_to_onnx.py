# convert_to_onnx.py
# model.pth (PyTorch) -> model.onnx (ONNX) に変換するスクリプト。
# IMAGEAI ルートディレクトリで実行する:
#   cd C:/Users/hamab/Downloads/IMAGEAI/IMAGEAI
#   python convert_to_onnx.py
import sys
import os
import torch

# imageapp パッケージが見つかるようにパスを追加
sys.path.insert(0, os.path.dirname(__file__))

from imageapp.ai.network import create_model

PTH_PATH  = os.path.join(os.path.dirname(__file__), "model", "model.pth")
ONNX_PATH = os.path.join(os.path.dirname(__file__), "docs", "model", "model.onnx")

def main():
    print(f"Loading model from {PTH_PATH} ...")
    model = create_model()
    model.load_state_dict(torch.load(PTH_PATH, map_location="cpu"))
    model.eval()

    # CIFAR-10 用: 入力形状 [1, 3, 32, 32]
    dummy_input = torch.randn(1, 3, 32, 32)

    print(f"Exporting to ONNX at {ONNX_PATH} ...")
    torch.onnx.export(
        model,
        dummy_input,
        ONNX_PATH,
        opset_version=11,
        input_names=["input"],
        output_names=["output"],
        dynamic_axes={"input": {0: "batch_size"}},
    )

    size_mb = os.path.getsize(ONNX_PATH) / (1024 ** 2)
    print(f"Done! {ONNX_PATH}  ({size_mb:.1f} MB)")
    print()
    print("次のステップ:")
    print("  docs/index.html と docs/model/model.onnx を GitHub リポジトリに push してください。")
    print("  GitHub Pages の設定: Settings > Pages > Source: main / docs")

if __name__ == "__main__":
    main()
