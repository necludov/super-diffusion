# coding=utf-8
# Copyright 2020 The Google Research Authors.
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

# pylint: skip-file
"""DDPM model.

This code is the FLAX equivalent of:
https://github.com/hojonathanho/diffusion/blob/master/diffusion_tf/models/unet.py
"""

import flax.linen as nn
import jax.numpy as jnp
import ml_collections
import functools

from . import utils, layers, normalization

RefineBlock = layers.RefineBlock
ResidualBlock = layers.ResidualBlock
ResnetBlockDDPM = layers.ResnetBlockDDPM
Upsample = layers.Upsample
Downsample = layers.Downsample
conv3x3 = layers.ddpm_conv3x3
get_act = layers.get_act
get_normalization = normalization.get_normalization
default_initializer = layers.default_init


@utils.register_model(name='score-net')
class ScoreNet(nn.Module):
  """ScoreNet model architecture."""
  config: ml_collections.ConfigDict

  @nn.compact
  def __call__(self, t: jnp.ndarray, x: jnp.ndarray, y: jnp.ndarray, train: bool):
    # config parsing
    config = self.config
    act = get_act(config)
    normalize = get_normalization(config)

    nf = config.model.nf
    ch_mult = config.model.ch_mult
    num_res_blocks = config.model.num_res_blocks
    attn_resolutions = config.model.attn_resolutions
    dropout = config.model.dropout
    resamp_with_conv = config.model.resamp_with_conv
    num_resolutions = len(ch_mult)

    AttnBlock = functools.partial(layers.AttnBlock, normalize=normalize)
    ResnetBlock = functools.partial(ResnetBlockDDPM, act=act, normalize=normalize, dropout=dropout)

    temb = layers.get_timestep_embedding(t.ravel(), nf)
    temb = nn.Dense(nf * 4, kernel_init=default_initializer())(temb)
    temb = nn.Dense(nf * 4, kernel_init=default_initializer())(act(temb))
    if config.model.conditioned:
      temb = temb + nn.Embed(num_embeddings=config.data.num_classes, features=nf * 4)(y.astype(jnp.int32))

    # Downsampling block
    hs = [conv3x3(x, nf)]
    for i_level in range(num_resolutions):
      # Residual blocks for this resolution
      for i_block in range(num_res_blocks):
        h = ResnetBlock(out_ch=nf * ch_mult[i_level])(hs[-1], temb, train)
        if h.shape[1] in attn_resolutions:
          h = AttnBlock()(h)
        hs.append(h)
      if i_level != num_resolutions - 1:
        hs.append(Downsample(with_conv=resamp_with_conv)(hs[-1]))

    h = hs[-1]
    h = ResnetBlock()(h, temb, train)
    h = AttnBlock()(h)
    h = ResnetBlock()(h, temb, train)

    # Upsampling block
    for i_level in reversed(range(num_resolutions)):
      for i_block in range(num_res_blocks + 1):
        h = ResnetBlock(out_ch=nf * ch_mult[i_level])(jnp.concatenate([h, hs.pop()], axis=-1), temb, train)
      if h.shape[1] in attn_resolutions:
        h = AttnBlock()(h)
      if i_level != 0:
        h = Upsample(with_conv=resamp_with_conv)(h)

    assert not hs

    h = act(normalize()(h))
    h = conv3x3(h, x.shape[-1], init_scale=0.)

    return h
