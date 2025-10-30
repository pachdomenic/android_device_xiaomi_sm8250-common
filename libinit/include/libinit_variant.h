/*
 * Copyright (C) 2021 The LineageOS Project
 *
 * SPDX-License-Identifier: Apache-2.0
 */

#ifndef LIBINIT_VARIANT_H
#define LIBINIT_VARIANT_H

#include <libvariant.h>

#include <vector>

void search_variant(const std::vector<variant_info_t> variants);

void search_variant(const std::vector<variant_info>& variants);


void set_variant_props(const variant_info_t variant);

#endif // LIBINIT_VARIANT_H
