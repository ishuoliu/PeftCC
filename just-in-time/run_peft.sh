#!/bin/bash


pretrained_model="codebert"
method="prefix"     # prefix, prompt
structure="concat"     # single, concat

python run_peft.py \
    --pretrained_model ${pretrained_model} \
    --method ${method} \
    --structure ${structure} \
    --train_data_file ../datasets/jitfine/changes_train.pkl ../datasets/jitfine/features_train.pkl \
    --eval_data_file ../datasets/jitfine/changes_valid.pkl ../datasets/jitfine/features_valid.pkl \
    --test_data_file ../datasets/jitfine/changes_test.pkl ../datasets/jitfine/features_test.pkl \
    --output_dir ../results/jit/${pretrained_model}/${method}/${structure}/checkpoints_50_1e-2 \
    --learning_rate 1e-2 \
    --epochs 10 \
    --do_train





