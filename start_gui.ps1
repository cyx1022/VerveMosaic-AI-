$ErrorActionPreference = "Stop"
$Kohya = "C:\LoraTraining\kohya_ss"
$TrainDir = "C:\LoraTraining\ich_flower_train"
$OutDir = "C:\LoraTraining\ich_flower_outputs"
$Model = "C:\LoraTraining\kohya_ss\models\v1-5-pruned-emaonly.safetensors"
$TokenizerCache = "C:\LoraTraining\kohya_ss\tokenizer_cache"
$OutputName = "ICH_flower_pattern_lora"

New-Item -ItemType Directory -Force -Path $OutDir | Out-Null
Get-ChildItem -LiteralPath $OutDir -Force -ErrorAction SilentlyContinue | Where-Object {
    $_.Name -like "$OutputName*" -or $_.Name -in @("sample", "logs") -or $_.Extension -in @(".log", ".json", ".toml")
} | Remove-Item -Recurse -Force -ErrorAction SilentlyContinue
New-Item -ItemType Directory -Force -Path (Join-Path $OutDir "logs") | Out-Null

$SamplePrompt = Join-Path $OutDir "sample_prompts.txt"
@"
ichpattern_flower, peony motif, Chinese intangible cultural heritage pattern, traditional floral ornament, symmetrical flat decorative pattern, red and gold, clean vector-like composition --w 512 --h 512 --d 1234 --l 7.5 --s 28
ichpattern_flower, lotus motif, Chinese intangible cultural heritage pattern, ornamental flat design, blue and white porcelain palette, seamless decorative pattern --w 512 --h 512 --d 2234 --l 7.5 --s 28
ichpattern_flower, scroll grass motif, traditional Chinese decorative textile pattern, flat ornamental motif, balanced composition, warm earth colors --w 512 --h 512 --d 3234 --l 7.5 --s 28
"@ | Set-Content -LiteralPath $SamplePrompt -Encoding UTF8

Set-Location $Kohya
$env:HF_HOME = "C:\LoraTraining\hf_home"
$env:TRANSFORMERS_OFFLINE = "1"
$env:HF_HUB_OFFLINE = "1"
$env:PYTHONUTF8 = "1"
$env:PYTHONUNBUFFERED = "1"
$env:CUDA_VISIBLE_DEVICES = "0"

Write-Host "Starting high-quality ICH flower LoRA training"
Write-Host "Train dir: $TrainDir"
Write-Host "Output dir: $OutDir"
Write-Host "Progress shows below. Do not close this window."
Write-Host "Samples appear after each epoch in: C:\LoraTraining\ich_flower_outputs\sample"

& "C:\LoraTraining\kohya_ss\venv\Scripts\python.exe" "C:\LoraTraining\kohya_ss\sd-scripts\train_network.py" `
  "--pretrained_model_name_or_path=$Model" `
  "--train_data_dir=$TrainDir" `
  "--output_dir=$OutDir" `
  "--output_name=$OutputName" `
  "--save_model_as=safetensors" `
  "--save_precision=fp16" `
  "--caption_extension=.txt" `
  "--mixed_precision=fp16" `
  "--optimizer_type=AdamW8bit" `
  "--learning_rate=0.0001" `
  "--unet_lr=0.0001" `
  "--text_encoder_lr=0.00003" `
  "--lr_scheduler=cosine" `
  "--lr_warmup_steps=300" `
  "--resolution=512,512" `
  "--train_batch_size=1" `
  "--max_train_epochs=6" `
  "--save_every_n_epochs=1" `
  "--network_module=networks.lora" `
  "--network_dim=32" `
  "--network_alpha=16" `
  "--enable_bucket" `
  "--bucket_no_upscale" `
  "--min_bucket_reso=256" `
  "--max_bucket_reso=2048" `
  "--bucket_reso_steps=64" `
  "--cache_latents" `
  "--gradient_checkpointing" `
  "--shuffle_caption" `
  "--keep_tokens=1" `
  "--clip_skip=1" `
  "--max_data_loader_n_workers=0" `
  "--tokenizer_cache_dir=$TokenizerCache" `
  "--logging_dir=C:\LoraTraining\ich_flower_outputs\logs" `
  "--log_prefix=$OutputName" `
  "--sample_prompts=$SamplePrompt" `
  "--sample_every_n_epochs=1" `
  "--sample_sampler=euler_a" `
  "--xformers"

Write-Host "Training command finished with exit code $LASTEXITCODE"
Write-Host "Outputs: C:\LoraTraining\ich_flower_outputs"
Read-Host "按 Enter 关闭窗口"
