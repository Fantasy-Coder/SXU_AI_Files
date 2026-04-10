# -*- coding: utf-8 -*-
'''
Train CIFAR10/CIFAR100 with PyTorch and Vision Transformers!
written by @kentaroy47, @arutema47
modified to support CIFAR100
'''

from __future__ import print_function

import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import torch.backends.cudnn as cudnn
import numpy as np

import torchvision
import torchvision.transforms as transforms

import os
import argparse
import pandas as pd
import csv
import time
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from models import *
from utils import progress_bar
from randomaug import RandAugment
from models.vit import ViT
from models.convmixer import ConvMixer
from models.mobilevit import mobilevit_xxs
from models.dyt import DyT

# parsers
parser = argparse.ArgumentParser(description='PyTorch CIFAR10/100 Training')
parser.add_argument('--lr', default=1e-4, type=float, help='learning rate') # resnets.. 1e-3, Vit..1e-4
parser.add_argument('--opt', default="adam")
parser.add_argument('--resume', '-r', action='store_true', help='resume from checkpoint')
parser.add_argument('--noaug', action='store_false', help='disable use randomaug')
parser.add_argument('--noamp', action='store_true', help='disable mixed precision training. for older pytorch versions')
parser.add_argument('--nowandb', action='store_true', help='disable wandb')
parser.add_argument('--mixup', action='store_true', help='add mixup augumentations')
parser.add_argument('--net', default='vit')
parser.add_argument('--dp', action='store_true', help='use data parallel')
parser.add_argument('--bs', default='512')
parser.add_argument('--size', default="32")
parser.add_argument('--n_epochs', type=int, default='200')
parser.add_argument('--patch', default='4', type=int, help="patch for ViT")
parser.add_argument('--dimhead', default="512", type=int)
parser.add_argument('--convkernel', default='8', type=int, help="parameter for convmixer")
parser.add_argument('--dataset', default='cifar10', type=str, help='dataset to use (cifar10 or cifar100)')

args = parser.parse_args()

run_label = f"{args.net}_{args.dataset}_patch{args.patch}"
run_timestamp = time.strftime("%Y%m%d-%H%M%S")
base_dir = Path("log") / run_label
base_dir.mkdir(parents=True, exist_ok=True)

history_paths = [
    base_dir / f"log_{run_label}.csv",
    base_dir / f"history_{run_label}_{run_timestamp}.csv",
]
plot_path = base_dir / f"{run_label}_{run_timestamp}.png"
summary_csv_path = base_dir / "summary.csv"
text_log_path = base_dir / f"log_{run_label}.txt"

# take in args
usewandb = not args.nowandb
if usewandb:
    import wandb
    watermark = "{}_lr{}_{}".format(args.net, args.lr, args.dataset)
    wandb.init(project="cifar-challenge",
            name=watermark)
    wandb.config.update(args)

bs = int(args.bs)
imsize = int(args.size)

use_amp = not args.noamp
aug = args.noaug

device = 'cuda' if torch.cuda.is_available() else 'cpu'
best_acc = 0  # best test accuracy
start_epoch = 0  # start from epoch 0 or last checkpoint epoch

# Data
print('==> Preparing data..')
if args.net=="vit_timm":
    size = 384
else:
    size = imsize

# Set up normalization based on the dataset
if args.dataset == 'cifar10':
    mean = (0.4914, 0.4822, 0.4465)
    std = (0.2023, 0.1994, 0.2010)
    num_classes = 10
    dataset_class = torchvision.datasets.CIFAR10
elif args.dataset == 'cifar100':
    mean = (0.5071, 0.4867, 0.4408)
    std = (0.2675, 0.2565, 0.2761)
    num_classes = 100
    dataset_class = torchvision.datasets.CIFAR100
else:
    raise ValueError("Dataset must be either 'cifar10' or 'cifar100'")

transform_train = transforms.Compose([
    transforms.RandomCrop(32, padding=4),
    transforms.Resize(size),
    transforms.RandomHorizontalFlip(),
    transforms.ToTensor(),
    transforms.Normalize(mean, std),
])

transform_test = transforms.Compose([
    transforms.Resize(size),
    transforms.ToTensor(),
    transforms.Normalize(mean, std),
])

# Add RandAugment with N, M(hyperparameter)
if aug:  
    N = 2; M = 14;
    transform_train.transforms.insert(0, RandAugment(N, M))

