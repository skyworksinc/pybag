# SPDX-License-Identifier: BSD-3-Clause AND Apache-2.0
# Copyright 2018 Regents of the University of California
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.
#
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
#
# * Neither the name of the copyright holder nor the names of its
#   contributors may be used to endorse or promote products derived from
#   this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

# Copyright 2019 Blue Cheetah Analog Design Inc.
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

from typing import Union, List, Tuple

import pytest

from pybag.core import PyRoutingGrid
from pybag.enum import RoundMode, Orient2D

coord_htr_data = [
    (1, 90, RoundMode.NONE, False, 0),
    (1, 180, RoundMode.NONE, False, 1),
    (1, 270, RoundMode.NONE, False, 2),
    (1, 0, RoundMode.NONE, False, -1),
    (1, -90, RoundMode.NONE, False, -2),
    (5, 180, RoundMode.NONE, False, 0),
    (5, 360, RoundMode.NONE, False, 1),
    (5, 540, RoundMode.NONE, False, 2),
    (5, 0, RoundMode.NONE, False, -1),
    (5, -180, RoundMode.NONE, False, -2),
]

pitch_data = [
    (1, 180),
    (2, 192),
    (3, 180),
    (4, 192),
    (5, 360),
    (6, 288),
    (7, 540),
    (8, 960),
]


@pytest.mark.parametrize("layer_id, coord, mode, even, htr", coord_htr_data)
def test_coord_htr(layer_id: int, coord: int, mode: RoundMode, even: bool,
                   htr: int, routing_grid: PyRoutingGrid) -> None:
    assert routing_grid.coord_to_htr(layer_id, coord, mode, even) == htr


@pytest.mark.parametrize("layer_id, pitch", pitch_data)
def test_track_pitch(layer_id: int, pitch: int, routing_grid: PyRoutingGrid) -> None:
    assert routing_grid.get_track_pitch(layer_id) == pitch
    assert routing_grid.get_track_offset(layer_id) == pitch // 2


@pytest.mark.parametrize("lay, coord, w_ntr, mode, even, expect", [
    (4, 720, 1, RoundMode.LESS_EQ, False, 6),
])
def test_find_next_htr(routing_grid: PyRoutingGrid, lay: int, coord: int, w_ntr: int,
                       mode: Union[RoundMode, int], even: bool, expect: int) -> None:
    """Check that find_next_htr() works properly."""
    ans = routing_grid.find_next_htr(lay, coord, w_ntr, mode, even)
    assert ans == expect


@pytest.mark.parametrize("tr_specs", [
    [(1, 1, 20, 20, 10)],
    [(2, 0, 24, 24, 10)],
])
def test_copy_grid(tr_specs: List[Tuple[int, int, int, int, int]],
                   routing_grid: PyRoutingGrid) -> None:
    copy_grid = routing_grid.get_copy_with(routing_grid.top_ignore_layer,
                                           routing_grid.top_private_layer,
                                           tr_specs)

    for level, dir_code, w, sp, offset in tr_specs:
        tr_info = copy_grid.get_track_info(level)
        assert tr_info.width == w
        assert tr_info.space == sp
        assert tr_info.offset == offset
        assert copy_grid.get_direction(level) is Orient2D(dir_code)


def test_hash(routing_grid: PyRoutingGrid) -> None:
    copy_grid = routing_grid.get_copy_with(routing_grid.top_ignore_layer,
                                           routing_grid.top_private_layer,
                                           [])

    assert copy_grid == routing_grid
    assert hash(copy_grid) == hash(routing_grid)
