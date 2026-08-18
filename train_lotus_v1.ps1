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
$root = "C:\LoraTraining"
$sourceRoot = Join-Path $root "ich_lotus_train"
$sourceDir = Get-ChildItem -Path $sourceRoot -Directory | Select-Object -First 1 -ExpandProperty FullName
$trainDir = Join-Path $root "ich_lotus_train_en\10_lotus"
$outputDir = Join-Path $root "ich_lotus_outputs"
$logPath = Join-Path $root "lotus_lora_training.log"
$samplePrompts = Join-Path $root "lotus_sample_prompts.txt"

New-Item -ItemType Directory -Force -Path $trainDir, $outputDir | Out-Null
Copy-Item -Force -Path (Join-Path $sourceDir "*") -Destination $trainDir

Set-Location (Join-Path $kohyaDir "sd-scripts")

$args = @(
  $trainScript,
  "--pretrained_model_name_or_path=C:\LoraTraining\kohya_ss\models\v1-5-pruned-emaonly.safetensors",
  "--tokenizer_cache_dir=C:\kohya_ss_link\tokenizer_cache",
  "--train_data_dir=C:\LoraTraining\ich_lotus_train_en",
  "--resolution=512,512",
  "--enable_bucket",
  "--min_bucket_reso=256",
  "--max_bucket_reso=768",
  "--bucket_reso_steps=64",
  "--output_dir=C:\LoraTraining\ich_lotus_outputs",
  "--output_name=ICH_lotus_pattern_lora",
  "--save_model_as=safetensors",
  "--save_precision=fp16",
  "--save_every_n_epochs=1",
  "--network_module=networks.lora",
  "--network_dim=32",
  "--network_alpha=16",
  "--network_dropout=0.05",
  "--train_batch_size=1",
  "--max_train_epochs=8",
  "--learning_rate=0.00008",
  "--unet_lr=0.00008",
  "--text_encoder_lr=0.00001",
  "--lr_scheduler=cosine",
  "--lr_warmup_steps=40",
  "--optimizer_type=AdamW",
  "--caption_extension=.txt",
  "--shuffle_caption",
  "--keep_tokens=2",
  "--mixed_precision=fp16",
  "--cache_latents",
  "--cache_latents_to_disk",
  "--gradient_checkpointing",
  "--max_data_loader_n_workers=0",
  "--sample_prompts=$samplePrompts",
  "--sample_every_n_epochs=1",
  "--sample_sampler=euler_a"
)

& $python @args 2>&1 | Tee-Object -FilePath $logPath
