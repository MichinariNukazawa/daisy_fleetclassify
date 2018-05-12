# Copyright 2017 Hazuki Tachibana
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#	 http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import sys

#import nijiflow
#from nijiflow.nijiflow.classifier import classifier
import classifier


def main(argv):
	image_paths = argv[2:]
	if not image_paths:
		print('Usage: classify.py model_file file1 file2...')
		return 1

	classifier_ = classifier.Classifier(argv[1])
	predictions = classifier_.classify(image_paths)
	for image_path, prediction in zip(image_paths, predictions):
		print('%.3f\t%s' % (prediction, image_path))


if __name__ == '__main__':
	sys.exit(main(sys.argv))
