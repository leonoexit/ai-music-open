#!/usr/bin/env sh
set -eu

model_dir="${1:-./models}"
mkdir -p "$model_dir/HeartMuLa-oss-3B" "$model_dir/HeartCodec-oss"

hf download --local-dir "$model_dir" HeartMuLa/HeartMuLaGen
hf download --local-dir "$model_dir/HeartMuLa-oss-3B" HeartMuLa/HeartMuLa-oss-3B-happy-new-year
hf download --local-dir "$model_dir/HeartCodec-oss" HeartMuLa/HeartCodec-oss-20260123

echo "HeartMuLa checkpoints downloaded to $model_dir"
