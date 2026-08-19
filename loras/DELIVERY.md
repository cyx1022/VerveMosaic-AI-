# VerveMosaic AI 花卉纹样 LoRA 交付

## 底模
所有 LoRA 基于 **SD 1.5**（`v1-5-pruned-emaonly.safetensors`）训练。

## 模型清单
| 中文名 | 触发词（训练实际用词） | 文件名 | 推荐权重 | 版本 |
| --- | --- | --- | --- | --- |
| 牡丹 | ich_flower_pattern, ich_peony_pattern | ICH_peony_pattern_lora_v7_clear.safetensors | 0.8 | v7_clear 最终版 |
| 菊花 | ichpattern_chrysanthemum | ICH_chrysanthemum_pattern_lora_v3.safetensors | 0.8 | v3 最终版（dim64） |
| 梅花 | ichpattern_plum_blossom | ICH_plum_blossom_pattern_lora_v2.safetensors | 0.8 | v2 最终版 |
| 莲花 | ich_flower_pattern, ich_lotus_pattern | ICH_lotus_pattern_lora_v3_attr.safetensors | 0.8 | v3_attr 最终版 |
| 花鸟 | ich_flower_pattern, ich_flower_bird_pattern | ICH_flower_bird_pattern_lora_v3.safetensors | 0.8 | v3 最终版 |
| 通用花卉 | ich_flower_pattern | ICH_flower_general_final.safetensors | 0.8 | 最终合并版 |

## 说明
- 每类仅 1 个最终 .safetensors，不含 epoch 中间版。
- 触发词为训练时实际使用的词。如需统一为 ichpattern_peony / ichpattern_lotus / ichpattern_plum / ichpattern_flower_bird 等，需用对应触发词重新训练（可另行提供）。
- 推荐权重 0.7~0.85，表中统一给 0.8。
- 预览图见 previews/<子类>/，每类 2 张。
- 葫芦纹 / 缠枝纹 / 植物纹暂无单独模型，由通用花卉覆盖。