# Prepare dataset
trainset = dataset_class(root='./data', train=True, download=True, transform=transform_train)
trainloader = torch.utils.data.DataLoader(trainset, batch_size=bs, shuffle=True, num_workers=8)

testset = dataset_class(root='./data', train=False, download=True, transform=transform_test)
testloader = torch.utils.data.DataLoader(testset, batch_size=100, shuffle=False, num_workers=8)

# Set up class names based on the dataset
if args.dataset == 'cifar10':
    classes = ('plane', 'car', 'bird', 'cat', 'deer', 'dog', 'frog', 'horse', 'ship', 'truck')
else:
    # CIFAR100 has 100 classes, so we don't list them all here
    classes = None

# Model factory..
print('==> Building model..')
# net = VGG('VGG19')
if args.net=='res18':
    net = ResNet18(num_classes=num_classes)
elif args.net=='vgg':
    net = VGG('VGG19', num_classes=num_classes)
elif args.net=='res34':
    net = ResNet34(num_classes=num_classes)
elif args.net=='res50':
    net = ResNet50(num_classes=num_classes)
elif args.net=='res101':
    net = ResNet101(num_classes=num_classes)
elif args.net=="convmixer":
    # from paper, accuracy >96%. you can tune the depth and dim to scale accuracy and speed.
    net = ConvMixer(256, 16, kernel_size=args.convkernel, patch_size=1, n_classes=num_classes)
elif args.net=="mlpmixer":
    from models.mlpmixer import MLPMixer
    net = MLPMixer(
    image_size = 32,
    channels = 3,
    patch_size = args.patch,
    dim = 512,
    depth = 6,
    num_classes = num_classes
)
elif args.net=="vit_small":
    from models.vit_small import ViT
    net = ViT(
    image_size = size,
    patch_size = args.patch,
    num_classes = num_classes,
    dim = int(args.dimhead),
    depth = 6,
    heads = 8,
    mlp_dim = 512,
    dropout = 0.1,
    emb_dropout = 0.1
)
elif args.net=="vit_tiny":
    from models.vit_small import ViT
    net = ViT(
    image_size = size,
    patch_size = args.patch,
    num_classes = num_classes,
    dim = int(args.dimhead),
    depth = 4,
    heads = 6,
    mlp_dim = 256,
    dropout = 0.1,
    emb_dropout = 0.1
)
elif args.net=="simplevit":
    from models.simplevit import SimpleViT
    net = SimpleViT(
    image_size = size,
    patch_size = args.patch,
    num_classes = num_classes,
    dim = int(args.dimhead),
    depth = 6,
    heads = 8,
    mlp_dim = 512
)
elif args.net=="vit":
    # ViT for cifar10/100
    net = ViT(
    image_size = size,
    patch_size = args.patch,
    num_classes = num_classes,
    dim = int(args.dimhead),
    depth = 6,
    heads = 8,
    mlp_dim = 512,
    dropout = 0.1,
    emb_dropout = 0.1
)
elif args.net=="dyt":
    # DyT for cifar10/100
    net = DyT(
    image_size = size,
    patch_size = args.patch,
    num_classes = num_classes,
    dim = int(args.dimhead),
    depth = 6,
    heads = 8,
    mlp_dim = 512,
    dropout = 0.1,
    emb_dropout = 0.1
)
elif args.net=="vit_timm":
    import timm
    net = timm.create_model("vit_base_patch16_384", pretrained=True)
    net.head = nn.Linear(net.head.in_features, num_classes)
elif args.net=="cait":
    from models.cait import CaiT
    net = CaiT(
    image_size = size,
    patch_size = args.patch,
    num_classes = num_classes,
    dim = int(args.dimhead),
    depth = 6,   # depth of transformer for patch to patch attention only
    cls_depth=2, # depth of cross attention of CLS tokens to patch
    heads = 8,
    mlp_dim = 512,
    dropout = 0.1,
    emb_dropout = 0.1,
    layer_dropout = 0.05
)
elif args.net=="cait_small":
    from models.cait import CaiT
    net = CaiT(
    image_size = size,
    patch_size = args.patch,
    num_classes = num_classes,
    dim = int(args.dimhead),
    depth = 6,   # depth of transformer for patch to patch attention only
    cls_depth=2, # depth of cross attention of CLS tokens to patch
    heads = 6,
    mlp_dim = 256,
    dropout = 0.1,
    emb_dropout = 0.1,
    layer_dropout = 0.05
)
elif args.net=="swin":
    from models.swin import swin_t
    net = swin_t(window_size=args.patch,
                num_classes=num_classes,
                downscaling_factors=(2,2,2,1))
