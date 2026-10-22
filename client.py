"""Multi-Modal Token Budget & Resolution Scaler.
100% Python Standard Library.
"""

import math

class MultiModalResolutionScaler:
    """Scales high-resolution image and video frame dimensions to stay within vision LLM token budgets."""

    @staticmethod
    def scale_dimensions(orig_width: int, orig_height: int, max_tokens: int = 1000, tokens_per_patch: int = 85, patch_size: int = 14) -> dict:
        max_patches = max_tokens // tokens_per_patch
        curr_w, curr_h = orig_width, orig_height

        patches_w = math.ceil(curr_w / patch_size)
        patches_h = math.ceil(curr_h / patch_size)
        total_patches = patches_w * patches_h

        scale_factor = 1.0
        if total_patches > max_patches:
            scale_factor = math.sqrt(max_patches / float(total_patches))
            curr_w = max(patch_size, int(orig_width * scale_factor))
            curr_h = max(patch_size, int(orig_height * scale_factor))
            patches_w = math.ceil(curr_w / patch_size)
            patches_h = math.ceil(curr_h / patch_size)
            total_patches = patches_w * patches_h

            while total_patches > max_patches and (curr_w > patch_size or curr_h > patch_size):
                scale_factor *= 0.95
                curr_w = max(patch_size, int(orig_width * scale_factor))
                curr_h = max(patch_size, int(orig_height * scale_factor))
                patches_w = math.ceil(curr_w / patch_size)
                patches_h = math.ceil(curr_h / patch_size)
                total_patches = patches_w * patches_h

        return {
            "original_resolution": f"{orig_width}x{orig_height}",
            "scaled_resolution": f"{curr_w}x{curr_h}",
            "scale_factor": round(scale_factor, 3),
            "estimated_vision_tokens": total_patches * tokens_per_patch,
            "within_budget": (total_patches * tokens_per_patch) <= max_tokens
        }
