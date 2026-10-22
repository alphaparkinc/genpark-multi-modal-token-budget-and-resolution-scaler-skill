"""Example usage for Multi-Modal Token Budget & Resolution Scaler."""
from client import MultiModalResolutionScaler

if __name__ == "__main__":
    res = MultiModalResolutionScaler.scale_dimensions(3840, 2160, max_tokens=1000)
    print("Scaled Resolution:", res["scaled_resolution"], "Within Budget:", res["within_budget"])