elif args.net=="mobilevit":
    net = mobilevit_xxs(size, num_classes)
else:
    raise ValueError(f"'{args.net}' is not a valid model")

# For Multi-GPU
if 'cuda' in device:
    print(device)
    if args.dp:
        print("using data parallel")
        net = torch.nn.DataParallel(net) # make parallel
        cudnn.benchmark = True

if args.resume:
    # Load checkpoint.
    print('==> Resuming from checkpoint..')
    assert os.path.isdir('checkpoint'), 'Error: no checkpoint directory found!'
    checkpoint_path = './checkpoint/{}-{}-{}-ckpt.t7'.format(args.net, args.dataset, args.patch)
    checkpoint = torch.load(checkpoint_path)
    net.load_state_dict(checkpoint['net'])
    best_acc = checkpoint['acc']
    start_epoch = checkpoint['epoch']

# Loss is CE
criterion = nn.CrossEntropyLoss()

if args.opt == "adam":
    optimizer = optim.Adam(net.parameters(), lr=args.lr)
elif args.opt == "sgd":
    optimizer = optim.SGD(net.parameters(), lr=args.lr)  
    
# use cosine scheduling
scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, args.n_epochs)

SUMMARY_FIELDNAMES = [
    "timestamp",
    "run_name",
    "model",
    "dataset",
    "patch",
    "optimizer",
    "lr",
    "epochs",
    "best_val_acc",
    "best_val_epoch",
    "final_val_acc",
    "final_val_loss",
    "final_train_acc",
    "final_train_loss",
    "total_time_sec",
    "history_csv",
    "plot_path",
]


def save_history_csv(history):
    """Persist per-epoch metrics to the configured CSV paths."""
    if not history:
        return
    df = pd.DataFrame(history)
    for path in history_paths:
        df.to_csv(path, index=False)


def save_training_plot(history):
    """Render loss/accuracy curves for the current run."""
    if not history:
        return
    epochs = [entry['epoch'] for entry in history]
    train_loss = [entry['train_loss'] for entry in history]
    val_loss = [entry['val_loss'] for entry in history]
    train_acc = [entry['train_acc'] for entry in history]
    val_acc = [entry['val_acc'] for entry in history]

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    axes[0].plot(epochs, train_loss, label='Train Loss')
    axes[0].plot(epochs, val_loss, label='Val Loss')
    axes[0].set_xlabel('Epoch')
    axes[0].set_ylabel('Loss')
    axes[0].set_title('Loss vs Epoch')
    axes[0].grid(True, alpha=0.3)
    axes[0].legend()

    axes[1].plot(epochs, train_acc, label='Train Acc')
    axes[1].plot(epochs, val_acc, label='Val Acc')
    axes[1].set_xlabel('Epoch')
    axes[1].set_ylabel('Accuracy (%)')
    axes[1].set_title('Accuracy vs Epoch')
    axes[1].grid(True, alpha=0.3)
    axes[1].legend()

    fig.suptitle(f'Training Curves: {run_label}', fontsize=14)
    fig.tight_layout()
    fig.savefig(plot_path, dpi=300)
    plt.close(fig)


def update_summary_csv(history, total_time_sec):
    """Append a one-line summary for the completed run."""
    if not history:
        return
    best_entry = max(history, key=lambda entry: entry['val_acc'])
    final_entry = history[-1]
    payload = {
        "timestamp": run_timestamp,
        "run_name": run_label,
        "model": args.net,
        "dataset": args.dataset,
        "patch": args.patch,
        "optimizer": args.opt,
        "lr": args.lr,
        "epochs": len(history),
        "best_val_acc": round(best_entry['val_acc'], 4),
        "best_val_epoch": int(best_entry['epoch']),
        "final_val_acc": round(final_entry['val_acc'], 4),
        "final_val_loss": round(final_entry['val_loss'], 6),
        "final_train_acc": round(final_entry['train_acc'], 4),
        "final_train_loss": round(final_entry['train_loss'], 6),
        "total_time_sec": round(total_time_sec, 2),
        "history_csv": str(history_paths[-1]),
        "plot_path": str(plot_path),
    }
    file_exists = summary_csv_path.exists()
    with summary_csv_path.open('a', newline='') as handle:
        writer = csv.DictWriter(handle, fieldnames=SUMMARY_FIELDNAMES)
        if not file_exists:
            writer.writeheader()
        writer.writerow(payload)

