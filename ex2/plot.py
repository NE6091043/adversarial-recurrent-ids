#!/usr/bin/env python3

import os
import sys
import re
import itertools
import json

import numpy as np
import matplotlib.pyplot as plt
import math
import ast

DIR_NAME = sys.argv[1]

featmap = json.load(open('featmap.json'))

hist = "hist" in sys.argv

for f in os.listdir(DIR_NAME):
	match = re.match('(.*)_(nn|rf)_0((?:_bd)?)((?:_\(\d+\.?\d*,\d+\.?\d*\))?)\.npy', f)
	if match is not None:
		feature = match.group(1)

		if not match.group(4):
			continue

		all_legends = []
		for fold in (range(1) if hist else itertools.count()):
			try:
				pdp = np.load('%s/%s_%s_%d%s%s.npy' % (DIR_NAME, feature, match.group(2), fold, match.group(3), match.group(4)))
			except FileNotFoundError as e:
				break
			if match.group(2) == 'rf':
				pdp[1:,:] = -pdp[1:,:] if sys.argv[1] == 'ale' else (1-pdp[1:,:]) # dirty hack
			fig, ax1 = plt.subplots()

			if hist:
				data = np.load('%s/%s_%s_%d%s%s_data.npy' % (DIR_NAME, feature, match.group(2), fold, match.group(3), match.group(4)))
				ax2 = ax1.twinx()
				bbox = ax2.get_window_extent().transformed(fig.dpi_scale_trans.inverted())
				width = int(math.floor(bbox.width*fig.dpi))
				bins = min(max(int(math.ceil(max(data)))-int(math.floor(min(data))+1), 1), width)
				print("featmap[feature]", featmap[feature], "bins", bins)#, "data", data)
				ret2 = ax2.hist(data, bins=bins, color="gray", density=True, label="{} occurrence".format(featmap[feature]))
				ax2.set_ylabel("occurrence")
			ret1 = ax1.plot(pdp[0,:], pdp[1:,:].transpose(), label="{} confidence".format(featmap[feature]))
			all_legends += ret1
			if hist:
				all_legends.append(ret2)
		ax1.set_xlabel(featmap[feature])
		ax1.set_ylabel(DIR_NAME.upper())
		if fold > 1:
			plt.legend(['Fold %d' % (i+1) for i in range(fold)])
		else:
			all_legends = [item if type(item)!=tuple else item[-1][0] for item in all_legends]
			all_labels = [item.get_label() for item in all_legends]
			plt.legend(all_legends, all_labels)
		plt.tight_layout()
		plt.savefig(DIR_NAME+'/%s_%s%s%s%s.pdf' % (feature, match.group(2), match.group(3), match.group(4), "_hist" if hist else ""))
		plt.close()
