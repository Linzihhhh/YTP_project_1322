from Dataset import Dataset
from Nlp import Nlp

dataset = Dataset()

nlp = Nlp()

x_data = dataset.get_comment()
y_data = ["excited"]

nlp.train(x_data=x_data, y_data=y_data)