##### Training
scaler = torch.cuda.amp.GradScaler(enabled=use_amp)
def train(epoch):
    print('\nEpoch: %d' % epoch)
    net.train()
    train_loss = 0
    correct = 0
    total = 0
    for batch_idx, (inputs, targets) in enumerate(trainloader):
        inputs, targets = inputs.to(device), targets.to(device)
        # Train with amp
        with torch.cuda.amp.autocast(enabled=use_amp):
            outputs = net(inputs)
            loss = criterion(outputs, targets)
        scaler.scale(loss).backward()
        scaler.step(optimizer)
        scaler.update()
        optimizer.zero_grad()

        train_loss += loss.item()
        _, predicted = outputs.max(1)
        total += targets.size(0)
        correct += predicted.eq(targets).sum().item()

        progress_bar(batch_idx, len(trainloader), 'Loss: %.3f | Acc: %.3f%% (%d/%d)'
            % (train_loss/(batch_idx+1), 100.*correct/total, correct, total))
    avg_loss = train_loss / len(trainloader)
    train_acc = 100. * correct / total
    return avg_loss, train_acc

##### Validation
def test(epoch):
    global best_acc
    net.eval()
    test_loss = 0
    correct = 0
    total = 0
    with torch.no_grad():
        for batch_idx, (inputs, targets) in enumerate(testloader):
            inputs, targets = inputs.to(device), targets.to(device)
            outputs = net(inputs)
            loss = criterion(outputs, targets)

            test_loss += loss.item()
            _, predicted = outputs.max(1)
            total += targets.size(0)
            correct += predicted.eq(targets).sum().item()

            progress_bar(batch_idx, len(testloader), 'Loss: %.3f | Acc: %.3f%% (%d/%d)'
                % (test_loss/(batch_idx+1), 100.*correct/total, correct, total))

    avg_loss = test_loss / len(testloader)
    acc = 100.*correct/total
    # Save checkpoint.
    if acc > best_acc:
        print('Saving..')
        state = {
            "net": net.state_dict(),
            "optimizer": optimizer.state_dict(),
            "scaler": scaler.state_dict(),
            "acc": acc,
            "epoch": epoch,
        }
        if not os.path.isdir('checkpoint'):
            os.mkdir('checkpoint')
        torch.save(state, './checkpoint/{}-{}-{}-ckpt.t7'.format(args.net, args.dataset, args.patch))
        best_acc = acc
    return avg_loss, acc

net = net.to(device)

if usewandb:
    wandb.watch(net)

history = []
run_start_time = time.time()
for epoch in range(start_epoch, args.n_epochs):
    epoch_start = time.time()
    train_loss, train_acc = train(epoch)
    val_loss, val_acc = test(epoch)

    current_lr = optimizer.param_groups[0]["lr"]
    epoch_time = time.time() - epoch_start

    history_entry = {
        'epoch': epoch,
        'train_loss': train_loss,
        'train_acc': train_acc,
        'val_loss': val_loss,
        'val_acc': val_acc,
        'lr': current_lr,
        'epoch_time': epoch_time,
    }
    history.append(history_entry)

    save_history_csv(history)
    save_training_plot(history)

    log_line = (
        f"{time.ctime()} Epoch {epoch:03d} | lr: {current_lr:.7f} | "
        f"train loss: {train_loss:.5f} | train acc: {train_acc:.3f}% | "
        f"val loss: {val_loss:.5f} | val acc: {val_acc:.3f}%"
    )
    print(log_line)
    with text_log_path.open('a') as appender:
        appender.write(log_line + "\n")

    if usewandb:
        wandb.log({
            'epoch': epoch,
            'train_loss': train_loss,
            'train_acc': train_acc,
            'val_loss': val_loss,
            'val_acc': val_acc,
            'lr': current_lr,
            'epoch_time': epoch_time,
        })

    scheduler.step(epoch-1)

total_train_time = time.time() - run_start_time
save_history_csv(history)
save_training_plot(history)
update_summary_csv(history, total_train_time)

# writeout wandb
if usewandb:
    wandb.save("wandb_{}_{}.h5".format(args.net, args.dataset))