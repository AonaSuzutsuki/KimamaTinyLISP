#!/usr/bin/env python
# -*- coding: utf-8 -*-


def replace_newline(text):
    text = text.replace('\r\n', '\r')
    text = text.replace('\r', '\n')
    return text
