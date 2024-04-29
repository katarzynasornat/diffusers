# coding=utf-8
# Copyright 2024 HuggingFace Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import unittest

import torch

from diffusers import Transformer2DModel
from diffusers.utils.testing_utils import (
    enable_full_determinism,
    floats_tensor,
    torch_device,
)

from ..test_modeling_common import ModelTesterMixin, TransformerTesterMixin


enable_full_determinism()


class ContinuousTransformer2DModelTests(ModelTesterMixin, TransformerTesterMixin, unittest.TestCase):
    # This is the regular setting that's used in classes like `UNet2DConditionModel`.
    model_class = Transformer2DModel
    main_input_name = "hidden_states"

    @property
    def dummy_input(self):
        batch_size = 4
        in_channels = 4
        sample_size = 8
        scheduler_num_train_steps = 1000
        sequence_length = 4
        cross_attention_dim = 8

        hidden_states = floats_tensor((batch_size, in_channels, sample_size, sample_size)).to(torch_device)
        timesteps = torch.randint(0, scheduler_num_train_steps, size=(batch_size,)).to(torch_device)
        encoder_hidden_states = floats_tensor((batch_size, sequence_length, cross_attention_dim)).to(torch_device)

        return {
            "hidden_states": hidden_states,
            "timestep": timesteps,
            "encoder_hidden_states": encoder_hidden_states,
        }

    @property
    def input_shape(self):
        return (4, 4, 8, 8)

    @property
    def output_shape(self):
        return (4, 4, 8, 8)

    def prepare_init_args_and_inputs_for_common(self):
        init_dict = {
            "activation_fn": "geglu",
            "attention_head_dim": 2,
            "cross_attention_dim": 8,
            "in_channels": 4,
            "norm_num_groups": 1,
            "norm_type": "layer_norm",
            "num_attention_heads": 2,
            "num_embeds_ada_norm": None,
            "num_layers": 1,
            "out_channels": None,
        }
        inputs_dict = self.dummy_input
        return init_dict, inputs_dict

    def test_output(self):
        super().test_output(expected_output_shape=self.output_shape)

    def test_forward_with_norm_groups(self):
        super().test_forward_with_norm_groups(norm_num_groups=4)
