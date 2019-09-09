#!/usr/bin/env python3

import os
import pickle

for dir_name in ['prune_CAIA_backdoor_15', 'prune_CAIA_backdoor_17']:
	for f in os.listdir(dir_name):
		path = '%s/%s' % (dir_name, f)
		if not f.endswith('.pickle') or not '_nn' in f:
			continue
		try:
			with open(path, 'rb') as f:
				# relSteps, steps, scores, models, scoresbd, mean_activation_per_neuron, concatenated_results = pickle.load(f)
				relSteps, steps, scores, scoresbd, mean_activation_per_neuron, concatenated_results = pickle.load(f)
			print("Succeeded")
		except Exception as e:
			print(e)
			# print ('Failed to process %s' % path)
			# pass
			continue

		tot_neurons = len(mean_activation_per_neuron)
		plt.plot(np.arange(tot_neurons)+1, concatenated_results[np.argsort(mean_activation_per_neuron)])
		av_len = 10
		plt.plot(np.arange(av_len, tot_neurons+1), np.convolve(concatenated_results[np.argsort(mean_activation_per_neuron)], np.ones(av_len), mode='valid')/av_len)
		plt.xlabel(xlabel)
		plt.ylabel('Correlation coefficient')
		plt.tight_layout()
		plt.savefig(path[:-7] + '.pdf')

		plt.close()