# SPDX-FileCopyrightText: Copyright (c) 1993-2022 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: LicenseRef-NvidiaProprietary
#
# NVIDIA CORPORATION, its affiliates and licensors retain all intellectual
# property and proprietary rights in and to this material, related
# documentation and any modifications thereto. Any use, reproduction,
# disclosure or distribution of this material and related documentation
# without an express license agreement from NVIDIA CORPORATION or
# its affiliates is strictly prohibited.

# This script exports torch version of resnet50 to onnx and torchscript format

import torch
import torchvision.models as models

torch.hub._validate_not_a_forked_repo=lambda a,b,c: True

# load model; We are going to use a pretrained resnet model
model = models.resnet50(pretrained=True).eval()
x = torch.randn(1, 3, 224, 224, requires_grad=True)

dir = "triton-server/model_repository/resnet50_onxx/1/"

# Export the onnx model
torch.onnx.export(model,                        # model being run
                  x,                            # model input (or a tuple for multiple inputs)
                  "triton-server/model_repository/resnet50_onnx/1/model.onnx",              # where to save the model (can be a file or file-like object)
                  export_params=True,           # store the trained parameter weights inside the model file
                  input_names = ['input'],      # the model's input names
                  output_names = ['output'],    # the model's output names
                  )


# Export torchscript model
traced_script_module = torch.jit.trace(model, x)
traced_script_module.save("triton-server/model_repository/resnet50_torch/1/model.pt")