import csv


# This class handles working with files
class FileHandler:
    def __init__(self, file_path='data.csv'):
        self.file_path = file_path

    # read information from a file
    def read_file(self):
        with open(self.file_path, 'r') as myfile:
            reader = csv.DictReader(myfile)
            return list(reader)

    # add informations as a dictionary to a file
    def add_to_file(self, new_value):
        if isinstance(new_value, dict):
            fields = new_value.keys()
            new_value = [new_value]
        elif isinstance(new_value, list):
            fields = new_value[0].keys()

        with open(self.file_path, 'a') as myfile:
            writer = csv.DictWriter(myfile, fieldnames=fields)
            if myfile.tell() == 0:
                writer.writeheader()
            writer.writerows(new_value)


