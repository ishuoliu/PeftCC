#!/bin/bash


pretrained_model="codet5"
method="prefix"     # prefix, prompt
lang="javascript"

python run_peft.py \
    --pretrained_model ${pretrained_model} \
    --method ${method} \
    --train_data_file ../datasets/MCMD/${lang}/contextual_medits/train.jsonl .. \
    --eval_data_file ../datasets/MCMD/${lang}/contextual_medits/valid.jsonl .. \
    --test_data_file ../datasets/MCMD/${lang}/contextual_medits/test.jsonl .. \
    --output_dir ../results/mcmd/${method}/${lang}/${pretrained_model}/checkpoints_50_5e-4_relayer3 \
    --gradient_accumulation_steps 2 \
    --learning_rate 5e-4 \
    --epochs 10 \
    --do_train


python run_peft_layer.py \
    --pretrained_model ${pretrained_model} \
    --method ${method} \
    --train_data_file ../datasets/MCMD/${lang}/contextual_medits/train.jsonl .. \
    --eval_data_file ../datasets/MCMD/${lang}/contextual_medits/valid.jsonl .. \
    --test_data_file ../datasets/MCMD/${lang}/contextual_medits/test.jsonl .. \
    --output_dir ../results/mcmd/${method}/${lang}/${pretrained_model}/checkpoints_50_5e-5_relayer12 \
    --gradient_accumulation_steps 2 \
    --batch_size 16 \
    --learning_rate 5e-5 \
    --layer 6 \
    --epochs 10 \
    --do_train


python run_peft_relayer.py \
    --pretrained_model ${pretrained_model} \
    --method ${method} \
    --train_data_file ../datasets/MCMD/${lang}/contextual_medits/train.jsonl .. \
    --eval_data_file ../datasets/MCMD/${lang}/contextual_medits/valid.jsonl .. \
    --test_data_file ../datasets/MCMD/${lang}/contextual_medits/test.jsonl .. \
    --output_dir ../results/mcmd/${method}/${lang}/${pretrained_model}/checkpoints_50_5e-5_relayer12 \
    --gradient_accumulation_steps 2 \
    --batch_size 16 \
    --learning_rate 5e-5 \
    --layer 6 \
    --epochs 10 \
    --do_train
