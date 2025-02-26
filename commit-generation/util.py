import argparse
import random
import numpy as np
import torch
import json
from transformers import (RobertaModel, RobertaTokenizer, RobertaConfig, T5ForConditionalGeneration, T5Config,
                          PLBartTokenizer, PLBartForConditionalGeneration, PLBartConfig)


def parse_cmg_args():
    parser = argparse.ArgumentParser()

    parser.add_argument("--train_data_file", nargs=2, type=str, default=[".../datasets/MCMD/java/contextual_medits/train.jsonl", ".."])
    parser.add_argument("--eval_data_file", nargs=2, type=str, default=[".../datasets/MCMD/java/contextual_medits/valid.jsonl", ".."])
    parser.add_argument("--test_data_file", nargs=2, type=str, default=[".../datasets/MCMD/java/contextual_medits/test.jsonl", ".."])
    parser.add_argument("--output_dir", type=str, default=None)

    parser.add_argument("--seed", type=int, default=33)
    parser.add_argument("--pretrained_model", type=str, default="codet5")
    parser.add_argument("--batch_size", type=int, default=24)
    parser.add_argument("--epochs", type=int, default=10)
    parser.add_argument("--learning_rate", type=float, default=5e-5)
    parser.add_argument('--gradient_accumulation_steps', type=int, default=1,
                        help="Number of updates steps to accumulate before performing a backward/update pass.")
    parser.add_argument("--beam_size", default=10, type=int,
                        help="beam size for beam search")
    parser.add_argument("--max_grad_norm", type=float, default=1.0)
    parser.add_argument('--patience', type=int, default=5,
                        help='patience for early stop')

    parser.add_argument("--manual_feature_size", type=int, default=14)
    parser.add_argument("--hidden_size", type=int, default=768)
    parser.add_argument("--dropout", type=float, default=0.1)
    parser.add_argument("--num_attention_heads", type=int, default=12)
    parser.add_argument("--max_input_tokens", type=int, default=512)
    parser.add_argument("--max_output_tokens", type=int, default=128)

    parser.add_argument("--available_gpu", type=list, default=[3])
    parser.add_argument("--do_train", action='store_true')
    parser.add_argument("--do_test", action='store_true')
    parser.add_argument("--use_lora", action='store_true')

    parser.add_argument("--data_num", type=int, default=-1, help="DATA_NUM == -1 means all data")
    parser.add_argument("--sampled_num", type=int, default=-1)
    parser.add_argument("--prompt_token_num", type=int, default=50)
    parser.add_argument("--method", type=str, default="")
    parser.add_argument("--layer", type=int, default=-1)

    args = parser.parse_args()
    return args


def set_seed(args):
    random.seed(args.seed)
    np.random.seed(args.seed)
    torch.manual_seed(args.seed)
    if args.n_gpu > 0:
        torch.cuda.manual_seed_all(args.seed)


def build_model_tokenizer_config(args):
    model_classes = {
        "codebert": (RobertaModel, RobertaTokenizer, RobertaConfig, "microsoft/codebert-base"),
        "graphcodebert": (RobertaModel, RobertaTokenizer, RobertaConfig, "microsoft/graphcodebert-base"),
        "codet5": (T5ForConditionalGeneration, RobertaTokenizer, T5Config, "Salesforce/codet5-base"),
        "unixcoder": (RobertaModel, RobertaTokenizer, RobertaConfig, "microsoft/unixcoder-base"),
        "plbart": (PLBartForConditionalGeneration, PLBartTokenizer, PLBartConfig, "uclanlp/plbart-base"),
        "plbart-large": (PLBartForConditionalGeneration, PLBartTokenizer, PLBartConfig, "uclanlp/plbart-large")
    }

    model_class, tokenizer_class, config_class, actual_name = model_classes[args.pretrained_model]
    args.actual_name = actual_name

    # load config.
    config = config_class.from_pretrained(actual_name)
    if args.pretrained_model in ["codebert", "graphcodebert", "unixcoder"]:
        config.hidden_size = args.hidden_size
    elif args.pretrained_model in ["codet5", "plbart", "plbart-large"]:
        config.d_model = args.hidden_size
    config.hidden_dropout_prob = args.dropout
    config.attention_probs_dropout_prob = args.dropout
    if args.pretrained_model in ["unixcoder"]:
        config.is_decoder = True
    # load tokenizer.
    tokenizer = tokenizer_class.from_pretrained(actual_name)
    special_tokens_dict = {"additional_special_tokens": ["<add>", "<del>", "<keep>"]}
    tokenizer.add_special_tokens(special_tokens_dict)
    # load pretrained model.
    model = model_class.from_pretrained(actual_name, config=config)
    model.resize_token_embeddings(len(tokenizer))

    return model, tokenizer, config


def get_msg_label(args, mode):
    file_name = ""
    if mode == "eval":
        file_name = args.eval_data_file
    elif mode == "test":
        file_name = args.test_data_file

    msgs = []
    with open(file_name, 'r') as fr:
        line = fr.readline()
        while line is not None and line != "":
            dict_type = json.loads(line)
            msg = dict_type["nl"]
            msgs.append(msg)
            line = fr.readline()
    return msgs