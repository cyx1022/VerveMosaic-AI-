$ErrorActionPreference = "Continue"

$env:NO_PROXY = "127.0.0.1,localhost"
$env:no_proxy = "127.0.0.1,localhost"
$env:HTTP_PROXY = ""
$env:HTTPS_PROXY = ""
$env:http_proxy = ""
$env:https_proxy = ""
$env:ALL_PROXY = ""
$env:all_proxy = ""
$env:HF_HUB_OFFLINE = "1"
$env:TRANSFORMERS_OFFLINE = "1"

$kohyaDir = "C:\kohya_ss_link"
$python = Join-Path $kohyaDir "venv\Scripts\python.exe"
$trainScript = Join-Path $kohyaDir "sd-scripts\train_network.py"
$logPath = Join-Path $PSScriptRoot "detail_other_flower_training.log"
$samplePrompts = "C:\LoraTraining\ich_detail_outputs_v1\other_flower\sample_prompts.txt"

Set-Location (Join-Path $kohyaDir "sd-scripts")

$args = @(
  $trainScript,
  "--pretrained_model_name_or_path=C:\kohya_ss_link\models\v1-5-pruned-emaonly.safetensors",
  "--tokenizer_cache_dir=C:\kohya_ss_link\tokenizer_cache",
  "--train_data_dir=C:\LoraTraining\ich_clean_train_v1\other_flower",
  "--resolution=768,768",
  "--enable_bucket",
  "--bucket_no_upscale",
  "--min_bucket_reso=384",
  "--max_bucket_reso=1024",
  "--bucket_reso_steps=64",
  "--output_dir=C:\LoraTraining\ich_detail_outputs_v1\other_flower",
  "--output_name=ICH_detail_other_flower_lora_v1",
  "--save_model_as=safetensors",
  "--save_precision=fp16",
  "--save_every_n_epochs=1",
  "--network_module=networks.lora",
  "--network_dim=64",
  "--network_alpha=32",
  "--network_dropout=0.05",
  "--train_batch_size=1",
  "--max_train_epochs=20",
  "--learning_rate=0.00005",
  "--unet_lr=0.00005",
  "--text_encoder_lr=0.000005",
  "--lr_scheduler=cosine",
  "--lr_warmup_steps=60",
  "--optimizer_type=AdamW8bit",
  "--caption_extension=.txt",
  "--mixed_precision=fp16",
  "--cache_latents",
  "--cache_latents_to_disk",
  "--gradient_checkpointing",
  "--max_data_loader_n_workers=0",
  "--clip_skip=1",
  "--logging_dir=C:\LoraTraining\ich_detail_outputs_v1\other_flower\logs",
  "--log_prefix=ICH_detail_other_flower_lora_v1",
  "--sample_prompts=$samplePrompts",
  "--sample_every_n_epochs=2",
  "--sample_sampler=euler_a",
  "--xformers"
)

& $python @args 2>&1 | Tee-Object -FilePath $logPath
Write-Host "Training finished with exit code $LASTEXITCODE"
