#!/usr/bin/env -S PYTHONPATH=../../../tools/extract-utils python3
#
# SPDX-FileCopyrightText: 2016 The CyanogenMod Project
# SPDX-FileCopyrightText: 2017-2024 The LineageOS Project
# SPDX-License-Identifier: Apache-2.0
#

import os
import sys
import argparse
import re
from pathlib import Path

from extract_utils.fixups_blob import (
    blob_fixup,
    blob_fixups_user_type,
)
from extract_utils.main import (
    ExtractUtils,
    ExtractUtilsModule,
)

def wfdmmsrc_system_fixup(file_path, obj_file_path):
    """Add libgui_shim.so dependency to libwfdmmsrc_system.so"""
    if not obj_file_path:
        return True
    
    # Use the fixup helper from extract_utils
    return blob_fixup().add_needed("libgui_shim.so")(file_path, obj_file_path)

def wfdnative_fixup(file_path, obj_file_path):
    """Add libbinder_shim.so and libinput_shim.so dependencies to libwfdnative.so"""
    if not obj_file_path:
        return True
    
    # Use the fixup helper from extract_utils
    return (blob_fixup()
            .add_needed("libbinder_shim.so")
            .add_needed("libinput_shim.so"))(file_path, obj_file_path)

def wfdservice_fixup(file_path, obj_file_path):
    """Replace needed library for libwfdservice.so"""
    if not obj_file_path:
        return True
    
    # Use the fixup helper from extract_utils
    return blob_fixup().replace_needed(
        "android.media.audio.common.types-V2-cpp.so",
        "android.media.audio.common.types-V4-cpp.so"
    )(file_path, obj_file_path)

def mi_thermald_rc_fixup(file_path, obj_file_path):
    """Remove seclabel line from init.mi_thermald.rc"""
    if not obj_file_path:
        return True
    
    with open(obj_file_path, 'r') as f:
        content = f.read()
    
    content = content.replace("seclabel u:r:mi_thermald:s0\n", "")
    
    with open(obj_file_path, 'w') as f:
        f.write(content)
    
    return True

def atfwd_policy_fixup(file_path, obj_file_path):
    """Add gettid entry to atfwd@2.0.policy if missing"""
    if not obj_file_path:
        return True
    
    with open(obj_file_path, 'r') as f:
        content = f.read()
    
    if 'gettid: ' not in content:
        with open(obj_file_path, 'a') as f:
            f.write('gettid: 1\n')
    
    return True

def dolby_dax_xml_fixup(file_path, obj_file_path):
    """Modify volume-leveler setting in multimedia_dolby_dax_default.xml"""
    if not obj_file_path:
        return True
    
    with open(obj_file_path, 'r') as f:
        content = f.read()
    
    content = content.replace('volume-leveler-enable>true<', 'volume-leveler-enable>false<')
    
    with open(obj_file_path, 'w') as f:
        f.write(content)
    
    return True

def dolby_service_fixup(file_path, obj_file_path):
    """Add libstagefright_foundation-v33.so dependency to Dolby service"""
    if not obj_file_path:
        return True
    
    return blob_fixup().add_needed("libstagefright_foundation-v33.so")(file_path, obj_file_path)

def wvdrm_fixup(file_path, obj_file_path):
    """Add libcrypto_shim.so dependency to DRM libraries"""
    if not obj_file_path:
        return True
    
    return blob_fixup().add_needed("libcrypto_shim.so")(file_path, obj_file_path)

def libril_fixup(file_path, obj_file_path):
    """Replace property string in libril-qc-hal-qmi.so"""
    if not obj_file_path:
        return True
    
    with open(obj_file_path, 'rb') as f:
        content = f.read()
    
    content = content.replace(
        b'ro.product.vendor.device',
        b'ro.vendor.radio.midevice'
    )
    
    with open(obj_file_path, 'wb') as f:
        f.write(content)
    
    return True

def dolby_codec_fixup(file_path, obj_file_path):
    """Replace needed library for Dolby codec libraries"""
    if not obj_file_path:
        return True
    
    return blob_fixup().replace_needed(
        "libstagefright_foundation.so",
        "libstagefright_foundation-v33.so"
    )(file_path, obj_file_path)

def dolby_bin_fixup(file_path, obj_file_path):
    """Add libstagefright_foundation-v33.so dependency to Dolby binaries"""
    if not obj_file_path:
        return True
    
    return blob_fixup().add_needed("libstagefright_foundation-v33.so")(file_path, obj_file_path)

