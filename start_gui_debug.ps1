$ErrorActionPreference = "Stop"
$Kohya = "C:\LoraTraining\kohya_ss"
$TrainDir = "C:\LoraTraining\ich_flower_train"
$OutDir = "C:\LoraTraining\ich_flower_outputs"
$Model = "C:\LoraTraining\kohya_ss\models\v1-5-pruned-emaonly.safetensors"
$TokenizerCache = "C:\LoraTraining\kohya_ss\tokenizer_cache"
$OutputName = "ICH_flower_pattern_lora"
New-Item -ItemType Directory -Force -Path $OutDir | Out-Null
$StdOut = Join-Path $OutDir "debug_stdout.log"
$StdErr = Join-Path $OutDir "debug_stderr.log"
Remove-Item -LiteralPath $StdOut,$StdErr -Force -ErrorAction SilentlyContinue
Set-Location $Kohya
$env:HF_HOME = "C:\LoraTraining\hf_home"
$env:TRANSFORMERS_OFFLINE = "1"
$env:HF_HUB_OFFLINE = "1"
$env:PYTHONUTF8 = "1"
$env:PYTHONUNBUFFERED = "1"
$env:CUDA_VISIBLE_DEVICES = "0"
$Args = @(
  "C:\LoraTraining\kohya_ss\sd-scripts\train_network.py",
  "--pretrained_model_name_or_path=$Model",
  "--train_data_dir=$TrainDir",
  "--output_dir=$OutDir",
  "--output_name=$OutputName",
  "--save_model_as=safetensors",
  "--save_precision=fp16",
  "--caption_extension=.txt",
  "--mixed_precision=fp16",
  "--optimizer_type=AdamW8bit",
  "--learning_rate=0.0001",
  "--unet_lr=0.0001",
  "--text_encoder_lr=0.00003",
  "--lr_scheduler=cosine",
  "--lr_warmup_steps=300",
  "--resolution=512,512",
  "--train_batch_size=1",
  "--max_train_epochs=6",
  "--save_every_n_epochs=1",
  "--network_module=networks.lora",
  "--network_dim=32",
  "--network_alpha=16",
  "--enable_bucket",
  "--bucket_no_upscale",
  "--min_bucket_reso=256",
  "--max_bucket_reso=2048",
  "--bucket_reso_steps=64",
  "--cache_latents",
  "--gradient_checkpointing",
  "--shuffle_caption",
  "--keep_tokens=1",
  "--clip_skip=1",
  "--max_data_loader_n_workers=0",
  "--tokenizer_cache_dir=$TokenizerCache",
  "--logging_dir=C:\LoraTraining\ich_flower_outputs\logs",
  "--log_prefix=$OutputName",
  "--sample_prompts=C:\LoraTraining\ich_flower_outputs\sample_prompts.txt",
  "--sample_every_n_epochs=1",
  "--sample_sampler=euler_a",
  "--xformers"
)
$p = Start-Process -FilePath "C:\LoraTraining\kohya_ss\venv\Scripts\python.exe" -ArgumentList $Args -WorkingDirectory $Kohya -RedirectStandardOutput $StdOut -RedirectStandardError $StdErr -PassThru
"Started debug training process id $($p.Id)" | Set-Content -LiteralPath (Join-Path $OutDir "debug_process.txt") -Encoding UTF8
