/*
 * Copyright (C) 2021-2025 The LineageOS Project
 *
 * SPDX-License-Identifier: Apache-2.0
 */

#pragma once

#include <libvariant.h>

#include <vector>

struct variant_info {
    std::string hwc_value;
    std::string sku_value;

    std::string brand;
    std::string device;
    std::string marketname;
    std::string model;
    std::string build_fingerprint;

    bool nfc;
};

void search_variant(const std::vector<variant_info>& variants);

void set_variant_props(const variant_info& variant);