def dolby_client_fixup(file_path, obj_file_path):
    """Add libcodec2_hidl_shim.so dependency to Dolby client library"""
    if not obj_file_path:
        return True
    
    return blob_fixup().add_needed("libcodec2_hidl_shim.so")(file_path, obj_file_path)

# Define blob fixups
blob_fixups: blob_fixups_user_type = {
    # WFD fixups
    'system_ext/lib64/libwfdmmsrc_system.so': wfdmmsrc_system_fixup,
    'system_ext/lib64/libwfdnative.so': wfdnative_fixup,
    'system_ext/lib64/libwfdservice.so': wfdservice_fixup,
    
    # System component fixups
    'vendor/etc/init/init.mi_thermald.rc': mi_thermald_rc_fixup,
    'vendor/etc/seccomp_policy/atfwd@2.0.policy': atfwd_policy_fixup,
    'vendor/lib64/libril-qc-hal-qmi.so': libril_fixup,
    
    # DRM fixups
    'vendor/lib64/mediadrm/libwvdrmengine.so': wvdrm_fixup,
    'vendor/lib64/libwvhidl.so': wvdrm_fixup,
    
    # Dolby fixups
    'odm/etc/dolby/multimedia_dolby_dax_default.xml': dolby_dax_xml_fixup,
    'odm/bin/hw/vendor.dolby_v3_6.hardware.dms360@2.0-service': dolby_service_fixup,
    'vendor/lib/c2.dolby.avc.dec.so': dolby_codec_fixup,
    'vendor/lib/c2.dolby.avc.sec.dec.so': dolby_codec_fixup,
    'vendor/lib/c2.dolby.hevc.dec.so': dolby_codec_fixup,
    'vendor/lib/c2.dolby.hevc.sec.dec.so': dolby_codec_fixup,
    'vendor/bin/hw/dolbycodec2': dolby_bin_fixup,
    'vendor/bin/hw/vendor.qti.media.c2@1.0-service': dolby_bin_fixup,
    'vendor/lib/c2.dolby.client.so': dolby_client_fixup,
}  # fmt: skip

module = ExtractUtilsModule(
    'sm8250-common',
    'xiaomi',
    blob_fixups=blob_fixups,
    check_elf=True,
    add_firmware_proprietary_file=False,
)

if __name__ == '__main__':
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Extract proprietary blobs for Xiaomi SM8250 devices')
    parser.add_argument('--only-common', action='store_true', help='Extract only common blobs')
    parser.add_argument('--only-firmware', action='store_true', help='Extract only firmware blobs')
    parser.add_argument('--only-target', action='store_true', help='Extract only target-specific blobs')
    parser.add_argument('-n', '--no-cleanup', action='store_true', help='Skip vendor folder cleanup')
    parser.add_argument('-k', '--kang', action='store_true', help='Extract proprietary blobs from existing vendor image')
    parser.add_argument('-s', '--section', help='Extract only specified section')
    parser.add_argument('src', nargs='?', default='adb', help='Source directory or "adb"')
    
    args = parser.parse_args()
    
    # Create ExtractUtils instance for this device
    if not args.only_target:
        # For common device
        utils = ExtractUtils.device(
            module,
            clean_vendor=not (args.no_cleanup or args.section),
            kang=args.kang,
            section=args.section
        )
        
        if not args.only_firmware:
            utils.extract_file('proprietary-files.txt')
            utils.extract_file('proprietary-files-phone.txt')
    
    # For specific device
    if not args.only_common:
        device_dir = Path(f'../../xiaomi/{os.environ.get("DEVICE", "")}')
        prop_file = device_dir / 'proprietary-files.txt'
        
        if prop_file.exists():
            device_name = os.environ.get('DEVICE', '')
            device_module = ExtractUtilsModule(
                device_name,
                'xiaomi',
                blob_fixups=blob_fixups,
                check_elf=True
            )
            
            device_utils = ExtractUtils.device(
                device_module,
                clean_vendor=not (args.no_cleanup or args.section),
                kang=args.kang,
                section=args.section
            )
            
            if not args.only_firmware:
                device_utils.extract_file(str(prop_file))
            
            # Extract firmware if specified
            if not args.section:
                firmware_file = device_dir / 'proprietary-firmware.txt'
                if firmware_file.exists():
                    device_utils.extract_firmware(str(firmware_file))
