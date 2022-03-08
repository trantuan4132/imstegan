# 
# Fast discrete cosine transform algorithms (Python)
# 
# Copyright (c) 2020 Project Nayuki. (MIT License)
# https://www.nayuki.io/page/fast-discrete-cosine-transform-algorithms
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the "Software"), to deal in
# the Software without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
# the Software, and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
# - The above copyright notice and this permission notice shall be included in
#   all copies or substantial portions of the Software.
# - The Software is provided "as is", without warranty of any kind, express or
#   implied, including but not limited to the warranties of merchantability,
#   fitness for a particular purpose and noninfringement. In no event shall the
#   authors or copyright holders be liable for any claim, damages or other
#   liability, whether in an action of contract, tort or otherwise, arising from,
#   out of or in connection with the Software or the use or other dealings in the
#   Software.
# 

# 20toduc01's note:
# I moved all the constants inside the functions so it's horrible to read now.
# I wrote a wrapper for 2-D DCT based on provided 1-D DCT code.
# I wrote this in a hurry, so it's probably not the prettiest code and I suspect
# the way I calculate 2-D DCT is not the most efficient.

import numba
import numpy as np


@numba.njit()
def dct8x8(block):
	# DCT type II, scaled. Algorithm by Arai, Agui, Nakajima, 1988.
	# See: https://web.stanford.edu/class/ee398a/handouts/lectures/07-TransformCoding.pdf#page=30	
	def dct8(vector):
		v0 = vector[0] + vector[7]
		v1 = vector[1] + vector[6]
		v2 = vector[2] + vector[5]
		v3 = vector[3] + vector[4]
		v4 = vector[3] - vector[4]
		v5 = vector[2] - vector[5]
		v6 = vector[1] - vector[6]
		v7 = vector[0] - vector[7]
		
		v8 = v0 + v3
		v9 = v1 + v2
		v10 = v1 - v2
		v11 = v0 - v3
		v12 = -v4 - v5
		v13 = (v5 + v6) * 0.7071067811865476
		v14 = v6 + v7
		
		v15 = v8 + v9
		v16 = v8 - v9
		v17 = (v10 + v11) * 0.7071067811865476
		v18 = (v12 + v14) * 0.38268343236508984
		
		v19 = -v12 * 0.5411961001461969 - v18
		v20 = v14 * 1.3065629648763766 - v18
		
		v21 = v17 + v11
		v22 = v11 - v17
		v23 = v13 + v7
		v24 = v7 - v13
		
		v25 = v19 + v24
		v26 = v23 + v20
		v27 = v23 - v20
		v28 = v24 - v19
		
		return np.array([
			0.35355339059327373 * v15,
			0.25489778955207960 * v26,
			0.27059805007309850 * v21,
			0.30067244346752264 * v28,
			0.35355339059327373 * v16,
			0.44998811156820780 * v25,
			0.65328148243818820 * v22,
			1.28145772387075270 * v27,
		])

	ans = np.zeros((8, 8))
	for idx in range(8):
		ans[:, idx] = dct8(block[:, idx])
	for idx in range(8):
		ans[idx, :] = dct8(ans[idx, :])
	return ans


def idct8x8(block):
	# DCT type III, scaled. A straightforward inverse of the forward algorithm.
	def idct8(vector):
		v15 = vector[0] / 0.35355339059327373
		v26 = vector[1] / 0.25489778955207960
		v21 = vector[2] / 0.27059805007309850
		v28 = vector[3] / 0.30067244346752264
		v16 = vector[4] / 0.35355339059327373
		v25 = vector[5] / 0.44998811156820780
		v22 = vector[6] / 0.65328148243818820
		v27 = vector[7] / 1.28145772387075270
		
		v19 = (v25 - v28) / 2
		v20 = (v26 - v27) / 2
		v23 = (v26 + v27) / 2
		v24 = (v25 + v28) / 2
		
		v7  = (v23 + v24) / 2
		v11 = (v21 + v22) / 2
		v13 = (v23 - v24) / 2
		v17 = (v21 - v22) / 2
		
		v8 = (v15 + v16) / 2
		v9 = (v15 - v16) / 2
		
		v18 = (v19 - v20) * 0.38268343236508984  # Different from original
		v12 = -(v19 * 1.3065629648763766 - v18)
		v14 = -(v18 - v20 * 0.5411961001461969)
		
		v6 = v14 - v7
		v5 = v13 / 0.7071067811865476 - v6
		v4 = -v5 - v12
		v10 = v17 / 0.7071067811865476 - v11
		
		v0 = (v8 + v11) / 2
		v1 = (v9 + v10) / 2
		v2 = (v9 - v10) / 2
		v3 = (v8 - v11) / 2
		
		return np.array([
			(v0 + v7) / 2,
			(v1 + v6) / 2,
			(v2 + v5) / 2,
			(v3 + v4) / 2,
			(v3 - v4) / 2,
			(v2 - v5) / 2,
			(v1 - v6) / 2,
			(v0 - v7) / 2,
		])

	ans = np.zeros((8, 8))
	for idx in range(8):
		ans[:, idx] = idct8(block[:, idx])
	for idx in range(8):
		ans[idx, :] = idct8(ans[idx, :])
	return ans