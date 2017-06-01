def distribuicao_dataset():

	count_total = 0

	with open("../dataset/train.csv") as f:

		labels = set()
		labelsSize = dict()

		for line in f:
			count_total = count_total + 1

			tokens = line.split(",")
			labelStr = tokens[1].rstrip().split(" ")

			for label in labelStr:
				if(label not in labels):
					labels.add(label)
					labelsSize[label] = 1;
				else:
					labelsSize[label] = labelsSize[label] + 1;


		print(list(labels))
		
		for key, value in labelsSize.items():
			print(key, value)
			


if __name__ == "__main__":

	distribuicao_dataset()