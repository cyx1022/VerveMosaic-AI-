# ICH_peony_pattern_lora_v7_clear

这是当前效果最好的牡丹模型 `ICH_peony_pattern_lora_v7_clear` 的还原数据集。

## 完整训练链路

v7_clear 不是从基础模型直接训出来的，它是“v2 继续训练”：

1. `01_v2_base`：v2 阶段训练数据，70 张图和 caption
2. `02_v7_finetune`：v7_clear 阶段训练数据，12 张精选清晰图和 caption

所以这个模型实际吸收的牡丹图是 `70 张 v2 底图 + 12 张 v7 精选图`。

## 触发词

- v2 / v7 caption 都使用：`ich_flower_pattern, ich_peony_pattern`

## v2 阶段参数
- 数据集：70 张
- Epoch：8，batch size：1
- 学习率：UNet 8e-5，Text Encoder 1e-5
- 优化器：AdamW8bit，cosine，warmup 40
- LoRA：dim 32，alpha 16，dropout 0.05
- Caption shuffle 开启，keep_tokens 2
- 每 1 epoch 出预览，Euler a

## v7_clear 阶段参数
- 基础模型：`v1-5-pruned-emaonly.safetensors`
- 继续训练权重：`C:\LoraTraining\ich_peony_outputs_v2\ICH_peony_pattern_lora_v2.safetensors`
- 数据集：12 张
- 分辨率：512 x 512，开启 bucket，256-768，步长 64
- Epoch：20，batch size：1，总步数：240
- 学习率：UNet 1e-4，Text Encoder 1e-5
- 优化器：AdamW8bit
- Scheduler：cosine，warmup 50
- LoRA：dim 32，alpha 16，dropout 0.05
- 混合精度：fp16
- Caption：shuffle 开启，keep_tokens 2
- 采样：每 1 epoch 出预览，Euler a
- 保存：每 1 epoch 保存检查点
- 其它：gradient checkpointing，xformers，clip_skip 1，seed 0

## 生成推荐
- LoRA 权重：`1.0-1.1`
- 触发词开头：`ich_flower_pattern, ich_peony_pattern`
