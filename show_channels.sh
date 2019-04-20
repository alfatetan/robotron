#!/usr/bin/env bash
sudo asterisk -vvvvvvrx 'core show channels' | grep call > channels.list