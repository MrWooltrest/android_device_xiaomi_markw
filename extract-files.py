#!/usr/bin/env -S PYTHONPATH=../../../tools/extract-utils python3
#
# SPDX-FileCopyrightText: 2024 The LineageOS Project
# SPDX-License-Identifier: Apache-2.0
#

from extract_utils.fixups_blob import (
    blob_fixup,
    blob_fixups_user_type,
)
from extract_utils.fixups_lib import (
    lib_fixup_remove,
    lib_fixups,
    lib_fixups_user_type,
)
from extract_utils.main import (
    ExtractUtils,
    ExtractUtilsModule,
)

namespace_imports = [
    'device/xiaomi/markw',
    'hardware/qcom-caf/msm8953',
    'vendor/qcom/opensource/dataservices',
    'vendor/qcom/opensource/commonsys/display',
    'vendor/qcom/opensource/display',
]

def lib_fixup_vendor_suffix(lib: str, partition: str, *args, **kwargs):
    return f'{lib}_{partition}' if partition == 'vendor' else None
lib_fixups: lib_fixups_user_type = {
    **lib_fixups,
    (
        'com.qualcomm.qti.dpm.api@1.0',
        'vendor.qti.imsrtpservice@3.0',
    ): lib_fixup_vendor_suffix,
}

blob_fixups: blob_fixups_user_type = {
    # Camera - mm-qcamera-daemon
    'vendor/bin/mm-qcamera-daemon': blob_fixup()
        .add_needed('libc_mutexdestroy_shim.so')
        .add_needed('libc_pthreadts_shim.so')
        .binary_regex_replace(b'/data/misc/camera/cam_socket', b'/data/vendor/qcam/cam_socket'),

    # Camera - Path fixups
    ('vendor/lib/libmmcamera2_cpp_module.so',
    'vendor/lib/libmmcamera2_dcrf.so',
    'vendor/lib/libmmcamera2_iface_modules.so',
    'vendor/lib/libmmcamera2_imglib_modules.so',
    'vendor/lib/libmmcamera2_mct.so',
    'vendor/lib/libmmcamera2_pproc_modules.so',
    'vendor/lib/libmmcamera2_q3a_core.so',
    'vendor/lib/libmmcamera2_stats_algorithm.so',
    'vendor/lib/libmmcamera_dcrf_lib.so',
    'vendor/lib/libmmcamera_imglib.so',
    'vendor/lib/libmmcamera_tintless_algo.so'): blob_fixup()
        .binary_regex_replace(b'data/misc/camera', b'data/vendor/qcam'),

    # Camera - libmmcamera_dbg
    'vendor/lib/libmmcamera_dbg.so': blob_fixup()
        .add_needed('liblog.so')
        .binary_regex_replace(b'data/misc/camera', b'data/vendor/qcam')
        .binary_regex_replace(b'persist.camera.debug.logfile', b'persist.vendor.camera.dbglog'),

    # Camera - libmmcamera_hdr_gb_lib
    'vendor/lib/libmmcamera_hdr_gb_lib.so': blob_fixup()
        .add_needed('liblog.so')
        .replace_needed('libstdc++.so', 'libstdc++_vendor.so'),

    # Camera - libmmcamera_pdaf/pdafcamif
    ('vendor/lib/libmmcamera_pdafcamif.so',
    'vendor/lib/libmmcamera_pdaf.so'): blob_fixup()
        .add_needed('liblog.so')
        .binary_regex_replace(b'data/misc/camera', b'data/vendor/qcam'),

    # Camera - libmmcamera2_sensor_modules
    'vendor/lib/libmmcamera2_sensor_modules.so': blob_fixup()
        .add_needed('liblog.so')
        .binary_regex_replace(b'data/misc/camera', b'data/vendor/qcam')
        .binary_regex_replace(b'system/etc/camera', b'vendor/etc/camera'),

    # Camera - libmmcamera2_stats_modules
    'vendor/lib/libmmcamera2_stats_modules.so': blob_fixup()
        .replace_needed('libgui.so', 'libwui.so')
        .replace_needed('libandroid.so', 'libcamshim.so')
        .binary_regex_replace(b'data/misc/camera', b'data/vendor/qcam')
        .binary_regex_replace(b'persist.camera.debug.logfile', b'persist.vendor.camera.dbglog'),

    # Camera - libmmcamera_tintless_bg_pca_algo
    'vendor/lib/libmmcamera_tintless_bg_pca_algo.so': blob_fixup()
        .add_needed('liblog.so')
        .binary_regex_replace(b'data/misc/camera', b'data/vendor/qcam'),

    # Camera - libmmcamera_tuning
    'vendor/lib/libmmcamera_tuning.so': blob_fixup()
        .remove_needed('libmm-qcamera.so')
        .binary_regex_replace(b'data/misc/camera', b'data/vendor/qcam'),

    # Camera - libstdc++.so => libstdc++_vendor.so
    ('vendor/lib/liboptizoom.so',
    'vendor/lib/libseemore.so',
    'vendor/lib/libtrueportrait.so',
    'vendor/lib/libubifocus.so',
    'vendor/lib/libchromaflash.so'): blob_fixup()
        .replace_needed('libstdc++.so', 'libstdc++_vendor.so'),

    # Camera - liblog dep.
    ('vendor/lib/libjpegehw.so',
    'vendor/lib/libjpegdhw.so',
    'vendor/lib/libjpegdmahw.so',
    'vendor/lib/libmmcamera_le2464c_master_eeprom.so',
    'vendor/lib/libqomx_jpegenc.so',
    'vendor/lib/libqomx_jpegdec.so',
    'vendor/lib/libqomx_jpegenc_pipe.so'): blob_fixup()
        .add_needed('liblog.so'),

    # Fingerprint - Goodix
    'vendor/bin/gx_fpd': blob_fixup()
        .add_needed('libshims_gxfpd.so')
        .add_needed('fakelogprint.so')
        .remove_needed('libunwind.so')
        .remove_needed('libbacktrace.so'),
    'vendor/lib64/hw/fingerprint.goodix.so': blob_fixup()
        .add_needed('fakelogprint.so')
        .replace_needed('libstdc++.so', 'libstdc++_vendor.so'),
    'vendor/lib64/gxfingerprint.default.so': blob_fixup()
        .add_needed('fakelogprint.so')
        .replace_needed('libstdc++.so', 'libstdc++_vendor.so'),
    'vendor/lib64/libfp_client.so': blob_fixup()
        .add_needed('liblog.so')
        .replace_needed('libstdc++.so', 'libstdc++_vendor.so'),
    'vendor/lib64/libfpnav.so': blob_fixup()
        .replace_needed('libstdc++.so', 'libstdc++_vendor.so'),
    'vendor/lib64/libfpservice.so': blob_fixup()
        .add_needed('liblog.so')
        .add_needed('libbinder_shim.so')
        .replace_needed('libstdc++.so', 'libstdc++_vendor.so'),

    # IMS
    'system_ext/lib64/lib-imscamera.so': blob_fixup()
        .add_needed('libgui_shim.so'),
    'system_ext/lib64/lib-imsvideocodec.so': blob_fixup()
        .add_needed('libgui_shim.so')
        .replace_needed('libqdMetaData.so', 'libqdMetaData.system.so'),
}  # fmt: skip

# Define the module
module = ExtractUtilsModule(
    'markw',
    'xiaomi',
    blob_fixups=blob_fixups,
    lib_fixups=lib_fixups,
    namespace_imports=namespace_imports,
)

if __name__ == '__main__':
    utils = ExtractUtils.device(module)
    utils.run()
